"""
webhook/middleware.py — Security & Observability Middleware
===========================================================
SecurityHeadersMiddleware : يُضيف security headers لكل رد
RequestIDMiddleware       : يُضيف X-Request-ID لكل طلب للتتبع
"""
from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """يُضيف security headers لكل response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        h = response.headers
        h["X-Frame-Options"]           = "SAMEORIGIN"
        h["X-Content-Type-Options"]    = "nosniff"
        h["X-XSS-Protection"]          = "1; mode=block"
        h["Referrer-Policy"]           = "strict-origin-when-cross-origin"
        h["Content-Security-Policy"]   = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.openai.com;"
        )
        h["X-Powered-By"] = "AzaBot/4.0"
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    يُضيف X-Request-ID لكل طلب.
    إذا أرسل العميل X-Request-ID يُعيده، وإلا يولّد واحداً.
    يُسجّل كل طلب مع وقت الاستجابة.
    """
    import logging
    _log = logging.getLogger("alazab.webhook.requests")

    async def dispatch(self, request: Request, call_next):
        req_id = (
            request.headers.get("X-Request-ID")
            or str(uuid.uuid4())[:8]
        )
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000)

        response.headers["X-Request-ID"] = req_id

        # تسجيل كل طلب (بدون /health لأنها كثيرة)
        if request.url.path != "/health":
            self._log.info(
                "%s %s → %s | %dms | req=%s",
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
                req_id,
            )
        return response
