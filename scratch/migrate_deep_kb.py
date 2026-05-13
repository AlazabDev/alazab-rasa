#!/usr/bin/env python3
"""
Deep Migration: Alazab Knowledge Base → rasa-calm-demo RAG Structure
- Copies entire knowledge/ directory
- Creates Arabic-ready Qdrant loader for alazab_kb.json
- Creates proper CALM search domain (domain/search/alazab_kb.yml)
- Creates CALM flows for each alazab service domain
- Updates rag.jinja2 with Arabic support
- Creates proper action_trigger_alazab_search.py
"""
import json, shutil, yaml, os
from pathlib import Path

SRC = Path("/home/azab/azabot/alazab-rasa")
DST = Path("/home/azab/azabot/rasa-calm-demo")

# ── 1. Copy entire knowledge directory ────────────────────────────────────────
def copy_knowledge():
    src_kb = SRC / "knowledge"
    dst_kb = DST / "knowledge"
    if dst_kb.exists():
        shutil.rmtree(dst_kb)
    shutil.copytree(src_kb, dst_kb)
    print(f"  ✅ Copied knowledge/ → {dst_kb}")

# ── 2. Create Qdrant loader for Arabic KB ─────────────────────────────────────
def create_qdrant_loader():
    script = '''\
#!/usr/bin/env python3
"""
Load Alazab KB → Qdrant vector store for RAG search.
Supports Arabic content using multilingual embeddings.

Usage:
    python scripts/load-alazab-kb-to-qdrant.py
    python scripts/load-alazab-kb-to-qdrant.py --category electrical
    python scripts/load-alazab-kb-to-qdrant.py --source construction
"""
import json
import argparse
import logging
from pathlib import Path
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.qdrant import Qdrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KB_PATH = Path("knowledge/production/alazab_kb.json")
CATEGORIES_DIR = Path("knowledge/production/categories")
COLLECTION_NAME = "alazab_kb"

# Multilingual model that handles Arabic well
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

CATEGORY_MAP = {
    "construction": "إنشاء",
    "maintenance": "صيانة",
    "electrical": "كهرباء",
    "plumbing": "سباكة",
    "carpentry": "نجارة",
    "flooring": "أرضيات",
    "painting": "دهانات",
    "hvac": "تكييف",
    "security": "أمن وسلامة",
    "invoice_history": "فواتير",
    "purchase_history": "مشتريات",
    "product_catalog": "كتالوج منتجات",
}


def kb_to_documents(items: list, filter_category=None, filter_source=None) -> list:
    """Convert KB items to LangChain Document objects for vector indexing."""
    docs = []
    for item in items:
        cat = item.get("category", "")
        src = item.get("source", "")

        if filter_category and cat != filter_category:
            continue
        if filter_source and src != filter_source:
            continue

        # Build rich text for embedding (Arabic + context)
        item_text = item.get("item", "")
        original_text = item.get("original", "")
        action = item.get("action", "")
        price = item.get("price", "")

        # Compose searchable text
        content_parts = [item_text]
        if original_text and original_text != item_text:
            content_parts.append(original_text)
        if action and action != "other":
            content_parts.append(f"نوع العمل: {action}")
        if cat:
            content_parts.append(f"التصنيف: {cat}")
        if price:
            content_parts.append(f"السعر: {price}")

        page_content = "\\n".join(content_parts)

        metadata = {
            "id": item.get("id", 0),
            "category": cat,
            "source": src,
            "action": action,
            "unit": item.get("unit", ""),
            "price": price,
            "original": original_text,
        }

        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs


def load_to_qdrant(
    kb_path=KB_PATH,
    collection_name=COLLECTION_NAME,
    filter_category=None,
    filter_source=None,
    qdrant_host="localhost",
    qdrant_port=6333,
):
    logger.info(f"📂 Loading KB from: {kb_path}")
    items = json.loads(Path(kb_path).read_text(encoding="utf-8"))
    logger.info(f"📊 Total KB items: {len(items)}")

    docs = kb_to_documents(items, filter_category, filter_source)
    logger.info(f"📝 Documents to index: {len(docs)}")

    if not docs:
        logger.warning("⚠️  No documents to index. Check your filters.")
        return None

    logger.info(f"🤖 Loading embedding model: {EMBED_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    logger.info(f"🔌 Connecting to Qdrant at {qdrant_host}:{qdrant_port}")
    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        host=qdrant_host,
        port=qdrant_port,
        prefer_grpc=False,
        collection_name=collection_name,
        force_recreate=True,
    )
    logger.info(f"✅ Indexed {len(docs)} items into collection '{collection_name}'")

    # Quick sanity-check search
    test_queries = [
        "تركيب كهرباء فرع",
        "صيانة سباكة",
        "تركيب دهانات",
        "توريد رخام",
    ]
    logger.info("🔍 Sanity-check searches:")
    for q in test_queries:
        results = qdrant.similarity_search_with_score(q, k=2)
        for doc, score in results:
            logger.info(f"  [{score:.3f}] {doc.page_content[:80]}")

    return qdrant


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Alazab KB into Qdrant")
    parser.add_argument("--kb", default=str(KB_PATH), help="Path to KB JSON file")
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--category", default=None, help="Filter by category")
    parser.add_argument("--source", default=None, help="Filter by source (construction/maintenance/...)")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=6333)
    args = parser.parse_args()

    load_to_qdrant(
        kb_path=args.kb,
        collection_name=args.collection,
        filter_category=args.category,
        filter_source=args.source,
        qdrant_host=args.host,
        qdrant_port=args.port,
    )
'''
    out = DST / "scripts" / "load-alazab-kb-to-qdrant.py"
    out.write_text(script, encoding="utf-8")
    print(f"  ✅ Created {out.name}")

