"""Application service for maintenance conversations."""

from __future__ import annotations

import logging
from typing import Any, Optional

from . import responses
from .errors import MaintenanceConfigError, MaintenanceGatewayError, MaintenanceValidationError
from .gateway_client import MaintenanceGatewayClient
from .schemas import build_create_request, extract_request_number

logger = logging.getLogger(__name__)


class MaintenanceService:
    def __init__(self, gateway: Optional[MaintenanceGatewayClient] = None):
        self.gateway = gateway or MaintenanceGatewayClient()

    def create_request(
        self,
        *,
        client_name: Any,
        client_phone: Any,
        description: Any,
        tracker_sender_id: Optional[str],
    ) -> dict[str, Any]:
        try:
            request = build_create_request(
                client_name=client_name,
                client_phone=client_phone,
                description=description,
                tracker_sender_id=tracker_sender_id,
            )
            ticket = self.gateway.create_request(request)
            logger.info(
                "Maintenance request created | request=%s | service=%s | priority=%s | phone_suffix=%s",
                ticket.display_number,
                request.service_type,
                request.priority,
                request.client_phone[-4:],
            )
            return responses.create_success(ticket)
        except MaintenanceValidationError as exc:
            return responses.missing_fields(exc.missing_fields)
        except MaintenanceConfigError:
            logger.exception("Maintenance gateway is not configured")
            return responses.not_configured()
        except MaintenanceGatewayError:
            logger.exception("Maintenance gateway failed while creating request")
            return responses.create_failed()

    def track_request(self, text: str) -> dict[str, Any]:
        order_id = extract_request_number(text)
        if not order_id:
            return responses.track_prompt()
        status = self.gateway.get_status_text(order_id)
        return responses.track_result(order_id, status)

    def subscriptions(self) -> dict[str, Any]:
        return responses.subscriptions()
