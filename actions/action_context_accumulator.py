"""
actions/action_context_accumulator.py
=======================================
محرك الذاكرة السياقية لـ AzaBot

المشكلة التي يحلها:
  المستخدم العربي يتحدث كأنه مع إنسان —
  يذكر الموقع في رسالة، ثم يذكر العطل في رسالة ثانية
  ويفترض أن البوت يربط الاثنتين.

  مثال:
    User: "أريد صيانة لفرع أبو عوف شارع المرغني مصر الجديدة"
    Bot:  "ما التفاصيل؟"
    User: "التكيف عطلان في الفرع"
    ← "في الفرع" = "فرع أبو عوف شارع المرغني مصر الجديدة"
    ← البوت يجب أن يربط السياق تلقائياً

الحل:
  1. بعد كل رسالة من المستخدم، نُحلّل كامل تاريخ المحادثة بـ GPT
  2. نستخرج كل المعلومات المتراكمة (موقع + مشكلة + بيانات عميل + ...)
  3. نحفظها في slot "context_memory" كـ JSON
  4. أي action تحتاج بيانات تسحب من context_memory أولاً
  5. إذا وجدت المعلومة في السياق → لا نسأل المستخدم مجدداً
"""

import json
import logging
import re
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

# استخدام الـ GPT client المركزي بدلاً من استدعاء API مباشرة
from .core.gpt import extract_json as gpt_extract_json

# ──────────────────────────────────────────────────────────────
#  استخراج السياق بـ GPT من كامل المحادثة
# ──────────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """أنت محلل محادثات عربية ذكي متخصص في خدمات مجموعة العزب.

البراند الحالي: {brand}
سجل المحادثة:
{conversation}

استخرج المعلومات التالية (اترك فارغاً إذا لم يُذكر):
- user_name: اسم العميل أو الشركة
- user_phone: رقم الهاتف
- location: الموقع أو العنوان
- branch_name: اسم الفرع إذا ذُكر
- problem_description: وصف الطلب أو المشكلة
- urgency: مدى الإلحاح (طارئ / عادي / غير محدد)
{brand_specific_fields}

قواعد:
1. لا تخترع معلومات — استخرج فقط ما ذُكر صراحةً.
2. ادمج المعلومات المتفرقة في رسائل مختلفة.
3. الأولوية للمعلومات الأحدث إذا تعارضت.

