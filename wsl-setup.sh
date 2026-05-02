#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  wsl-setup.sh — إعداد بيئة WSL كاملة لـ AzaBot
#  Ubuntu 22.04 / WSL2
#  الاستخدام: bash wsl-setup.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'; BOLD=$'\033[1m'; NC=$'\033[0m'

step() { echo; printf "${CYAN}${BOLD}[%s]${NC} %s\n" "$1" "$2"; }
ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }
fail() { printf "${RED}❌ %s${NC}\n" "$*" >&2; exit 1; }

# ── تحقق من WSL ──────────────────────────────────────────────
if ! grep -qi "microsoft\|wsl" /proc/version 2>/dev/null; then
  warn "لا يبدو أنك في WSL — لكن الإعداد سيستمر"
fi

# ══════════════════════════════════════════════════════════════
step "1/9" "تحديث النظام وتثبيت الأدوات الأساسية"
# ══════════════════════════════════════════════════════════════
sudo apt-get update -qq
sudo apt-get install -y -qq \
  curl wget git build-essential \
  python3.11 python3.11-venv python3.11-dev \
  libpq-dev pkg-config \
  redis-server redis-tools \
  postgresql postgresql-contrib \
  lsof net-tools jq \
  dos2unix
ok "System packages installed"

# ══════════════════════════════════════════════════════════════
step "2/9" "تثبيت Node.js 22 + pnpm"
# ══════════════════════════════════════════════════════════════
if ! command -v node >/dev/null 2>&1 || [[ "$(node -v | cut -d. -f1 | tr -d 'v')" -lt 20 ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - -q
  sudo apt-get install -y -qq nodejs
  ok "Node.js $(node -v) installed"
else
  ok "Node.js $(node -v) already installed"
fi

if ! command -v pnpm >/dev/null 2>&1; then
  sudo npm install -g pnpm -q
  ok "pnpm $(pnpm -v) installed"
else
  ok "pnpm $(pnpm -v) already installed"
fi

# ══════════════════════════════════════════════════════════════
step "3/9" "إعداد Redis (للـ dev يشتغل بدون password)"
# ══════════════════════════════════════════════════════════════
sudo sed -i 's/^bind 127.0.0.1.*/bind 127.0.0.1/' /etc/redis/redis.conf
sudo sed -i 's/^# requirepass .*//' /etc/redis/redis.conf
sudo service redis-server start || sudo systemctl start redis-server 2>/dev/null || true
sleep 1
if redis-cli ping | grep -q PONG; then
  ok "Redis يعمل على 127.0.0.1:6379"
else
  warn "Redis لم يبدأ — تحقق: sudo service redis-server start"
fi

# ══════════════════════════════════════════════════════════════
step "4/9" "إعداد PostgreSQL"
# ══════════════════════════════════════════════════════════════
sudo service postgresql start || sudo systemctl start postgresql 2>/dev/null || true
sleep 2

# إنشاء user وقاعدة بيانات للتطوير
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='azab_user'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER azab_user WITH PASSWORD 'devpassword123';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='alazab_core'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE alazab_core OWNER azab_user;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE alazab_core TO azab_user;" -q
ok "PostgreSQL: user=azab_user, db=alazab_core, pass=devpassword123"

# إنشاء الجداول المطلوبة
sudo -u postgres psql -d alazab_core -c "
  CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name TEXT, phone TEXT, location TEXT, service_type TEXT,
    brand TEXT, sender_id TEXT, created_at TEXT,
    source TEXT DEFAULT 'chatbot', status TEXT DEFAULT 'new'
  );
  CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    sender_id TEXT, service TEXT, rating REAL,
    feedback_text TEXT, brand TEXT, created_at TEXT
  );
  CREATE TABLE IF NOT EXISTS suggestions (
    id SERIAL PRIMARY KEY,
    sender_id TEXT, suggestion TEXT, brand TEXT, created_at TEXT
  );
  CREATE TABLE IF NOT EXISTS escalation_tickets (
    id SERIAL PRIMARY KEY,
    sender_id TEXT, details TEXT, brand TEXT,
    status TEXT DEFAULT 'open', created_at TEXT
  );
" -q
ok "قاعدة البيانات: 4 جداول جاهزة"

# ══════════════════════════════════════════════════════════════
step "5/9" "إنشاء .env للـ WSL dev"
# ══════════════════════════════════════════════════════════════
if [[ ! -f "$ROOT/.env" ]]; then
  cat > "$ROOT/.env" << 'ENVFILE'
# ── AzaBot WSL Dev Environment ──────────────────────────────
# تم إنشاؤه بواسطة wsl-setup.sh
# ⚠️  أضف RASA_PRO_LICENSE و OPENAI_API_KEY من بياناتك الحقيقية

# ── REQUIRED: أضف هذين قبل التشغيل ──────────────────────────
RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY

# ── Admin ─────────────────────────────────────────────────────
ADMIN_EMAIL=admin@alazab.local
ADMIN_PASSWORD=AdminDev2024!
ADMIN_SESSION_SECRET=ZGV2c2Vzc2lvbnNlY3JldGtleWZvcnRlc3Rpbmc=

# ── Database (WSL local) ──────────────────────────────────────
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=alazab_core
DB_USER=azab_user
DB_PASSWORD=devpassword123

# ── Redis (WSL local, no password) ───────────────────────────
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USE_SSL=false
REDIS_DB=0
REDIS_LOCK_DB=1
REDIS_KEY_PREFIX=azabot_dev

