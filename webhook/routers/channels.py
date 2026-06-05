"""
webhook/routers/channels.py — Incoming Channel Webhooks
=========================================================
Meta (WhatsApp + Messenger) · Telegram · Brands · Leads
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from ..config import (
    BRAND_PROFILES, META_SECRET, META_TOKEN,
    META_VERIFY, TG_TOKEN, TG_WEBHOOK_SECRET,
)
from ..models import LeadData
from ..services.channels import (
    send_messenger, send_telegram, send_telegram_keyboard,
    send_whatsapp, send_whatsapp_buttons,
)
from ..services.notifications import notify_all_channels
from ..services.rasa_client import rasa_send

logger = logging.getLogger("alazab.webhook.channels_router")
router = APIRouter(tags=["Channels"])


# ── Brands ───────────────────────────────────────────────────

@router.get("/brands")
async def get_brands():
    return [
        {"id": bid, "name": p["name"], "slug": p["slug"],
         "title": p["title"], "subtitle": p["subtitle"]}
        for bid, p in BRAND_PROFILES.items()
    ]


# ── Leads ────────────────────────────────────────────────────

@router.post("/lead")
async def receive_lead(lead: LeadData, background_tasks: BackgroundTasks):
    from cryptography.fernet import Fernet
    from ..config import ENCRYPTION_KEY

    original_phone_end = str(lead.user_phone)[-4:] if lead.user_phone else ""

    if ENCRYPTION_KEY:
        try:
            cipher = Fernet(ENCRYPTION_KEY)
            if lead.user_phone:
                lead.user_phone = cipher.encrypt(lead.user_phone.encode()).decode()
            if getattr(lead, "user_email", None):
                lead.user_email = cipher.encrypt(lead.user_email.encode()).decode()
        except Exception as e:
            logger.error("خطأ في تشفير بيانات Lead: %s", e)

    logger.info("Lead | brand=%s channel=%s phone=...%s",
                lead.brand, lead.channel, original_phone_end)
    background_tasks.add_task(notify_all_channels, lead)
    return {"status": "received"}


# ══════════════════════════════════════════════════════════════
#  Meta — WhatsApp + Messenger
# ══════════════════════════════════════════════════════════════

@router.get("/webhook/meta")
async def meta_verify(
    hub_mode:         str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge:    str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == META_VERIFY:
        logger.info("Meta webhook verified ✅")
        return PlainTextResponse(hub_challenge or "")
    logger.warning("Meta verify failed — token mismatch")
    raise HTTPException(403, "Verification failed")


@router.post("/webhook/meta")
async def meta_messages(request: Request, background_tasks: BackgroundTasks):
    body_bytes = await request.body()

    # التحقق من توقيع Meta
    if META_SECRET:
        sig = request.headers.get("X-Hub-Signature-256", "")
        if not _verify_meta_sig(body_bytes, sig):
            raise HTTPException(403, "Invalid signature")

    try:
        data = json.loads(body_bytes)
    except Exception:
        raise HTTPException(400, "Invalid JSON")

    for entry in data.get("entry", []):
        # WhatsApp Business
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                wa_id   = msg.get("from", "")
                msg_type = msg.get("type", "")
                if msg_type == "text":
                    text = msg["text"]["body"]
                    background_tasks.add_task(_handle_whatsapp, wa_id, text)
                elif msg_type == "interactive":
                    # reply button أو list reply
                    inter = msg.get("interactive", {})
                    reply = inter.get("button_reply") or inter.get("list_reply", {})
                    text  = reply.get("title") or reply.get("id", "")
                    if text:
                        background_tasks.add_task(_handle_whatsapp, wa_id, text)
                elif msg_type == "audio":
                    # رسائل صوتية — نرسل للـ Whisper
                    media_id = msg.get("audio", {}).get("id", "")
                    background_tasks.add_task(_handle_whatsapp_audio, wa_id, media_id)

        # Facebook Messenger
        for messaging in entry.get("messaging", []):
            msg = messaging.get("message", {})
            sender_id = messaging.get("sender", {}).get("id", "")
            if msg.get("text") and sender_id:
                background_tasks.add_task(_handle_messenger, sender_id, msg["text"])
            elif msg.get("quick_reply") and sender_id:
                payload = msg["quick_reply"].get("payload", "")
                if payload:
                    background_tasks.add_task(_handle_messenger, sender_id, payload)

    return {"status": "ok"}


# ══════════════════════════════════════════════════════════════
#  Telegram
# ══════════════════════════════════════════════════════════════

@router.post("/webhook/telegram")
async def telegram_messages(request: Request, background_tasks: BackgroundTasks):
    # التحقق من الـ secret token
    if TG_WEBHOOK_SECRET:
        token_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if token_header != TG_WEBHOOK_SECRET:
            raise HTTPException(403, "Invalid Telegram secret")

    try:
        data = json.loads(await request.body())
    except Exception:
        raise HTTPException(400, "Invalid JSON")

    # رسالة عادية
    msg = data.get("message", {})
    if msg:
        chat_id = msg["chat"]["id"]
        if msg.get("text"):
            background_tasks.add_task(_handle_telegram, chat_id, msg["text"])
        elif msg.get("voice"):
            file_id = msg["voice"]["file_id"]
            background_tasks.add_task(_handle_telegram_voice, chat_id, file_id)

    # callback من inline keyboard
    callback = data.get("callback_query", {})
    if callback:
        chat_id = callback["from"]["id"]
        text    = callback.get("data", "")
        if text:
            background_tasks.add_task(_handle_telegram, chat_id, text)

    return {"status": "ok"}


# ══════════════════════════════════════════════════════════════
#  Channel Handlers
# ══════════════════════════════════════════════════════════════

async def _handle_whatsapp(wa_id: str, text: str) -> None:
    try:
        responses = await rasa_send(
            sender_id=f"wa_{wa_id}",
            text=text,
            brand=None,
            extra_metadata={"channel": "whatsapp", "wa_id": wa_id},
        )
        for resp in (responses or []):
            if not isinstance(resp, dict):
                continue
            if resp.get("buttons") and resp.get("text"):
                await send_whatsapp_buttons(wa_id, resp["text"], resp["buttons"])
            elif resp.get("text"):
                await send_whatsapp(wa_id, resp["text"])
    except Exception as exc:
        logger.error("WhatsApp handler ...%s: %s", wa_id[-4:], exc)


async def _handle_whatsapp_audio(wa_id: str, media_id: str) -> None:
    """رسالة صوتية — نحمّل الملف ونرسله للـ Whisper."""
    import httpx
    import uuid
    from datetime import datetime, timezone
    from ..config import UPLOADS_DIR
    from ..services.audio import transcribe_audio

    try:
        # إرسال رد مؤقت
        await send_whatsapp(wa_id, "🎙️ جارٍ معالجة رسالتك الصوتية...")
        
        if not META_TOKEN:
            logger.error("WhatsApp audio handler failed: META_TOKEN is missing")
            return
            
        async with httpx.AsyncClient() as client:
            # 1. الحصول على رابط الملف
            resp = await client.get(
                f"https://graph.facebook.com/v18.0/{media_id}",
                headers={"Authorization": f"Bearer {META_TOKEN}"}
            )
            if resp.status_code >= 300:
                logger.error("WhatsApp media info failed: %s", resp.text)
                await send_whatsapp(wa_id, "عذراً، حدث خطأ أثناء جلب الرسالة الصوتية.")
                return
                
            media_url = resp.json().get("url")
            if not media_url:
                logger.error("WhatsApp media URL is empty")
                return
                
            # 2. تنزيل الملف
            media_resp = await client.get(
                media_url,
                headers={"Authorization": f"Bearer {META_TOKEN}"}
            )
            if media_resp.status_code >= 300:
                logger.error("WhatsApp media download failed: %s", media_resp.text)
                await send_whatsapp(wa_id, "عذراً، لم أتمكن من تنزيل الرسالة الصوتية.")
                return
                
            # 3. حفظ الملف مؤقتاً
            bucket = datetime.now(timezone.utc).strftime("%Y/%m")
            target_dir = UPLOADS_DIR / bucket
            target_dir.mkdir(parents=True, exist_ok=True)
            file_path = target_dir / f"wa_audio_{uuid.uuid4().hex[:10]}.ogg"
            file_path.write_bytes(media_resp.content)
            
            # 4. تفريغ الصوت
            transcript = await transcribe_audio(str(file_path))
            if not transcript:
                await send_whatsapp(wa_id, "عذراً، لم أتمكن من فهم الرسالة الصوتية. هل يمكنك كتابتها؟")
                return
                
            # 5. تمرير النص للـ Handler الأساسي
            logger.info("WhatsApp audio transcribed for ...%s: %s", wa_id[-4:], transcript)
            await _handle_whatsapp(wa_id, transcript)
            
    except Exception as exc:
        logger.error("WhatsApp audio handler: %s", exc)


async def _handle_messenger(sender_id: str, text: str) -> None:
    try:
        responses = await rasa_send(
            sender_id=f"fb_{sender_id}",
            text=text,
            brand=None,
            extra_metadata={"channel": "messenger"},
        )
        for resp in (responses or []):
            if isinstance(resp, dict) and resp.get("text"):
                await send_messenger(sender_id, resp["text"])
    except Exception as exc:
        logger.error("Messenger handler: %s", exc)


async def _handle_telegram(chat_id: int, text: str) -> None:
    try:
        responses = await rasa_send(
            sender_id=f"tg_{chat_id}",
            text=text,
            brand=None,
            extra_metadata={"channel": "telegram"},
        )
        for resp in (responses or []):
            if not isinstance(resp, dict):
                continue
            if resp.get("buttons") and resp.get("text"):
                # تحويل buttons لـ Telegram keyboard
                buttons = [[b.get("title", "")] for b in resp["buttons"]]
                await send_telegram_keyboard(chat_id, resp["text"], buttons)
            elif resp.get("text"):
                await send_telegram(chat_id, resp["text"])
    except Exception as exc:
        logger.error("Telegram handler %s: %s", chat_id, exc)


async def _handle_telegram_voice(chat_id: int, file_id: str) -> None:
    """رسالة صوتية من Telegram."""
    try:
        await send_telegram(chat_id, "🎙️ جارٍ معالجة رسالتك الصوتية...")
        logger.info("Telegram voice from %s — file_id=%s", chat_id, file_id)
    except Exception as exc:
        logger.error("Telegram voice handler: %s", exc)


# ── Helpers ──────────────────────────────────────────────────

def _verify_meta_sig(body: bytes, signature: str) -> bool:
    if not META_SECRET or not signature:
        return False
    expected = "sha256=" + hmac.new(
        META_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
