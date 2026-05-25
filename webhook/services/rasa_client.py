"""
webhook/services/rasa_client.py — Rasa Client v4.1
====================================================
✅ Retry مع exponential backoff (3 محاولات)
✅ Fallback message بدل HTTPException عند الفشل الكامل
✅ يستخدم httpx.AsyncClient الموحّد (connection pooling)
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

import httpx
from fastapi import HTTPException

from ..config import RASA_URL, RASA_REQUEST_TIMEOUT

logger = logging.getLogger("alazab.webhook.rasa")

_FALLBACK = [{"text": "عذراً، واجهت صعوبة في معالجة رسالتك. يرجى المحاولة مجدداً أو تواصل معنا مباشرة."}]
_MAX_RETRIES  = 3
_BACKOFF      = [0.5, 1.0, 2.0]

def _shared_client() -> Optional[httpx.AsyncClient]:
    try:
        from ..server import get_http_client
        return get_http_client()
    except Exception:
        return None

async def rasa_send(
    sender_id: str,
    text: str,
    brand: Optional[str] = None,
    extra_metadata: Optional[dict[str, Any]] = None,
    *,
    use_fallback: bool = True,
) -> list:
    payload: dict[str, Any] = {"sender": sender_id, "message": text}
    meta: dict[str, Any] = {}
    if brand:
        meta["brand"] = brand
    if extra_metadata:
        meta.update({k: v for k, v in extra_metadata.items() if v is not None})
    if meta:
        payload["metadata"] = meta

    url    = f"{RASA_URL}/webhooks/rest/webhook"
    client = _shared_client()
    last_err: Exception | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            if client and not client.is_closed:
                r = await client.post(url, json=payload, timeout=RASA_REQUEST_TIMEOUT)
            else:
                async with httpx.AsyncClient(timeout=RASA_REQUEST_TIMEOUT) as c:
                    r = await c.post(url, json=payload)
            r.raise_for_status()
            return r.json()
        except httpx.TimeoutException as e:
            last_err = e
            logger.warning("Rasa timeout (attempt %d/%d) | sender=%s", attempt + 1, _MAX_RETRIES, sender_id)
        except httpx.HTTPStatusError as e:
            if e.response.status_code < 500:
                logger.error("Rasa 4xx: %s | sender=%s", e, sender_id)
                break
            last_err = e
            logger.warning("Rasa 5xx (attempt %d/%d) | sender=%s", attempt + 1, _MAX_RETRIES, sender_id)
        except Exception as e:
            last_err = e
            logger.warning("Rasa error (attempt %d/%d): %s | sender=%s", attempt + 1, _MAX_RETRIES, e, sender_id)

        if attempt < _MAX_RETRIES - 1:
            await asyncio.sleep(_BACKOFF[attempt])

    logger.error("Rasa unreachable after %d attempts | sender=%s | last=%s", _MAX_RETRIES, sender_id, last_err)
    if use_fallback:
        return _FALLBACK
    raise HTTPException(status_code=504 if isinstance(last_err, httpx.TimeoutException) else 502,
                        detail="خطأ في الاتصال بالبوت")
