"""
actions/action_submit_lead.py
==============================
جمع بيانات العميل المحتمل، التحقق من صحتها، وإرسال إشعار لفريق المبيعات.
[محسّن] يستخدم core.whatsapp بدلاً من كود مكرر.
"""

import json as _ctx_json
import logging
import re
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict

from .config import NOTIFY_PHONE
from .core.whatsapp import send_text as wa_send

logger = logging.getLogger(__name__)

import os
LEAD_RECEIVER_URL = os.getenv("LEAD_RECEIVER_URL", os.getenv("WEBHOOK_NOTIFY_URL", ""))


# ── Context Helpers ───────────────────────────────────────────

def _ctx_get(tracker: Tracker, field: str, fallback: str = "غير محدد") -> str:
    direct = tracker.get_slot(field)
    if direct:
        return str(direct)
    raw = tracker.get_slot("context_memory") or "{}"
    try:
        ctx = _ctx_json.loads(raw)
    except Exception:
        ctx = {}
    return str(ctx.get(field) or fallback)


def _ctx_build_message(tracker: Tracker) -> str:
    raw = tracker.get_slot("context_memory") or "{}"
    try:
        ctx = _ctx_json.loads(raw)
    except Exception:
        ctx = {}
    parts = []
    if tracker.get_slot("user_message"):
        parts.append(tracker.get_slot("user_message"))
    elif ctx.get("problem_description"):
        parts.append(ctx["problem_description"])
    for key, label in [
        ("branch_name", "الفرع"),
        ("location", "الموقع"),
        ("service_type", "نوع الخدمة"),
        ("technical_specs", "المواصفات الفنية"),
        ("material_needed", "الخامات المطلوبة"),
    ]:
        if ctx.get(key):
            parts.append(f"{label}: {ctx[key]}")
    return " | ".join(parts) if parts else "غير محدد"


# ══════════════════════════════════════════════════════════════
#  Action
# ══════════════════════════════════════════════════════════════

class ActionSubmitLead(Action):
    """يُنفَّذ بعد اكتمال collect_lead flow."""

    def name(self) -> Text:
        return "action_submit_lead"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        user_name    = _ctx_get(tracker, "user_name")
        user_phone   = _ctx_get(tracker, "user_phone")
        user_message = _ctx_build_message(tracker)

        # البراند من slot مباشرة — يُضبط من action_session_start في بداية الجلسة
        # لا نستخدم intent detection لأنه fragile
        brand = tracker.get_slot("brand") or "مجموعة العزب"

        lead_data = {
            "brand":           brand,
            "user_name":       user_name,
            "user_phone":      user_phone,
            "user_message":    user_message,
            "conversation_id": tracker.sender_id,
            "channel":         "rasa",
        }

        logger.info(
            "Lead collected | brand=%s | phone_suffix=%s | conversation=%s",
            brand,
            _phone_suffix(user_phone),
            tracker.sender_id[:8],
        )

        await _send_notification(lead_data)
        dispatcher.utter_message(response="utter_lead_submitted")
        return [AllSlotsReset()]


# ══════════════════════════════════════════════════════════════
#  Notification
# ══════════════════════════════════════════════════════════════

async def _send_notification(data: dict) -> bool:
    """يُرسل بيانات العميل عبر Webhook أو WhatsApp."""
    # 1. محاولة webhook أولاً
    if LEAD_RECEIVER_URL:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.post(LEAD_RECEIVER_URL, json=data)
                r.raise_for_status()
            logger.info("Lead sent via webhook")
            return True
        except Exception as exc:
            logger.warning("Lead webhook failed: %s — falling back to WhatsApp", exc)

    # 2. WhatsApp كـ fallback
    if NOTIFY_PHONE:
        msg = (
            f"🔔 *عميل جديد — {data.get('brand', 'غير محدد')}*\n"
            f"الاسم: {data.get('user_name')}\n"
            f"الهاتف: {data.get('user_phone')}\n"
            f"الطلب: {data.get('user_message', '')[:300]}\n"
            f"المحادثة: {data.get('conversation_id')}"
        )
        return await wa_send(NOTIFY_PHONE, msg)

    logger.warning("No notification channel configured for leads")
    return False


# ── Helpers ───────────────────────────────────────────────────
# ✅ تم حذف _detect_brand() — كانت تكتشف البراند من آخر intent في
#    المحادثة (fragile، القاعدة 4 في التشخيص). الآن نعتمد كلياً
#    على slots.brand المضبوط في action_session_start (القاعدة 1).

def _phone_suffix(value: Any) -> str:
    digits = re.sub(r"\D", "", str(value or ""))
    return digits[-4:] if len(digits) >= 4 else "unknown"


