"""
actions/knowledge_search.py
============================
محرك البحث في قاعدة معرفة آل عزب الإنتاجية.

يبحث في:
  - knowledge/production/alazab_kb.json   (قاعدة البيانات الرئيسية)
  - knowledge/production/categories/*.json (تصنيفات تفصيلية)

يدعم:
  - تطبيع النص العربي (إزالة التشكيل، توحيد الألف والتاء)
  - بحث جزئي (substring) في حقل item
  - حد أقصى للنتائج (limit)
  - Singleton: instance واحد يُحمَّل مرة واحدة طوال عمر الـ process
    (يحل مشكلة القراءة المتكررة من الـ disk عند كل طلب)
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

from .config import CATEGORIES_PATH, PROD_DATA_PATH

logger = logging.getLogger(__name__)


_instance: "KnowledgeSearch | None" = None


def get_knowledge_search(prod_path: str = PROD_DATA_PATH) -> "KnowledgeSearch":
    """
    Singleton factory — يُنشئ instance واحد ويُعيد استخدامه.
    يُحمّل ملفات JSON من الـ disk مرة واحدة فقط.
    """
    global _instance
    if _instance is None:
        _instance = KnowledgeSearch(prod_path)
        logger.info(
            "KnowledgeSearch singleton created: %d inventory + %d categories",
            len(_instance.inventory),
            len(_instance.categories_data),
        )
    return _instance


class KnowledgeSearch:
    """بحث في قاعدة معرفة آل عزب الإنتاجية."""

    def __init__(self, prod_path: str = PROD_DATA_PATH):
        self.prod_path = prod_path
        self.inventory: list[dict] = self._load_json("alazab_kb.json")
        self.categories_data: dict[str, list[dict]] = self._load_categories()

        if not self.inventory:
            logger.warning(
                "KnowledgeSearch: alazab_kb.json not found or empty at %s",
                prod_path,
            )

    # ── Loaders ───────────────────────────────────────────────────────────────

    def _load_json(self, filename: str) -> Any:
        full_path = os.path.join(self.prod_path, filename)
        if not os.path.exists(full_path):
            logger.debug("KnowledgeSearch: file not found: %s", full_path)
            return []
        try:
            with open(full_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("KnowledgeSearch: failed to load %s — %s", full_path, exc)
            return []

    def _load_categories(self) -> dict[str, list[dict]]:
        cats: dict[str, list[dict]] = {}
        if not os.path.isdir(CATEGORIES_PATH):
            logger.debug(
                "KnowledgeSearch: categories dir not found: %s", CATEGORIES_PATH
            )
            return cats
        for fname in os.listdir(CATEGORIES_PATH):
            if not fname.endswith(".json"):
                continue
            cat_name = fname[:-5]  # strip .json
            fpath = os.path.join(CATEGORIES_PATH, fname)
            try:
                with open(fpath, encoding="utf-8") as f:
                    cats[cat_name] = json.load(f)
            except Exception as exc:
                logger.error(
                    "KnowledgeSearch: failed to load category %s — %s", fpath, exc
                )
        return cats

    # ── Arabic Normalization ──────────────────────────────────────────────────

    @staticmethod
    def normalize_arabic(text: str) -> str:
        """إزالة التشكيل وتوحيد الألف والتاء والياء."""
        if not text:
            return ""
        text = re.sub(r"[\u064B-\u0652\u0670]", "", text)   # تشكيل
        text = re.sub(r"[أإآا]", "ا", text)                  # ألف
        text = re.sub(r"ة", "ه", text)                        # تاء مربوطة
        text = re.sub(r"ى", "ي", text)                        # ألف مقصورة
        return text.strip().lower()

    # ── Search ────────────────────────────────────────────────────────────────

    def search_items(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        """
        يبحث عن query في حقل item بالقاعدة الرئيسية ثم التصنيفات.
        يُرجع قائمة بحد أقصى limit نتيجة.
        """
        norm_query = self.normalize_arabic(query)
        if not norm_query:
            return []

        results: list[dict] = []
        seen_ids: set = set()

        def _add(item: dict) -> bool:
            item_id = item.get("id") or id(item)
            if item_id in seen_ids:
                return False
            seen_ids.add(item_id)
            results.append(item)
            return True

        # 1. البحث في القاعدة الرئيسية
        for item in self.inventory:
            if norm_query in self.normalize_arabic(item.get("item", "")):
                _add(item)
                if len(results) >= limit:
                    return results

        # 2. البحث في التصنيفات إذا لم تكتمل النتائج
        for cat_items in self.categories_data.values():
            for item in cat_items:
                if norm_query in self.normalize_arabic(item.get("item", "")):
                    _add(item)
                    if len(results) >= limit:
                        return results

        return results

    # ── Formatting ────────────────────────────────────────────────────────────

    def format_results(self, results: list[dict[str, Any]]) -> str:
        """يُنسّق نتائج البحث كرسالة نصية للمستخدم."""
        if not results:
            return "لم أجد نتائج دقيقة لهذا البند."

        lines = ["🔍 **إليك ما وجدته في سجلات آل عزب:**\n"]
        for i, res in enumerate(results, 1):
            item_name = res.get("item") or "بند غير معروف"
            category  = res.get("category") or "عام"
            action    = res.get("action") or "صيانة"
            unit      = res.get("unit") or ""
            ref_id    = res.get("id")

            lines.append(f"{i}. {item_name}")
            lines.append(f"   - التخصص: {category}")
            lines.append(f"   - الإجراء: {action}")
            if unit and unit not in ("unit", "other"):
                lines.append(f"   - وحدة القياس: {unit}")
            if ref_id:
                lines.append(f"   - كود المرجع: #{ref_id}")
            lines.append("")

        return "\n".join(lines).strip()
