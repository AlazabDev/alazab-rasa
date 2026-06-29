"""
actions/action_uberfix_ops.py
================================
عمليات UberFix الإضافية — تستخدم gateway_client
"""
import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .maintenance import gateway_client as gw

logger = logging.getLogger(__name__)


class ActionUberFixTriage(Action):
    def name(self) -> Text:
        return "action_uberfix_triage_request"

    def run(self, dispatcher, tracker, domain):
        order_id = tracker.get_slot("order_id") or ""
        if not order_id:
            dispatcher.utter_message(text="يرجى تزويد رقم الطلب.")
            return []
        resp = gw.transition_stage(order_id, "triaged", "مراجعة فنية من البوت")
        if resp.get("success"):
            dispatcher.utter_message(text="✅ تمت مراجعة طلبك، سيتم توجيه فني قريباً.")
        else:
            dispatcher.utter_message(text="✅ طلبك قيد المراجعة.")
        return []
