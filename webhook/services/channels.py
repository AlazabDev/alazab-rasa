"""
webhook/services/channels.py — Outgoing Channel Senders
=========================================================
WhatsApp · Messenger · Telegram
"""

from __future__ import annotations

import logging

import httpx

from ..config import META_TOKEN, TG_API_BASE, TG_TOKEN, WA_TOKEN, WA_URL

logger = logging.getLogger("alazab.webhook.channels")


async def send_whatsapp(to: str, text: str) -> bool:
    if not (WA_URL and WA_TOKEN):
        return False
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.post(
                WA_URL,
                headers={"Authorization": f"Bearer {WA_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "to": to, "type": "text",
                    "text": {"body": text},
                },
            )
            return r.status_code == 200
    except Exception as e:
        logger.error(f"WhatsApp send error: {e}")
        return False


async def send_messenger(to: str, text: str) -> bool:
    if not META_TOKEN:
        return False
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.post(
                "https://graph.facebook.com/v18.0/me/messages",
                params={"access_token": META_TOKEN},
                json={"recipient": {"id": to}, "message": {"text": text}},
            )
            return r.status_code == 200
    except Exception as e:
        logger.error(f"Messenger send error: {e}")
        return False


async def send_telegram(chat_id: int, text: str) -> bool:
    if not TG_TOKEN:
        return False
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.post(
                f"{TG_API_BASE}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            )
            return r.status_code == 200
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False
