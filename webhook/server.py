"""
webhook/server.py — AzaBot Central Webhook v4.1
=================================================
✅ lifespan context manager (بدل on_event deprecated)
✅ httpx.AsyncClient موحّد (connection pooling)
✅ /docs مغلق في الإنتاج
✅ /health عامة (status only)
✅ /health/details للأدمن مع metrics
✅ RateLimitMiddleware + SecurityHeadersMiddleware + RequestIDMiddleware
"""
from __future__ import annotations

import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from .config import (
    ALLOWED_ORIGINS, FRONTEND_ASSETS_DIR, FRONTEND_DIST_DIR,
    FRONTEND_EMBED_DIR, META_TOKEN, RASA_URL,
    STATIC_DIR, TG_TOKEN, WA_TOKEN,
)
from .middleware import RateLimitMiddleware, RequestIDMiddleware, SecurityHeadersMiddleware
from .routers import admin_router, channels_router, chat_router

# ── Logging ───────────────────────────────────────────────────
_IS_PROD  = os.getenv("NODE_ENV") == "production"
_LOG_FMT  = (
    '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    if _IS_PROD else
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.basicConfig(level=logging.INFO, format=_LOG_FMT, stream=sys.stdout)
logger      = logging.getLogger("alazab.webhook")
_start_time = time.time()

# ══════════════════════════════════════════════════════════════
#  Shared HTTP Client
# ══════════════════════════════════════════════════════════════
_http_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    """يُعيد الـ AsyncClient الموحّد — استخدمه في كل الـ services."""
    if _http_client is None or _http_client.is_closed:
        raise RuntimeError("HTTP client not initialized")
    return _http_client


# ══════════════════════════════════════════════════════════════
#  Lifespan
# ══════════════════════════════════════════════════════════════
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _http_client
    _http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0, connect=5.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        follow_redirects=False,
    )
    logger.info("AzaBot Webhook v4.1 بدأ | prod=%s | RASA=%s", _IS_PROD, RASA_URL)
    logger.info("قنوات: WA=%s | TG=%s | META=%s", bool(WA_TOKEN), bool(TG_TOKEN), bool(META_TOKEN))
    yield
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
    logger.info("AzaBot Webhook أُغلق بشكل نظيف")


# ══════════════════════════════════════════════════════════════
#  App
# ══════════════════════════════════════════════════════════════
app = FastAPI(
    title="Alazab Group — Central Webhook",
    version="4.1.0",
    lifespan=lifespan,
    docs_url=None    if _IS_PROD else "/docs",
    redoc_url=None   if _IS_PROD else "/redoc",
    openapi_url=None if _IS_PROD else "/openapi.json",
)

# ── Middleware (الترتيب: آخر مضاف = أول مُنفَّذ) ──────────────
app.add_middleware(CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# ── Static Files — يُعرض /static/widget فقط ──────────────────
# /static/uploads يُخدَّم عبر /admin/uploads/{id}/download فقط
_widget_dir = STATIC_DIR / "widget"
_admin_dir  = STATIC_DIR / "admin"
if _widget_dir.exists():
    app.mount("/static/widget", StaticFiles(directory=str(_widget_dir)), name="widget")
if _admin_dir.exists():
    app.mount("/static/admin", StaticFiles(directory=str(_admin_dir)), name="admin_static")
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
async def _validation_err(request: Request, exc: RequestValidationError):
    logger.warning("Validation error | %s | %s", request.url.path, exc.errors())
    return JSONResponse(422, {"detail": exc.errors()})


@app.exception_handler(HTTPException)
async def _http_err(request: Request, exc: HTTPException):
    return JSONResponse(exc.status_code, {"detail": exc.detail})


@app.exception_handler(Exception)
async def _generic_err(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    # لا نكشف stack trace للعميل
    return JSONResponse(500, {"detail": "خطأ داخلي في الخادم"})


# ══════════════════════════════════════════════════════════════
#  Health Endpoints
# ══════════════════════════════════════════════════════════════
@app.get("/health", tags=["System"])
async def health():
    """
    فحص سريع للـ load balancer.
    لا يكشف تفاصيل — للعموم.
    """
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/health/details", tags=["System"])
async def health_details(request: Request):
    """
    فحص تفصيلي لجميع الخدمات + metrics.
    للأدمن المُصادَق فقط.
    """
    from .routers.admin import _require_admin
    from .services.monitoring.health import full_health_check
    from .services.monitoring import metrics as _m

    user = _require_admin(request)

    result = await full_health_check(RASA_URL)
    result["metrics"]   = _m.snapshot()
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return result


# ══════════════════════════════════════════════════════════════
#  UberFix Bot Gateway
# ══════════════════════════════════════════════════════════════
from .models import BotGatewayRequest


@app.post("/uberfix/bot-gateway", tags=["UberFix"])
async def uberfix_bot_gateway(request: Request, payload: BotGatewayRequest):
    from ._uberfix_gateway import handle_uberfix_gateway_sync
    from .utils import jsonable

    ctx = {
        "route":         str(request.url.path),
        "client_ip":     request.client.host if request.client else None,
        "user_agent":    request.headers.get("user-agent"),
        "origin":        request.headers.get("origin"),
        "authorization": request.headers.get("authorization"),
        "x_api_key":     request.headers.get("x-api-key"),
    }
    resp, status = await run_in_threadpool(handle_uberfix_gateway_sync, payload.model_dump(), ctx)
    return JSONResponse(status_code=status, content=jsonable(resp))


# ══════════════════════════════════════════════════════════════
#  Frontend SPA
# ══════════════════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse, tags=["Widget"])
async def root():
    return _spa_response()


@app.get("/{brand_slug}", response_class=HTMLResponse, tags=["Widget"])
@app.get("/{brand_slug}/", response_class=HTMLResponse, include_in_schema=False)
async def brand_page(brand_slug: str):
    return _spa_response()


@app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def spa_fallback(full_path: str):
    return _spa_response()


def _spa_response():
    for idx in (FRONTEND_DIST_DIR / "index.html", STATIC_DIR / "index.html"):
        if idx.exists():
            return FileResponse(str(idx))
    return HTMLResponse("<h1>AzaBot — يرجى بناء الفرونت: pnpm build</h1>", status_code=503)