# ── 3. Create CALM search domain for alazab KB ────────────────────────────────
def create_search_domain():
    domain = {
        "version": "3.1",
        "responses": {
            "utter_alazab_search_intro": [{"text": "سأبحث في قاعدة بيانات مجموعة العزب عن هذا الطلب..."}],
            "utter_alazab_no_results": [{"text": "لم أجد نتائج مطابقة في قاعدة البيانات. يمكنني تحويل طلبك للفريق المختص."}],
            "utter_alazab_search_error": [{"text": "حدث خطأ أثناء البحث. برجاء المحاولة مرة أخرى أو التواصل مع الفريق مباشرة."}],
        }
    }
    out = DST / "domain" / "search" / "alazab_kb.yml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(domain, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"  ✅ Created domain/search/alazab_kb.yml")

# ── 4. Create CALM flows for alazab services ──────────────────────────────────
def create_alazab_flows():
    flows_data = {
        "version": "3.1",
        "flows": {
            "alazab_maintenance_request": {
                "description": "طلب صيانة UberFix — يجمع بيانات الفرع والعطل ويفتح تذكرة",
                "nlu_trigger": [
                    {"intent": "ask_uberfix_services"},
                    {"intent": "start_maintenance_request"},
                    {"intent": "uberfix_specific_repair"},
                ],
                "steps": [
                    {"collect": "branch_name", "description": "اسم الفرع أو الموقع المطلوب الصيانة فيه", "ask_before_filling": True},
                    {"collect": "service_item", "description": "وصف العطل أو البند المطلوب", "ask_before_filling": True},
                    {"collect": "user_name", "description": "اسم المسؤول عن الفرع", "ask_before_filling": True},
                    {"collect": "user_phone", "description": "رقم التواصل", "ask_before_filling": True},
                    {"action": "alazab_action_create_maintenance_request"},
                ]
            },
            "alazab_kb_search": {
                "description": "بحث في قاعدة معرفة مجموعة العزب عن خدمات، أسعار، أو مواصفات",
                "nlu_trigger": [
                    {"intent": "faq_search"},
                    {"intent": "request_quote"},
                ],
                "steps": [
                    {"collect": "keyword", "description": "كلمة البحث أو الخدمة المطلوبة", "ask_before_filling": True},
                    {"action": "action_trigger_search"},
                ]
            },
            "alazab_brand_identity": {
                "description": "استفسارات Brand Identity — تجهيز فروع وهوية تجارية",
                "nlu_trigger": [
                    {"intent": "ask_brand_services"},
                    {"intent": "ask_brand_shop_fitting"},
                    {"intent": "ask_brand_complete_identity"},
                    {"intent": "ask_brand_quote"},
                ],
                "steps": [
                    {"action": "utter_brand_services"},
                ]
            },
            "alazab_luxury_finishing": {
                "description": "استفسارات Luxury Finishing — تشطيبات فاخرة",
                "nlu_trigger": [
                    {"intent": "ask_luxury_services"},
                ],
                "steps": [
                    {"action": "utter_luxury_services"},
                ]
            },
            "alazab_human_handoff": {
                "description": "تحويل المحادثة لممثل بشري",
                "nlu_trigger": [
                    {"intent": "request_human_handoff"},
                ],
                "steps": [
                    {"collect": "handoff_reason", "description": "سبب طلب التواصل مع الفريق", "ask_before_filling": True},
                    {"action": "alazab_action_human_handoff"},
                ]
            },
            "alazab_lead_capture": {
                "description": "تسجيل بيانات عميل جديد وإرسالها لفريق المبيعات",
                "nlu_trigger": [
                    {"intent": "ask_alazab_quote"},
                    {"intent": "ask_alazab_contact"},
                ],
                "steps": [
                    {"collect": "user_name", "description": "اسم العميل", "ask_before_filling": True},
                    {"collect": "user_phone", "description": "رقم التواصل", "ask_before_filling": True},
                    {"collect": "location", "description": "المنطقة أو المحافظة", "ask_before_filling": True},
                    {"collect": "service_type", "description": "نوع الخدمة المطلوبة", "ask_before_filling": True},
                    {"action": "alazab_action_submit_lead"},
                ]
            },
        }
    }
    out = DST / "data" / "flows" / "alazab_services.yml"
    out.write_text(yaml.safe_dump(flows_data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    print(f"  ✅ Created data/flows/alazab_services.yml ({len(flows_data['flows'])} flows)")

# ── 5. Update rag.jinja2 with Arabic support ──────────────────────────────────
def create_arabic_rag_template():
    template = """\
Given the following information from Alazab Group knowledge base, answer the user's question.
يرجى الإجابة بناءً على المستندات التالية من قاعدة بيانات مجموعة العزب.

### المستندات ذات الصلة / Relevant Documents
{% for doc in docs %}
{{ loop.index }}. {{ doc.text }}
   [التصنيف: {{ doc.metadata.get('category', '') }} | المصدر: {{ doc.metadata.get('source', '') }}{% if doc.metadata.get('price') %} | السعر: {{ doc.metadata.get('price') }}{% endif %}]
{% endfor %}

{% if slots|length > 0 %}
### المعلومات المتوفرة / Available Slots
{% for slot in slots -%}
- {{ slot.name }}: {{ slot.value }}
{% endfor %}
{% endif %}

### المحادثة الحالية / Current Conversation
{{ current_conversation }}

## الإجابة / Answer
يرجى اتباع هذه الإرشادات:
- أجب بناءً على المستندات فقط.
- إذا كانت المعلومات غير متوفرة، قل ذلك بوضوح واعرض تحويل الطلب للفريق المختص.
- اذكر السعر إن وجد في المستندات.
- أجب بنفس لغة السؤال (عربي أو إنجليزي).
- لا تتجاوز 3-4 جمل في الإجابة.
- لا تذكر "المستندات المقدمة" أو "قاعدة البيانات" صراحة.

{% for slot in slots -%}
    {% if slot.name == "language" -%}
    {% set language = slot.value %}- يجب أن تكون إجابتك باللغة {{ language }}
    {% endif %}
{% endfor %}

إجابتك:
"""
    out = DST / "rag.jinja2"
    out.write_text(template, encoding="utf-8")
    print(f"  ✅ Updated rag.jinja2 with Arabic/bilingual support")

# ── 6. Create custom alazab search action ─────────────────────────────────────
def create_search_action():
    action_code = '''\
"""
action_trigger_alazab_search.py
Custom Rasa CALM action that queries Qdrant for Alazab KB items.
Replaces the default action_trigger_search with Arabic-aware version.
"""
from typing import Any, Dict, List, Text
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

logger = logging.getLogger(__name__)

try:
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores.qdrant import Qdrant
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    logger.warning("langchain/qdrant not installed. KB search will be disabled.")

COLLECTION = "alazab_kb"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 5


class ActionTriggerAlazabSearch(Action):
    """Search Alazab KB in Qdrant and return structured results."""

    def name(self) -> Text:
        return "action_trigger_alazab_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        query = tracker.get_slot("keyword") or tracker.latest_message.get("text", "")
        if not query:
            dispatcher.utter_message(response="utter_alazab_no_results")
            return []

        if not QDRANT_AVAILABLE:
            dispatcher.utter_message(text=f"بحث عن: {query} (Qdrant غير متوفر)")
            return []

        try:
            embeddings = HuggingFaceEmbeddings(
                model_name=EMBED_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            qdrant = Qdrant(
                client=None,  # Will use env QDRANT_URL
                collection_name=COLLECTION,
                embeddings=embeddings,
            )
            results = qdrant.similarity_search_with_score(query, k=TOP_K)

            if not results:
                dispatcher.utter_message(response="utter_alazab_no_results")
                return [SlotSet("search_found", False)]

            # Format results
            lines = [f"🔍 نتائج البحث عن: **{query}**\\n"]
            for doc, score in results:
                meta = doc.metadata
                item_text = doc.page_content.split("\\n")[0]
                cat = meta.get("category", "")
                price = meta.get("price", "")
                action_type = meta.get("action", "")
                line = f"• {item_text}"
                if price:
                    line += f" — السعر: {price} جنيه"
                if cat:
                    line += f" [{cat}]"
                lines.append(line)

            dispatcher.utter_message(text="\\n".join(lines))
            return [SlotSet("search_found", True), SlotSet("results", "\\n".join(lines))]

        except Exception as e:
            logger.error(f"Qdrant search error: {e}")
            dispatcher.utter_message(response="utter_alazab_search_error")
            return [SlotSet("search_found", False)]
'''
    out = DST / "actions" / "action_trigger_alazab_search.py"
    out.write_text(action_code, encoding="utf-8")
    print(f"  ✅ Created actions/action_trigger_alazab_search.py")

# ── 7. Update domain/_shared.yml slots for CALM ───────────────────────────────
def add_calm_slots():
    shared_path = DST / "domain" / "_shared.yml"
    data = yaml.safe_load(shared_path.read_text(encoding="utf-8")) or {}

    new_slots = {
        "branch_name": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "service_item": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "service_type": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "user_name": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "user_phone": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "location": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "keyword": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "search_found": {"type": "bool", "mappings": [{"type": "from_llm"}]},
        "results": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "handoff_reason": {"type": "text", "mappings": [{"type": "from_llm"}]},
        "summary": {"type": "text", "mappings": [{"type": "from_llm"}]},
    }

    existing = data.get("slots", {})
    added = 0
    for k, v in new_slots.items():
        if k not in existing:
            existing[k] = v
            added += 1
        else:
            # Upgrade custom slots to from_llm for CALM
            existing[k] = v

    data["slots"] = existing
    shared_path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8"
    )
    print(f"  ✅ Added/updated {added} CALM slots in _shared.yml")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Deep Migration: Knowledge Base + CALM Structure")
    print("=" * 60)

    print("\n[1/7] Copying full knowledge/ directory...")
    copy_knowledge()

    print("\n[2/7] Creating Arabic Qdrant loader script...")
    create_qdrant_loader()

    print("\n[3/7] Creating CALM search domain...")
    create_search_domain()

    print("\n[4/7] Creating proper CALM flows for alazab services...")
    create_alazab_flows()

    print("\n[5/7] Updating RAG template with Arabic support...")
    create_arabic_rag_template()

    print("\n[6/7] Creating Arabic-aware search action...")
    create_search_action()

    print("\n[7/7] Updating CALM slots in _shared.yml...")
    add_calm_slots()

    print("\n" + "=" * 60)
    print("✅ Deep Migration Complete!")
    print("\nNext steps:")
    print("  1. Start Qdrant:  docker run -p 6333:6333 qdrant/qdrant")
    print("  2. Load KB:       python scripts/load-alazab-kb-to-qdrant.py")
    print("  3. Validate:      rasa data validate")
    print("  4. Train:         rasa train")
