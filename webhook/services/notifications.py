"""
webhook/services/notifications.py — Lead & Integration Notifications
=====================================================================
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from ..config import (
    META_TOKEN,
    NOTIFY_PHONE,
    NOTIFY_TG_CHAT,
    TG_TOKEN,
    WA_TOKEN,
    WA_URL,
    WEBHOOK_NOTIFY,
)
from ..models import LeadData
from ..utils import is_internal_lead_notify_url
from .admin_data import load_admin_data, save_admin_data
from .channels import send_telegram, send_whatsapp

logger = logging.getLogger("alazab.webhook.notifications")


async def notify_all_channels(lead: LeadData) -> None:
    """يُرسل إشعار عميل جديد عبر كل القنوات المفعلة."""
    msg = (
        f"🔔 *عميل جديد — {lead.brand}*\n"
        f"الاسم: {lead.user_name}\n"
        f"الهاتف: {lead.user_phone}\n"
        f"الطلب: {lead.user_message}\n"
        f"القناة: {lead.channel}\n"
        f"المحادثة: {lead.conversation_id or 'غير محدد'}"
    )

    # WhatsApp
    if NOTIFY_PHONE and WA_URL and WA_TOKEN:
        await send_whatsapp(NOTIFY_PHONE, msg)

    # Telegram
    if NOTIFY_TG_CHAT and TG_TOKEN:
        await send_telegram(int(NOTIFY_TG_CHAT), msg)

    # CRM Webhook
    if WEBHOOK_NOTIFY:
        if is_internal_lead_notify_url(WEBHOOK_NOTIFY):
            logger.warning(
                "WEBHOOK_NOTIFY_URL points back to this bot /lead endpoint; skipping to avoid a notification loop."
            )
            return
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                await client.post(WEBHOOK_NOTIFY, json={
                    "brand":           lead.brand,
                    "user_name":       lead.user_name,
                    "user_phone":      lead.user_phone,
                    "user_message":    lead.user_message,
                    "channel":         lead.channel,
                    "conversation_id": lead.conversation_id,
                    "timestamp":       datetime.now(timezone.utc).isoformat(),
                })
        except Exception as e:
            logger.error(f"CRM webhook error: {e}")


# ══════════════════════════════════════════════════════════════
#  Integration Dispatch
# ══════════════════════════════════════════════════════════════
def format_integration_message(event: str, payload: dict[str, Any]) -> str:
    conversation = payload.get("conversation", {}) if isinstance(payload.get("conversation"), dict) else {}
    message = payload.get("message", {}) if isinstance(payload.get("message"), dict) else {}
    responses = payload.get("responses", []) if isinstance(payload.get("responses"), list) else []
    response_text = "\n".join(
        str(item.get("content", "")).strip()
        for item in responses
        if isinstance(item, dict) and str(item.get("content", "")).strip()
    )
    lines = [
        f"AzaBot event: {event}",
        f"Channel: {conversation.get('channel') or '-'}",
        f"Brand: {conversation.get('brand') or '-'}",
        f"Session: {conversation.get('session_id') or '-'}",
        "",
        f"User: {message.get('content') or '-'}",
    ]
    if response_text:
        lines.extend(["", f"Bot: {response_text}"])
    return "\n".join(lines).strip()


async def deliver_integration_event(
    integration: dict[str, Any],
    event: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    config = integration.get("config", {}) if isinstance(integration.get("config"), dict) else {}
    request_payload = {
        "event": event,
        "integration": {
            "id": integration.get("id"),
            "type": integration.get("type"),
            "name": integration.get("name"),
        },
        "data": payload,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }
    log_item = {
        "id": str(uuid.uuid4()),
        "integration_id": integration.get("id"),
        "integration_type": integration.get("type"),
        "event": event,
        "request_payload": request_payload,
        "status": "success",
        "status_code": None,
        "response_body": "",
        "error_message": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        integration_type = integration.get("type")
        response = None

        if integration_type == "webhook":
            url = str(config.get("url") or "").strip()
            if not url:
                raise ValueError("Webhook URL is required")
            headers = {"Content-Type": "application/json"}
            secret = str(config.get("secret") or "").strip()
            if secret:
                headers["X-AzaBot-Secret"] = secret
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=request_payload, headers=headers)

        elif integration_type == "telegram":
            bot_token = str(config.get("bot_token") or "").strip()
            chat_id = str(config.get("chat_id") or "").strip()
            if not bot_token or not chat_id:
                raise ValueError("Telegram bot_token and chat_id are required")
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": format_integration_message(event, payload)},
                )

        elif integration_type == "whatsapp":
            phone_number_id = str(config.get("phone_number_id") or "").strip()
            access_token = str(config.get("access_token") or "").strip()
            recipient = str(config.get("recipient") or "").strip()
            if not phone_number_id or not access_token or not recipient:
                raise ValueError("WhatsApp phone_number_id, access_token and recipient are required")
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"https://graph.facebook.com/v20.0/{phone_number_id}/messages",
                    headers={"Authorization": f"Bearer {access_token}"},
                    json={
                        "messaging_product": "whatsapp",
                        "to": recipient,
                        "type": "text",
                        "text": {"body": format_integration_message(event, payload)[:4000]},
                    },
                )

        elif integration_type == "twilio":
            account_sid = str(config.get("account_sid") or "").strip()
            auth_token = str(config.get("auth_token") or "").strip()
            from_number = str(config.get("from") or "").strip()
            to_number = str(config.get("to") or "").strip()
            if not account_sid or not auth_token or not from_number or not to_number:
                raise ValueError("Twilio account_sid, auth_token, from and to are required")
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
                    data={
                        "From": from_number,
                        "To": to_number,
                        "Body": format_integration_message(event, payload)[:1500],
                    },
                    auth=(account_sid, auth_token),
                )

        else:
            raise ValueError(f"Unsupported integration type: {integration_type}")

        if response is not None:
            log_item["status_code"] = response.status_code
            log_item["response_body"] = response.text[:2000]
            if response.status_code >= 400:
                log_item["status"] = "failed"
                log_item["error_message"] = response.text[:500]

    except Exception as exc:
        log_item["status"] = "failed"
        log_item["error_message"] = str(exc)

    return log_item


async def dispatch_integrations(event: str, payload: dict[str, Any]) -> None:
    """Send event to all enabled integrations."""
    data = load_admin_data()
    integrations = [
        item for item in data.get("integrations", [])
        if item.get("enabled") and event in (item.get("events") or [])
    ]
    if not integrations:
        return

    logs = data.setdefault("logs", [])
    for integration in integrations:
        log_item = await deliver_integration_event(integration, event, payload)
        logs.insert(0, log_item)
    data["logs"] = logs[:200]
    save_admin_data(data)


async def test_integration(integration: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    """Test an integration by sending a sample event."""
    event = "integration.test"
    payload = {
        "conversation": {
            "id": "test",
            "session_id": "integration-test",
            "brand": "test",
            "channel": "admin",
            "message_count": 1,
        },
        "message": {
            "id": "test-message",
            "role": "user",
            "content": "اختبار تكامل AzaBot",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        "responses": [{
            "id": "test-response",
            "role": "assistant",
            "content": "هذه رسالة اختبار من لوحة تحكم AzaBot.",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }],
    }
    log_item = await deliver_integration_event(integration, event, payload)
    logs = data.setdefault("logs", [])
    logs.insert(0, log_item)
    data["logs"] = logs[:200]
    save_admin_data(data)
    return {
        "status": "success" if log_item["status"] == "success" else "failed",
        "statusCode": log_item.get("status_code"),
        "errorMessage": log_item.get("error_message"),
    }
