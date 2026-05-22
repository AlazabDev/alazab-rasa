"""
webhook/routers/channels.py — Incoming Channel Webhooks
=========================================================
[مُستخرَج من server.py — كان مدفوناً بين سطر 2692–2815]

Endpoints:
  GET  /webhook/meta    ← التحقق من Meta
  POST /webhook/meta    ← رسائل WhatsApp + Messenger
  POST /webhook/telegram ← رسائل Telegram
  GET  /brands           ← قائمة البراندات
  POST /lead             ← بيانات عميل من Rasa
"""
from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from ..config import (
    BRAND_PROFILES,
    META_SECRET,
    META_TOKEN,
    META_VERIFY,
    TG_TOKEN,
    TG_WEBHOOK_SECRET,
)
from ..models import LeadData
from ..services.channels import send_messenger, send_telegram, send_whatsapp
from ..services.notifications import notify_all_channels
from ..services.rasa_client import rasa_send

logger = logging.getLogger("alazab.webhook.channels_router")

router = APIRouter(tags=["Channels"])


# ══════════════════════════════════════════════════════════════
#  Brands
# ══════════════════════════════════════════════════════════════

@router.get("/brands")
async def get_brands():
    return [
        {
            "id": brand_id,
            "name": profile["name"],
            "slug": profile["slug"],
            "title": profile["title"],
            "subtitle": profile["subtitle"],
        }
        for brand_id, profile in BRAND_PROFILES.items()
    ]


# ══════════════════════════════════════════════════════════════
#  Leads
# ══════════════════════════════════════════════════════════════

@router.post("/lead")
async def receive_lead(lead: LeadData, background_tasks: BackgroundTasks):
    logger.info(
        "Lead received | brand=%s | channel=%s | phone_suffix=%s",
        lead.brand,
        lead.channel,
        str(lead.user_phone)[-4:],
    )
    background_tasks.add_task(notify_all_channels, lead)
    return {"status": "received"}


# ══════════════════════════════════════════════════════════════
#  Meta (WhatsApp + Messenger)
# ══════════════════════════════════════════════════════════════

@router.get("/webhook/meta")
async def meta_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == META_VERIFY:
        return PlainTextResponse(hub_challenge or "")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook/meta")
async def meta_messages(request: Request, background_tasks: BackgroundTasks):
    body_bytes = await request.body()

    # التحقق من التوقيع
    if META_SECRET:
        sig = request.headers.get("X-Hub-Signature-256", "")
        if not _verify_meta_signature(body_bytes, sig):
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        import json
        data = json.loads(body_bytes)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            # WhatsApp
            for msg in value.get("messages", []):
                if msg.get("type") == "text":
                    wa_id = msg["from"]
                    text = msg["text"]["body"]
                    background_tasks.add_task(_handle_whatsapp, wa_id, text)
            # Messenger
            for messaging in value.get("messaging", []):
                msg = messaging.get("message", {})
                if msg.get("text"):
                    sender_id = messaging["sender"]["id"]
                    background_tasks.add_task(_handle_messenger, sender_id, msg["text"])

    return {"status": "ok"}


# ══════════════════════════════════════════════════════════════
#  Telegram
# ══════════════════════════════════════════════════════════════

@router.post("/webhook/telegram")
async def telegram_messages(request: Request, background_tasks: BackgroundTasks):
    # التحقق من Telegram secret
    if TG_WEBHOOK_SECRET:
        token_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if token_header != TG_WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Invalid Telegram secret")

    try:
        import json
        data = json.loads(await request.body())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    msg = data.get("message", {})
    if msg and msg.get("text"):
        chat_id = msg["chat"]["id"]
        text = msg["text"]
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
            extra_metadata={"channel": "whatsapp"},
        )
        for resp in responses:
            if isinstance(resp, dict) and resp.get("text"):
                await send_whatsapp(wa_id, resp["text"])
    except Exception as exc:
        logger.error("WhatsApp handler error for %s: %s", wa_id[-4:], exc)


async def _handle_messenger(sender_id: str, text: str) -> None:
    try:
        responses = await rasa_send(
            sender_id=f"fb_{sender_id}",
            text=text,
            brand=None,
            extra_metadata={"channel": "messenger"},
        )
        for resp in responses:
            if isinstance(resp, dict) and resp.get("text"):
                await send_messenger(sender_id, resp["text"])
    except Exception as exc:
        logger.error("Messenger handler error: %s", exc)


async def _handle_telegram(chat_id: int, text: str) -> None:
    try:
        responses = await rasa_send(
            sender_id=f"tg_{chat_id}",
            text=text,
            brand=None,
            extra_metadata={"channel": "telegram"},
        )
        for resp in responses:
            if isinstance(resp, dict) and resp.get("text"):
                await send_telegram(chat_id, resp["text"])
    except Exception as exc:
        logger.error("Telegram handler error for %s: %s", chat_id, exc)


# ══════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════

def _verify_meta_signature(body: bytes, signature: str) -> bool:
    if not META_SECRET or not signature:
        return False
    expected = "sha256=" + hmac.new(
        META_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
