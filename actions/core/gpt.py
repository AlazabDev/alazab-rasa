"""
actions/core/gpt.py
====================
GPT client مركزي لجميع الـ actions.

المشكلة القديمة:
  - action_context_accumulator.py يستدعي GPT مباشرة بدون أي حماية
  - action_human_handoff.py يستدعي GPT بطريقة مختلفة
  - لا يوجد caching لأي نتيجة
  - لا يوجد rate limiting
  - لا يوجد timeout موحد

الحل:
  1. Client واحد مشترك (openai.AsyncOpenAI singleton)
  2. LRU cache للردود المتكررة (توفير tokens)
  3. Semaphore لمنع طوفان calls متزامنة
  4. Exponential backoff عند الفشل
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import os
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)

# حد أقصى للاستدعاءات المتزامنة (يمنع استهلاك rate limit دفعة واحدة)
_MAX_CONCURRENT = int(os.getenv("GPT_MAX_CONCURRENT", "5"))
_semaphore: asyncio.Semaphore | None = None

# Cache بسيط في الذاكرة: hash → نتيجة
# حجم أقصى 256 نتيجة (يُقلّل calls متكررة)
_CACHE_SIZE = 256
_cache: dict[str, str] = {}
_cache_order: list[str] = []

_DEFAULT_MODEL = os.getenv("OPENAI_HANDOFF_MODEL", "gpt-4o-mini")
_DEFAULT_TIMEOUT = float(os.getenv("GPT_TIMEOUT_SECONDS", "30"))

_client = None  # openai.AsyncOpenAI | None


def _get_semaphore() -> asyncio.Semaphore:
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(_MAX_CONCURRENT)
    return _semaphore


def _get_client():
    global _client
    if _client is None:
        try:
            from openai import AsyncOpenAI  # type: ignore
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set")
                return None
            _client = AsyncOpenAI(api_key=api_key, timeout=_DEFAULT_TIMEOUT)
        except ImportError:
            logger.error("openai package not installed")
            return None
    return _client


def _cache_key(system: str, user: str, model: str) -> str:
    raw = f"{model}|{system[:500]}|{user[:1000]}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _cache_get(key: str) -> str | None:
    return _cache.get(key)


def _cache_set(key: str, value: str) -> None:
    if len(_cache) >= _CACHE_SIZE and _cache_order:
        oldest = _cache_order.pop(0)
        _cache.pop(oldest, None)
    _cache[key] = value
    _cache_order.append(key)


async def complete(
    system_prompt: str,
    user_message: str,
    model: Optional[str] = None,
    max_tokens: int = 800,
    temperature: float = 0.3,
    use_cache: bool = True,
    retries: int = 2,
) -> str:
    """
    استدعاء GPT مع cache + rate limiting + retry.

    Args:
        system_prompt: رسالة النظام
        user_message: رسالة المستخدم
        model: اسم الموديل (افتراضي: gpt-4o-mini)
        max_tokens: حد أقصى للرد
        temperature: درجة الإبداع (0 = دقيق، 1 = إبداعي)
        use_cache: هل نُخزّن الرد في الذاكرة؟
        retries: عدد المحاولات عند الفشل

    Returns:
        نص الرد أو "" عند الفشل
    """
    _model = model or _DEFAULT_MODEL
    client = _get_client()

    if client is None:
        logger.warning("GPT client not available")
        return ""

    # فحص الـ cache أولاً
    if use_cache:
        key = _cache_key(system_prompt, user_message, _model)
        cached = _cache_get(key)
        if cached:
            logger.debug("GPT cache hit | key=%s", key[:8])
            return cached

    # تنفيذ مع semaphore لتحديد التزامن
    sem = _get_semaphore()
    for attempt in range(retries + 1):
        try:
            async with sem:
                response = await client.chat.completions.create(
                    model=_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            result = (response.choices[0].message.content or "").strip()

            # حفظ في الـ cache
            if use_cache and result:
                _cache_set(key, result)

            return result

        except Exception as exc:
            wait = 2 ** attempt
            if attempt < retries:
                logger.warning(
                    "GPT attempt %d/%d failed (%s) — retry in %ds",
                    attempt + 1, retries + 1, type(exc).__name__, wait,
                )
                await asyncio.sleep(wait)
            else:
                logger.error("GPT all attempts failed: %s", exc)
                return ""

    return ""


async def extract_json(
    system_prompt: str,
    user_message: str,
    model: Optional[str] = None,
    max_tokens: int = 600,
) -> dict:
    """
    استدعاء GPT ويُرجع dict (JSON فقط).
    عند الفشل يُرجع {} بدلاً من رفع exception.
    """
    import json
    import re

    raw = await complete(
        system_prompt=system_prompt,
        user_message=user_message,
        model=model,
        max_tokens=max_tokens,
        temperature=0.1,
        use_cache=True,
    )
    if not raw:
        return {}
    # إزالة backticks إذا أرسل الموديل ```json
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError as exc:
        logger.warning("GPT JSON parse failed: %s — raw: %s", exc, raw[:200])
        return {}


def clear_cache() -> int:
    """يُفرغ الـ cache ويُرجع عدد العناصر المحذوفة."""
    count = len(_cache)
    _cache.clear()
    _cache_order.clear()
    logger.info("GPT cache cleared (%d entries)", count)
    return count
