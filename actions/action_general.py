"""
actions/action_general.py
==========================
تنفيذ الأوامر العامة المشتركة بين جميع البراندات:
- Lead collection (CRM)
- Human handoff
- Feedback / rating / suggestion
- FAQ search
"""

import hmac
import logging
import os
import re
import time
from typing import Any, Dict, List, Text

import aiohttp
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

# ── ENV ────────────────────────────────────────────────────────
WHATSAPP_TOKEN   = os.getenv("WHATSAPP_TOKEN", "")
NOTIFY_PHONE     = os.getenv("NOTIFY_PHONE", "")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
NOTIFY_TG_CHAT   = os.getenv("NOTIFY_TG_CHAT_ID", "")
TG_BOT_TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
DB_HOST          = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT          = int(os.getenv("DB_PORT", 5432))
DB_NAME          = os.getenv("DB_NAME", "alazab_core")
DB_USER          = os.getenv("DB_USER", "")
DB_PASSWORD      = os.getenv("DB_PASSWORD", "")

# ── Helpers ────────────────────────────────────────────────────

async def _send_whatsapp_text(phone: str, text: str) -> bool:
    """إرسال إشعار واتساب (بشكل غير متزامن)."""
    if not (WHATSAPP_TOKEN and WHATSAPP_API_URL and phone):
        logger.warning("WhatsApp not configured — skip notification")
        return False
    payload = {
        "messaging_product": "whatsapp",
        "to": phone.lstrip("+"),
        "type": "text",
        "text": {"body": text},
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=8)) as r:
                ok = r.status < 300
                if not ok:
                    logger.error("WhatsApp send failed: %s %s", r.status, await r.text())
                return ok
    except Exception as exc:
        logger.error("WhatsApp send error: %s", exc)
        return False


async def _save_to_db(table: str, data: dict) -> bool:
    """حفظ البيانات في قاعدة البيانات PostgreSQL."""
    try:
        import asyncpg  # type: ignore
        conn = await asyncpg.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME,
            user=DB_USER, password=DB_PASSWORD,
        )
        cols   = ", ".join(data.keys())
        vals   = ", ".join(f"${i+1}" for i in range(len(data)))
        query  = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        await conn.execute(query, *data.values())
        await conn.close()
        return True
    except Exception as exc:
        logger.error("DB save error [%s]: %s", table, exc)
        return False


# ═══════════════════════════════════════════════════════════════
#  LEAD COLLECTION
# ═══════════════════════════════════════════════════════════════

class ActionSaveLeadToCRM(Action):
    """حفظ بيانات العميل في قاعدة البيانات."""

    def name(self) -> Text:
        return "action_save_lead_to_crm"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        lead = {
            "name":         tracker.get_slot("user_name") or "غير محدد",
            "phone":        tracker.get_slot("user_phone") or "",
            "location":     tracker.get_slot("location") or "",
            "service_type": tracker.get_slot("service_type") or "",
            "brand":        tracker.get_slot("brand") or "AzaBot",
            "sender_id":    tracker.sender_id,
            "created_at":   time.strftime("%Y-%m-%d %H:%M:%S"),
            "source":       "chatbot",
            "status":       "new",
        }

        saved = await _save_to_db("leads", lead)
        if not saved:
            logger.warning("Lead not saved to DB — continuing anyway")

        return []


class ActionNotifySalesTeam(Action):
    """إشعار فريق المبيعات بعميل جديد عبر واتساب."""

    def name(self) -> Text:
        return "action_notify_sales_team"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        name    = tracker.get_slot("user_name") or "?"
        phone   = tracker.get_slot("user_phone") or "?"
        loc     = tracker.get_slot("location") or "?"
        service = tracker.get_slot("service_type") or "?"
        brand   = tracker.get_slot("brand") or "AzaBot"

        msg = (
            f"🔔 *عميل جديد — {brand}*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👤 الاسم:  {name}\n"
            f"📞 هاتف:   {phone}\n"
            f"📍 موقع:   {loc}\n"
            f"🛠️ خدمة:  {service}\n"
            f"🕐 وقت:    {time.strftime('%Y-%m-%d %H:%M')}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📱 تواصل معه الآن عبر واتساب"
        )
        await _send_whatsapp_text(NOTIFY_PHONE, msg)
        return []


# ═══════════════════════════════════════════════════════════════
#  HUMAN HANDOFF
# ═══════════════════════════════════════════════════════════════

class ActionReceiveHandoffReason(Action):
    """استقبال سبب طلب التحويل وحفظه في slot."""

    def name(self) -> Text:
        return "action_receive_handoff_reason"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        reason = tracker.latest_message.get("text", "غير محدد")
        return [SlotSet("handoff_reason", reason)]


