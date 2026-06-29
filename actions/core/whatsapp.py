"""
actions/core/whatsapp.py
=========================
مُرسِل واتساب مركزي لجميع الـ actions.

المشكلة القديمة:
  نفس كود الإرسال مكرر في:
  - action_general.py (_send_whatsapp_text)
  - whatsapp_sender.py
  - webhook/services/channels.py

الحل:
  دالة send_text واحدة تُستخدم في كل مكان.
  تستخدم httpx بدلاً من aiohttp (أخف وموحد مع الـ webhook).
"""
from __future__ import annotations

import logging
from typing import Optional

import httpx

from ..config import WHATSAPP_API_URL, WHATSAPP_TOKEN

logger = logging.getLogger(__name__)

_TIMEOUT = 10.0


async def send_text(phone: str, text: str, token: Optional[str] = None, api_url: Optional[str] = None) -> bool:
    """
    يُرسل رسالة نصية عبر WhatsApp Cloud API.

    Args:
        phone: رقم الهاتف (بدون + أو مع)
        text: نص الرسالة
        token: Bearer token (اختياري — يأخذ من البيئة تلقائياً)
        api_url: رابط API (اختياري — يأخذ من البيئة تلقائياً)

    Returns:
        True عند النجاح، False عند الفشل
    """
    _token = token or WHATSAPP_TOKEN
    _url = api_url or WHATSAPP_API_URL

    if not (_token and _url and phone and text):
        missing = [k for k, v in {"token": _token, "url": _url, "phone": phone, "text": text}.items() if not v]
        logger.warning("send_text: missing config: %s", missing)
        return False

    clean_phone = phone.lstrip("+").strip()

    payload = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "text",
        "text": {"body": text[:4096]},
    }
    headers = {
        "Authorization": f"Bearer {_token}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(_url, json=payload, headers=headers)
            if resp.status_code >= 300:
                logger.error(
                    "WhatsApp send failed [%s]: %s",
                    resp.status_code,
                    resp.text[:200],
                )
                return False
            return True
    except httpx.TimeoutException:
        logger.error("WhatsApp send timeout for phone=%s", clean_phone[-4:])
        return False
    except Exception as exc:
        logger.error("WhatsApp send error: %s", exc)
        return False


async def send_notification(text: str, notify_phone: Optional[str] = None) -> bool:
    """
    اختصار لإرسال إشعار لفريق الدعم.
    يقرأ NOTIFY_PHONE من البيئة إذا لم يُحدد.
    """
    from ..config import NOTIFY_PHONE

    phone = notify_phone or NOTIFY_PHONE
    if not phone:
        logger.debug("send_notification: NOTIFY_PHONE not configured")
        return False
    return await send_text(phone, text)
