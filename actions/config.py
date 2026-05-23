"""
actions/config.py — إعدادات Actions Server
===========================================
جميع الـ env vars في مكان واحد.
DB_CONFIG حُذف — استخدم actions.core.db (Supabase).
"""
import os
from pathlib import Path

_ACTIONS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT  = _ACTIONS_DIR.parent

# ── Supabase (قاعدة البيانات الموحدة) ─────────────────────────
SUPABASE_URL              = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = (
    os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    or os.getenv("SUPABASE_SECRET_KEY", "")
).strip()
SUPABASE_ANON_KEY         = os.getenv("SUPABASE_ANON_KEY", "").strip()

# ── Gateway (UberFix) ─────────────────────────────────────────
GATEWAY_URL = (
    os.getenv("UBERFIX_API_URL", "")
    or os.getenv("MAINTENANCE_GATEWAY_URL", "")
    or os.getenv("UBERFIX_BOT_GATEWAY_URL", "")
).rstrip("/")

API_KEY = (
    os.getenv("MAINTENANCE_API_KEY", "")
    or os.getenv("UBERFIX_API_KEY", "")
).strip()

UBERFIX_TRACK_BASE_URL = os.getenv(
    "UBERFIX_TRACK_BASE_URL",
    os.getenv("MAINTENANCE_GATEWAY_URL_TRACK", "https://uberfix.shop/track")
).rstrip("/")

# ── Knowledge Base ────────────────────────────────────────────
PROD_DATA_PATH  = str(PROJECT_ROOT / "knowledge" / "production")
CATEGORIES_PATH = str(PROJECT_ROOT / "knowledge" / "production" / "categories")

# ── Notifications ─────────────────────────────────────────────
NOTIFY_PHONE     = os.getenv("NOTIFY_PHONE", "")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_TOKEN   = (
    os.getenv("WHATSAPP_TOKEN", "")
    or os.getenv("META_TOKEN", "")
    or os.getenv("FB_PAGE_ACCESS_TOKEN", "")
)

# ── Daftra ────────────────────────────────────────────────────
DAFTRA_SUBDOMAIN = os.getenv("DAFTRA_SUBDOMAIN", "alazab")
DAFTRA_API_KEY   = os.getenv("DAFTRA_API_KEY", "")
DAFTRA_BASE_URL  = f"https://{DAFTRA_SUBDOMAIN}.daftra.com/api2"

# ── OpenAI ────────────────────────────────────────────────────
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL       = os.getenv("OPENAI_HANDOFF_MODEL", "gpt-4o-mini")

# ── Telegram ──────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = (
    os.getenv("TELEGRAM_BOT_TOKEN", "")
    or os.getenv("TELEGRAM_TOKEN", "")
)

# ── Backward compat — يُحذف لاحقاً ───────────────────────────
# DB_CONFIG باقي فارغ لمنع ImportError في action_daftra_ops
DB_CONFIG: dict = {}

# ── Bot Gateway (موحّد — كل عمليات UberFix للبوت) ────────────
BOT_GATEWAY_URL = os.getenv(
    "BOT_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/bot-gateway"
).rstrip("/")

BOT_API_KEY = os.getenv("BOT_API_KEY", os.getenv("UBERFIX_API_KEY", "")).strip()

# maintenance-gateway (لتغيير المراحل من الخارج فقط)
MAINTENANCE_GATEWAY_URL = os.getenv(
    "MAINTENANCE_GATEWAY_URL",
    "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway"
).rstrip("/")
