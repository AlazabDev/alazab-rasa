"""
webhook/_uberfix_gateway.py — UberFix Gateway Proxy
=====================================================
يُحوّل كل طلبات bot-gateway إلى Supabase Edge Function (uberfix).

قبل: كان يتصل بـ PostgreSQL مباشرة عبر psycopg2 (37KB من الكود)
بعد: HTTP call واحد لـ Edge Function على Supabase

Edge Function URL:
  https://fjojyzvulhvqeitnaenv.supabase.co/functions/v1/uberfix
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("alazab.webhook.uberfix_gateway")

# ── Config ────────────────────────────────────────────────────
_SUPABASE_URL  = os.getenv("SUPABASE_URL", "").rstrip("/")
_API_KEY       = (
    os.getenv("UBERFIX_API_KEY", "")
    or os.getenv("MAINTENANCE_API_KEY", "")
)
_EDGE_URL      = f"{_SUPABASE_URL}/functions/v1/uberfix"
_TIMEOUT       = 15.0


def _headers() -> dict:
    return {
        "Content-Type":  "application/json",
        "x-api-key":     _API_KEY,
        "Authorization": f"Bearer {_API_KEY}",
    }


async def handle_uberfix_gateway(request: Request) -> JSONResponse:
    """
    النقطة الرئيسية — تستقبل طلب POST /uberfix/bot-gateway
    وتُعيد تحويله للـ Edge Function على Supabase.
    """
    if not _SUPABASE_URL:
        raise HTTPException(503, "SUPABASE_URL غير مضبوط")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "Request body يجب أن يكون JSON")

    # إضافة معلومات الطلب الأصلي
    body.setdefault("metadata", {})
    body["metadata"]["source"]     = "bot_gateway"
    body["metadata"]["user_agent"] = request.headers.get("user-agent", "")

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(_EDGE_URL, json=body, headers=_headers())

        data = resp.json()

        if resp.status_code >= 500:
            logger.error("UberFix Edge Function error %s: %s", resp.status_code, data)
            raise HTTPException(502, "خطأ في خدمة UberFix")

        return JSONResponse(content=data, status_code=resp.status_code)

    except httpx.TimeoutException:
        logger.error("UberFix Edge Function timeout")
        raise HTTPException(504, "انتهت مهلة الاستجابة من خدمة UberFix")
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("UberFix gateway error: %s", exc)
        raise HTTPException(500, "خطأ غير متوقع في بوابة UberFix")
