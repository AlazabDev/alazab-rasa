"""
actions/action_send_sweets_info.py
====================================
يعرض معلومات المحلويات من Laban Alasfour.

الفكرة: هذا النشاط (أبو عوف وما شابهه) يطلب UberFix للصيانة،
ويطلب Laban للتوريد. البوت يُوجّه للصيانة عبر UberFix
وللمنتجات عبر laban-alasfour.alazab.com.

المصدر: يقرأ من knowledge/production/alazab_kb.json إن وجد،
يسقط على قائمة ثابتة محترمة عند الغياب.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

# قائمة خدمات ذات صلة يمكن تقديمها لفروع المحلويات
_SWEETS_BRANCH_SERVICES = """🍬 *خدمات مجموعة العزب لفروع المحلويات:*

🔧 *UberFix — الصيانة والتشغيل:*
  • صيانة تكييف ثلاجات العرض
  • كهرباء وإضاءة الواجهات
  • سباكة ومياه المطبخ
  • نجارة وأعمال ديكور

🪵 *Laban Alasfour — التوريدات:*
  • وحدات عرض خشبية مخصصة
  • أثاث مطبخ وكاونترات
  • وحدات تبريد وعرض
  🌐 laban-alasfour.alazab.com

🎨 *Brand Identity — الهوية:*
  • تصميم واجهة الفرع
  • لافتات ومطبوعات
  • تجهيز المساحة بالكامل

قولّي إيه اللي محتاجه وأوجّهك للقسم الصح! 💪"""


class ActionSendSweetsInfo(Action):
    """
    يُعالج استفسارات فروع المحلويات (أبو عوف وما شابهه)
    ويعرض خدمات المجموعة المناسبة لهذا القطاع.
    """

    def name(self) -> Text:
        return "action_send_sweets_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # محاولة قراءة بيانات مخصصة من قاعدة المعرفة
        branch_info = self._get_branch_context(tracker)

        if branch_info:
            dispatcher.utter_message(text=f"أهلاً يا {branch_info}! 👋\n{_SWEETS_BRANCH_SERVICES}")
        else:
            dispatcher.utter_message(text=_SWEETS_BRANCH_SERVICES)

        return []

    def _get_branch_context(self, tracker: Tracker) -> str:
        """يحاول استخراج اسم الفرع من السياق."""
        import json
        ctx_raw = tracker.get_slot("context_memory") or "{}"
        try:
            ctx = json.loads(ctx_raw)
        except Exception:
            ctx = {}

        branch = (
            tracker.get_slot("branch_name")
            or ctx.get("branch_name")
            or ""
        )
        return branch.strip()
