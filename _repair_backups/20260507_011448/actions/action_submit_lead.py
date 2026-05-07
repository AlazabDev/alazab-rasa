"""
actions/action_submit_lead.py
==============================
جمع بيانات العميل المحتمل، التحقق من صحتها، وإرسال إشعار لفريق المبيعات
عبر Webhook أو WhatsApp Business API.
"""

import os
import re
import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

WEBHOOK_NOTIFY_URL = os.getenv("WEBHOOK_NOTIFY_URL", "")
LEAD_RECEIVER_URL  = os.getenv("LEAD_RECEIVER_URL", WEBHOOK_NOTIFY_URL)
WHATSAPP_API_URL   = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_TOKEN     = os.getenv("WHATSAPP_TOKEN", "")
NOTIFY_PHONE       = os.getenv("NOTIFY_PHONE", "")


# ──────────────────────────────────────────────────────────────
#  Action: إرسال بيانات العميل
# ──────────────────────────────────────────────────────────────
import json as _ctx_json

def _ctx_get(tracker, field: str, fallback: str = "غير محدد") -> str:
    direct = tracker.get_slot(field)
    if direct:
        return direct
    raw = tracker.get_slot("context_memory") or "{}"
    try:
        ctx = _ctx_json.loads(raw)
    except Exception:
        ctx = {}
    return ctx.get(field) or fallback

def _ctx_build_message(tracker) -> str:
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
    for key, label in [("branch_name","الفرع"),("location","الموقع"),("service_type","نوع الخدمة")]:
        if ctx.get(key):
            parts.append(f"{label}: {ctx[key]}")
    return " | ".join(parts) if parts else "غير محدد"

class ActionSubmitLead(Action):
    """
    يُنفَّذ بعد اكتمال collect_lead flow.
    يحفظ البيانات ويرسل إشعارًا فوريًا لفريق المبيعات.
    """

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
        brand        = tracker.get_slot("brand") or _detect_brand(tracker)

        lead_data = {
            "brand":           brand,
            "user_name":       user_name,
            "user_phone":      user_phone,
            "user_message":    user_message,
            "conversation_id": tracker.sender_id,
        }

        logger.info(
            "New lead collected | brand=%s | conversation_id=%s | phone_suffix=%s",
            brand,
            tracker.sender_id,
            _phone_suffix(user_phone),
        )
        await _send_notification(lead_data)

        dispatcher.utter_message(response="utter_lead_submitted")
        return [AllSlotsReset()]


# ──────────────────────────────────────────────────────────────
#  أداة: إرسال إشعار داخلي (Webhook / WhatsApp)
# ──────────────────────────────────────────────────────────────
async def _send_notification(data: dict) -> bool:
    """يرسل بيانات العميل إلى webhook داخلي أو WhatsApp Business API."""
    try:
        import httpx

        if LEAD_RECEIVER_URL:
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.post(LEAD_RECEIVER_URL, json=data)
                r.raise_for_status()
            logger.info("Lead notification sent via lead receiver webhook.")
            return True

        if WHATSAPP_API_URL and WHATSAPP_TOKEN and NOTIFY_PHONE:
            msg = (
                f"🔔 *عميل جديد — {data.get('brand', 'غير محدد')}*\n"
                f"الاسم: {data.get('user_name')}\n"
                f"الهاتف: {data.get('user_phone')}\n"
                f"الطلب: {data.get('user_message')}\n"
                f"المحادثة: {data.get('conversation_id')}"
            )
            payload = {
                "messaging_product": "whatsapp",
                "to":   NOTIFY_PHONE,
                "type": "text",
                "text": {"body": msg},
            }
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.post(
                    WHATSAPP_API_URL,
                    headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
                    json=payload,
                )
                r.raise_for_status()
            logger.info("Lead notification sent via WhatsApp.")
            return True

    except Exception as e:
        logger.error(f"Notification error: {e}")

    return False


# ──────────────────────────────────────────────────────────────
#  أداة: اكتشاف العلامة التجارية من سياق المحادثة
# ──────────────────────────────────────────────────────────────
def _detect_brand(tracker: Tracker) -> str:
    """يستنتج العلامة التجارية من آخر intent في المحادثة."""
    intent_map = {
        "alazab":  "Alazab Construction",
        "luxury":  "Luxury Finishing",
        "brand":   "Brand Identity",
        "uberfix": "UberFix",
        "laban":   "Laban Alasfour",
    }
    for event in reversed(tracker.events):
        if event.get("event") == "user":
            intent = event.get("parse_data", {}).get("intent", {}).get("name", "")
            for key, brand in intent_map.items():
                if key in intent:
                    return brand
    return "مجموعة العزب"


def _phone_suffix(value: Any) -> str:
    digits = re.sub(r"\D", "", str(value or ""))
    return digits[-4:] if len(digits) >= 4 else "unknown"
