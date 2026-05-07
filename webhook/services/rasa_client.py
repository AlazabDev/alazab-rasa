"""
webhook/services/rasa_client.py — Rasa Server Communication
=============================================================
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import httpx
from fastapi import HTTPException

from ..config import RASA_URL, RASA_REQUEST_TIMEOUT

logger = logging.getLogger("alazab.webhook.rasa")


async def rasa_send(
    sender_id: str,
    text: str,
    brand: Optional[str] = None,
    extra_metadata: Optional[dict[str, Any]] = None,
) -> list:
    """Send a message to Rasa and return responses."""
    payload: dict[str, Any] = {"sender": sender_id, "message": text}
    metadata: dict[str, Any] = {}
    if brand:
        metadata["brand"] = brand
    if extra_metadata:
        metadata.update({k: v for k, v in extra_metadata.items() if v is not None})
    if metadata:
        payload["metadata"] = metadata

    try:
        async with httpx.AsyncClient(timeout=RASA_REQUEST_TIMEOUT) as client:
            r = await client.post(
                f"{RASA_URL}/webhooks/rest/webhook",
                json=payload,
            )
            r.raise_for_status()
            return r.json()
    except httpx.TimeoutException:
        logger.error(f"Rasa timeout | sender={sender_id}")
        raise HTTPException(status_code=504, detail="انتهت مهلة الاتصال بالبوت")
    except Exception as e:
        logger.error(f"Rasa error | {e}")
        raise HTTPException(status_code=502, detail="خطأ في الاتصال بالبوت")
