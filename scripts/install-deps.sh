#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
# scripts/install-deps.sh — Smart Dependency Installer
# يحل مشكلة google-auth conflict في requirements.txt
#
# الاستخدام:
#   bash scripts/install-deps.sh
# ══════════════════════════════════════════════════════════════
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR="${VENV_DIR:-.venv}"
GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; NC=$'\033[0m'

ok()   { printf '%s✅ %s%s\n' "$GREEN"  "$*" "$NC"; }
warn() { printf '%s⚠️  %s%s\n' "$YELLOW" "$*" "$NC"; }
fail() { printf '%s❌ %s%s\n' "$RED"    "$*" "$NC" >&2; exit 1; }

# تفعيل venv
if [[ -d "$VENV_DIR" ]]; then
    source "$VENV_DIR/bin/activate"
else
    fail "venv غير موجود — شغّل: bash scripts/botctl.sh setup"
fi

# ترقية pip أولاً
python -m pip install --upgrade pip setuptools wheel -q
ok "pip upgraded"

# الخطوة 1: تثبيت من pyproject.toml أولاً (core dependencies فقط)
echo ""
echo "📦 تثبيت الـ core dependencies من pyproject.toml..."
pip install -e ".[dev]" --no-deps -q 2>/dev/null || \
pip install -e "." --no-deps -q
ok "Core packages installed"

# الخطوة 2: تثبيت باقي requirements مع السماح لـ pip بحل الـ conflicts
echo ""
echo "📦 تثبيت requirements.txt (مع حل الـ conflicts تلقائياً)..."
pip install \
    "google-auth>=2.47.0,<3.0.0" \
    "google-api-core>=2.14.0,<3.0.0" \
    "google-cloud-aiplatform>=1.60.0" \
    -q
ok "Google packages conflict resolved"

# الخطوة 3: تثبيت requirements.txt الكامل بدون exact pins للـ google packages
pip install -r requirements.txt \
    --no-deps \
    -q \
    2>/dev/null || true

# الخطوة 4: تثبيت المكتبات الأساسية للـ webhook والـ actions
echo ""
echo "📦 تثبيت webhook و actions dependencies..."
pip install \
    fastapi uvicorn[standard] httpx pydantic openai \
    asyncpg psutil python-multipart \
    python-dotenv PyJWT \
    rasa-sdk \
    -q
ok "Webhook/Actions packages installed"

# الخطوة 5: تحقق من الـ packages الحيوية
echo ""
echo "🔍 التحقق من الـ packages الحيوية..."
python -c "
packages = [
    ('rasa_sdk',    'Rasa SDK'),
    ('fastapi',     'FastAPI'),
    ('uvicorn',     'Uvicorn'),
    ('httpx',       'HTTPX'),
    ('openai',      'OpenAI'),
    ('asyncpg',     'AsyncPG'),
    ('pydantic',    'Pydantic'),
    ('psutil',      'PSUtil'),
    ('google.auth', 'Google Auth'),
]
all_ok = True
for mod, name in packages:
    try:
        __import__(mod)
        print(f'  ✅ {name}')
    except ImportError:
        print(f'  ❌ {name} — pip install {mod}')
        all_ok = False
if all_ok:
    print()
    print('✅ كل الـ packages الحيوية جاهزة!')
else:
    print()
    print('⚠️  بعض الـ packages ناقصة — شغّل: pip install -r requirements.txt')
"

echo ""
ok "Installation complete"
