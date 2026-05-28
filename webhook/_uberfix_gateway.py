"""
webhook/_uberfix_gateway.py
============================
UberFix gateway bridge for AzaBot.

This module supports both styles used in the project:
1) Async FastAPI request forwarding.
2) Sync handler used from webhook/server.py through run_in_threadpool.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional, Tuple

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("alazab.uberfix")

_BOT_GW = os.getenv(
    "BOT_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/bot-gateway",
).rstrip("/")

_MAINT_GW = os.getenv(
    "MAINTENANCE_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway",
).rstrip("/")

_API_KEY = os.getenv("BOT_API_KEY", os.getenv("UBERFIX_API_KEY", "")).strip()
_TIMEOUT = float(os.getenv("UBERFIX_GATEWAY_TIMEOUT", "20"))


def _headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if _API_KEY:
        headers["x-api-key"] = _API_KEY
    return headers


def _safe_json_response(resp: httpx.Response) -> dict[str, Any]:
    try:
        data = resp.json()
        if isinstance(data, dict):
            return data
        return {"success": False, "data": data}
    except Exception:
        return {
            "success": False,
            "error": "non_json_gateway_response",
            "message": resp.text[:1000],
        }


def _normalize_payload(payload: dict[str, Any], context: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    body = dict(payload or {})
    metadata = body.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    metadata.setdefault("source", "azabot")
    metadata.setdefault("proxy", "webhook/_uberfix_gateway.py")

    if context:
        metadata["request_context"] = {
            "route": context.get("route"),
            "client_ip": context.get("client_ip"),
            "user_agent": context.get("user_agent"),
            "origin": context.get("origin"),
        }

    body["metadata"] = metadata
    return body


def _forward_sync(url: str, body: dict[str, Any]) -> Tuple[dict[str, Any], int]:
    if not url:
        return {
            "success": False,
            "error": "gateway_url_missing",
            "message": "UberFix gateway URL is not configured.",
        }, 500

    try:
        with httpx.Client(timeout=_TIMEOUT, follow_redirects=False) as client:
            resp = client.post(url, json=body, headers=_headers())
        return _safe_json_response(resp), resp.status_code
    except httpx.TimeoutException:
        logger.exception("UberFix gateway timeout | url=%s", url)
        return {
            "success": False,
            "error": "gateway_timeout",
            "message": "UberFix gateway timeout.",
        }, 504
    except Exception as exc:
        logger.exception("UberFix gateway failed | url=%s", url)
        return {
            "success": False,
            "error": "gateway_failed",
            "message": str(exc),
        }, 502


async def _forward_async(url: str, body: dict[str, Any]) -> JSONResponse:
    data, status = await _run_sync_forward(url, body)
    return JSONResponse(content=data, status_code=status)


async def _run_sync_forward(url: str, body: dict[str, Any]) -> Tuple[dict[str, Any], int]:
    """Keep forwarding behavior identical between async and sync routes."""
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT, follow_redirects=False) as client:
            resp = await client.post(url, json=body, headers=_headers())
        return _safe_json_response(resp), resp.status_code
    except httpx.TimeoutException:
        logger.exception("UberFix gateway timeout | url=%s", url)
        return {
            "success": False,
            "error": "gateway_timeout",
            "message": "UberFix gateway timeout.",
        }, 504
    except Exception as exc:
        logger.exception("UberFix gateway failed | url=%s", url)
        return {
            "success": False,
            "error": "gateway_failed",
            "message": str(exc),
        }, 502


def handle_uberfix_gateway_sync(
    payload: dict[str, Any],
    context: Optional[dict[str, Any]] = None,
) -> Tuple[dict[str, Any], int]:
    """
    Sync handler used by webhook/server.py:
        resp, status = await run_in_threadpool(handle_uberfix_gateway_sync, payload, ctx)

    It forwards the normalized BotGatewayRequest payload to the unified bot-gateway.
    """
    body = _normalize_payload(payload, context)
    return _forward_sync(_BOT_GW, body)


def handle_uberfix_transition_sync(
    payload: dict[str, Any],
    context: Optional[dict[str, Any]] = None,
) -> Tuple[dict[str, Any], int]:
    """Sync helper for maintenance workflow transitions."""
    body = _normalize_payload(payload, context)
    return _forward_sync(_MAINT_GW, body)


async def handle_uberfix_gateway(request: Request) -> JSONResponse:
    """POST /uberfix/bot-gateway -> bot-gateway."""
    try:
        body = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="JSON مطلوب") from exc

    body = _normalize_payload(body, {
        "route": str(request.url.path),
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "origin": request.headers.get("origin"),
    })
    return await _forward_async(_BOT_GW, body)


async def handle_uberfix_transition(request: Request) -> JSONResponse:
    """POST /uberfix/transition -> maintenance-gateway."""
    try:
        body = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="JSON مطلوب") from exc

    body = _normalize_payload(body, {
        "route": str(request.url.path),
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "origin": request.headers.get("origin"),
    })
    return await _forward_async(_MAINT_GW, body)
