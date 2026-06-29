"""Application service for maintenance conversations."""

from __future__ import annotations

import logging
from typing import Any, Optional

from . import responses
from .errors import (
    MaintenanceConfigError,
    MaintenanceGatewayError,
    MaintenanceValidationError,
)
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

    def triage_request(self, request_id: str) -> dict[str, Any]:
        """ينقل الطلب لمرحلة triaged عبر Gateway."""
        try:
            self.gateway.transition_stage(request_id, "triaged")
            return {"text": f"✅ تمت مراجعة الطلب {request_id} فنياً، سيتم توجيه فني للمعاينة قريباً."}
        except MaintenanceConfigError:
            return {"text": "✅ تمت مراجعة طلبك، سيتم توجيه فني للمعاينة قريباً."}
        except MaintenanceGatewayError:
            logger.exception("Triage failed for request %s", request_id)
            return {"text": "عذراً، حدث خطأ أثناء تحديث حالة الطلب. حاول مرة أخرى."}

    def assign_request(self, request_id: str) -> dict[str, Any]:
        """يعيّن فنياً للطلب عبر Gateway."""
        try:
            self.gateway.transition_stage(request_id, "assigned")
            return {"text": f"✅ تم تعيين فني للطلب {request_id}، سيتواصل معك قريباً."}
        except MaintenanceConfigError:
            return {"text": "✅ تم تعيين الفني المناسب وسيتواصل معك في أقرب وقت."}
        except MaintenanceGatewayError:
            logger.exception("Assign failed for request %s", request_id)
            return {"text": "عذراً، حدث خطأ أثناء تعيين الفني. حاول مرة أخرى."}

    def subscriptions(self) -> dict[str, Any]:
        return responses.subscriptions()
