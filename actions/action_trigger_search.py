"""
actions/action_trigger_search.py
==================================
يُستدعى من pattern_search عند knowledge_answer command.
EnterpriseSearchPolicy تتولى الـ retrieval والـ generation،
هذا الـ action يهيئ السياق فقط.

من الـ PDF:
  "action_trigger_search sends relevant queries
   to the default action action_trigger_search"
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)


class ActionTriggerSearch(Action):
    """
    يُشغّل Enterprise Search لإجابة الأسئلة المعرفية.
    EnterpriseSearchPolicy تتولى الـ RAG فعلياً.
    هذا الـ action يُهيّئ السياق ويسجّل الطلب.
    """

    def name(self) -> Text:
        return "action_trigger_search"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        brand = tracker.get_slot("brand") or "مجموعة العزب"
        query = tracker.latest_message.get("text", "")

        logger.info(
            "Enterprise Search triggered | brand=%s | query=%s",
            brand,
            query[:50],
        )

        # EnterpriseSearchPolicy تتولى الإجابة تلقائياً
        # هذا الـ action لا يُرجع شيئاً — الـ policy هي من ترد
        return []
