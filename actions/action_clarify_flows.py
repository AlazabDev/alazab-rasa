"""
actions/action_clarify_flows.py
=================================
يُستدعى من pattern_clarification عند clarify command.
يعرض خيارات الـ flows المحتملة للمستخدم.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

FLOW_LABELS: dict[str, str] = {
    "uberfix_request":     "🔧 طلب صيانة",
    "uberfix_track":       "📍 تتبع طلب",
    "uberfix_subscriptions": "📦 الباقات",
    "collect_lead":        "📋 تواصل معنا",
    "human_handoff":       "👤 التحدث مع موظف",
    "laban_inquiry":       "🪵 الوحدات الخشبية",
    "laban_bulk_order":    "📦 طلب بالجملة",
}


class ActionClarifyFlows(Action):

    def name(self) -> Text:
        return "action_clarify_flows"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # CALM يُمرّر الـ flows المحتملة في context.names
        flow_names = tracker.get_slot("context") or {}
        candidates = flow_names.get("names", []) if isinstance(flow_names, dict) else []

        if not candidates:
            dispatcher.utter_message(response="utter_clarification_no_options_rasa")
            return []

        buttons = []
        for flow in candidates[:4]:  # max 4 خيارات
            label = FLOW_LABELS.get(flow, flow.replace("_", " ").title())
            buttons.append({
                "title": label,
                "payload": f"/start_flow{{\"flow\": \"{flow}\"}}",
            })

        dispatcher.utter_message(
            text="أيّ من الخيارات التالية تقصد؟",
            buttons=buttons,
        )
        return []
