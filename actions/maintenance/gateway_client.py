"""Gateway client for UberFix maintenance operations."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from .errors import MaintenanceConfigError, MaintenanceGatewayError
from .schemas import MaintenanceRequest, MaintenanceTicket, build_track_url, normalize_ticket

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MaintenanceGatewayConfig:
    maintenance_gateway_url: str
    bot_gateway_url: str
    status_api_url: str
    api_key: str
    track_base_url: str

    @classmethod
    def from_env(cls) -> "MaintenanceGatewayConfig":
        return cls(
            maintenance_gateway_url=(
                os.getenv("MAINTENANCE_GATEWAY_URL", "")
                or os.getenv("UBERFIX_API_URL", "")
            ).rstrip("/"),
            bot_gateway_url=os.getenv("UBERFIX_BOT_GATEWAY_URL", "").rstrip("/"),
            status_api_url=os.getenv("UBERFIX_STATUS_API_URL", "").rstrip("/"),
            api_key=(
                os.getenv("MAINTENANCE_API_KEY", "")
                or os.getenv("UBERFIX_API_KEY", "")
            ).strip(),
            track_base_url=os.getenv("UBERFIX_TRACK_BASE_URL", "https://uberfix.shop/track").rstrip("/"),
        )


class MaintenanceGatewayClient:
    def __init__(self, config: MaintenanceGatewayConfig | None = None):
        self.config = config or MaintenanceGatewayConfig.from_env()

    def create_request(self, request: MaintenanceRequest) -> MaintenanceTicket:
        if self.config.maintenance_gateway_url and not self.config.bot_gateway_url:
            return self._create_via_maintenance_gateway(request)
        if self.config.bot_gateway_url:
            return self._create_via_bot_gateway(request)
        raise MaintenanceConfigError("Maintenance gateway is not configured")

    def get_status_text(self, request_number: str) -> str:
        normalized = (request_number or "").strip().upper()
        if not normalized:
            return "من فضلك أرسل رقم الطلب كاملًا وسأتحقق منه فورًا."

        if self.config.bot_gateway_url:
            try:
                data = self._post_json(
                    self.config.bot_gateway_url,
                    {
                        "action": "check_status",
                        "payload": {
                            "search_term": normalized,
                            "search_type": "request_number",
                        },
                        "session_id": f"track_{normalized}",
                        "metadata": {"source": "azabot", "locale": "ar"},
                    },
                    timeout=12,
                )
                if data.get("success"):
                    return self._format_status_response(normalized, data)
                logger.warning("UberFix status gateway rejected request | request=%s", normalized)
            except MaintenanceGatewayError:
                logger.exception("UberFix status gateway failed | request=%s", normalized)

        if self.config.status_api_url:
            try:
                response = httpx.get(
                    f"{self.config.status_api_url}/{quote(normalized, safe='')}",
                    headers=self._headers(),
                    timeout=8,
                )
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict):
                    return self._format_status_response(normalized, data)
            except Exception:
                logger.exception("UberFix legacy status failed | request=%s", normalized)

        return self._track_link_message(normalized)

    def _create_via_maintenance_gateway(self, request: MaintenanceRequest) -> MaintenanceTicket:
        payload = {
            "channel": request.channel,
            "client_name": request.client_name,
            "client_phone": request.client_phone,
            "service_type": request.service_type,
            "description": request.description,
            "priority": request.priority,
            "location": request.location,
            "idempotency_key": request.idempotency_key,
        }
        data = self._post_json(
            self.config.maintenance_gateway_url,
            payload,
            timeout=10,
            idempotency_key=request.idempotency_key,
        )
        if not data.get("success"):
            raise MaintenanceGatewayError(str(data.get("error") or data.get("message") or "Create request failed"))
        return normalize_ticket(data, self.config.track_base_url)

    def _create_via_bot_gateway(self, request: MaintenanceRequest) -> MaintenanceTicket:
        data = self._post_json(
            self.config.bot_gateway_url,
            {
                "action": "create_request",
                "payload": {
                    "client_name": request.client_name,
                    "client_phone": request.client_phone,
                    "location": request.location,
                    "service_type": request.service_type,
                    "title": request.title,
                    "description": request.description,
                    "priority": request.priority,
                    "idempotency_key": request.idempotency_key,
                },
                "session_id": request.session_id,
                "metadata": {
                    "source": "azabot",
                    "locale": "ar",
                    "idempotency_key": request.idempotency_key,
                },
            },
            timeout=12,
            idempotency_key=request.idempotency_key,
        )
        if not data.get("success"):
            raise MaintenanceGatewayError(str(data.get("error") or data.get("message") or "Create request failed"))
        return normalize_ticket(data, self.config.track_base_url)

    def _post_json(
        self,
        url: str,
        payload: dict[str, Any],
        *,
        timeout: int,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        try:
            headers = self._headers()
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key
            response = httpx.post(url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise MaintenanceGatewayError("Invalid gateway response")
            return data
        except MaintenanceGatewayError:
            raise
        except Exception as exc:
            raise MaintenanceGatewayError(str(exc)) from exc

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["x-api-key"] = self.config.api_key
        return headers

    def _format_status_response(self, order_id: str, data: dict[str, Any]) -> str:
        result: Any = data.get("data")
        if isinstance(result, dict):
            items = result.get("items") or result.get("requests") or result.get("results")
            if isinstance(items, list) and items:
                result = items[0]
        elif isinstance(result, list) and result:
            result = result[0]

        if not isinstance(result, dict):
            message = str(data.get("message") or "").strip()
            return f"{message}\n{build_track_url(self.config.track_base_url, order_id)}" if message else self._track_link_message(order_id)

        status = result.get("status") or result.get("workflow_stage") or result.get("stage") or "غير محدد"
        request_number = result.get("request_number") or result.get("tracking_number") or order_id
        tech = result.get("technician_name") or result.get("assigned_technician_name") or ""
        eta = result.get("eta") or result.get("scheduled_at") or result.get("appointment_time") or ""
        track_url = result.get("track_url") or build_track_url(self.config.track_base_url, str(request_number))

        msg = f"الحالة: *{status}*"
        if tech:
            msg += f" | الفني: {tech}"
        if eta:
            msg += f" | الموعد: {eta}"
        if track_url:
            msg += f"\nرابط التتبع: {track_url}"
        return msg

    def _track_link_message(self, order_id: str) -> str:
        track_url = build_track_url(self.config.track_base_url, order_id)
        return (
            "رقم الطلب صحيح وتم التعرف عليه.\n"
            "متابعة الحالة تتم من رابط التتبع المباشر:\n"
            f"{track_url}"
        )