class ActionCheckHumanAvailability(Action):
    """التحقق من توفر ممثل خدمة العملاء."""

    def name(self) -> Text:
        return "action_check_human_availability"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # نموذج بسيط: متاح خلال ساعات العمل (9ص–10م)
        current_hour = int(time.strftime("%H"))
        is_available = 9 <= current_hour < 22
        return [SlotSet("is_available", is_available)]


class ActionCheckQueuePosition(Action):
    """التحقق من رقم المستخدم في قائمة الانتظار."""

    def name(self) -> Text:
        return "action_check_queue_position"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # افتراضياً قائمة الانتظار 1 (يمكن ربطها لاحقاً بنظام حي)
        queue_position = 1
        return [SlotSet("queue_position", queue_position)]


class ActionInitiateHumanHandoff(Action):
    """بدء إجراءات التحويل وتسجيل الطلب."""

    def name(self) -> Text:
        return "action_initiate_human_handoff"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        reason = tracker.get_slot("handoff_reason") or "غير محدد"
        msg = (
            f"🙋 *طلب تحويل إنسان*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📋 السبب: {reason}\n"
            f"🆔 Session: {tracker.sender_id}\n"
            f"🕐 الوقت: {time.strftime('%Y-%m-%d %H:%M')}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"برجاء التواصل مع العميل فوراً."
        )
        await _send_whatsapp_text(NOTIFY_PHONE, msg)
        return []


class ActionWaitForAgent(Action):
    """انتظار ممثل خدمة العملاء."""

    def name(self) -> Text:
        return "action_wait_for_agent"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="⏳ جاري تحويلك... برجاء الانتظار لحظة.")
        return []


class ActionTransferToAgent(Action):
    """إتمام التحويل الكامل للممثل."""

    def name(self) -> Text:
        return "action_transfer_to_agent"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "✅ تم التحويل.\n"
                "ستكون المحادثة مع ممثلنا مباشرة.\n"
                "شكراً لصبرك!"
            )
        )
        return []


class ActionNotifyTeamViaWhatsapp(Action):
    """إشعار الفريق عبر واتساب بمحادثة فورية."""

    def name(self) -> Text:
        return "action_notify_team_via_whatsapp"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        reason = tracker.get_slot("handoff_reason") or "غير محدد"
        msg = f"🚨 *تحويل فوري*\nالسبب: {reason}\nSession: {tracker.sender_id}"
        await _send_whatsapp_text(NOTIFY_PHONE, msg)
        return []


# ═══════════════════════════════════════════════════════════════
#  ESCALATION
# ═══════════════════════════════════════════════════════════════

class ActionCollectEscalationDetails(Action):
    """جمع تفاصيل التصعيد."""

    def name(self) -> Text:
        return "action_collect_escalation_details"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        details = tracker.latest_message.get("text", "غير محدد")
        return [SlotSet("escalation_details", details)]


