"""
webhook/server.py — AzaBot Central Webhook v4.1 (إنتاج)
=========================================================
✅ /docs مغلق في الإنتاج
✅ /health عامة (status only) | /health/details للأدمن
✅ httpx.AsyncClient موحّد (connection pooling)
✅ RateLimitMiddleware مُفعَّل
✅ on_event("startup") مستبدَل بـ lifespan context manager
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
import psutil
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

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
from .middleware import RateLimitMiddleware, RequestIDMiddleware, SecurityHeadersMiddleware
from .routers import admin_router, channels_router, chat_router

# ══════════════════════════════════════════════════════════════
#  Logging
# ══════════════════════════════════════════════════════════════
_IS_PROD   = os.getenv("NODE_ENV") == "production"
_LOG_FMT   = (
    '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    if _IS_PROD else
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.basicConfig(level=logging.INFO, format=_LOG_FMT, stream=sys.stdout)
logger       = logging.getLogger("alazab.webhook")
_start_time  = time.time()

# ══════════════════════════════════════════════════════════════
#  Shared HTTP Client
# ══════════════════════════════════════════════════════════════
_http_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    if _http_client is None or _http_client.is_closed:
        raise RuntimeError("HTTP client not ready")
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
    logger.info("AzaBot Webhook أُغلق")

# ══════════════════════════════════════════════════════════════
#  App
# ══════════════════════════════════════════════════════════════
app = FastAPI(
    title="Alazab Group — Central Webhook",
    description="ويب هوك مركزي: WhatsApp · Messenger · Telegram · Website",
    version="4.1.0",
    lifespan=lifespan,
    docs_url=None   if _IS_PROD else "/docs",
    redoc_url=None  if _IS_PROD else "/redoc",
    openapi_url=None if _IS_PROD else "/openapi.json",
)

# ── Middleware (الترتيب مهم: آخر مضاف = أول مُنفَّذ) ─────────
app.add_middleware(CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# ── Static Files ──────────────────────────────────────────────
if STATIC_DIR.exists():
    # نُعرض /static لكن نحجب /static/uploads — يُخدَّم عبر route محمي
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
    logger.warning("Validation error: %s | %s", exc.errors(), request.url.path)
    return JSONResponse(422, {"detail": exc.errors()})

@app.exception_handler(HTTPException)
async def _http_err(request: Request, exc: HTTPException):
    return JSONResponse(exc.status_code, {"detail": exc.detail})

@app.exception_handler(Exception)
async def _generic_err(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", request.url.path)
    return JSONResponse(500, {"detail": "خطأ داخلي في الخادم"})

# ══════════════════════════════════════════════════════════════
#  Health Endpoints
# ══════════════════════════════════════════════════════════════
@app.get("/health", tags=["System"])
async def health():
    """فحص سريع للـ load balancer — لا يكشف تفاصيل."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/health/details", tags=["System"])
async def health_details(request: Request):
    """فحص تفصيلي — للأدمن المُصادَق فقط."""
    from .auth import verify_session
    token = ""
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        token = auth[7:].strip()
    if not token:
        token = request.cookies.get("azabot_admin_token", "")
    if not verify_session(token):
        raise HTTPException(401, "يرجى تسجيل الدخول")

    import asyncio
    rasa_ok, db_ok = await asyncio.gather(_check_rasa(), _check_db_health())
    process = psutil.Process(os.getpid())
    mem     = process.memory_info()
    uptime  = round(time.time() - _start_time)
    status  = "ok" if (rasa_ok and db_ok) else ("critical" if not rasa_ok and not db_ok else "degraded")
    return {
        "status":  status,
        "version": "4.1.0",
        "services": {"rasa": "up" if rasa_ok else "down", "database": "up" if db_ok else "down"},
        "channels": {"website": True, "whatsapp": bool(WA_TOKEN), "messenger": bool(META_TOKEN), "telegram": bool(TG_TOKEN)},
        "system":  {
            "memory_mb":      round(mem.rss / (1024 * 1024), 1),
            "cpu_percent":    psutil.cpu_percent(interval=None),
            "load_avg":       list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "uptime_seconds": uptime,
            "uptime_human":   _fmt_uptime(uptime),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ══════════════════════════════════════════════════════════════
#  UberFix Bot-Gateway
# ══════════════════════════════════════════════════════════════
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, UBERFIX_API_KEY
from .models import BotGatewayRequest

@app.post("/uberfix/bot-gateway", tags=["UberFix"])
async def uberfix_bot_gateway(request: Request, payload: BotGatewayRequest):
    from .utils import jsonable
    from ._uberfix_gateway import handle_uberfix_gateway_sync
    ctx = {
        "route": str(request.url.path),
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "origin": request.headers.get("origin"),
        "authorization": request.headers.get("authorization"),
        "x_api_key": request.headers.get("x-api-key"),
    }
    resp, status = await run_in_threadpool(handle_uberfix_gateway_sync, payload.model_dump(), ctx)
    return JSONResponse(status_code=status, content=jsonable(resp))

# ══════════════════════════════════════════════════════════════
#  Frontend SPA
# ══════════════════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse, tags=["Widget"])
async def brand_home():
    return _spa()

@app.get("/{brand_slug}", response_class=HTMLResponse, tags=["Widget"])
@app.get("/{brand_slug}/", response_class=HTMLResponse, include_in_schema=False)
async def brand_path(brand_slug: str):
    return _spa(brand_slug)

@app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def spa_fallback(full_path: str):
    return _spa(full_path)

def _spa(path: str = "") -> FileResponse:
    for idx in [FRONTEND_DIST_DIR / "index.html", STATIC_DIR / "index.html"]:
        if idx.exists():
            return FileResponse(str(idx))
    return HTMLResponse("<h1>AzaBot — Frontend not built</h1>")

# ══════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════
async def _check_rasa() -> bool:
    try:
        client = get_http_client()
        r = await client.get(f"{RASA_URL}/", timeout=3.0)
        return r.status_code == 200
    except Exception:
        return False

async def _check_db_health() -> bool:
    try:
        from supabase import create_client  # type: ignore
        url = os.getenv("SUPABASE_URL", "").strip()
        key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") or os.getenv("SUPABASE_SECRET_KEY", "")).strip()
        if not (url and key):
            return False
        client = create_client(url, key)
        client.table("bot_settings").select("id").limit(1).execute()
        return True
    except Exception:
        return False

def _fmt_uptime(s: int) -> str:
    d, r = divmod(s, 86400); h, r = divmod(r, 3600); m, s = divmod(r, 60)
    if d: return f"{d}d {h}h {m}m"
    if h: return f"{h}h {m}m"
    return f"{m}m {s}s"
