"""
actions/brand_actions/uberfix.py
==================================
Actions بوت UberFix — تستخدم bot-gateway الموحّد
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from ..maintenance import gateway_client as gw

logger = logging.getLogger(__name__)

TRACK_BASE = "https://uberfix.shop/track"

SERVICE_LABELS = {
    "plumbing":    "سباكة",
    "electrical":  "كهرباء",
    "ac":          "تكييف",
    "painting":    "دهانات",
    "carpentry":   "نجارة",
    "cleaning":    "تنظيف",
    "general":     "صيانة عامة",
    "appliance":   "أجهزة منزلية",
    "pest_control":"مكافحة حشرات",
    "finishing":   "تشطيبات",
    "renovation":  "تجديد",
}

STAGE_LABELS = {
    "submitted":    "✅ تم الاستلام",
    "triaged":      "📋 قيد المراجعة",
    "assigned":     "👷 تم تعيين الفني",
    "scheduled":    "🗓️ تم تحديد الموعد",
    "in_progress":  "🔧 جارٍ التنفيذ",
    "inspection":   "🔍 الفحص",
    "waiting_parts":"⏳ انتظار قطع الغيار",
    "completed":    "✅ مكتمل",
    "billed":       "🧾 تم إصدار الفاتورة",
    "paid":         "💰 تم الدفع",
    "closed":       "🏁 مغلق",
    "cancelled":    "❌ ملغي",
}


class ActionUberfixCreateRequest(Action):
    def name(self) -> Text:
        return "action_uberfix_create_request"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker, domain: Dict) -> List[Dict]:
        name    = tracker.get_slot("user_name") or ""
        phone   = tracker.get_slot("user_phone") or ""
        message = tracker.get_slot("user_message") or ""
        brand   = tracker.get_slot("brand") or "uberfix"

        if not name or not phone or not message:
            dispatcher.utter_message(
                text="يرجى تزويدي بـ: اسمك، رقم هاتفك، ووصف المشكلة."
            )
            return []

        # تحديد نوع الخدمة من السياق
        service_type = _detect_service(message)

        resp = await gw.create_request(
            client_name  = name,
            client_phone = phone,
            service_type = service_type,
            description  = message,
            priority     = "medium",
            session_id   = tracker.sender_id,
        )

        if resp.get("success"):
            req_num   = resp.get("request_number", "")
            track_url = resp.get("track_url", f"{TRACK_BASE}/{resp.get('request_id','')}")
            dispatcher.utter_message(
                text=(
                    f"✅ تم تسجيل طلب الصيانة بنجاح!\n\n"
                    f"📋 رقم الطلب: *{req_num}*\n"
                    f"🔗 تتبع الطلب: {track_url}\n\n"
                    f"سيتواصل معك فريقنا قريباً. 🙏"
                )
            )
            return [
                SlotSet("order_id",     resp.get("request_id", "")),
                SlotSet("order_number", req_num),
            ]
        else:
            dispatcher.utter_message(
                text="عذراً، حدث خطأ في تسجيل طلبك. يرجى المحاولة مرة أخرى أو التواصل معنا على واتساب."
            )
            return []


class ActionUberfixTrackRequest(Action):
    def name(self) -> Text:
        return "action_uberfix_track_request"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker, domain: Dict) -> List[Dict]:
        # البحث بالـ slot أو آخر رسالة
        order_num = tracker.get_slot("order_number") or ""
        phone     = tracker.get_slot("user_phone") or ""
        msg       = tracker.latest_message.get("text", "")

        # استخراج رقم الطلب من الرسالة إذا لم يكن في slot
        if not order_num:
            import re
            m = re.search(r"(AZ-UF-\d+-\d+|UF/MR/\d+/\d+)", msg)
            if m:
                order_num = m.group(1)

        if not order_num and not phone:
            dispatcher.utter_message(
                text="يرجى تزويدي برقم الطلب أو رقم هاتفك للاستعلام."
            )
            return []

        if order_num:
            resp = await gw.check_status(order_num, "request_number")
        else:
            resp = await gw.check_status(phone, "phone")

        if resp.get("success"):
            stage     = resp.get("workflow_stage", resp.get("status", ""))
            stage_lbl = STAGE_LABELS.get(stage, stage)
            req_num   = resp.get("request_number", order_num)
            track_url = resp.get("track_url", "")

            msg_text = f"📋 *طلب الصيانة {req_num}*\n\n"
            msg_text += f"الحالة: {stage_lbl}\n"
            if track_url:
                msg_text += f"🔗 التتبع: {track_url}"

            dispatcher.utter_message(text=msg_text)
        else:
            dispatcher.utter_message(
                text="لم أجد طلباً بهذه البيانات. تأكد من رقم الطلب أو الهاتف."
            )
        return []


class ActionUberfixShowSubscriptions(Action):
    def name(self) -> Text:
        return "action_uberfix_show_subscriptions"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker, domain: Dict) -> List[Dict]:
        dispatcher.utter_message(text="""
