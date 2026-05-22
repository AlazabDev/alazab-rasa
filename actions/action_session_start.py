"""
actions/action_session_start.py
================================
Session Start مخصص — يضبط brand slot من metadata.

هذا هو حل القاعدة 1: Brand Context أول خطوة.

عندما يفتح أي مستخدم المحادثة، الـ webhook يُرسل metadata.brand
بناءً على الـ URL أو الـ domain. هذا الـ action يضبطه في slot.

بعد ذلك، كل action في النظام تعرف:
  - "أنا داخل سياق UberFix" ← تُحلّل طلبات صيانة فقط
  - "أنا داخل سياق Laban"   ← تُوجّه لموقع laban-alasfour.alazab.com
  - "أنا داخل سياق Alazab"  ← تُعالج مشاريع مقاولات
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

# خريطة تطبيع أسماء البراندات
_BRAND_ALIASES: dict[str, str] = {
    # UberFix
    "uberfix":              "uberfix",
    "uber_fix":             "uberfix",
    "uberfix_shop":         "uberfix",
    # Laban Alasfour
    "laban_alasfour":       "laban_alasfour",
    "laban-alasfour":       "laban_alasfour",
    "laban":                "laban_alasfour",
    # Alazab Construction
    "alazab_construction":  "alazab_construction",
    "alazab-construction":  "alazab_construction",
    "alazab":               "alazab_construction",
    # Luxury Finishing
    "luxury_finishing":     "luxury_finishing",
    "luxury-finishing":     "luxury_finishing",
    "luxury":               "luxury_finishing",
    # Brand Identity
    "brand_identity":       "brand_identity",
    "brand-identity":       "brand_identity",
    "brand":                "brand_identity",
}

# Welcome messages per brand — موجزة ومحددة
_BRAND_GREETINGS: dict[str, str] = {
    "uberfix": (
        "👋 أهلاً! أنا عزبوت، مساعد UberFix الذكي.\n"
        "كيف أساعدك؟ 🔧 صيانة | 📍 تتبع طلب | 📦 الباقات"
    ),
    "laban_alasfour": (
        "👋 أهلاً! أنا مساعد Laban Alasfour.\n"
        "هل تسأل عن الوحدات الخشبية والتصاميم؟ "
        "زور موقعنا المتخصص: 🌐 laban-alasfour.alazab.com\n"
        "أو اترك بياناتك وفريقنا يتواصل معاك."
    ),
    "alazab_construction": (
        "👋 أهلاً! أنا عزبوت، مساعد Alazab Construction.\n"
        "كيف أساعدك؟ 🏗️ عرض سعر | 📋 مشاريع | 📞 تواصل"
    ),
    "luxury_finishing": (
        "👋 أهلاً! أنا مساعد Luxury Finishing.\n"
        "كيف أساعدك؟ ✨ عرض سعر تشطيب | 🎨 خامات | 📐 استشارة"
    ),
    "brand_identity": (
        "👋 أهلاً! أنا مساعد Brand Identity.\n"
        "كيف أساعدك؟ 🎯 عرض سعر هوية | 🏬 تجهيز مساحة | 🎨 استشارة"
    ),
}

_DEFAULT_GREETING = (
    "👋 أهلاً! أنا عزبوت، مساعد مجموعة العزب الذكي.\n"
    "كيف أساعدك؟ 🔧 صيانة | ✨ تشطيب | 🏗️ مقاولات | 🎨 هوية | 📦 توريدات"
)


class ActionSessionStart(Action):
    """
    يُستدعى عند بداية كل جلسة.
    يضبط brand slot من metadata المرسلة من الـ webhook.
    """

    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        events: List[Dict[Text, Any]] = [SessionStarted()]

        # استخراج البراند من metadata
        metadata = tracker.get_slot("session_started_metadata") or {}
        if not isinstance(metadata, dict):
            metadata = {}

        raw_brand = (
            metadata.get("brand")
            or metadata.get("Brand")
            or tracker.get_slot("brand")
            or ""
        ).strip().lower().replace("-", "_")

        brand = _BRAND_ALIASES.get(raw_brand, "")

        if brand:
            events.append(SlotSet("brand", brand))
            logger.info("Session started | brand=%s | sender=%s", brand, tracker.sender_id[:8])
        else:
            logger.info("Session started | brand=unknown | sender=%s", tracker.sender_id[:8])

        # رد الترحيب المناسب للـ brand
        greeting = _BRAND_GREETINGS.get(brand, _DEFAULT_GREETING)
        events.append(ActionExecuted("action_listen"))

        dispatcher.utter_message(text=greeting)
        return events
