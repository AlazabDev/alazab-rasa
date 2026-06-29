"""
actions/core/db.py — Supabase Database Layer
=============================================
قاعدة بيانات موحدة: Supabase (PostgreSQL Cloud).

الاستخدام:
    from actions.core.db import sb, insert, fetch_one, fetch_all, upsert

جداول Supabase المستخدمة:
    conversations       محادثات البوت
    messages            رسائل كل محادثة
    maintenance_requests طلبات الصيانة (UberFix)
    integrations        التكاملات الخارجية
    webhook_logs        سجل التكاملات
    bot_settings        إعدادات البوت
    leads               العملاء المحتملين (جدول مضاف)
    laban_orders        طلبات Laban (جدول مضاف)
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)

_client = None


def _sb():
    """Supabase client singleton — service_role للعمليات server-side."""
    global _client
    if _client is not None:
        return _client
    try:
        from supabase import create_client  # type: ignore
        url = os.getenv("SUPABASE_URL", "").strip()
        key = (
            os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
            or os.getenv("SUPABASE_SECRET_KEY", "")
        ).strip()
        if not (url and key):
            logger.warning("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set")
            return None
        _client = create_client(url, key)
    except Exception as exc:
        logger.error("Supabase client init failed: %s", exc)
    return _client


# ── Public alias ─────────────────────────────────────────────
def sb():
    """يُعيد Supabase client — يُستخدم في الكود مباشرة."""
    return _sb()


# ── CRUD Helpers ─────────────────────────────────────────────

async def insert(table: str, data: dict) -> bool:
    """INSERT صف واحد في Supabase."""
    if not data:
        return False
    try:
        client = _sb()
        if not client:
            return False
        client.table(table).insert(data).execute()
        return True
    except Exception as exc:
        logger.error("Supabase insert [%s]: %s", table, exc)
        return False


async def upsert(table: str, data: dict, on_conflict: str = "id") -> bool:
    """INSERT or UPDATE في Supabase."""
    if not data:
        return False
    try:
        client = _sb()
        if not client:
            return False
        client.table(table).upsert(data, on_conflict=on_conflict).execute()
        return True
    except Exception as exc:
        logger.error("Supabase upsert [%s]: %s", table, exc)
        return False


async def fetch_one(table: str, filters: dict) -> Optional[dict]:
    """SELECT صف واحد بـ filter."""
    try:
        client = _sb()
        if not client:
            return None
        query = client.table(table).select("*")
        for k, v in filters.items():
            query = query.eq(k, v)
        res = query.limit(1).execute()
        return res.data[0] if res.data else None
    except Exception as exc:
        logger.error("Supabase fetch_one [%s]: %s", table, exc)
        return None


async def fetch_all(table: str, filters: Optional[dict] = None,
                    order: Optional[str] = None, limit: int = 500) -> list[dict]:
    """SELECT قائمة من Supabase."""
    try:
        client = _sb()
        if not client:
            return []
        query = client.table(table).select("*")
        for k, v in (filters or {}).items():
            query = query.eq(k, v)
        if order:
            query = query.order(order, desc=True)
        res = query.limit(limit).execute()
        return res.data or []
    except Exception as exc:
        logger.error("Supabase fetch_all [%s]: %s", table, exc)
        return []


async def update(table: str, filters: dict, data: dict) -> bool:
    """UPDATE صفوف بـ filter."""
    if not data:
        return False
    try:
        client = _sb()
        if not client:
            return False
        query = client.table(table).update(data)
        for k, v in filters.items():
            query = query.eq(k, v)
        query.execute()
        return True
    except Exception as exc:
        logger.error("Supabase update [%s]: %s", table, exc)
        return False


async def delete(table: str, filters: dict) -> bool:
    """DELETE صفوف بـ filter."""
    try:
        client = _sb()
        if not client:
            return False
        query = client.table(table).delete()
        for k, v in filters.items():
            query = query.eq(k, v)
        query.execute()
        return True
    except Exception as exc:
        logger.error("Supabase delete [%s]: %s", table, exc)
        return False


def rpc(function_name: str, params: dict) -> Any:
    """استدعاء Supabase RPC (stored procedure)."""
    try:
        client = _sb()
        if not client:
            return None
        res = client.rpc(function_name, params).execute()
        return res.data
    except Exception as exc:
        logger.error("Supabase rpc [%s]: %s", function_name, exc)
        return None
