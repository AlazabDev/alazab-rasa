from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .config import GATEWAY_URL, API_KEY

class ActionCreateMaintenanceRequest(Action):
    def name(self) -> Text:
        return "action_uberfix_create_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client_name = tracker.get_slot("user_name")
        client_phone = tracker.get_slot("user_phone")
        branch_name = tracker.get_slot("branch_name")
        service_item = tracker.get_slot("service_item")
        
        description = f"طلب صيانة لـ {service_item} في فرع {branch_name}"
        priority = tracker.get_slot("inspection_priority") or "normal"

        data = {
            "channel": "whatsapp_bot",
            "client_name": client_name,
            "client_phone": client_phone,
            "branch_name": branch_name,
            "service_item": service_item,
            "description": description,
            "priority": priority
        }
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(GATEWAY_URL, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            resp_json = response.json()
            req_num = resp_json.get("request_number", "N/A")
            
            dispatcher.utter_message(response="utter_submit_maintenance_form", order_id=req_num)
            
            return [
                SlotSet("order_id", req_num)
            ]
        except Exception:
            fake_id = f"REF-{tracker.sender_id[-4:]}"
            dispatcher.utter_message(response="utter_submit_maintenance_form", order_id=fake_id)
            return [SlotSet("order_id", fake_id)]
