"""
webhook/routers/chat.py — Chat & Media Endpoints
==================================================
[مُستخرَج من server.py — كان مدفوناً بين سطر 2438–2680]

Endpoints:
  POST /chat         ← رسالة نصية
  POST /chat/upload  ← رسالة مع ملف
  POST /chat/audio   ← رسالة صوتية
  POST /chat/tts     ← text-to-speech (response bytes)
  POST /chat/tts/stream ← TTS streaming
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import Response, StreamingResponse

from ..config import (
    ALLOWED_FILE_EXTENSIONS,
    AUDIO_FILE_EXTENSIONS,
    RASA_URL,
)
from ..models import ChatRequest, ChatResponse, TTSRequest
from ..services.audio import text_to_speech, transcribe_audio
from ..services.integrations import dispatch_integrations, integration_conversation_payload
from ..services.rasa_client import rasa_send
from ..services.uploads import save_upload
from ..services.admin_data import record_conversation_simple as record_conversation
from ..utils import build_audio_prompt, build_file_prompt, jsonable, resolve_brand

logger = logging.getLogger("alazab.webhook.chat")

router = APIRouter(tags=["Chat"])


# ══════════════════════════════════════════════════════════════
#  POST /chat
# ══════════════════════════════════════════════════════════════

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    payload: ChatRequest,
    background_tasks: BackgroundTasks,
):
    brand = resolve_brand(
        payload.brand,
        site_host=payload.site_host,
        site_path=payload.site_path,
        request=request,
    )
    responses = await rasa_send(
        sender_id=payload.sender_id,
        text=payload.message,
        brand=brand,
        extra_metadata={
            "channel": payload.channel,
            "site_host": payload.site_host,
            "site_path": payload.site_path,
        },
    )
    ts = datetime.now(timezone.utc).isoformat()
    background_tasks.add_task(
        _record_and_dispatch,
        session_id=payload.sender_id,
        brand=brand,
        channel=payload.channel or "website",
        user_text=payload.message,
        bot_responses=responses,
        ts=ts,
    )
    return ChatResponse(
        responses=responses,
        sender_id=payload.sender_id,
        channel=payload.channel or "website",
        timestamp=ts,
    )


# ══════════════════════════════════════════════════════════════
#  POST /chat/upload
# ══════════════════════════════════════════════════════════════

@router.post("/chat/upload", response_model=ChatResponse)
async def chat_upload(
    request: Request,
    background_tasks: BackgroundTasks,
    sender_id: str = Form(...),
    brand: Optional[str] = Form(None),
    channel: Optional[str] = Form("website"),
    site_host: Optional[str] = Form(None),
    site_path: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    resolved_brand = resolve_brand(brand, site_host=site_host, site_path=site_path, request=request)

    attachment = await save_upload(file, ALLOWED_FILE_EXTENSIONS, kind="file")
    prompt = build_file_prompt(attachment, resolved_brand, site_host, message)

    responses = await rasa_send(
        sender_id=sender_id,
        text=prompt,
        brand=resolved_brand,
        extra_metadata={"channel": channel, "site_host": site_host, "attachment": attachment},
    )
    ts = datetime.now(timezone.utc).isoformat()
    background_tasks.add_task(
        _record_and_dispatch,
        session_id=sender_id,
        brand=resolved_brand,
        channel=channel or "website",
        user_text=prompt,
        bot_responses=responses,
        ts=ts,
        attachment=attachment,
    )
    return ChatResponse(
        responses=responses,
        sender_id=sender_id,
        channel=channel or "website",
        timestamp=ts,
        attachment=attachment,
    )


# ══════════════════════════════════════════════════════════════
#  POST /chat/audio
# ══════════════════════════════════════════════════════════════

@router.post("/chat/audio", response_model=ChatResponse)
async def chat_audio(
    request: Request,
    background_tasks: BackgroundTasks,
    sender_id: str = Form(...),
    brand: Optional[str] = Form(None),
    channel: Optional[str] = Form("website"),
    site_host: Optional[str] = Form(None),
    site_path: Optional[str] = Form(None),
    audio: UploadFile = File(...),
):
    resolved_brand = resolve_brand(brand, site_host=site_host, site_path=site_path, request=request)

    attachment = await save_upload(audio, AUDIO_FILE_EXTENSIONS, kind="audio")
    transcript = await transcribe_audio(attachment["path"])

    if not transcript:
        raise HTTPException(status_code=422, detail="تعذّر تفريغ الرسالة الصوتية")

    prompt = build_audio_prompt(transcript, attachment, resolved_brand, site_host)
    responses = await rasa_send(
        sender_id=sender_id,
        text=prompt,
        brand=resolved_brand,
        extra_metadata={"channel": channel, "site_host": site_host, "attachment": attachment},
    )
    ts = datetime.now(timezone.utc).isoformat()
    background_tasks.add_task(
        _record_and_dispatch,
        session_id=sender_id,
        brand=resolved_brand,
        channel=channel or "website",
        user_text=transcript,
        bot_responses=responses,
        ts=ts,
        attachment=attachment,
    )
    return ChatResponse(
        responses=responses,
        sender_id=sender_id,
        channel=channel or "website",
        timestamp=ts,
        attachment=attachment,
        transcript=transcript,
    )


# ══════════════════════════════════════════════════════════════
#  POST /chat/tts
# ══════════════════════════════════════════════════════════════

@router.post("/chat/tts")
async def chat_tts(payload: TTSRequest):
    audio = await text_to_speech(payload.text, payload.voice, payload.model)
    return Response(content=audio, media_type="audio/mpeg")


@router.post("/chat/tts/stream")
async def chat_tts_stream(payload: TTSRequest):
    """TTS streaming response لتقليل وقت الاستجابة الأولى."""
    import asyncio
    from openai import AsyncOpenAI
    from ..config import AUDIO_TTS_MODEL, AUDIO_TTS_VOICE
    import os

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")

    selected_voice = (payload.voice or AUDIO_TTS_VOICE).strip() or AUDIO_TTS_VOICE
    selected_model = (payload.model or AUDIO_TTS_MODEL).strip() or AUDIO_TTS_MODEL

    async def generate():
        try:
            client = AsyncOpenAI(api_key=api_key)
            async with client.audio.speech.with_streaming_response.create(
                model=selected_model,
                voice=selected_voice,
                input=payload.text[:4000],
                response_format="mp3",
            ) as resp:
                async for chunk in resp.iter_bytes(chunk_size=4096):
                    yield chunk
        except Exception as exc:
            logger.error("TTS stream error: %s", exc)

    return StreamingResponse(generate(), media_type="audio/mpeg")


# ══════════════════════════════════════════════════════════════
#  Background: Record + Dispatch
# ══════════════════════════════════════════════════════════════

async def _record_and_dispatch(
    session_id: str,
    brand: str,
    channel: str,
    user_text: str,
    bot_responses: list,
    ts: str,
    attachment: Optional[dict] = None,
) -> None:
    """يُسجّل المحادثة ويُرسل أحداث التكامل في الخلفية."""
    from ..services import admin_data as ad

    ad.count(channel)

    # بناء رسائل المحادثة
    messages = [
        {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": user_text,
            "created_at": ts,
            **({"attachments": [attachment]} if attachment else {}),
        }
    ]
    for resp in (bot_responses or []):
        if isinstance(resp, dict) and (resp.get("text") or resp.get("image")):
            messages.append({
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": resp.get("text") or "",
                "created_at": ts,
            })

    conversation = await record_conversation(
        session_id=session_id,
        brand=brand,
        channel=channel,
        messages=messages,
    )

    # أحداث التكامل
    payload = {
        "conversation": integration_conversation_payload(conversation),
        "message": messages[0] if messages else {},
        "responses": messages[1:],
    }
    await dispatch_integrations("message.received", payload)
