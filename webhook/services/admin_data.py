"""
webhook/services/admin_data.py — Admin Data Layer (Supabase)
=============================================================
يخزن ويقرأ بيانات لوحة التحكم من Supabase.

الجداول:
  bot_settings    → إعدادات البوت (صف واحد id=1)
  conversations   → المحادثات
  messages        → رسائل كل محادثة
  integrations    → التكاملات
  webhook_logs    → سجل التسليم
  leads           → العملاء
  laban_orders    → طلبات Laban
"""
from __future__ import annotations

import logging
import os
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Optional

logger = logging.getLogger("alazab.webhook.admin_data")

_stats: dict[str, int] = defaultdict(int)
_start_time = time.time()
_stats_lock = Lock()


def _sb():
    """Supabase client — service_role."""
    try:
        from supabase import create_client  # type: ignore
        url = os.getenv("SUPABASE_URL", "").strip()
        key = (
            os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
            or os.getenv("SUPABASE_SECRET_KEY", "")
        ).strip()
        if url and key:
            return create_client(url, key)
    except Exception as exc:
        logger.error("Supabase client: %s", exc)
    return None


# ══════════════════════════════════════════════════════════════
#  Stats
# ══════════════════════════════════════════════════════════════

def count(channel: str) -> None:
    with _stats_lock:
        _stats[channel] += 1


def admin_stats_payload() -> dict[str, Any]:
    client = _sb()
    convs = msgs = today = 0
    try:
        if client:
            convs = len(client.table("conversations").select("id").execute().data or [])
            msgs  = len(client.table("messages").select("id").execute().data or [])
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            today = len(
                client.table("conversations")
                .select("id")
                .gte("created_at", today_str)
                .execute().data or []
            )
    except Exception as exc:
        logger.warning("stats fetch: %s", exc)

    return {
        "conversations": convs,
        "messages": msgs,
        "today": today,
        "uptime_seconds": round(time.time() - _start_time),
        "message_counts": dict(_stats),
        "memory_mb": _memory_mb(),
    }


def _memory_mb() -> float:
    try:
        import psutil, os
        return round(psutil.Process(os.getpid()).memory_info().rss / (1024*1024), 1)
    except Exception:
        return 0.0


# ══════════════════════════════════════════════════════════════
#  Settings
# ══════════════════════════════════════════════════════════════

def load_settings() -> dict:
    """قراءة إعدادات البوت من Supabase."""
    try:
        client = _sb()
        if client:
            res = client.table("bot_settings").select("*").eq("id", 1).limit(1).execute()
            if res.data:
                return res.data[0]
    except Exception as exc:
        logger.warning("load_settings: %s", exc)
    return _default_settings()


def save_settings(data: dict) -> bool:
    """حفظ إعدادات البوت في Supabase."""
    try:
        client = _sb()
        if client:
            client.table("bot_settings").upsert({**data, "id": 1}).execute()
            return True
    except Exception as exc:
        logger.error("save_settings: %s", exc)
    return False


def _default_settings() -> dict:
    return {
        "id": 1,
        "bot_name": "AzaBot",
        "primary_color": "#d6a318",
        "welcome_message": "مرحباً! كيف يمكنني مساعدتك؟",
        "quick_replies": ["ما هي خدماتكم؟", "أريد عرض سعر", "كيف أتواصل معكم؟"],
        "voice_enabled": True,
        "auto_speak": False,
        "tts_model": "gpt-4o-mini-tts",
        "tts_voice": "nova",
    }


# ══════════════════════════════════════════════════════════════
#  Conversations
# ══════════════════════════════════════════════════════════════

def list_conversations(q: str = "", channel: str = "") -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        query = client.table("conversations").select(
            "id, session_id, metadata, created_at, updated_at"
        ).order("created_at", desc=True).limit(500)
        res = query.execute()
        rows = res.data or []
        if channel:
            rows = [r for r in rows if (r.get("metadata") or {}).get("channel") == channel]
        if q:
            q = q.lower()
            rows = [r for r in rows if q in str(r.get("session_id", "")).lower()
                    or q in str((r.get("metadata") or {}).get("brand", "")).lower()]
        return rows
    except Exception as exc:
        logger.error("list_conversations: %s", exc)
        return []


