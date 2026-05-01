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
