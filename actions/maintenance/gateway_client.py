"""
actions/maintenance/gateway_client.py
=======================================
Client يتصل بـ bot-gateway الموحّد.

الـ class MaintenanceGatewayClient يتوافق مع MaintenanceService:
  - create_request(request: MaintenanceRequest) -> MaintenanceTicket
  - get_status_text(order_id: str) -> str
  - transition_stage(request_id, to_stage, reason) -> dict
"""
from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

from .errors import MaintenanceConfigError, MaintenanceGatewayError
from .schemas import MaintenanceRequest, MaintenanceTicket, normalize_ticket

logger = logging.getLogger(__name__)

_BOT_GATEWAY   = os.getenv("BOT_GATEWAY_URL", "").rstrip("/")
_MAINT_GATEWAY = os.getenv("MAINTENANCE_GATEWAY_URL", "").rstrip("/")
_API_KEY       = os.getenv("BOT_API_KEY", os.getenv("UBERFIX_API_KEY", "")).strip()
_TRACK_BASE    = os.getenv("MAINTENANCE_GATEWAY_URL_TRACK", "https://uberfix.shop/track")
_TIMEOUT       = 20.0


def _headers() -> dict:
    return {"Content-Type": "application/json", "x-api-key": _API_KEY}


def _call(action: str, payload: dict, session_id: Optional[str] = None) -> dict:
    """استدعاء bot-gateway — متزامن (sync)."""
    if not _BOT_GATEWAY:
        raise MaintenanceConfigError("BOT_GATEWAY_URL not configured")
    body = {"action": action, "payload": payload, "metadata": {"source": "azabot"}}
    if session_id:
        body["session_id"] = session_id
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            r = client.post(_BOT_GATEWAY, json=body, headers=_headers())
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("bot-gateway %s → HTTP %s", action, exc.response.status_code)
        raise MaintenanceGatewayError(f"Gateway HTTP {exc.response.status_code}") from exc
    except Exception as exc:
        logger.error("bot-gateway %s → %s", action, exc)
        raise MaintenanceGatewayError(str(exc)) from exc


async def _async_call(action: str, payload: dict,
                      session_id: Optional[str] = None) -> dict:
    """نسخة async من _call."""
    if not _BOT_GATEWAY:
        raise MaintenanceConfigError("BOT_GATEWAY_URL not configured")
    body = {"action": action, "payload": payload, "metadata": {"source": "azabot"}}
    if session_id:
        body["session_id"] = session_id
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(_BOT_GATEWAY, json=body, headers=_headers())
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("bot-gateway %s → HTTP %s", action, exc.response.status_code)
        raise MaintenanceGatewayError(f"Gateway HTTP {exc.response.status_code}") from exc
    except Exception as exc:
        logger.error("bot-gateway %s → %s", action, exc)
        raise MaintenanceGatewayError(str(exc)) from exc


# ── Async helpers (تُستخدم من brand_actions/uberfix.py) ──────

async def create_request(
    client_name: str,
    client_phone: str,
    service_type: str = "general",
    description: str = "",
    location: str = "",
    priority: str = "medium",
    session_id: Optional[str] = None,
) -> dict:
    return await _async_call("create_request", {
        "client_name":  client_name,
        "client_phone": client_phone,
        "service_type": service_type,
        "title":        description[:80],
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
    return await _async_call("add_note", {"request_id": request_id, "note": note})


async def list_services() -> dict:
    return await _async_call("list_services", {})


async def list_categories() -> dict:
    return await _async_call("list_categories", {})


async def get_branches() -> dict:
    return await _async_call("get_branches", {})


async def get_quote(service_type: str, description: str = "") -> dict:
    return await _async_call("get_quote", {
        "service_type": service_type,
        "description":  description,
    })


def transition_stage(request_id: str, to_stage: str, reason: str = "") -> dict:
    """تغيير مرحلة الطلب — عبر maintenance-gateway."""
    if not _MAINT_GATEWAY:
        raise MaintenanceConfigError("MAINTENANCE_GATEWAY_URL not configured")
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
        raise MaintenanceGatewayError(str(exc)) from exc


# ══════════════════════════════════════════════════════════════
# MaintenanceGatewayClient — متوافق مع MaintenanceService
# ══════════════════════════════════════════════════════════════

class MaintenanceGatewayClient:
    """
    Wrapper يتوافق مع MaintenanceService:
      - create_request(request: MaintenanceRequest) -> MaintenanceTicket
      - get_status_text(order_id: str) -> str
      - transition_stage(request_id, to_stage, reason) -> dict
    """

    def create_request(self, request: MaintenanceRequest) -> MaintenanceTicket:
        """
        يستقبل MaintenanceRequest dataclass ويُعيد MaintenanceTicket.
        يتوافق مع: ticket = self.gateway.create_request(request)
        """
        data = _call("create_request", {
            "client_name":     request.client_name,
            "client_phone":    request.client_phone,
            "service_type":    request.service_type,
            "title":           request.title,
            "description":     request.description,
            "location":        request.location,
            "priority":        request.priority,
            "idempotency_key": request.idempotency_key,
            "channel":         request.channel,
        }, session_id=request.session_id)

        if not data.get("success", True):
            raise MaintenanceGatewayError(
                str(data.get("error") or data.get("message") or "Gateway failed")
            )

        return normalize_ticket(data, _TRACK_BASE)

    def get_status_text(self, order_id: str) -> str:
        """
        يُعيد نص الحالة كـ string.
        يتوافق مع: status = self.gateway.get_status_text(order_id)
        """
        try:
            data = _call("check_status", {
                "search_term": order_id,
                "search_type": "request_number",
            })
        except MaintenanceGatewayError:
            return "لم أتمكن من جلب حالة الطلب الآن."

        if not data.get("success", True):
            return "لم أتمكن من جلب حالة الطلب الآن."

        # استخراج نص الحالة
        stage = (
            data.get("workflow_stage")
            or data.get("status")
            or data.get("message")
            or "قيد المراجعة"
        )
        stage_labels = {
            "submitted":    "✅ تم الاستلام، جارٍ المراجعة",
            "triaged":      "📋 قيد المراجعة الفنية",
            "assigned":     "👷 تم تعيين الفني",
            "scheduled":    "🗓️ تم تحديد موعد الزيارة",
            "in_progress":  "🔧 جارٍ التنفيذ الآن",
            "inspection":   "🔍 جارٍ فحص العمل",
            "waiting_parts":"⏳ انتظار قطع غيار",
            "completed":    "✅ تم الإنجاز بنجاح",
            "billed":       "🧾 تم إصدار الفاتورة",
            "paid":         "💰 تم الدفع",
            "closed":       "🏁 تم الإغلاق النهائي",
            "cancelled":    "❌ ملغي",
        }
        return stage_labels.get(str(stage), str(stage))

    def transition_stage(
        self, request_id: str, to_stage: str, reason: str = ""
    ) -> dict:
        return transition_stage(request_id, to_stage, reason)