📦 *باقات الاشتراك السنوي — UberFix*

🥉 *الأساسية*
4 زيارات دورية — للمنازل والوحدات الصغيرة

🥈 *المتقدمة*
8 زيارات + أولوية — للمحلات والمكاتب

🥇 *البريميوم*
12 زيارة + أولوية قصوى — للمنشآت الكبيرة

للاشتراك: contact@uberfix.com
        """.strip())
        return []


class ActionUberfixGetServices(Action):
    def name(self) -> Text:
        return "action_uberfix_get_services"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker, domain: Dict) -> List[Dict]:
        resp = await gw.list_services()
        if resp.get("success") and resp.get("data"):
            services = resp["data"]
            lines = ["🔧 *الخدمات المتاحة:*\n"]
            for s in services:
                label = s.get("label") or SERVICE_LABELS.get(s.get("key",""), s.get("key",""))
                lines.append(f"• {label}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            # fallback
            dispatcher.utter_message(text=
                "🔧 *خدمات UberFix:*\n"
                "• كهرباء • سباكة • تكييف\n"
                "• دهانات • نجارة • تنظيف\n"
                "• أجهزة منزلية • تشطيبات"
            )
        return []


class ActionUberfixGetQuote(Action):
    def name(self) -> Text:
        return "action_uberfix_get_quote"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker, domain: Dict) -> List[Dict]:
        message      = tracker.get_slot("user_message") or ""
        service_type = _detect_service(message)

        resp = await gw.get_quote(service_type, message)
        if resp.get("success") and resp.get("data"):
            d = resp["data"]
            label = SERVICE_LABELS.get(service_type, service_type)
            dispatcher.utter_message(text=
                f"💰 *تقدير سعر — {label}*\n\n"
                f"من {d.get('min_price','?')} إلى {d.get('max_price','?')} جنيه\n"
                f"_(السعر النهائي يُحدد بعد المعاينة)_"
            )
        else:
            dispatcher.utter_message(text=
                "يمكنني تقديم تقدير بعد المعاينة المجانية. "
                "هل تريد تسجيل طلب الآن؟"
            )
        return []


def _detect_service(text: str) -> str:
    """يحدد نوع الخدمة من النص."""
    text = text.lower()
    if any(w in text for w in ["كهرب", "تمديد", "لوحة", "بريكر", "فيوز"]):
        return "electrical"
    if any(w in text for w in ["سباك", "تسريب", "مياه", "حنفي", "بالوع"]):
        return "plumbing"
    if any(w in text for w in ["تكيي", "مكيف", "فريون", "تبريد"]):
        return "ac"
    if any(w in text for w in ["دهان", "طلاء", "صباغ"]):
        return "painting"
    if any(w in text for w in ["نجار", "باب", "شباك", "خشب"]):
        return "carpentry"
    if any(w in text for w in ["تنظيف", "نظاف"]):
        return "cleaning"
    if any(w in text for w in ["حشر", "مكافح"]):
        return "pest_control"
    if any(w in text for w in ["تشطيب", "تجديد", "ديكور"]):
        return "finishing"
    return "general"
