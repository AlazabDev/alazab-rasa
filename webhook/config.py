"""
webhook/config.py — Central Configuration v4.1
================================================
جميع الإعدادات والثوابت ومتغيرات البيئة.
يُحقق من المتغيرات الحرجة عند الـ import.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger("alazab.config")

# ══════════════════════════════════════════════════════════════
#  Paths
# ══════════════════════════════════════════════════════════════
BASE_DIR             = Path(__file__).resolve().parent
ROOT_DIR             = BASE_DIR.parent
STATIC_DIR           = BASE_DIR / "static"
DEFAULT_UPLOADS_DIR  = STATIC_DIR / "uploads"
FRONTEND_DIST_DIR    = ROOT_DIR / "azabot" / "dist"
FRONTEND_ASSETS_DIR  = FRONTEND_DIST_DIR / "assets"
FRONTEND_EMBED_DIR   = ROOT_DIR / "azabot" / "embed"
UPLOADS_DIR          = Path(os.getenv("UPLOADS_DIR", str(DEFAULT_UPLOADS_DIR))).expanduser()
ADMIN_DATA_FILE      = Path(
    os.getenv("ADMIN_DATA_FILE", str(ROOT_DIR / ".runtime" / "admin-data.json"))
).expanduser()
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
ADMIN_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
UPLOADS_ROOT                  = UPLOADS_DIR.resolve()
PIPER_PRONUNCIATION_LEXICON_FILE = ROOT_DIR / "piper" / "pronunciation_lexicon.yml"

# ══════════════════════════════════════════════════════════════
#  Environment
# ══════════════════════════════════════════════════════════════
_IS_PROD = os.getenv("NODE_ENV") == "production"

# ══════════════════════════════════════════════════════════════
#  Public
# ══════════════════════════════════════════════════════════════
PUBLIC_BASE_URL          = os.getenv("PUBLIC_BASE_URL", "https://bot.alazab.com").rstrip("/")
UPLOADS_PUBLIC_ENABLED   = os.getenv("UPLOADS_PUBLIC_ENABLED", "false").strip().lower() in {"1","true","yes"}
MAX_UPLOAD_BYTES         = int(os.getenv("MAX_UPLOAD_BYTES", str(12 * 1024 * 1024)))

ALLOWED_FILE_EXTENSIONS = {
    ".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx",
    ".jpg",".jpeg",".png",".webp",".gif",".txt",".csv",".zip",
}
AUDIO_FILE_EXTENSIONS        = {".mp3",".wav",".ogg",".m4a",".webm",".aac",".mp4"}
AUDIO_TRANSCRIPTION_MODEL    = os.getenv("AUDIO_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")
AUDIO_TTS_MODEL              = os.getenv("AUDIO_TTS_MODEL", "gpt-4o-mini-tts")
AUDIO_TTS_VOICE              = os.getenv("AUDIO_TTS_VOICE", "nova")

# ══════════════════════════════════════════════════════════════
#  Brand Maps
# ══════════════════════════════════════════════════════════════
BRAND_PATH_MAP: dict[str, str] = {
    "/":                  "alazab_construction",
    "/luxury-finishing":  "luxury_finishing",
    "/brand-identity":    "brand_identity",
    "/uberfix":           "uberfix",
    "/laban-alasfour":    "laban_alasfour",
}

BRAND_ALIAS_MAP: dict[str, str] = {
    "alazab":                "alazab_construction",
    "alazab-construction":   "alazab_construction",
    "alazab_construction":   "alazab_construction",
    "luxury-finishing":      "luxury_finishing",
    "luxury_finishing":      "luxury_finishing",
    "brand-identity":        "brand_identity",
    "brand_identity":        "brand_identity",
    "uberfix":               "uberfix",
    "laban-alasfour":        "laban_alasfour",
    "laban_alasfour":        "laban_alasfour",
}

BRAND_PROFILES: dict[str, dict[str, str]] = {
    "alazab_construction": {"slug": "",               "name": "Alazab Construction", "title": "عزبوت",         "subtitle": "المساعد الذكي لمجموعة العزب"},
    "luxury_finishing":    {"slug": "luxury-finishing","name": "Luxury Finishing",    "title": "لاكشري بوت",    "subtitle": "مستشار التشطيبات الراقية"},
    "brand_identity":      {"slug": "brand-identity", "name": "Brand Identity",       "title": "براند بوت",     "subtitle": "خبير الهوية البصرية وتجهيز العلامات"},
    "uberfix":             {"slug": "uberfix",        "name": "UberFix",              "title": "فيكس بوت",      "subtitle": "مستشار الصيانة والتشغيل"},
    "laban_alasfour":      {"slug": "laban-alasfour", "name": "Laban Alasfour",       "title": "مساعد العصفور", "subtitle": "مستشار التوريدات والخامات"},
}

SITE_BRAND_MAP: dict[str, str] = {
    "alazab.com":                   "alazab_construction",
    "www.alazab.com":               "alazab_construction",
    "bot.alazab.com":               "alazab_construction",
    "www.bot.alazab.com":           "alazab_construction",
    "luxury-finishing.alazab.com":  "luxury_finishing",
    "brand-identity.alazab.com":    "brand_identity",
    "uberfix.alazab.com":           "uberfix",
    "laban-alasfour.alazab.com":    "laban_alasfour",
}

# ══════════════════════════════════════════════════════════════
#  CORS
# ══════════════════════════════════════════════════════════════
_raw_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://bot.alazab.com,https://www.bot.alazab.com,http://localhost:3000",
)
ALLOWED_ORIGINS: list[str] = [
    o.strip().rstrip("/") for o in _raw_origins.split(",") 
    if o.strip() and o.strip() != "*"
]

# ══════════════════════════════════════════════════════════════
#  Supabase
# ══════════════════════════════════════════════════════════════
SUPABASE_URL              = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = (os.getenv("SUPABASE_SERVICE_ROLE_KEY","") or os.getenv("SUPABASE_SECRET_KEY","")).strip()
SUPABASE_ANON_KEY         = os.getenv("SUPABASE_ANON_KEY","").strip()

# ══════════════════════════════════════════════════════════════
#  Redis
# ══════════════════════════════════════════════════════════════
REDIS_HOST     = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT     = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None
REDIS_DB       = int(os.getenv("REDIS_DB", "0"))

# ══════════════════════════════════════════════════════════════
#  Rasa
# ══════════════════════════════════════════════════════════════
RASA_URL             = os.getenv("RASA_URL", "http://127.0.0.1:5005")
RASA_REQUEST_TIMEOUT = float(os.getenv("RASA_REQUEST_TIMEOUT", "45"))

# ══════════════════════════════════════════════════════════════
#  Meta (WhatsApp + Messenger)
# ══════════════════════════════════════════════════════════════
META_VERIFY = os.getenv("FB_VERIFY_TOKEN", "").strip()
META_SECRET = os.getenv("FB_APP_SECRET", "")
META_TOKEN  = os.getenv("FB_PAGE_ACCESS_TOKEN", "")

_PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "").strip()
_META_API_VER    = os.getenv("META_API_VERSION", "v18.0")
WA_URL   = f"https://graph.facebook.com/{_META_API_VER}/{_PHONE_NUMBER_ID}/messages" if _PHONE_NUMBER_ID else ""
WA_TOKEN = (os.getenv("WHATSAPP_TOKEN","") or os.getenv("META_TOKEN","") or os.getenv("FB_PAGE_ACCESS_TOKEN","")).strip()

# ══════════════════════════════════════════════════════════════
#  Telegram
# ══════════════════════════════════════════════════════════════
TG_TOKEN          = os.getenv("TELEGRAM_BOT_TOKEN", "")
TG_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "").strip()
TG_API_BASE       = f"https://api.telegram.org/bot{TG_TOKEN}" if TG_TOKEN else ""

# ══════════════════════════════════════════════════════════════
#  Admin
# ══════════════════════════════════════════════════════════════
ADMIN_API_KEY             = os.getenv("ADMIN_API_KEY", "")
ADMIN_EMAIL               = os.getenv("ADMIN_EMAIL", "admin@alazab.com").strip().lower()
# ✅ ADMIN_PASSWORD حُذف — يُستخدم ADMIN_PASSWORD_HASH_* في auth.py
ADMIN_SESSION_TTL_SECONDS = int(os.getenv("ADMIN_SESSION_TTL_SECONDS", str(7*24*3600)))
ADMIN_SESSION_SECRET      = os.getenv("ADMIN_SESSION_SECRET", "").strip()

# ══════════════════════════════════════════════════════════════
#  Security
# ══════════════════════════════════════════════════════════════
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").strip()

# ══════════════════════════════════════════════════════════════
#  UberFix
# ══════════════════════════════════════════════════════════════
UBERFIX_API_KEY        = os.getenv("UBERFIX_API_KEY", "")
UBERFIX_TRACK_BASE_URL = os.getenv("UBERFIX_TRACK_BASE_URL","https://uberfix.shop/track").rstrip("/")

# DB vars (للـ backward compat مع endpoints.yml)
DB_HOST     = os.getenv("DB_HOST", "")
DB_PORT     = int(os.getenv("DB_PORT", "5432"))
DB_NAME     = os.getenv("DB_NAME", "postgres")
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", os.getenv("DB_PASSWORD", ""))

UBERFIX_SERVICE_TYPES: list[dict[str, str]] = [
    {"key": "plumbing",     "label": "سباكة"},
    {"key": "electrical",   "label": "كهرباء"},
    {"key": "ac",           "label": "تكييف"},
    {"key": "painting",     "label": "دهانات"},
    {"key": "carpentry",    "label": "نجارة"},
    {"key": "cleaning",     "label": "تنظيف"},
    {"key": "general",      "label": "صيانة عامة"},
    {"key": "appliance",    "label": "أجهزة منزلية"},
    {"key": "pest_control", "label": "مكافحة حشرات"},
    {"key": "landscaping",  "label": "حدائق وتنسيق"},
    {"key": "finishing",    "label": "تشطيبات"},
    {"key": "renovation",   "label": "ترميم"},
]

# Notifications
NOTIFY_PHONE    = os.getenv("NOTIFY_PHONE", "")
NOTIFY_TG_CHAT  = os.getenv("NOTIFY_TG_CHAT_ID", "")
WEBHOOK_NOTIFY  = os.getenv("WEBHOOK_NOTIFY_URL", "")

# ══════════════════════════════════════════════════════════════
#  Admin Defaults
# ══════════════════════════════════════════════════════════════
DEFAULT_ADMIN_DATA: dict[str, Any] = {
    "settings": {
        "bot_name":               "AzaBot",
        "primary_color":          "#d6a318",
        "position":               "left",
        "welcome_message":        "مرحباً! كيف يمكنني مساعدتك؟",
        "quick_replies":          ["ما هي خدمات الشركة؟","أريد عرض سعر تشطيب","ما هي أسعار التشطيب؟","كيف أتواصل معكم؟"],
        "ai_model":               "rasa-pro",
        "system_prompt":          "Rasa Pro هو مصدر الردود الأساسي في هذا المشروع.",
        "voice_enabled":          True,
        "auto_speak":             False,
        "voice_name":             "ar-SA",
        "business_hours_enabled": False,
        "business_hours":         {"start": "09:00", "end": "18:00"},
        "offline_message":        "وصلت رسالتك خارج ساعات العمل وسنرد عليك في أقرب وقت.",
    },
    "integrations": [],
    "logs":          [],
    "conversations": [],
    "uploads":       [],
}

# ══════════════════════════════════════════════════════════════
#  Startup Validation (يُطبَع تحذير — لا يمنع التشغيل في dev)
# ══════════════════════════════════════════════════════════════
def _validate_config() -> None:
    warnings: list[str] = []
    errors:   list[str] = []

    if not ADMIN_SESSION_SECRET:
        errors.append("ADMIN_SESSION_SECRET غير مضبوط")
    elif len(ADMIN_SESSION_SECRET) < 32:
        errors.append("ADMIN_SESSION_SECRET قصير جداً (يجب ≥ 32 حرف)")

    if not SUPABASE_URL:
        warnings.append("SUPABASE_URL غير مضبوط — قاعدة البيانات لن تعمل")
    if not SUPABASE_SERVICE_ROLE_KEY:
        warnings.append("SUPABASE_SERVICE_ROLE_KEY غير مضبوط")

    if not ENCRYPTION_KEY:
        warnings.append("ENCRYPTION_KEY غير مضبوط — لن يتم تشفير بيانات Leads الحساسة")

    # تحقق من bcrypt hashes
    for env_key in ("ADMIN_PASSWORD_HASH_ADMIN","ADMIN_PASSWORD_HASH_DEVOPS","ADMIN_PASSWORD_HASH_CEO","ADMIN_PASSWORD_HASH_MOHAMED"):
        val = os.getenv(env_key, "").strip()
        if not val:
            warnings.append(f"{env_key} غير مضبوط — المستخدم معطَّل")
        elif not val.startswith("$2b$"):
            errors.append(f"{env_key} ليس bcrypt hash صحيح — شغّل: python scripts/gen_password_hash.py")

    if not REDIS_HOST:
        warnings.append("REDIS_HOST غير مضبوط — rate limiting وجلسات قد تتأثر")

    for w in warnings:
        logger.warning("[config] ⚠️  %s", w)

    if errors:
        for e in errors:
            logger.error("[config] ❌ %s", e)
        if _IS_PROD:
            logger.critical("[config] إيقاف التشغيل — أصلح الأخطاء أعلاه وأعد المحاولة")
            sys.exit(1)
        else:
            logger.warning("[config] وضع dev — الأخطاء أعلاه تمنع الإنتاج لكن لا تمنع التطوير")


_validate_config()
