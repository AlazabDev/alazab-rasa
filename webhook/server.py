"""
webhook/server.py — AzaBot Central Webhook v4.0
=================================================
مجموعة العزب | Alazab Group Chatbot

[v4.0] إعادة هيكلة كاملة — من 3649 سطر إلى بنية نظيفة:

  server.py          ← نقطة الدخول فقط (app creation + startup + health)
  routers/admin.py   ← /admin/*
  routers/chat.py    ← /chat, /chat/upload, /chat/audio, /chat/tts
  routers/channels.py ← /webhook/meta, /webhook/telegram, /brands, /lead
  services/          ← طبقة الخدمات (admin_data, audio, channels, integrations, ...)

Architecture:
  ┌──────────────────────────────────────────────┐
  │           INCOMING CHANNELS                  │
  │  Website · WhatsApp · Messenger · Telegram   │
  └─────────────────┬────────────────────────────┘
                    │
             ┌──────▼──────┐
             │  server.py  │ ← app + middleware + health
             └──────┬──────┘
          ┌─────────┼─────────┐
    routers/    routers/   routers/
    admin.py    chat.py    channels.py
          └─────────┼─────────┘
                    │
              services/          ← admin_data, audio, channels,
              integrations,         notifications, rasa_client,
              uploads              uploads
"""
from __future__ import annotations

import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
import psutil
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from .config import (
    ALLOWED_ORIGINS,
    FRONTEND_ASSETS_DIR,
    FRONTEND_DIST_DIR,
    FRONTEND_EMBED_DIR,
    META_TOKEN,
    RASA_URL,
    STATIC_DIR,
    TG_TOKEN,
    WA_TOKEN,
    WA_URL,
)
from .middleware import SecurityHeadersMiddleware, RequestIDMiddleware
from .routers import admin_router, channels_router, chat_router
from .services.admin_data import admin_stats_payload

# ══════════════════════════════════════════════════════════════
#  Logging
# ══════════════════════════════════════════════════════════════
_LOG_FORMAT = (
    '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    if os.getenv("NODE_ENV") == "production"
    else "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT, stream=sys.stdout)
logger = logging.getLogger("alazab.webhook")

_start_time = time.time()

# ══════════════════════════════════════════════════════════════
#  App
# ══════════════════════════════════════════════════════════════
app = FastAPI(
    title="Alazab Group — Central Webhook",
    description="ويب هوك مركزي: WhatsApp · Messenger · Telegram · Website",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ────────────────────────────────────────────────
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files ──────────────────────────────────────────────
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if FRONTEND_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_ASSETS_DIR)), name="assets")
if FRONTEND_EMBED_DIR.exists():
    app.mount("/embed", StaticFiles(directory=str(FRONTEND_EMBED_DIR)), name="embed")

# ── Routers ───────────────────────────────────────────────────
app.include_router(admin_router)
app.include_router(chat_router)
app.include_router(channels_router)

# ══════════════════════════════════════════════════════════════
#  Error Handlers
# ══════════════════════════════════════════════════════════════
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error: %s | path=%s", exc.errors(), request.url.path)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(exc.body)[:200] if exc.body else None},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "خطأ داخلي في الخادم"})


# ══════════════════════════════════════════════════════════════
#  System Endpoints
# ══════════════════════════════════════════════════════════════
@app.get("/health", tags=["System"])
async def health():
    """
    فحص صحة جميع الخدمات.
    يُستخدم من load balancer وmonitoring systems.
    """
    import asyncio

    async def _check_rasa() -> bool:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f"{RASA_URL}/")
            return r.status_code == 200
        except Exception:
            return False

    # فحص متوازي لتسريع الاستجابة
    rasa_ok, db_ok = await asyncio.gather(
        _check_rasa(),
        _check_db_health(),
        return_exceptions=False,
    )

    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    uptime = round(time.time() - _start_time)

    channels = {
        "website":   True,
        "whatsapp":  bool(WA_URL and WA_TOKEN),
        "messenger": bool(META_TOKEN),
        "telegram":  bool(TG_TOKEN),
    }
    active_channels = sum(channels.values())

    # degraded = رسا أو DB واقع | ok = كل شيء شغال
    if rasa_ok and db_ok:
        status = "ok"
    elif not rasa_ok and not db_ok:
        status = "critical"
    else:
        status = "degraded"

    return {
        "status":   status,
        "version":  "4.0.0",
        "services": {
            "rasa":     "up" if rasa_ok else "down",
            "database": "up" if db_ok  else "down",
        },
        "channels": {**channels, "_active_count": active_channels},
        "system": {
            "memory_mb":   round(mem.rss / (1024 * 1024), 1),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "load_avg":    list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "uptime_seconds": uptime,
            "uptime_human":   _fmt_uptime(uptime),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _fmt_uptime(seconds: int) -> str:
    d, r = divmod(seconds, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m"
    return f"{m}m {s}s"


# ══════════════════════════════════════════════════════════════
#  UberFix Bot-Gateway
#  (ثقيل جداً — يبقى هنا بشكل مؤقت حتى ينتقل لـ router منفصل)
# ══════════════════════════════════════════════════════════════
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, UBERFIX_API_KEY
from .models import BotGatewayRequest
from starlette.concurrency import run_in_threadpool

@app.post("/uberfix/bot-gateway", tags=["UberFix"])
async def uberfix_bot_gateway(request: Request, payload: BotGatewayRequest):
    """بوابة UberFix المحلية لعزبوت."""
    from .utils import jsonable
    from ._uberfix_gateway import handle_uberfix_gateway_sync

    request_context = {
        "route": str(request.url.path),
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "origin": request.headers.get("origin"),
        "authorization": request.headers.get("authorization"),
        "x_api_key": request.headers.get("x-api-key"),
    }
    response_payload, status_code = await run_in_threadpool(
        handle_uberfix_gateway_sync,
        payload.model_dump(),
        request_context,
    )
    return JSONResponse(status_code=status_code, content=jsonable(response_payload))


# ══════════════════════════════════════════════════════════════
#  Frontend SPA
# ══════════════════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse, tags=["Widget"])
async def brand_home():
    return _frontend_response()


@app.get("/{brand_slug}", response_class=HTMLResponse, tags=["Widget"])
@app.get("/{brand_slug}/", response_class=HTMLResponse, include_in_schema=False)
async def brand_path(brand_slug: str):
    return _frontend_response(brand_slug)


@app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def spa_fallback(full_path: str):
    return _frontend_response(full_path)


def _frontend_response(path: str = "") -> FileResponse:
    index = FRONTEND_DIST_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    static_index = STATIC_DIR / "index.html"
    if static_index.exists():
        return FileResponse(str(static_index))
    return HTMLResponse("<h1>AzaBot — Frontend not built</h1>", status_code=200)


# ══════════════════════════════════════════════════════════════
#  Startup / Shutdown
# ══════════════════════════════════════════════════════════════
@app.on_event("startup")
async def on_startup():
    logger.info("AzaBot Webhook v4.0 starting up")
    logger.info("RASA_URL=%s | WA=%s | TG=%s", RASA_URL, bool(WA_URL), bool(TG_TOKEN))


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("AzaBot Webhook shutting down")


# ══════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════
async def _check_db_health() -> bool:
    if not all([DB_HOST, DB_NAME, DB_USER]):
        return False
    try:
        import asyncpg
        conn = await asyncpg.connect(
            host=DB_HOST, port=DB_PORT,
            database=DB_NAME, user=DB_USER, password=DB_PASSWORD,
            timeout=3,
        )
        await conn.fetchval("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False
