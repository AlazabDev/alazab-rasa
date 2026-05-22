"""
actions/core/db.py
==================
Connection pool مركزي لجميع الـ actions.

المشكلة القديمة:
  كل action كانت تفتح connection جديد وتغلقه
  → بطء، وضياع connections عند ضغط عالي

الحل:
  asyncpg Pool واحد يُنشأ مرة وحدة، يُعاد استخدامه
  بحد أقصى 10 connections موازية
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

logger = logging.getLogger(__name__)

_pool = None  # asyncpg.Pool | None


async def get_pool():
    """يُنشئ الـ pool عند أول استخدام (lazy init)."""
    global _pool
    if _pool is not None:
        return _pool
    try:
        import asyncpg  # type: ignore

        from ..config import DB_CONFIG

        _pool = await asyncpg.create_pool(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            min_size=2,
            max_size=10,
            command_timeout=15,
        )
        logger.info("DB pool created (min=2, max=10)")
    except Exception as exc:
        logger.error("DB pool creation failed: %s", exc)
        _pool = None
    return _pool


@asynccontextmanager
async def acquire() -> AsyncGenerator[Any, None]:
    """Context manager يُعطي connection من الـ pool."""
    pool = await get_pool()
    if pool is None:
        raise RuntimeError("Database pool is not available")
    async with pool.acquire() as conn:
        yield conn


async def insert(table: str, data: dict) -> bool:
    """
    INSERT صف واحد في الجدول المحدد.
    يُرجع True عند النجاح، False عند الفشل.

    مثال:
        await insert("leads", {"name": "أحمد", "phone": "01012345678"})
    """
    if not data:
        logger.warning("insert(%s): empty data dict — skipped", table)
        return False

    # تأكد من أن الأعمدة safe (لا SQL injection)
    cols = ", ".join(f'"{k}"' for k in data.keys())
    placeholders = ", ".join(f"${i + 1}" for i in range(len(data)))
    query = f'INSERT INTO "{table}" ({cols}) VALUES ({placeholders})'

    try:
        async with acquire() as conn:
            await conn.execute(query, *data.values())
        return True
    except Exception as exc:
        logger.error("DB insert error [%s]: %s", table, exc)
        return False


async def fetch_one(query: str, *args) -> dict | None:
    """
    تُنفّذ SELECT وتُرجع أول صف كـ dict أو None.

    مثال:
        row = await fetch_one("SELECT * FROM leads WHERE phone=$1", "01012345678")
    """
    try:
        async with acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    except Exception as exc:
        logger.error("DB fetch_one error: %s", exc)
        return None


async def fetch_all(query: str, *args) -> list[dict]:
    """
    تُنفّذ SELECT وتُرجع كل الصفوف كـ list[dict].
    """
    try:
        async with acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(r) for r in rows]
    except Exception as exc:
        logger.error("DB fetch_all error: %s", exc)
        return []


async def close_pool() -> None:
    """يُغلق الـ pool عند إيقاف الخادم (اختياري)."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("DB pool closed")
