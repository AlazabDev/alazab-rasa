"""
actions/brand_actions/maintenance_actions.py
=============================================
Actions لتدفقات الصيانة في data/flows/maintenance.yml

هذا الملف يُغطي:
  - action_create_maintenance_request
  - action_get_maintenance_status
  - action_triage_maintenance_request
  - action_assign_maintenance_request

كل action تستخدم MaintenanceService الموجودة في actions/maintenance/
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from ..maintenance import MaintenanceService

logger = logging.getLogger(__name__)


def _slot(tracker: Tracker, *names: str, fallback: str = "") -> str:
    """يقرأ أول slot غير فارغة من القائمة."""
    for name in names:
        val = tracker.get_slot(name)
        if val:
            return str(val).strip()
    return fallback


# ══════════════════════════════════════════════════════════════
#  Create
# ══════════════════════════════════════════════════════════════

class ActionCreateMaintenanceRequest(Action):
    """ينشئ طلب صيانة جديد عبر UberFix Bot Gateway."""

    def name(self) -> Text:
        return "action_create_maintenance_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        service = MaintenanceService()
        result = service.create_request(
            client_name=_slot(tracker, "maintenance_client_name", "user_name"),
            client_phone=_slot(tracker, "maintenance_client_phone", "user_phone"),
            description=_slot(
                tracker,
                "maintenance_description",
                "user_message",
                fallback="طلب صيانة",
            ),
            tracker_sender_id=tracker.sender_id,
        )
        dispatcher.utter_message(
            text=str(result.get("text", "")),
            buttons=result.get("buttons") or None,
        )
        # تخزين رقم الطلب إذا وُجد
        events: List[Dict[Text, Any]] = []
        ticket_num = result.get("ticket_number") or result.get("request_number")
        if ticket_num:
            events.append(SlotSet("maintenance_request_number", str(ticket_num)))
        events.append(SlotSet("brand", "uberfix"))
        return events


# ══════════════════════════════════════════════════════════════
#  Get Status
# ══════════════════════════════════════════════════════════════

class ActionGetMaintenanceStatus(Action):
    """يجلب حالة طلب صيانة من النظام."""

    def name(self) -> Text:
        return "action_get_maintenance_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        request_id = _slot(
            tracker,
            "maintenance_request_id",
            "maintenance_request_number",
            "order_id",
        )
        service = MaintenanceService()
        result = service.track_request(request_id or tracker.latest_message.get("text", ""))
        dispatcher.utter_message(
            text=str(result.get("text", "")),
            buttons=result.get("buttons") or None,
        )
        if request_id:
            return [SlotSet("maintenance_status", result.get("status", ""))]
        return []


# ══════════════════════════════════════════════════════════════
#  Triage
# ══════════════════════════════════════════════════════════════

class ActionTriageMaintenanceRequest(Action):
    """ينقل الطلب لمرحلة المراجعة الفنية (triaged)."""

    def name(self) -> Text:
        return "action_triage_maintenance_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        request_id = _slot(
            tracker,
            "maintenance_request_id",
            "maintenance_request_number",
            "order_id",
        )
        if not request_id:
            dispatcher.utter_message(text="يرجى تزويدي برقم الطلب لمتابعة عملية المراجعة.")
            return []

        service = MaintenanceService()
        result = service.triage_request(request_id)
        dispatcher.utter_message(
            text=str(result.get("text", "تمت مراجعة الطلب بنجاح.")),
        )
        return [SlotSet("maintenance_stage", "triaged")]


# ══════════════════════════════════════════════════════════════
#  Assign
# ══════════════════════════════════════════════════════════════

class ActionAssignMaintenanceRequest(Action):
    """يعيّن فنياً لطلب الصيانة."""

    def name(self) -> Text:
        return "action_assign_maintenance_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        request_id = _slot(
            tracker,
            "maintenance_request_id",
            "maintenance_request_number",
            "order_id",
        )
        if not request_id:
            dispatcher.utter_message(text="يرجى تزويدي برقم الطلب لتعيين الفني.")
            return []

        service = MaintenanceService()
        result = service.assign_request(request_id)
        dispatcher.utter_message(
            text=str(result.get("text", "تم تعيين الفني وسيتواصل معك قريباً.")),
        )
        return [SlotSet("maintenance_stage", "assigned")]
