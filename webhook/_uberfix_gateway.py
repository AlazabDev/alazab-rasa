"""
webhook/_uberfix_gateway.py
============================
يُوجّه طلبات /uberfix/bot-gateway للـ bot-gateway الموحّد.
يُوجّه طلبات /uberfix/transition للـ maintenance-gateway.
"""
import logging, os
import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("alazab.uberfix")

# ✅ بدون project ID مكتوب صريحاً — يجب ضبط هذه المتغيرات في .env
_BOT_GW   = os.getenv("BOT_GATEWAY_URL", "").strip()
_MAINT_GW = os.getenv("MAINTENANCE_GATEWAY_URL", "").strip()
_API_KEY  = os.getenv("BOT_API_KEY", os.getenv("UBERFIX_API_KEY", ""))
_TIMEOUT  = 20.0

if not _BOT_GW or not _MAINT_GW:
    logger.warning("[_uberfix_gateway] ⚠️  BOT_GATEWAY_URL/MAINTENANCE_GATEWAY_URL غير مضبوطة في .env")


def _headers():
    return {"Content-Type": "application/json", "x-api-key": _API_KEY}


async def handle_uberfix_gateway(request: Request) -> JSONResponse:
    """POST /uberfix/bot-gateway → bot-gateway"""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "JSON مطلوب")
    return await _forward(_BOT_GW, body)


async def handle_uberfix_transition(request: Request) -> JSONResponse:
    """POST /uberfix/transition → maintenance-gateway"""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "JSON مطلوب")
    return await _forward(_MAINT_GW, body)


async def _forward(url: str, body: dict) -> JSONResponse:
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=body, headers=_headers())
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.TimeoutException:
        raise HTTPException(504, "timeout")
    except Exception as exc:
        logger.error("uberfix gateway: %s", exc)
        raise HTTPException(500, str(exc))