class ActionCreateEscalationTicket(Action):
    """إنشاء تذكرة تصعيد في قاعدة البيانات."""

    def name(self) -> Text:
        return "action_create_escalation_ticket"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        ticket = {
            "sender_id":  tracker.sender_id,
            "details":    tracker.get_slot("escalation_details") or "غير محدد",
            "brand":      tracker.get_slot("brand") or "AzaBot",
            "status":     "open",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        await _save_to_db("escalation_tickets", ticket)
        return []


class ActionNotifyManager(Action):
    """إشعار المدير بتذكرة تصعيد."""

    def name(self) -> Text:
        return "action_notify_manager"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        details = tracker.get_slot("escalation_details") or "غير محدد"
        msg = (
            f"🆘 *تصعيد للمدير*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📋 التفاصيل: {details}\n"
            f"🆔 Session: {tracker.sender_id}\n"
            f"🕐 {time.strftime('%Y-%m-%d %H:%M')}"
        )
        await _send_whatsapp_text(NOTIFY_PHONE, msg)
        return []


# ═══════════════════════════════════════════════════════════════
#  FEEDBACK
# ═══════════════════════════════════════════════════════════════

class ActionReceiveFeedbackService(Action):
    """استقبال اسم الخدمة المُقيَّمة."""

    def name(self) -> Text:
        return "action_receive_feedback_service"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("feedback_service") or tracker.latest_message.get("text", "غير محدد")
        return [SlotSet("feedback_service", service)]


class ActionReceiveRating(Action):
    """استقبال التقييم الرقمي وحفظه."""

    def name(self) -> Text:
        return "action_receive_rating"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        rating_slot = tracker.get_slot("rating")
        if rating_slot:
            return [SlotSet("rating", float(rating_slot))]
        # استخراج الرقم من النص
        text = tracker.latest_message.get("text", "")
        match = re.search(r"[1-5]", text)
        if match:
            return [SlotSet("rating", float(match.group()))]
        return [SlotSet("rating", 3.0)]


class ActionReceiveFeedbackText(Action):
    """استقبال نص التعليق."""

    def name(self) -> Text:
        return "action_receive_feedback_text"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        feedback = tracker.latest_message.get("text", "")
        return [SlotSet("feedback_text", feedback)]


class ActionReceiveSuggestion(Action):
    """استقبال نص الاقتراح."""

    def name(self) -> Text:
        return "action_receive_suggestion"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        suggestion = tracker.latest_message.get("text", "")
        return [SlotSet("suggestion_text", suggestion)]


class ActionSaveFeedback(Action):
    """حفظ التقييم في قاعدة البيانات."""

    def name(self) -> Text:
        return "action_save_feedback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        record = {
            "sender_id":       tracker.sender_id,
            "service":         tracker.get_slot("feedback_service") or "general",
            "rating":          tracker.get_slot("rating") or 3,
            "feedback_text":   tracker.get_slot("feedback_text") or "",
            "brand":           tracker.get_slot("brand") or "AzaBot",
            "created_at":      time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        await _save_to_db("feedback", record)
        return []


class ActionSaveSuggestion(Action):
    """حفظ الاقتراح في قاعدة البيانات."""

    def name(self) -> Text:
        return "action_save_suggestion"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        record = {
            "sender_id":   tracker.sender_id,
            "suggestion":  tracker.get_slot("suggestion_text") or "",
            "brand":       tracker.get_slot("brand") or "AzaBot",
            "created_at":  time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        await _save_to_db("suggestions", record)
        return []


class ActionCollectFollowUpContact(Action):
    """جمع بيانات التواصل للمتابعة بعد تقييم سلبي."""

    def name(self) -> Text:
        return "action_collect_follow_up_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="📞 ممكن تزودنا برقم هاتفك؟ فريقنا سيتواصل معك لحل المشكلة."
        )
        return []


# ═══════════════════════════════════════════════════════════════
#  FAQ
# ═══════════════════════════════════════════════════════════════

# قاموس الأسئلة الشائعة للبحث
_FAQ_INDEX: List[Dict[str, str]] = [
    {"keywords": ["سعر", "تكلفة", "كام", "price", "تسعير"],
     "answer": "أسعارنا تبدأ من: البناء 2500ج/م²، التشطيب 1500ج/م²، الهوية 15,000ج، الصيانة 150ج."},
    {"keywords": ["ضمان", "guarantee", "warranty"],
     "answer": "الضمانات: هيكل البناء 10 سنوات، التشطيب 3 سنوات، صيانة UberFix 3 أشهر."},
    {"keywords": ["مدة", "وقت", "يوم", "شهر", "timeline", "duration"],
     "answer": "المدد: البناء 12-18 شهر، التشطيب 30-45 يوم، الهوية 15-25 يوم، الصيانة نفس اليوم."},
    {"keywords": ["دفع", "تقسيط", "payment", "فيزا", "كريدت"],
     "answer": "طرق الدفع: نقداً، تحويل بنكي، Visa/Mastercard، إنستاباي، تقسيط."},
    {"keywords": ["محافظة", "منطقة", "فين", "location", "غطية", "تغطية"],
     "answer": "نغطي: القاهرة الكبرى، الإسكندرية، مدن الأقاليم، العاصمة الإدارية."},
    {"keywords": ["صيانة", "كهرباء", "سباكة", "تكييف", "uberfix", "أوبرفيكس"],
     "answer": "UberFix يقدم: صيانة كهرباء، سباكة، تكييف، وعقود صيانة سنوية."},
    {"keywords": ["تشطيب", "luxury", "ديكور", "داخلي"],
     "answer": "Luxury Finishing: تشطيب سكني وتجاري فاخر، رخام إيطالي، بورسلان، دهانات Jotun."},
    {"keywords": ["بناء", "عمارة", "مقاولات", "construction", "هيكل"],
     "answer": "Alazab Construction: بناء سكني وتجاري وخدمي، تسليم مفتاح، ضمان 10 سنوات."},
]


class ActionSearchFaqByKeyword(Action):
    """البحث في الأسئلة الشائعة بكلمة مفتاحية."""

    def name(self) -> Text:
        return "action_search_faq_by_keyword"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        keyword = tracker.get_slot("keyword") or tracker.latest_message.get("text", "")
        keyword_lower = keyword.lower()

        results = []
        for faq in _FAQ_INDEX:
            if any(k in keyword_lower for k in faq["keywords"]):
                results.append(faq["answer"])

        if results:
            return [
                SlotSet("search_found", True),
                SlotSet("results", "\n\n".join(f"• {r}" for r in results[:3])),
                SlotSet("keyword", keyword),
            ]
        return [
            SlotSet("search_found", False),
            SlotSet("keyword", keyword),
        ]
