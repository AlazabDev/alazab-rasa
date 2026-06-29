"""
actions/action_human_handoff.py
================================
يلخص المحادثة بالكامل باستخدام GPT ويرسل الملخص لفريق الدعم،
ثم يُبلغ المستخدم بموعد التحويل.

[محسّن] يستخدم core.gpt و core.whatsapp بدلاً من استدعاء مباشر.
"""

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .core.gpt import complete as gpt_complete
from .core.whatsapp import send_notification

logger = logging.getLogger(__name__)

_SUMMARY_SYSTEM = (
    "أنت مساعد ذكي لخدمة العملاء. مهمتك تلخيص المحادثات باختصار "
    "باللغة العربية ليفهم الموظف البشري السياق فوراً."
)


class ActionHumanHandoff(Action):
    def name(self) -> Text:
        return "action_human_handoff"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # ── بناء سجل المحادثة ───────────────────────────────
        convo: List[str] = []
        for event in tracker.events:
            if event.get("event") == "user":
                text = str(event.get("text") or "")
                if text:
                    convo.append(f"المستخدم: {text}")
            elif event.get("event") == "bot":
                text = str(event.get("text") or "")
                if text:
                    convo.append(f"البوت: {text}")

        brand = tracker.get_slot("brand") or "مجموعة العزب"
        user_name = tracker.get_slot("user_name") or "غير محدد"
        user_phone = tracker.get_slot("user_phone") or "غير محدد"

        # ── تلخيص بـ core.gpt (مع cache ومنع الطوفان) ──────
        summary = "لا يوجد ملخص متاح."
        if convo:
            user_msg = (
                "المحادثة التالية جرت بين بوت خدمة عملاء ومستخدم. "
                "لخّصها باختصار في 3-5 جمل ليتمكن الموظف البشري من فهم "
                "السياق والطلب الرئيسي فورًا:\n\n"
                + "\n".join(convo[-20:])
            )
            result = await gpt_complete(
                system_prompt=_SUMMARY_SYSTEM,
                user_message=user_msg,
                max_tokens=250,
                temperature=0.3,
                use_cache=False,  # الملخصات ديناميكية — لا نُخزّنها
            )
            if result:
                summary = result

        # ── إشعار فريق الدعم عبر core.whatsapp ──────────────
        await _notify_support_team(brand, user_name, user_phone, summary, tracker.sender_id)

        dispatcher.utter_message(
            response="utter_transfer_to_manager",
            summary=summary,
        )
        return []


async def _notify_support_team(
    brand: str,
    user_name: str,
    user_phone: str,
    summary: str,
    conversation_id: str,
) -> None:
    """يرسل إشعار التحويل لفريق الدعم عبر core.whatsapp."""
    brand_emoji = {
        "uberfix": "🔧", "laban_alasfour": "🪵",
        "alazab_construction": "🏗️", "luxury_finishing": "✨",
        "brand_identity": "🎨",
    }.get((brand or "").lower(), "🏢")

    msg = (
        f"🙋 *تحويل لموظف بشري*\n"
        f"{brand_emoji} البراند: {brand}\n"
        f"👤 الاسم: {user_name}\n"
        f"📱 الهاتف: {user_phone}\n"
        f"💬 المحادثة: `{conversation_id}`\n\n"
        f"📋 *ملخص:*\n{summary}"
    )
    await send_notification(msg)
