import json
import os
import re
from typing import List, Dict, Any
from .config import PROD_DATA_PATH, CATEGORIES_PATH

class KnowledgeSearch:
    def __init__(self, prod_path: str = PROD_DATA_PATH):
        self.prod_path = prod_path
        self.inventory = self._load_json("alazab_kb.json")
        self.standards = self._load_json("engineering_standards.json")
        self.context_map = self._load_json("context_map.json")
        self.categories_data = self._load_categories()

    def _load_categories(self) -> Dict[str, List[Dict]]:
        cats = {}
        try:
            if os.path.exists(CATEGORIES_PATH):
                for f in os.listdir(CATEGORIES_PATH):
                    if f.endswith(".json"):
                        cat_name = f.replace(".json", "")
                        with open(os.path.join(CATEGORIES_PATH, f), 'r', encoding='utf-8') as file:
                            cats[cat_name] = json.load(file)
        except Exception:
            pass
        return cats

    def _load_json(self, filename: str) -> Any:
        full_path = os.path.join(self.prod_path, filename)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def normalize_arabic(self, text: str) -> str:
        if not text: return ""
        text = re.sub(r'[\u064B-\u0652]', '', text)
        text = re.sub(r'[أإآا]', 'ا', text)
        text = re.sub(r'ة', 'ه', text)
        text = re.sub(r'ى', 'ي', text)
        return text.strip().lower()

    def search_items(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        norm_query = self.normalize_arabic(query)
        results = []
        
        # 1. Search in Master Inventory
        if self.inventory:
            for item in self.inventory:
                if norm_query in self.normalize_arabic(item.get("item", "")):
                    results.append(item)
                    if len(results) >= limit: break
        
        # 2. Deep Search in Categories if needed
        if len(results) < limit and self.categories_data:
            for cat_name, items in self.categories_data.items():
                for item in items:
                    if norm_query in self.normalize_arabic(item.get("item", "")):
                        if item not in results:
                            results.append(item)
                            if len(results) >= limit: break
                if len(results) >= limit: break
                
        return results

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return "لم أجد نتائج دقيقة لهذا البند."
        
        response = "🔍 **إليك ما وجدته في سجلات آل عزب:**\n\n"
        for i, res in enumerate(results, 1):
            response += f"{i}. {res.get('item', 'بند غير معروف')}\n"
            response += f"   - التخصص: {res.get('category', 'عام')}\n"
            response += f"   - الإجراء: {res.get('action', 'صيانة')}\n"
            if res.get('id'):
                response += f"   - كود المرجع: #{res.get('id')}\n"
            response += "\n"
        return response
