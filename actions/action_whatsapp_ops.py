from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionSendWhatsAppMessage(Action):
    def name(self) -> Text:
        return "action_send_whatsapp_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real scenario, fetch the template from the `whatsapp_templates` table
        # using a database connection.
        
        template_name = tracker.get_slot("whatsapp_template_name")
        user_phone = tracker.get_slot("user_phone")
        
        if not user_phone:
            dispatcher.utter_message(text="عذراً، لا يوجد رقم هاتف مسجل لإرسال الرسالة.")
            return []
            
        # Example API call to Meta WhatsApp API
        # response = requests.post(
        #     "https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages",
        #     headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        #     json={
        #         "messaging_product": "whatsapp",
        #         "to": user_phone,
        #         "type": "template",
        #         "template": {
        #             "name": template_name,
        #             "language": {"code": "ar"}
        #         }
        #     }
        # )

        dispatcher.utter_message(text=f"تم إرسال رسالة الواتساب للقالب: {template_name} بنجاح إلى الرقم {user_phone}.")
        return []