# ── Rasa ─────────────────────────────────────────────────────
RASA_URL=http://127.0.0.1:5005
ACTION_SERVER_URL=http://127.0.0.1:5055/webhook
RASA_TELEMETRY_ENABLED=false

# ── CORS (Frontend dev port) ──────────────────────────────────
ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
PUBLIC_BASE_URL=http://localhost:8000

# ── Audio (optional in dev) ───────────────────────────────────
AUDIO_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
AUDIO_TTS_MODEL=gpt-4o-mini-tts
AUDIO_TTS_VOICE=nova

# ── Notifications (optional in dev) ──────────────────────────
FB_VERIFY_TOKEN=dev_verify_token
FB_APP_ID=
FB_APP_SECRET=
FB_PAGE_ACCESS_TOKEN=
WHATSAPP_TOKEN=
NOTIFY_PHONE=
WHATSAPP_API_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBHOOK_SECRET=
NOTIFY_TG_CHAT_ID=

# ── UberFix (optional in dev) ────────────────────────────────
UBERFIX_API_URL=https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway
UBERFIX_API_KEY=
MAINTENANCE_GETEWAY_URL=https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway
MAINTENANCE_GETEWAY_API=

# ── Security ──────────────────────────────────────────────────
JWT_SECRET=ZGV2andzZWNyZXRrZXlmb3JhemFib3RkZXZlbG9wbWVudA==
ENCRYPTION_KEY=ZGV2ZW5jcnlwdGlvbmtleWZvcmF6YWJvdGRldg==
ADMIN_API_KEY=ZGV2YWRtaW5hcGlrZXlmb3JhemFib3Q=

# ── Server ────────────────────────────────────────────────────
NODE_ENV=development
PUBLIC_IP=127.0.0.1
LOCAL_IP=127.0.0.1
HOSTNAME=wsl-dev

# ── Ports (override if conflict) ─────────────────────────────
RASA_PORT=5005
ACTIONS_PORT=5055
WEBHOOK_PORT=8000
FRONTEND_PORT=8080
ENVFILE
  ok ".env للـ WSL dev تم إنشاؤه"
  warn "⚠️  أضف RASA_PRO_LICENSE و OPENAI_API_KEY في .env"
else
  ok ".env موجود بالفعل — تم تخطيه"
fi

# ══════════════════════════════════════════════════════════════
step "6/9" "إنشاء Python venv وتثبيت packages"
# ══════════════════════════════════════════════════════════════
if [[ ! -d "$ROOT/.venv" ]]; then
  python3.11 -m venv "$ROOT/.venv"
  ok "venv أُنشئ"
else
  ok "venv موجود بالفعل"
fi

source "$ROOT/.venv/bin/activate"
pip install --upgrade pip setuptools wheel -q
pip install -e "$ROOT/.[dev]" -q
ok "Python packages installed"

# ══════════════════════════════════════════════════════════════
step "7/9" "تثبيت Frontend packages"
# ══════════════════════════════════════════════════════════════
if [[ -d "$ROOT/azabot" ]]; then
  (cd "$ROOT/azabot" && pnpm install --frozen-lockfile -s)
  ok "Frontend packages installed"
else
  warn "مجلد azabot غير موجود"
fi

# ══════════════════════════════════════════════════════════════
step "8/9" "إنشاء .wslconfig للأداء"
# ══════════════════════════════════════════════════════════════
WSLCONFIG_PATH="/mnt/c/Users/$USER/.wslconfig"
if [[ ! -f "$WSLCONFIG_PATH" ]] 2>/dev/null; then
  cat > "$ROOT/.wslconfig.recommended" << 'WSLCFG'
# .wslconfig — انسخ هذا الملف إلى: C:\Users\<اسمك>\.wslconfig
# يُحسّن أداء WSL2 لتشغيل Rasa (ثقيل على الذاكرة)
[wsl2]
memory=8GB          # الحد الأدنى المطلوب لـ Rasa Pro
processors=4        # عدد النوى
swap=4GB            # swap إضافي
localhostForwarding=true

[experimental]
autoMemoryReclaim=gradual
WSLCFG
  warn ".wslconfig.recommended أُنشئ — انسخه إلى: C:\\Users\\$USER\\.wslconfig"
else
  ok ".wslconfig موجود بالفعل في Windows"
fi

# ══════════════════════════════════════════════════════════════
step "9/9" "فحص المنافذ"
# ══════════════════════════════════════════════════════════════
CONFLICT=false
for port in 5005 5055 8000 8080; do
  if lsof -i ":$port" >/dev/null 2>&1; then
    proc=$(lsof -i ":$port" | awk 'NR==2{print $1}')
    warn "Port $port مشغول بـ $proc"
    CONFLICT=true
  else
    ok "Port $port متاح"
  fi
done

# ══════════════════════════════════════════════════════════════
echo ""
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
printf "${GREEN}${BOLD} ✅ الإعداد اكتمل!${NC}\n"
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
echo ""
echo "  الخطوات التالية:"
echo ""
echo "  1️⃣  أضف License و API Key:"
printf "     ${CYAN}nano .env${NC}\n"
echo "     ← غيّر RASA_PRO_LICENSE و OPENAI_API_KEY"
echo ""
echo "  2️⃣  درّب الموديل (مرة واحدة):"
printf "     ${CYAN}bash scripts/botctl.sh train${NC}\n"
echo ""
echo "  3️⃣  شغّل كل شيء:"
printf "     ${CYAN}bash dev.sh${NC}\n"
echo ""
echo "  ثم افتح: http://localhost:8080"
echo ""
