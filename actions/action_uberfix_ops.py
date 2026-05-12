from typing import Any, Text, Dict, List
import requests
import os
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .config import GATEWAY_URL, API_KEY

class ActionUberFixTriage(Action):
    def name(self) -> Text:
        return "action_uberfix_triage_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        if not order_id:
            dispatcher.utter_message(text="يرجى تزويد رقم الطلب للمراجعة.")
            return []
            
        data = {
            "channel": "whatsapp_bot",
            "action": "transition_stage",
            "request_number": order_id,
            "to_stage": "triaged",
            "reason": "تأكيد المراجعة الفنية"
        }
        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
        try:
            requests.post(GATEWAY_URL, json=data, headers=headers, timeout=10)
            dispatcher.utter_message(text="✅ تمت مراجعة طلبك فنياً، سيتم توجيه فني للمعاينة قريباً.")
            return []
        except Exception:
            dispatcher.utter_message(text="عذراً، حدث خطأ في تحديث حالة الطلب.")
            return []

class ActionUberFixGetStatus(Action):
    def name(self) -> Text:
        return "action_uberfix_track_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        if not order_id:
            dispatcher.utter_message(text="يرجى تزويد رقم الطلب للاستعلام عن حالته.")
            return []

        data = {
            "channel": "whatsapp_bot",
            "action": "get_status",
            "request_number": order_id
        }
        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
        try:
            response = requests.post(GATEWAY_URL, json=data, headers=headers, timeout=10)
            resp_json = response.json()
            status = resp_json.get("status", "قيد المراجعة")
            dispatcher.utter_message(text=f"📦 حالة طلبك ({order_id}) حالياً هي: {status}")
            return [SlotSet("handover_status", status)]
        except Exception:
            dispatcher.utter_message(text="عذراً، لم نتمكن من جلب الحالة حالياً. جرب مرة أخرى لاحقاً.")
            return []
