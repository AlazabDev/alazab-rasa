"""
actions/maintenance/gateway_client.py
=======================================
Client يتصل بـ bot-gateway الموحّد.

Gateway: https://zrrffsjbfkphridqyais.supabase.co/functions/v1/bot-gateway
Auth:    x-api-key header فقط

Actions المدعومة (من BOTS_API_INTEGRATION_GUIDE.md):
  create_request, check_status, get_request_details,
  update_request, cancel_request, add_note,
  list_technicians, assign_technician,
  list_services, list_categories, get_branches,
  find_nearest_branch, get_quote, collect_customer_info,
  daftra_sync_client, daftra_create_invoice, brand_navigator
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

_BOT_GATEWAY    = os.getenv("BOT_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/bot-gateway"
).rstrip("/")

_MAINT_GATEWAY  = os.getenv("MAINTENANCE_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway"
).rstrip("/")

_API_KEY        = os.getenv("BOT_API_KEY", os.getenv("UBERFIX_API_KEY", "")).strip()
_TIMEOUT        = 20.0


def _headers() -> dict:
    return {"Content-Type": "application/json", "x-api-key": _API_KEY}


def _call(action: str, payload: dict,
          session_id: Optional[str] = None,
          source: str = "azabot") -> dict:
    """استدعاء bot-gateway بأي action."""
    body: dict[str, Any] = {
        "action":   action,
        "payload":  payload,
        "metadata": {"source": source},
    }
    if session_id:
        body["session_id"] = session_id
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            r = client.post(_BOT_GATEWAY, json=body, headers=_headers())
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("bot-gateway %s → HTTP %s: %s", action, exc.response.status_code, exc.response.text[:200])
        return {"success": False, "error": str(exc)}
    except Exception as exc:
        logger.error("bot-gateway %s → %s", action, exc)
        return {"success": False, "error": str(exc)}


async def _async_call(action: str, payload: dict,
                      session_id: Optional[str] = None,
                      source: str = "azabot") -> dict:
    """نسخة async من _call."""
    body: dict[str, Any] = {
        "action":   action,
        "payload":  payload,
        "metadata": {"source": source},
    }
    if session_id:
        body["session_id"] = session_id
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(_BOT_GATEWAY, json=body, headers=_headers())
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("bot-gateway %s → HTTP %s", action, exc.response.status_code)
        return {"success": False, "error": str(exc)}
    except Exception as exc:
        logger.error("bot-gateway %s → %s", action, exc)
        return {"success": False, "error": str(exc)}


# ══════════════════════════════════════════════════════════════
# A. إدارة الطلبات
# ══════════════════════════════════════════════════════════════

async def create_request(
    client_name: str, client_phone: str, service_type: str,
    description: str, location: str = "",
    title: str = "", priority: str = "medium",
    session_id: Optional[str] = None,
) -> dict:
    return await _async_call("create_request", {
        "client_name":  client_name,
        "client_phone": client_phone,
        "service_type": service_type,
        "title":        title or description[:80],
        "description":  description,
        "location":     location,
        "priority":     priority,
    }, session_id)


async def check_status(search_term: str, search_type: str = "request_number") -> dict:
    return await _async_call("check_status", {
        "search_term": search_term,
        "search_type": search_type,
    })


async def get_request_details(request_number: str, client_phone: str = "") -> dict:
    return await _async_call("get_request_details", {
        "request_number": request_number,
        "client_phone":   client_phone,
    })


async def cancel_request(request_id: str, client_phone: str, reason: str = "") -> dict:
    return await _async_call("cancel_request", {
        "request_id":   request_id,
        "client_phone": client_phone,
        "reason":       reason or "إلغاء بطلب العميل",
    })


async def add_note(request_id: str, note: str) -> dict:
    return await _async_call("add_note", {
        "request_id": request_id,
        "note":       note,
    })


async def update_request(request_id: str, client_phone: str, updates: dict) -> dict:
    return await _async_call("update_request", {
        "request_id":   request_id,
        "client_phone": client_phone,
        "updates":      updates,
    })


# ══════════════════════════════════════════════════════════════
# B. الفنيون
# ══════════════════════════════════════════════════════════════

async def list_technicians(specialization: str = "", limit: int = 10) -> dict:
    payload: dict = {"limit": limit}
    if specialization:
        payload["specialization"] = specialization
    return await _async_call("list_technicians", payload)


async def assign_technician(request_id: str, auto: bool = True,
                             technician_id: Optional[str] = None) -> dict:
    payload: dict = {"request_id": request_id}
    if auto:
        payload["auto"] = True
    elif technician_id:
        payload["technician_id"] = technician_id
    return await _async_call("assign_technician", payload)


# ══════════════════════════════════════════════════════════════
# C. الكاتالوج
# ══════════════════════════════════════════════════════════════

async def list_services() -> dict:
    return await _async_call("list_services", {})


async def list_categories() -> dict:
    return await _async_call("list_categories", {})


async def get_branches() -> dict:
    return await _async_call("get_branches", {})


async def find_nearest_branch(lat: float, lng: float) -> dict:
    return await _async_call("find_nearest_branch", {"latitude": lat, "longitude": lng})


async def get_quote(service_type: str, description: str = "") -> dict:
    return await _async_call("get_quote", {
        "service_type": service_type,
        "description":  description,
    })


# ══════════════════════════════════════════════════════════════
# D. العميل والمحاسبة
# ══════════════════════════════════════════════════════════════

async def collect_customer_info(client_phone: str, client_name: str = "",
                                  location: str = "",
                                  session_id: Optional[str] = None) -> dict:
    return await _async_call("collect_customer_info", {
        "client_phone": client_phone,
        "client_name":  client_name,
        "location":     location,
    }, session_id)


async def daftra_sync_client(client_name: str, client_phone: str,
                               request_id: str = "") -> dict:
    return await _async_call("daftra_sync_client", {
        "client_name":  client_name,
        "client_phone": client_phone,
        "request_id":   request_id,
    })


async def daftra_create_invoice(request_id: str, amount: float,
                                  status: str = "draft") -> dict:
    return await _async_call("daftra_create_invoice", {
        "request_id": request_id,
        "amount":     amount,
        "status":     status,
    })


async def brand_navigator(interest: str, session_id: Optional[str] = None) -> dict:
    return await _async_call("brand_navigator", {"interest": interest}, session_id)


# ══════════════════════════════════════════════════════════════
# transition_stage — عبر maintenance-gateway (للإدارة الداخلية)
# ══════════════════════════════════════════════════════════════

def transition_stage(request_id: str, to_stage: str, reason: str = "") -> dict:
    """تغيير مرحلة الطلب — عبر maintenance-gateway (للاستخدام الإداري)."""
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            r = client.post(_MAINT_GATEWAY, json={
                "action":     "transition_stage",
                "request_id": request_id,
                "to_stage":   to_stage,
                "reason":     reason,
                "channel":    "azabot",
            }, headers=_headers())
            return r.json()
    except Exception as exc:
        logger.error("transition_stage %s: %s", to_stage, exc)
        return {"success": False, "error": str(exc)}
