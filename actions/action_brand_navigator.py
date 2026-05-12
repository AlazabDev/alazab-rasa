from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionBrandNavigator(Action):
    """
    يوجه العميل للموقع الإلكتروني المناسب بناءً على اهتمامه.
    """
    def name(self) -> Text:
        return "action_brand_navigator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # القائمة الكاملة لمواقع المجموعة
        brands = {
            "alazab": {
                "name": "آل عزب للمشروعات المعمارية",
                "url": "https://alazab.com",
                "desc": "تنفيذ وإدارة المشروعات المعمارية من الألف للياء."
            },
            "luxury": {
                "name": "Luxury Finishing",
                "url": "https://luxury-finishingalazab.com",
                "desc": "متخصصون في التشطيبات الراقية والديكورات الفاخرة."
            },
            "brand_identity": {
                "name": "Brand Identity",
                "url": "https://brand-identityalazab.com",
                "desc": "بناء وتصميم هوية العلامات التجارية المتميزة."
            },
            "uberfix": {
                "name": "UberFix",
                "url": "https://uberfix.alazab.com",
                "desc": "منصتكم الذكية لخدمات الصيانة والتشغيل الاحترافية."
            },
            "laban_alasfour": {
                "name": "Laban Alasfour",
                "url": "https://laban-alasfour.alazab.com",
                "desc": "لتوريد أجود الخامات والمعادن المعمارية."
            }
        }

        # تحديد البراند بناءً على الـ slot أو الكلمات المفتاحية في الرسالة الأخيرة
        last_message = tracker.latest_message.get("text", "").lower()
        selected_brand = tracker.get_slot("brand") or "alazab"
        
        # ذكاء إضافي في التعرف على البراند من الرسالة
        if "تشطيب" in last_message or "ديكور" in last_message:
            selected_brand = "luxury"
        elif "هوية" in last_message or "براند" in last_message or "شعار" in last_message:
            selected_brand = "brand_identity"
        elif "صيانة" in last_message or "عطل" in last_message:
            selected_brand = "uberfix"
        elif "خامات" in last_message or "توريد" in last_message:
            selected_brand = "laban_alasfour"

        brand_info = brands.get(selected_brand, brands["alazab"])

        response = (
            f"🏢 **{brand_info['name']}**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"✨ {brand_info['desc']}\n\n"
            f"🌐 يمكنك زيارة موقعنا لمزيد من التفاصيل:\n"
            f"{brand_info['url']}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"💡 تتميز مجموعة آل عزب بتقديم حلول متكاملة من مرحلة البناء حتى التشغيل والصيانة."
        )

        dispatcher.utter_message(text=response)
        return [SlotSet("brand", selected_brand)]
