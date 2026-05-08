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
import os
import re
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ──────────────────────────────────────────────────────────────
#  استخراج السياق بـ GPT من كامل المحادثة
# ──────────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """أنت محلل محادثات عربية ذكي متخصص في قطاع المقاولات، الصيانة، وتجهيز المحلات التجارية الكبرى (Shop Fitting & Brand Identity).
مهمتك: استخرج كل المعلومات المفيدة من سجل المحادثة التالي بدقة عالية، مع التركيز على "جوهر الهوية" والمواصفات الفنية والمواد المطلوبة.

سجل المحادثة:
{conversation}

استخرج هذه الحقول (اترك الحقل فارغاً إذا لم يُذكر):
- user_name: اسم العميل أو الشركة (غالباً أصحاب سلاسل وفروع)
- user_phone: رقم الهاتف
- location: الموقع أو العنوان (ادمج كل ذكر للموقع في رسائل مختلفة)
- branch_name: اسم الفرع إذا ذُكر
- problem_description: وصف طلب "بناء الهوية" أو التجهيز أو الصيانة (مثال: فتح فرع جديد، صيانة تكييف، توريد كشافات)
- service_type: نوع الخدمة (كهرباء وإضاءة / سباكة ومياه / تكييف وتهوية / نجارة وأثاث / دهانات وترميمات / رخام وأرضيات / أنظمة الحريق والسلامة / ترولي ومعدات / أبواب ونوافذ / لافتات وعلامات / تجهيز محلات تجارية)
- urgency: مدى الإلحاح (طارئ / عادي / غير محدد)
- brand: البراند (UberFix / Alazab / Luxury Finishing / Brand Identity / Laban Alasfour)
- technical_specs: أي مواصفات فنية ذكرها العميل (مثل: قواطع 3 فاز، كابلات معزولة، تكييف Package، ماكينة غلق زجاج أوتوماتيك، برمجة لوحة حريق)
- material_needed: أي خامات أو ماركات ذكرت (مثل: Schneider, Elsewedy, Philips, Venus, Al-Safa, Tank)
- additional_notes: أي معلومات إضافية (مثل: الحاجة لتروليات ستانلس، وحدات تخزين مدرجة، أو صيانة أبواب شطر)

قواعد ذهبية للمحلل الذكي:
1. التقط الماركات المعتمدة بدقة (Schneider, Elsewedy, Philips, Al-Safa) لأنها جزء من "جوهر الهوية".
2. صنف الطلب بدقة تحت أحد فئات `service_type` المذكورة أعلاه (مثل: "عجل الترولي" يندرج تحت "ترولي ومعدات").
3. إذا طلب العميل صيانة، حاول استنتاج القطعة التالفة بدقة (مثل: ماكينة زجاج، مفصلة هيدروليك، عجلات ترولي، حساس حريق).
4. افهم أن "Brand Identity" تعني اكتمال الهوية من التأسيس حتى تصنيع الأثاث (Island, Counters).
5. ميز بين قطاع "الصيانة والتشغيل" (UberFix) وقطاع "تجهيز السلاسل" (Brand Identity).

أجب بـ JSON فقط بدون أي نص إضافي:
{{
  "user_name": "",
  "user_phone": "",
  "location": "",
  "branch_name": "",
  "problem_description": "",
  "service_type": "",
  "urgency": "",
  "brand": "",
  "technical_specs": "",
  "material_needed": "",
  "additional_notes": "",
  "summary": "ملخص لطلب بناء الهوية المتكاملة وتحديد الماركات المطلوبة"
}}"""


async def _extract_context_with_gpt(conversation_text: str) -> dict:
    """استخدام GPT لاستخراج كل السياق من المحادثة كاملة."""
    if not OPENAI_API_KEY:
        return {}

    try:
        import aiohttp
        prompt = EXTRACTION_PROMPT.format(conversation=conversation_text)

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 800,
        }
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=12),
            ) as resp:
                if resp.status != 200:
                    return {}
                data = await resp.json()

        raw = data["choices"][0]["message"]["content"].strip()
        # إزالة ```json ... ``` إن وجدت
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)

    except Exception as exc:
        logger.warning("GPT context extraction failed: %s", exc)
        return {}


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

        # بناء نص المحادثة الكاملة
        conversation = _build_conversation_text(tracker)
        if not conversation:
            return []

        # استخراج السياق بـ GPT
        new_ctx = await _extract_context_with_gpt(conversation)
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
            "user_name":    merged.get("user_name", ""),
            "user_phone":   merged.get("user_phone", ""),
            "location":     merged.get("location", ""),
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
            "user_name":    ctx.get("user_name", ""),
            "user_phone":   ctx.get("user_phone", ""),
            "location":     ctx.get("location", ""),
            "service_type": ctx.get("service_type", ""),
            "branch_name":  ctx.get("branch_name", ""),
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
            if ctx.get("location") and ctx.get("location") not in (ctx.get("branch_name") or ""):
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
            dispatcher.utter_message(
                text=f"✅ فهمت منك:\n{understood}\n\nهل هذا صحيح؟"
            )
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