أجب بـ JSON فقط:
{{
  "user_name": "",
  "user_phone": "",
  "location": "",
  "branch_name": "",
  "problem_description": "",
  "urgency": "",
  {brand_specific_json}
  "summary": ""
}}"""

# حقول خاصة بكل segment
_BRAND_FIELDS: dict[str, tuple[str, str]] = {
    "uberfix": (
        "- service_type: نوع الخدمة (كهرباء / سباكة / تكييف / دهانات / نجارة / تنظيف / عام)\n"
        "- technical_specs: مواصفات فنية (ماركة قاطع، نوع تكييف، إلخ)\n"
        "- priority: أولوية (high/normal)",
        '"service_type": "", "technical_specs": "", "priority": "normal",'
    ),
    "laban_alasfour": (
        "- unit_type: نوع الوحدة المطلوبة (island / counter / shelving / cashier / display_wall)\n"
        "- material_needed: الخامة أو الماركة المطلوبة\n"
        "- quantity: الكمية إذا ذُكرت",
        '"unit_type": "", "material_needed": "", "quantity": "",'
    ),
    "alazab_construction": (
        "- project_type: نوع المشروع (سكني / تجاري / صناعي / خدمي)\n"
        "- area_size: المساحة التقريبية\n"
        "- project_stage: مرحلة المشروع (عظم / تشطيب / تجديد)",
        '"project_type": "", "area_size": "", "project_stage": "",'
    ),
    "luxury_finishing": (
        "- unit_type: نوع الوحدة (شقة / فيلا / مكتب / محل)\n"
        "- area_size: المساحة التقريبية\n"
        "- finishing_stage: مرحلة التشطيب (عظم / نص تشطيب / تجديد)\n"
        "- style_preference: الذوق المطلوب (مودرن / كلاسيك / مختلط)",
        '"unit_type": "", "area_size": "", "finishing_stage": "", "style_preference": "",'
    ),
    "brand_identity": (
        "- business_type: نوع النشاط التجاري\n"
        "- scope: نطاق المطلوب (شعار فقط / هوية كاملة / تجهيز مساحة)\n"
        "- num_branches: عدد الفروع إذا ذُكر\n"
        "- technical_specs: أي مواصفات (ماركات معتمدة، أبعاد، مواد)",
        '"business_type": "", "scope": "", "num_branches": "", "technical_specs": "",'
    ),
}

_DEFAULT_BRAND_FIELDS = (
    "- service_type: نوع الخدمة المطلوبة",
    '"service_type": "",'
)


async def _extract_context_with_gpt(conversation_text: str, brand: str = "") -> dict:
    """استخدام GPT (core) لاستخراج السياق بحسب segment البراند."""
    brand_fields, brand_json = _BRAND_FIELDS.get(brand, _DEFAULT_BRAND_FIELDS)
    prompt = EXTRACTION_PROMPT.format(
        brand=brand or "مجموعة العزب",
        conversation=conversation_text,
        brand_specific_fields=brand_fields,
        brand_specific_json=brand_json,
    )
    result = await gpt_extract_json(
        system_prompt="أنت محلل محادثات عربية متخصص. أجب بـ JSON فقط بدون أي نص إضافي.",
        user_message=prompt,
        max_tokens=600,
    )
    return result


def _build_conversation_text(tracker: Tracker) -> str:
    """بناء نص المحادثة الكاملة من تاريخ الـ tracker."""
    lines = []
    for event in tracker.events:
        if event.get("event") == "user":
            text = event.get("text", "").strip()
            if text:
                lines.append(f"المستخدم: {text}")
        elif event.get("event") == "bot":
            text = event.get("text", "").strip()
            if text:
                lines.append(f"البوت: {text[:120]}")  # اختصار ردود البوت

    return "\n".join(lines[-30:])  # آخر 30 سطر (تجنب الطول الزائد)


def _merge_contexts(old_ctx: dict, new_ctx: dict) -> dict:
    """دمج السياق القديم مع الجديد — الأولوية للجديد إلا إذا كان فارغاً."""
    merged = dict(old_ctx)
    for key, val in new_ctx.items():
        if val and str(val).strip():
            merged[key] = val
    return merged


# ──────────────────────────────────────────────────────────────
#  Action الرئيسي
# ──────────────────────────────────────────────────────────────


class ActionAccumulateContext(Action):
    """
    يُستدعى بعد كل رسالة من المستخدم.
    يحلل كامل المحادثة ويحدّث context_memory.
    """

    def name(self) -> Text:
        return "action_accumulate_context"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # قراءة البراند من الـ slot — يُضبط من metadata عند بداية الجلسة
        brand = (tracker.get_slot("brand") or "").strip().lower()

        # بناء نص المحادثة الكاملة
        conversation = _build_conversation_text(tracker)
        if not conversation:
            return []

        # استخراج السياق بـ GPT مع brand awareness
        new_ctx = await _extract_context_with_gpt(conversation, brand)
        if not new_ctx:
            return []

        # دمج مع السياق القديم
        old_ctx_raw = tracker.get_slot("context_memory") or "{}"
        try:
            old_ctx = json.loads(old_ctx_raw)
        except Exception:
            old_ctx = {}

        merged = _merge_contexts(old_ctx, new_ctx)

        # تحديث الـ slots المباشرة من السياق المتراكم
        events = [SlotSet("context_memory", json.dumps(merged, ensure_ascii=False))]

        # إذا استخرجنا بيانات واضحة → حدّث الـ slots مباشرة
        slot_map = {
            "user_name": merged.get("user_name", ""),
            "user_phone": merged.get("user_phone", ""),
            "location": merged.get("location", ""),
            "service_type": merged.get("service_type", ""),
        }
        for slot_name, val in slot_map.items():
            if val and not tracker.get_slot(slot_name):
                events.append(SlotSet(slot_name, val))

        # بناء user_message من السياق المتراكم إذا لزم
        if merged.get("problem_description") and not tracker.get_slot("user_message"):
            full_msg = merged["problem_description"]
            if merged.get("location"):
                full_msg = f"{full_msg} — الموقع: {merged['location']}"
            if merged.get("branch_name"):
                full_msg = f"{full_msg} ({merged['branch_name']})"
            events.append(SlotSet("user_message", full_msg))

        logger.info(
            "Context accumulated | summary=%s | slots_set=%d",
            merged.get("summary", ""),
            len(events) - 1,
        )
        return events


# ──────────────────────────────────────────────────────────────
#  Action: قرار ذكي بشأن الـ slots المحتاجة
# ──────────────────────────────────────────────────────────────


class ActionSmartSlotCheck(Action):
    """
    يفحص السياق المتراكم ويقرر أي slots تحتاج سؤالاً
    وأيها موجودة بالفعل في السياق.
    """

    def name(self) -> Text:
        return "action_smart_slot_check"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        ctx_raw = tracker.get_slot("context_memory") or "{}"
        try:
            ctx = json.loads(ctx_raw)
        except Exception:
            ctx = {}

        events = []

        # تحقق من كل slot مطلوبة وملّئها من السياق
        checks = {
            "user_name": ctx.get("user_name", ""),
            "user_phone": ctx.get("user_phone", ""),
            "location": ctx.get("location", ""),
            "service_type": ctx.get("service_type", ""),
            "branch_name": ctx.get("branch_name", ""),
        }

        filled = []
        for slot, val in checks.items():
            if val and not tracker.get_slot(slot):
                events.append(SlotSet(slot, val))
                filled.append(slot)

        # بناء user_message الكامل
        if not tracker.get_slot("user_message"):
            parts = []
            if ctx.get("problem_description"):
                parts.append(ctx["problem_description"])
            if ctx.get("branch_name"):
                parts.append(f"الفرع: {ctx['branch_name']}")
            if ctx.get("location") and ctx.get("location") not in (
                ctx.get("branch_name") or ""
            ):
                parts.append(f"الموقع: {ctx['location']}")
            if ctx.get("service_type"):
                parts.append(f"نوع الخدمة: {ctx['service_type']}")
            if parts:
                events.append(SlotSet("user_message", " | ".join(parts)))
                filled.append("user_message")

        if filled:
            logger.info("Smart slot check filled: %s", filled)

        return events


# ──────────────────────────────────────────────────────────────
#  Action: رد ذكي يؤكد الفهم قبل السؤال
# ──────────────────────────────────────────────────────────────


class ActionConfirmUnderstanding(Action):
    """
    عند الحاجة لمعلومة ناقصة، يُظهر ما فهمه البوت
    حتى يشعر المستخدم أنه يُفهَم.
    """

    def name(self) -> Text:
        return "action_confirm_understanding"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        ctx_raw = tracker.get_slot("context_memory") or "{}"
        try:
            ctx = json.loads(ctx_raw)
        except Exception:
            ctx = {}

        parts = []
        if ctx.get("service_type"):
            parts.append(f"نوع الخدمة: **{ctx['service_type']}**")
        if ctx.get("branch_name"):
            parts.append(f"الفرع: **{ctx['branch_name']}**")
        if ctx.get("location"):
            parts.append(f"الموقع: **{ctx['location']}**")
        if ctx.get("problem_description"):
            parts.append(f"المشكلة: **{ctx['problem_description']}**")

        if parts:
            understood = " | ".join(parts)
            dispatcher.utter_message(text=f"✅ فهمت منك:\n{understood}\n\nهل هذا صحيح؟")
        return []


# ──────────────────────────────────────────────────────────────
#  Action: تجميع user_message الكامل من السياق
# ──────────────────────────────────────────────────────────────


class ActionBuildFullRequest(Action):
    """
    يبني user_message كاملاً من السياق المتراكم
    قبل إرسال الطلب للفريق.
    """

    def name(self) -> Text:
        return "action_build_full_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        ctx_raw = tracker.get_slot("context_memory") or "{}"
        try:
            ctx = json.loads(ctx_raw)
        except Exception:
            ctx = {}

        # بناء رسالة شاملة
        lines = []
        if ctx.get("problem_description"):
            lines.append(f"المشكلة: {ctx['problem_description']}")
        if ctx.get("service_type"):
            lines.append(f"نوع الخدمة: {ctx['service_type']}")
        if ctx.get("branch_name"):
            lines.append(f"الفرع: {ctx['branch_name']}")
        if ctx.get("location"):
            lines.append(f"الموقع: {ctx['location']}")
        if ctx.get("urgency") and ctx["urgency"] != "غير محدد":
            lines.append(f"الإلحاح: {ctx['urgency']}")
        if ctx.get("additional_notes"):
            lines.append(f"ملاحظات: {ctx['additional_notes']}")

        if not lines:
            return []

        full_message = "\n".join(lines)

        events = [SlotSet("user_message", full_message)]

        # تحديث الاسم والهاتف من السياق إذا لم يكونا موجودَين
        if ctx.get("user_name") and not tracker.get_slot("user_name"):
            events.append(SlotSet("user_name", ctx["user_name"]))
        if ctx.get("user_phone") and not tracker.get_slot("user_phone"):
            events.append(SlotSet("user_phone", ctx["user_phone"]))

        logger.info("Full request built | chars=%d", len(full_message))
        return events
