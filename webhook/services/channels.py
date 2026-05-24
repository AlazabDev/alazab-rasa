"""
webhook/services/channels.py — Outgoing Channel Senders
=========================================================
WhatsApp Business API · Facebook Messenger · Telegram
"""
from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

from ..config import META_TOKEN, TG_API_BASE, TG_TOKEN, WA_TOKEN, WA_URL

logger = logging.getLogger("alazab.webhook.channels")

_TIMEOUT = float(os.getenv("CHANNEL_SEND_TIMEOUT", "10"))


# ══════════════════════════════════════════════════════════════
#  WhatsApp Business API
# ══════════════════════════════════════════════════════════════

async def send_whatsapp(to: str, text: str) -> bool:
    """إرسال رسالة نصية عبر WhatsApp Business API."""
    if not (WA_URL and WA_TOKEN and to):
        logger.warning("WhatsApp not configured — WA_URL=%s token=%s", bool(WA_URL), bool(WA_TOKEN))
        return False

    clean_to = to.lstrip("+").replace(" ", "").strip()

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                WA_URL,
                headers={
                    "Authorization": f"Bearer {WA_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": clean_to,
                    "type": "text",
                    "text": {"preview_url": False, "body": text[:4096]},
                },
            )
            if r.status_code >= 300:
                logger.error("WhatsApp [%s] to=...%s: %s", r.status_code, clean_to[-4:], r.text[:300])
                return False
            logger.info("WhatsApp sent to ...%s", clean_to[-4:])
            return True
    except httpx.TimeoutException:
        logger.error("WhatsApp timeout to=...%s", clean_to[-4:])
        return False
    except Exception as exc:
        logger.error("WhatsApp error: %s", exc)
        return False


async def send_whatsapp_template(
    to: str,
    template_name: str,
    lang: str = "ar",
    components: Optional[list] = None,
) -> bool:
    """إرسال WhatsApp Template Message."""
    if not (WA_URL and WA_TOKEN and to):
        return False

    clean_to = to.lstrip("+").replace(" ", "").strip()
    body: dict = {
        "messaging_product": "whatsapp",
        "to": clean_to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": lang},
        },
    }
    if components:
        body["template"]["components"] = components

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                WA_URL,
                headers={"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"},
                json=body,
            )
            if r.status_code >= 300:
                logger.error("WA template [%s]: %s", r.status_code, r.text[:200])
                return False
            return True
    except Exception as exc:
        logger.error("WA template error: %s", exc)
        return False


async def send_whatsapp_buttons(to: str, text: str, buttons: list[dict]) -> bool:
    """إرسال رسالة مع أزرار تفاعلية (Interactive Buttons)."""
    if not (WA_URL and WA_TOKEN and to) or not buttons:
        return await send_whatsapp(to, text)

    clean_to = to.lstrip("+").replace(" ", "").strip()
    btn_rows = [{"type": "reply", "reply": {"id": b.get("id", str(i)), "title": b["title"][:20]}}
                for i, b in enumerate(buttons[:3])]

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                WA_URL,
                headers={"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"},
                json={
                    "messaging_product": "whatsapp",
                    "to": clean_to,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {"text": text},
                        "action": {"buttons": btn_rows},
                    },
                },
            )
            if r.status_code >= 300:
                logger.error("WA buttons [%s]: %s", r.status_code, r.text[:200])
                return await send_whatsapp(to, text)
            return True
    except Exception as exc:
        logger.error("WA buttons error: %s", exc)
        return await send_whatsapp(to, text)


# ══════════════════════════════════════════════════════════════
#  Facebook Messenger
# ══════════════════════════════════════════════════════════════

async def send_messenger(to: str, text: str) -> bool:
    """إرسال رسالة عبر Facebook Messenger."""
    if not META_TOKEN:
        logger.warning("Messenger not configured — META_TOKEN missing")
        return False
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                "https://graph.facebook.com/v18.0/me/messages",
                params={"access_token": META_TOKEN},
                json={
                    "recipient": {"id": to},
                    "message": {"text": text[:2000]},
                    "messaging_type": "RESPONSE",
                },
            )
            if r.status_code >= 300:
                logger.error("Messenger [%s] to=%s: %s", r.status_code, to, r.text[:200])
                return False
            return True
    except httpx.TimeoutException:
        logger.error("Messenger timeout to=%s", to)
        return False
    except Exception as exc:
        logger.error("Messenger error: %s", exc)
        return False


# ══════════════════════════════════════════════════════════════
#  Telegram
# ══════════════════════════════════════════════════════════════

async def send_telegram(chat_id: int, text: str,
                         parse_mode: str = "Markdown") -> bool:
    """إرسال رسالة عبر Telegram Bot API."""
    if not TG_TOKEN:
        logger.warning("Telegram not configured — TELEGRAM_BOT_TOKEN missing")
        return False
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                f"{TG_API_BASE}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text[:4096],
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True,
                },
            )
            if r.status_code >= 300:
                logger.error("Telegram [%s] to=%s: %s", r.status_code, chat_id, r.text[:200])
                return False
            return True
    except httpx.TimeoutException:
        logger.error("Telegram timeout to=%s", chat_id)
        return False
    except Exception as exc:
        logger.error("Telegram error: %s", exc)
        return False


async def send_telegram_keyboard(chat_id: int, text: str, buttons: list[list[str]]) -> bool:
    """إرسال Telegram رسالة مع لوحة مفاتيح."""
    if not TG_TOKEN:
        return False
    keyboard = [[{"text": btn} for btn in row] for row in buttons]
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                f"{TG_API_BASE}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text[:4096],
                    "parse_mode": "Markdown",
                    "reply_markup": {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": True},
                },
            )
            return r.status_code < 300
    except Exception as exc:
        logger.error("Telegram keyboard error: %s", exc)
        return False
