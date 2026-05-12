from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSendSweetsInfo(Action):
    def name(self) -> Text:
        return "action_send_sweets_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # ⚠️ هذا الأكشن وهمي (placeholder). استبدل المنطق هنا لاحقاً بقراءة بيانات المحلويات الفعلية من قاعدة البيانات أو API.
        sample_sweets = [
            {"name": "كنافة نابلسية", "price": "50 جنيه"},
            {"name": "بسبوسة بالمكسرات", "price": "40 جنيه"},
            {"name": "بلح الشام", "price": "35 جنيه"},
        ]
        # الرد برسالة توضيحية ومحتوى وهمي
        message = "قائمة المحلويات المتاحة حالياً (بيانات تجريبية):\n"
        for sweet in sample_sweets:
            message += f"- {sweet['name']} ({sweet['price']})\n"
        message += "\n⚠️ سيتم تحديث القائمة بالبيانات الفعلية لاحقاً."
        dispatcher.utter_message(text=message)
        return []