def get_conversation(conv_id: str) -> Optional[dict]:
    try:
        client = _sb()
        if not client:
            return None
        res = client.table("conversations").select("*").eq("id", conv_id).limit(1).execute()
        if not res.data:
            return None
        conv = res.data[0]
        msgs = client.table("messages").select("*").eq(
            "conversation_id", conv_id
        ).order("created_at").execute()
        conv["messages"] = msgs.data or []
        return conv
    except Exception as exc:
        logger.error("get_conversation: %s", exc)
        return None


def delete_conversation(conv_id: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("messages").delete().eq("conversation_id", conv_id).execute()
        client.table("conversations").delete().eq("id", conv_id).execute()
        return True
    except Exception as exc:
        logger.error("delete_conversation: %s", exc)
        return False


async def record_conversation(
    session_id: str, brand: str, channel: str, messages: list[dict]
) -> dict:
    """يُسجّل أو يُحدّث محادثة في Supabase."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        client = _sb()
        if not client:
            return {"id": str(uuid.uuid4()), "session_id": session_id}

        res = client.table("conversations").select("id").eq(
            "session_id", session_id
        ).limit(1).execute()

        if res.data:
            conv_id = res.data[0]["id"]
            client.table("conversations").update({
                "updated_at": now,
                "metadata": {"brand": brand, "channel": channel},
            }).eq("id", conv_id).execute()
        else:
            conv_id = str(uuid.uuid4())
            client.table("conversations").insert({
                "id": conv_id,
                "session_id": session_id,
                "created_at": now,
                "updated_at": now,
                "metadata": {"brand": brand, "channel": channel},
            }).execute()

        for msg in messages:
            client.table("messages").insert({
                "id": msg.get("id", str(uuid.uuid4())),
                "conversation_id": conv_id,
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
                "created_at": msg.get("created_at", now),
                "attachments": msg.get("attachments", []),
            }).execute()

        return {"id": conv_id, "session_id": session_id}
    except Exception as exc:
        logger.error("record_conversation: %s", exc)
        return {"id": str(uuid.uuid4()), "session_id": session_id}


record_conversation_simple = record_conversation


# ══════════════════════════════════════════════════════════════
#  Integrations
# ══════════════════════════════════════════════════════════════

def list_integrations() -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        res = client.table("integrations").select("*").order("created_at", desc=True).execute()
        return res.data or []
    except Exception as exc:
        logger.error("list_integrations: %s", exc)
        return []


def save_integration(data: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    try:
        client = _sb()
        if not client:
            return data
        if not data.get("id"):
            data["id"] = str(uuid.uuid4())
            data.setdefault("created_at", now)
            client.table("integrations").insert(data).execute()
        else:
            data["updated_at"] = now
            client.table("integrations").upsert(data).execute()
        return data
    except Exception as exc:
        logger.error("save_integration: %s", exc)
        return data


def delete_integration(int_id: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("integrations").delete().eq("id", int_id).execute()
        return True
    except Exception as exc:
        logger.error("delete_integration: %s", exc)
        return False


def list_integration_logs(limit: int = 100) -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        res = client.table("webhook_logs").select("*").order(
            "created_at", desc=True
        ).limit(limit).execute()
        return res.data or []
    except Exception as exc:
        logger.error("list_integration_logs: %s", exc)
        return []


def save_integration_log(log: dict) -> None:
    try:
        client = _sb()
        if client:
            log.setdefault("id", str(uuid.uuid4()))
            client.table("webhook_logs").insert(log).execute()
    except Exception as exc:
        logger.error("save_integration_log: %s", exc)


# ══════════════════════════════════════════════════════════════
#  Laban Orders
# ══════════════════════════════════════════════════════════════

def list_laban_orders(status: str = "", q: str = "") -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        query = client.table("laban_orders").select("*").order("created_at", desc=True)
        if status:
            query = query.eq("status", status)
        res = query.limit(500).execute()
        rows = res.data or []
        if q:
            q = q.lower()
            rows = [r for r in rows if q in str(r.get("client_name","")).lower()
                    or q in str(r.get("order_number","")).lower()]
        return rows
    except Exception as exc:
        logger.error("list_laban_orders: %s", exc)
        return []


def save_laban_order(data: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    try:
        client = _sb()
        if not client:
            return data
        if not data.get("id"):
            data["id"] = str(uuid.uuid4())
            data.setdefault("created_at", now)
            # رقم طلب تسلسلي
            if not data.get("order_number"):
                count_res = client.table("laban_orders").select("id", count="exact").execute()
                n = (count_res.count or 0) + 1
                data["order_number"] = f"LBN-{datetime.now(timezone.utc).strftime('%Y%m')}-{n:04d}"
            client.table("laban_orders").insert(data).execute()
        else:
            data["updated_at"] = now
            client.table("laban_orders").upsert(data).execute()
        return data
    except Exception as exc:
        logger.error("save_laban_order: %s", exc)
        return data


def delete_laban_order(order_id: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("laban_orders").delete().eq("id", order_id).execute()
        return True
    except Exception as exc:
        logger.error("delete_laban_order: %s", exc)
        return False


def update_laban_order_status(order_id: str, status: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("laban_orders").update({
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", order_id).execute()
        return True
    except Exception as exc:
        logger.error("update_laban_order_status: %s", exc)
        return False


# ══════════════════════════════════════════════════════════════
#  Uploads (Supabase Storage)
# ══════════════════════════════════════════════════════════════

def list_uploads(kind: str = "", q: str = "") -> list[dict]:
    """يُعيد الملفات المرفوعة — يستخدم filesystem مؤقتاً."""
    # TODO: نقل إلى Supabase Storage
    return []


def serialize_attachment(upload: dict) -> dict:
    return {
        "id":           upload.get("id", ""),
        "name":         upload.get("name", ""),
        "kind":         upload.get("kind", "file"),
        "content_type": upload.get("content_type", ""),
        "size":         upload.get("size", 0),
        "created_at":   upload.get("created_at", ""),
        "session_id":   upload.get("session_id", ""),
        "brand":        upload.get("brand", ""),
    }


def serialize_conversation_messages(msgs: list) -> list:
    return [
        {
            "id":          m.get("id", ""),
            "role":        m.get("role", ""),
            "content":     m.get("content", ""),
            "created_at":  m.get("created_at", ""),
            "attachments": m.get("attachments", []),
        }
        for m in (msgs or [])
    ]


# ══════════════════════════════════════════════════════════════
#  KB Collections (Supabase Storage buckets)
# ══════════════════════════════════════════════════════════════

def list_kb_collections() -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        res = client.table("kb_collections").select("*").execute()
        return res.data or []
    except Exception:
        return []


def create_kb_collection(name: str, description: str = "") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    col = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "document_count": 0,
        "created_at": now,
    }
    try:
        client = _sb()
        if client:
            client.table("kb_collections").insert(col).execute()
    except Exception as exc:
        logger.error("create_kb_collection: %s", exc)
    return col


def delete_kb_collection(col_id: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("kb_documents").delete().eq("collection_id", col_id).execute()
        client.table("kb_collections").delete().eq("id", col_id).execute()
        return True
    except Exception as exc:
        logger.error("delete_kb_collection: %s", exc)
        return False


def list_kb_documents(col_id: str = "", q: str = "") -> list[dict]:
    try:
        client = _sb()
        if not client:
            return []
        query = client.table("kb_documents").select("*")
        if col_id:
            query = query.eq("collection_id", col_id)
        res = query.execute()
        rows = res.data or []
        if q:
            rows = [r for r in rows if q.lower() in r.get("name", "").lower()]
        return rows
    except Exception as exc:
        logger.error("list_kb_documents: %s", exc)
        return []


def delete_kb_document(doc_id: str) -> bool:
    try:
        client = _sb()
        if not client:
            return False
        client.table("kb_documents").delete().eq("id", doc_id).execute()
        return True
    except Exception as exc:
        logger.error("delete_kb_document: %s", exc)
        return False


# Training Jobs (بسيطة — في memory)
_training_jobs: list[dict] = []


def list_training_jobs() -> list[dict]:
    return _training_jobs


def save_training_job(job: dict) -> dict:
    _training_jobs.insert(0, job)
    return job


def delete_training_job(job_id: str) -> bool:
    global _training_jobs
    before = len(_training_jobs)
    _training_jobs = [j for j in _training_jobs if j.get("id") != job_id]
    return len(_training_jobs) < before


# ── Compat shims for old API ──────────────────────────────────
def load_admin_data() -> dict:
    """Backward compat — يُعيد dict مدمج من Supabase."""
    return {
        "settings":        load_settings(),
        "conversations":   list_conversations(),
        "integrations":    list_integrations(),
        "laban_orders":    list_laban_orders(),
        "logs":            list_integration_logs(50),
        "uploads":         [],
        "kb_collections":  list_kb_collections(),
        "kb_documents":    [],
        "training_jobs":   list_training_jobs(),
    }


def save_admin_data(data: dict) -> None:
    """Backward compat — يحفظ الأجزاء المعدّلة."""
    if "settings" in data:
        save_settings(data["settings"])
