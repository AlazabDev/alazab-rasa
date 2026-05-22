"""
webhook/services/channels.py — Outgoing Channel Senders
=========================================================
WhatsApp · Messenger · Telegram

[محسّن] 
- timeout موحد قابل للضبط عبر env
- تسجيل أوضح للأخطاء مع status code
- تجنب f-string logging مع exceptions
"""

from __future__ import annotations

import logging
import os

import httpx

from ..config import META_TOKEN, TG_API_BASE, TG_TOKEN, WA_TOKEN, WA_URL

logger = logging.getLogger("alazab.webhook.channels")

_TIMEOUT = float(os.getenv("CHANNEL_SEND_TIMEOUT", "10"))


async def send_whatsapp(to: str, text: str) -> bool:
    if not (WA_URL and WA_TOKEN and to):
        return False
    clean_to = to.lstrip("+").strip()
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                WA_URL,
                headers={"Authorization": f"Bearer {WA_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "to": clean_to,
                    "type": "text",
                    "text": {"body": text[:4096]},
                },
            )
            if r.status_code >= 300:
                logger.error(
                    "WhatsApp send failed [%s] to=%s: %s",
                    r.status_code, clean_to[-4:], r.text[:200],
                )
                return False
            return True
    except httpx.TimeoutException:
        logger.error("WhatsApp send timeout to=%s", clean_to[-4:])
        return False
    except Exception as exc:
        logger.error("WhatsApp send error: %s", exc)
        return False


async def send_messenger(to: str, text: str) -> bool:
    if not META_TOKEN:
        return False
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                "https://graph.facebook.com/v18.0/me/messages",
                params={"access_token": META_TOKEN},
                json={"recipient": {"id": to}, "message": {"text": text}},
            )
            if r.status_code >= 300:
                logger.error("Messenger send failed [%s] to=%s", r.status_code, to)
                return False
            return True
    except httpx.TimeoutException:
        logger.error("Messenger send timeout to=%s", to)
        return False
    except Exception as exc:
        logger.error("Messenger send error: %s", exc)
        return False


async def send_telegram(chat_id: int, text: str) -> bool:
    if not TG_TOKEN:
        return False
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                f"{TG_API_BASE}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            )
            if r.status_code >= 300:
                logger.error("Telegram send failed [%s] to=%s", r.status_code, chat_id)
                return False
            return True
    except httpx.TimeoutException:
        logger.error("Telegram send timeout to=%s", chat_id)
        return False
    except Exception as exc:
        logger.error("Telegram send error: %s", exc)
        return False
