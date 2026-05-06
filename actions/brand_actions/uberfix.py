"""
actions/brand_actions/uberfix.py
==================================
Rasa entry points for UberFix maintenance.

The heavy maintenance logic lives in actions/maintenance. This file stays thin:
read slots from Rasa, call the maintenance service, and return messages/buttons.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from ..maintenance import MaintenanceService


def _utter_result(dispatcher: CollectingDispatcher, result: dict[str, Any]) -> None:
    dispatcher.utter_message(
        text=str(result.get("text") or ""),
        buttons=result.get("buttons") or None,
    )


import json as _ctx_json

def _from_ctx(tracker, field: str, fallback: str = "غير محدد") -> str:
    """سحب قيمة من context_memory أو الـ slot مباشرة."""
    direct = tracker.get_slot(field)
    if direct:
        return direct
    raw = tracker.get_slot("context_memory") or "{}"
    try:
        ctx = _ctx_json.loads(raw)
    except Exception:
        ctx = {}
    return ctx.get(field) or fallback


def _build_full_message(tracker) -> str:
    """بناء رسالة شاملة من context_memory."""
    raw = tracker.get_slot("context_memory") or "{}"
    try:
        ctx = _ctx_json.loads(raw)
    except Exception:
        ctx = {}

    parts = []
    if tracker.get_slot("user_message"):
        parts.append(tracker.get_slot("user_message"))
    elif ctx.get("problem_description"):
        parts.append(ctx["problem_description"])
    if ctx.get("branch_name"):
        parts.append(f"الفرع: {ctx['branch_name']}")
    if ctx.get("location"):
        parts.append(f"الموقع: {ctx['location']}")
    if ctx.get("service_type"):
        parts.append(f"نوع الخدمة: {ctx['service_type']}")
    if ctx.get("urgency") and ctx["urgency"] not in ("غير محدد", ""):
        parts.append(f"الإلحاح: {ctx['urgency']}")
    return " | ".join(parts) if parts else "غير محدد"

class ActionUberfixCreateRequest(Action):
    """Creates a maintenance request through the isolated maintenance service."""

    def name(self) -> Text:
        return "action_uberfix_create_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        service = MaintenanceService()
        result = service.create_request(
            client_name=tracker.get_slot("user_name"),
            client_phone=tracker.get_slot("user_phone"),
            description=tracker.get_slot("user_message"),
            tracker_sender_id=tracker.sender_id,
        )
        _utter_result(dispatcher, result)
        return [SlotSet("brand", "UberFix")]


class ActionUberfixTrackRequest(Action):
    """Tracks an existing maintenance request."""

    def name(self) -> Text:
        return "action_uberfix_track_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        service = MaintenanceService()
        result = service.track_request(tracker.latest_message.get("text", ""))
        _utter_result(dispatcher, result)
        return [SlotSet("brand", "UberFix")]


class ActionUberfixShowSubscriptions(Action):
    """Shows UberFix maintenance plans."""

    def name(self) -> Text:
        return "action_uberfix_show_subscriptions"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        service = MaintenanceService()
        _utter_result(dispatcher, service.subscriptions())
        return [SlotSet("brand", "UberFix")]
