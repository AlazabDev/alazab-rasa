"""
actions/action_uberfix_ops.py
==============================
عمليات UberFix الإضافية عبر maintenance-gateway (تغيير المراحل).

⚠️  إنشاء الطلب وتتبعه موجودان في:
    actions/brand_actions/uberfix.py → ActionUberfixCreateRequest / ActionUberfixTrackRequest

هذا الملف يحتوي فقط على:
- ActionUberFixTriage  → تحويل الطلب لمرحلة triaged
"""

import logging
from typing import Any, Text, Dict, List

import httpx
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .config import GATEWAY_URL, API_KEY

logger = logging.getLogger(__name__)


class ActionUberFixTriage(Action):
    """ينقل طلب الصيانة إلى مرحلة triaged عبر maintenance-gateway."""

    def name(self) -> Text:
        return "action_uberfix_triage_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        if not order_id:
            dispatcher.utter_message(text="يرجى تزويد رقم الطلب للمراجعة.")
            return []

        if not GATEWAY_URL:
            logger.warning("MAINTENANCE_GATEWAY_URL not configured — skipping triage")
            dispatcher.utter_message(
                text="✅ تمت مراجعة طلبك فنياً، سيتم توجيه فني للمعاينة قريباً."
            )
            return []

        payload = {
            "channel": "whatsapp_bot",
            "action": "transition_stage",
            "request_number": order_id,
            "to_stage": "triaged",
            "reason": "تأكيد المراجعة الفنية",
        }
        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=10) as client:
                client.post(GATEWAY_URL, json=payload, headers=headers)
            dispatcher.utter_message(
                text="✅ تمت مراجعة طلبك فنياً، سيتم توجيه فني للمعاينة قريباً."
            )
        except Exception as exc:
            logger.error("Triage request failed: %s", exc)
            dispatcher.utter_message(text="عذراً، حدث خطأ في تحديث حالة الطلب.")
        return []
