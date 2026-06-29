"""
webhook/services/integrations.py — Integration Delivery Engine
================================================================
محرك التكاملات الخارجية: Webhook · Telegram · WhatsApp · Twilio · Daftra · OpenAI · Supabase

[مُستخرَج من server.py — كان مدفوناً بين سطر 2956–3210]

يوفر:
  dispatch_integrations()  → يُرسل حدثاً لكل التكاملات المفعّلة
  test_integration()        → يختبر تكامل واحد من لوحة التحكم
  deliver_event()           → يُرسل لتكامل واحد ويُعيد log
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger("alazab.webhook.integrations")

_TIMEOUT = 10.0


# ══════════════════════════════════════════════════════════════
#  Public API
# ══════════════════════════════════════════════════════════════

async def dispatch_integrations(event: str, payload: dict[str, Any]) -> None:
    """
    يُرسل حدثاً لجميع التكاملات المفعّلة المشتركة في الحدث.
    يُسجّل نتيجة كل عملية في admin_data.logs.
    """
    from .admin_data import load_admin_data, save_admin_data

    data = load_admin_data()
    integrations = [
        item
        for item in data.get("integrations", [])
        if item.get("enabled") and event in (item.get("events") or [])
    ]
    if not integrations:
        return

    logs = data.setdefault("logs", [])
    for integration in integrations:
        log_item = await deliver_event(integration, event, payload)
        logs.insert(0, log_item)
    data["logs"] = logs[:200]
    save_admin_data(data)


async def test_integration(
    integration: dict[str, Any], data: dict[str, Any]
) -> dict[str, Any]:
    """يختبر تكاملاً واحداً بإرسال حدث اختباري ويُعيد نتيجة مباشرة."""
    from .admin_data import save_admin_data

    event = "integration.test"
    now = datetime.now(timezone.utc).isoformat()
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
            "created_at": now,
        },
        "responses": [
            {
                "id": "test-response",
                "role": "assistant",
                "content": "هذه رسالة اختبار من لوحة تحكم AzaBot.",
                "created_at": now,
            }
        ],
    }
    log_item = await deliver_event(integration, event, payload)
    logs = data.setdefault("logs", [])
    logs.insert(0, log_item)
    data["logs"] = logs[:200]
    save_admin_data(data)
    return {
        "status": "success" if log_item["status"] == "success" else "failed",
        "statusCode": log_item.get("status_code"),
        "errorMessage": log_item.get("error_message"),
    }


async def deliver_event(
    integration: dict[str, Any],
    event: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    يُرسل حدثاً لتكامل واحد ويُعيد log item كاملاً.
    يدعم: webhook · telegram · whatsapp · twilio · daftra · openai · supabase
    """
    config: dict[str, Any] = integration.get("config", {}) or {}
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
    log_item: dict[str, Any] = {
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
        response = await _dispatch_by_type(
            integration.get("type", ""), config, event, payload, request_payload
        )
        log_item["status_code"] = response.status_code
        log_item["response_body"] = response.text[:2000]
        if response.status_code >= 400:
            log_item["status"] = "failed"
            log_item["error_message"] = response.text[:500]
    except Exception as exc:
        log_item["status"] = "failed"
        log_item["error_message"] = str(exc)
        logger.warning(
            "Integration delivery failed [%s / %s]: %s",
            integration.get("type"),
            event,
            exc,
        )

    return log_item


# ══════════════════════════════════════════════════════════════
#  Internal Dispatchers
# ══════════════════════════════════════════════════════════════

async def _dispatch_by_type(
    integration_type: str,
    config: dict[str, Any],
    event: str,
    payload: dict[str, Any],
    request_payload: dict[str, Any],
) -> httpx.Response:
    """يوجّه الطلب للـ handler المناسب حسب نوع التكامل."""
    handlers = {
        "webhook": _send_webhook,
        "telegram": _send_telegram,
        "whatsapp": _send_whatsapp,
        "twilio": _send_twilio,
        "daftra": _ping_daftra,
        "openai": _ping_openai,
        "supabase": _ping_supabase,
    }
    handler = handlers.get(integration_type)
    if handler is None:
        raise ValueError(f"Unsupported integration type: {integration_type!r}")
    return await handler(config, event, payload, request_payload)


# ══ SSRF Protection ════════════════════════════════════════════
import ipaddress as _ipaddress
import socket as _socket

_BLOCKED_NETS = [
    _ipaddress.ip_network("127.0.0.0/8"), _ipaddress.ip_network("::1/128"),
    _ipaddress.ip_network("10.0.0.0/8"), _ipaddress.ip_network("172.16.0.0/12"),
    _ipaddress.ip_network("192.168.0.0/16"), _ipaddress.ip_network("169.254.0.0/16"),
    _ipaddress.ip_network("fe80::/10"), _ipaddress.ip_network("fc00::/7"),
]
_BLOCKED_HOSTS = {"localhost", "metadata.google.internal", "169.254.169.254"}


def _validate_webhook_url(url: str) -> None:
    """يرفع ValueError إذا كان الـ URL يشير لموارد داخلية (SSRF)."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"بروتوكول غير مدعوم: {parsed.scheme!r}")
    if os.getenv("NODE_ENV") == "production" and parsed.scheme != "https":
        raise ValueError("يجب استخدام https:// في الإنتاج")
    hostname = (parsed.hostname or "").lower().strip()
    if not hostname:
        raise ValueError("URL لا يحتوي hostname صحيح")
    if hostname in _BLOCKED_HOSTS:
        raise ValueError(f"الوجهة محظورة لأسباب أمنية: {hostname!r}")
    try:
        for _f, _t, _p, _c, sockaddr in _socket.getaddrinfo(hostname, None):
            ip = _ipaddress.ip_address(sockaddr[0])
            if any(ip in net for net in _BLOCKED_NETS):
                raise ValueError(f"SSRF محظور — عنوان داخلي: {sockaddr[0]}")
    except _socket.gaierror:
        raise ValueError(f"تعذّر تحليل الـ hostname: {hostname!r}")


async def _send_webhook(config, event, payload, request_payload) -> httpx.Response:
    url = str(config.get("url") or "").strip()
    if not url:
        raise ValueError("Webhook URL مطلوب")
    _validate_webhook_url(url)  # ✅ حماية SSRF
    headers = {"Content-Type": "application/json", "User-Agent": "AzaBot-Webhook/4.1"}
    secret = str(config.get("secret") or "").strip()
    if secret:
        import hashlib as _h, hmac as _hm, json as _json, time as _time
        ts = str(int(_time.time()))
        body = _json.dumps(request_payload, ensure_ascii=False)
        sig = _hm.new(secret.encode(), f"{ts}.{body}".encode(), _h.sha256).hexdigest()
        headers["X-AzaBot-Signature"] = f"t={ts},v1={sig}"
    async with httpx.AsyncClient(timeout=_TIMEOUT, follow_redirects=False) as client:
        return await client.post(url, json=request_payload, headers=headers)


async def _send_telegram(config, event, payload, request_payload) -> httpx.Response:
    bot_token = str(config.get("bot_token") or "").strip()
    chat_id = str(config.get("chat_id") or "").strip()
    if not bot_token or not chat_id:
        raise ValueError("Telegram bot_token and chat_id are required")
    text = _format_message(event, payload)
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )


async def _send_whatsapp(config, event, payload, request_payload) -> httpx.Response:
    phone_number_id = str(config.get("phone_number_id") or "").strip()
    access_token = str(config.get("access_token") or "").strip()
    recipient = str(config.get("recipient") or "").strip()
    if not all([phone_number_id, access_token, recipient]):
        raise ValueError("WhatsApp phone_number_id, access_token and recipient are required")
    text = _format_message(event, payload)
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.post(
            f"https://graph.facebook.com/v20.0/{phone_number_id}/messages",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "text",
                "text": {"body": text[:4000]},
            },
        )


async def _send_twilio(config, event, payload, request_payload) -> httpx.Response:
    account_sid = str(config.get("account_sid") or "").strip()
    auth_token = str(config.get("auth_token") or "").strip()
    from_number = str(config.get("from") or "").strip()
    to_number = str(config.get("to") or "").strip()
    if not all([account_sid, auth_token, from_number, to_number]):
        raise ValueError("Twilio account_sid, auth_token, from and to are required")
    text = _format_message(event, payload)
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
            data={"From": from_number, "To": to_number, "Body": text[:1500]},
            auth=(account_sid, auth_token),
        )


async def _ping_daftra(config, event, payload, request_payload) -> httpx.Response:
    api_key = str(config.get("api_key") or "").strip()
    base_url = str(config.get("base_url") or "").strip()
    if not api_key or not base_url:
        raise ValueError("Daftra api_key and base_url are required")
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.get(f"{base_url}/clients", headers={"apikey": api_key})


async def _ping_openai(config, event, payload, request_payload) -> httpx.Response:
    api_key = str(config.get("api_key") or "").strip()
    if not api_key:
        raise ValueError("OpenAI api_key is required")
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
        )


async def _ping_supabase(config, event, payload, request_payload) -> httpx.Response:
    url = str(config.get("url") or "").strip()
    anon_key = str(config.get("anon_key") or "").strip()
    if not url or not anon_key:
        raise ValueError("Supabase url and anon_key are required")
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        return await client.get(
            f"{url}/rest/v1/",
            headers={"apikey": anon_key, "Authorization": f"Bearer {anon_key}"},
        )


# ══════════════════════════════════════════════════════════════
#  Message Formatter
# ══════════════════════════════════════════════════════════════

def _format_message(event: str, payload: dict[str, Any]) -> str:
    """يُنسّق رسالة نصية قابلة للقراءة من حدث التكامل."""
    conversation = payload.get("conversation") or {}
    message = payload.get("message") or {}
    responses = payload.get("responses") or []
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


def integration_conversation_payload(conversation: dict[str, Any]) -> dict[str, Any]:
    """يبني payload مبسّط للمحادثة لإرساله مع أحداث التكامل."""
    return {
        "id": conversation.get("id"),
        "session_id": conversation.get("session_id"),
        "brand": conversation.get("brand"),
        "channel": conversation.get("channel"),
        "created_at": conversation.get("created_at"),
        "last_message_at": conversation.get("last_message_at"),
        "message_count": conversation.get(
            "message_count", len(conversation.get("messages", []))
        ),
    }
