"""
webhook/services/notifications.py — Lead & Event Notifications
===============================================================
يُرسل إشعارات العملاء الجدد عبر:
  - WhatsApp (للفريق)
  - Telegram (للفريق)
  - CRM Webhook (لأي نظام خارجي)

يتجنب loop التكرار عند إرسال /lead لنفس الـ webhook.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from ..config import (
    NOTIFY_PHONE,
    NOTIFY_TG_CHAT,
    TG_TOKEN,
    WA_TOKEN,
    WA_URL,
    WEBHOOK_NOTIFY,
)
from ..models import LeadData
from ..utils import is_internal_lead_notify_url
from .channels import send_telegram, send_whatsapp

logger = logging.getLogger("alazab.webhook.notifications")

_TIMEOUT = 8.0


async def notify_all_channels(lead: LeadData) -> None:
    """يُرسل إشعار عميل جديد عبر كل القنوات المفعّلة."""
    msg = _format_lead_message(lead)

    if NOTIFY_PHONE and WA_URL and WA_TOKEN:
        ok = await send_whatsapp(NOTIFY_PHONE, msg)
        logger.info("Lead WA notification: %s | brand=%s", "sent" if ok else "failed", lead.brand)

    if NOTIFY_TG_CHAT and TG_TOKEN:
        try:
            ok = await send_telegram(int(NOTIFY_TG_CHAT), msg)
            logger.info("Lead TG notification: %s", "sent" if ok else "failed")
        except (ValueError, TypeError):
            logger.error("NOTIFY_TG_CHAT is not a valid integer: %r", NOTIFY_TG_CHAT)

    if WEBHOOK_NOTIFY:
        if is_internal_lead_notify_url(WEBHOOK_NOTIFY):
            logger.warning(
                "WEBHOOK_NOTIFY_URL loops back to this server — skipping to prevent infinite loop"
            )
            return
        await _post_crm_webhook(lead)


def _format_lead_message(lead: LeadData) -> str:
    brand_emoji = {
        "uberfix":             "🔧",
        "laban_alasfour":      "🪵",
        "alazab_construction": "🏗️",
        "luxury_finishing":    "✨",
        "brand_identity":      "🎨",
    }.get((lead.brand or "").lower(), "🏢")

    return (
        f"{brand_emoji} *عميل جديد — {lead.brand}*\n"
        f"الاسم: {lead.user_name}\n"
        f"الهاتف: {lead.user_phone}\n"
        f"الطلب: {lead.user_message[:300]}\n"
        f"القناة: {lead.channel}\n"
        f"المحادثة: {lead.conversation_id or '—'}"
    )


async def _post_crm_webhook(lead: LeadData) -> None:
    """يُرسل بيانات العميل لـ CRM Webhook."""
    payload = {
        "brand":           lead.brand,
        "user_name":       lead.user_name,
        "user_phone":      lead.user_phone,
        "user_message":    lead.user_message,
        "channel":         lead.channel,
        "conversation_id": lead.conversation_id,
        "timestamp":       datetime.now(timezone.utc).isoformat(),
    }
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(WEBHOOK_NOTIFY, json=payload)
            if r.status_code >= 300:
                logger.warning(
                    "CRM webhook returned %s for brand=%s",
                    r.status_code, lead.brand
                )
    except httpx.TimeoutException:
        logger.error("CRM webhook timeout for brand=%s", lead.brand)
    except Exception as exc:
        logger.error("CRM webhook error: %s", exc)
