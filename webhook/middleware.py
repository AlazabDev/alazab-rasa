"""
webhook/middleware.py — Security, Rate Limiting & Observability v4.1
=====================================================================
✅ RateLimitMiddleware  — Redis sliding-window, /chat/* + /admin/login
✅ SecurityHeadersMiddleware — HSTS · CSP nonce · no X-Powered-By
✅ RequestIDMiddleware  — X-Request-ID · metrics · request logging
"""
from __future__ import annotations

import hashlib
import logging
import os
import secrets
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .services.monitoring import metrics as _metrics

logger = logging.getLogger("alazab.webhook")

# ── Rate Limit Config ─────────────────────────────────────────
_RATE_LIMITS: dict[str, tuple[int, int]] = {
    "/chat/tts":    (10,  60),
    "/chat/audio":  (10,  60),
    "/chat/upload": (20,  60),
    "/chat":        (30,  60),
    "/admin/login": (10, 300),
}


def _redis_client():
    try:
        import redis  # type: ignore
        return redis.Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD") or None,
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
    except Exception:
        return None


def _get_client_ip(request: Request) -> str:
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    real = request.headers.get("X-Real-IP", "")
    if real:
        return real.strip()
    return request.client.host if request.client else "unknown"


def _rate_check(ip: str, path: str) -> tuple[bool, int, int]:
    """يُعيد (allowed, remaining, retry_after)."""
    prefix = next(
        (p for p in sorted(_RATE_LIMITS, key=len, reverse=True) if path.startswith(p)),
        None,
    )
    if not prefix:
        return True, 999, 0

    max_req, window = _RATE_LIMITS[prefix]
    r = _redis_client()
    if r is None:
        return True, max_req, 0

    ip_hash = hashlib.md5(ip.encode(), usedforsecurity=False).hexdigest()[:12]
    bucket  = int(time.time()) // window
    key     = f"rl:{ip_hash}:{prefix.replace('/','_')}:{bucket}"
    try:
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, window * 2)
        count = pipe.execute()[0]
    except Exception as exc:
        logger.warning("Rate-limit Redis error: %s", exc)
        return True, max_req, 0

    if count > max_req:
        retry = window - (int(time.time()) % window)
        return False, 0, retry
    return True, max(0, max_req - count), 0


# ══════════════════════════════════════════════════════════════
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not any(path.startswith(p) for p in _RATE_LIMITS):
            return await call_next(request)

        ip = _get_client_ip(request)
        allowed, remaining, retry = _rate_check(ip, path)

        if not allowed:
            logger.warning("Rate limit exceeded | ip=%s path=%s", ip, path)
            return JSONResponse(
                status_code=429,
                content={"detail": "طلبات كثيرة — انتظر قليلاً وحاول مجدداً"},
                headers={"Retry-After": str(retry), "X-RateLimit-Remaining": "0"},
            )
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    _IS_PROD = os.getenv("NODE_ENV") == "production"

    async def dispatch(self, request: Request, call_next):
        nonce = secrets.token_urlsafe(16)
        request.state.csp_nonce = nonce

        response = await call_next(request)
        h = response.headers

        h["X-Frame-Options"]        = "DENY"
        h["X-Content-Type-Options"] = "nosniff"
        h["X-XSS-Protection"]       = "0"
        h["Referrer-Policy"]        = "strict-origin-when-cross-origin"
        h["Permissions-Policy"]     = "geolocation=(), microphone=(self), camera=()"

        if self._IS_PROD:
            h["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        h["Content-Security-Policy"] = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://fonts.googleapis.com; "
            f"style-src 'self' 'nonce-{nonce}' https://fonts.googleapis.com; "
            f"font-src 'self' https://fonts.gstatic.com; "
            f"img-src 'self' data: https:; "
            f"connect-src 'self' https://api.openai.com; "
            f"frame-ancestors 'none';"
        )
        # ❌ بدون X-Powered-By — لا إفصاح عن التقنية
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    _log = logging.getLogger("alazab.webhook.requests")
    _SKIP = {"/health", "/favicon.ico", "/robots.txt"}

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
        start  = time.perf_counter()

        response = await call_next(request)

        latency_ms = (time.perf_counter() - start) * 1000
        is_error   = response.status_code >= 400
        response.headers["X-Request-ID"] = req_id

        path = request.url.path
        if path not in self._SKIP:
            # تسجيل الطلب
            level = logging.WARNING if is_error else logging.INFO
            self._log.log(
                level,
                "%s %s → %s | %.1fms | ip=%s | req=%s",
                request.method, path,
                response.status_code,
                latency_ms,
                _get_client_ip(request),
                req_id,
            )
            # تسجيل المقاييس
            _metrics.inc_endpoint(path, round(latency_ms, 1), is_error)

        return response
