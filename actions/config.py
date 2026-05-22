import os
from pathlib import Path

# Central Configuration for AzaBot Actions
# ========================================

# ── Project Root ──────────────────────────────────────────────────────────────
# المسار المطلق لجذر المشروع (مجلد alazab-rasa)
# يعمل بغض النظر عن مجلد التشغيل الحالي
_ACTIONS_DIR = Path(__file__).resolve().parent          # actions/
PROJECT_ROOT  = _ACTIONS_DIR.parent                     # alazab-rasa/

# ── Supabase / Gateway Settings ───────────────────────────────────────────────
GATEWAY_URL = (
    os.getenv("UBERFIX_BOT_GATEWAY_URL", "")
    or os.getenv("MAINTENANCE_GATEWAY_URL", "")
).rstrip("/")

API_KEY = (
    os.getenv("MAINTENANCE_API_KEY", "")
    or os.getenv("UBERFIX_API_KEY", "")
    or os.getenv("AZAB_API_KEY", "")
).strip()

# ── Knowledge Base Paths (مطلقة دائماً) ──────────────────────────────────────
PROD_DATA_PATH  = str(PROJECT_ROOT / "knowledge" / "production")
CATEGORIES_PATH = str(PROJECT_ROOT / "knowledge" / "production" / "categories")

# ── Notification Settings ─────────────────────────────────────────────────────
NOTIFY_PHONE    = os.getenv("NOTIFY_PHONE", "")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_TOKEN  = os.getenv("WHATSAPP_TOKEN", "") or os.getenv("META_TOKEN", "")

# ── Daftra Accounting Settings ────────────────────────────────────────────────
DAFTRA_SUBDOMAIN = os.getenv("DAFTRA_SUBDOMAIN", "alazab")
DAFTRA_API_KEY   = os.getenv("DAFTRA_API_KEY", "")
DAFTRA_BASE_URL  = f"https://{DAFTRA_SUBDOMAIN}.daftra.com/api2"

# ── Central Database Configuration (PostgreSQL) ───────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "127.0.0.1"),
    "port":     int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "alazab_core"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}
