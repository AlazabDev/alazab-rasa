#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  wsl-setup.sh — إعداد WSL لـ AzaBot (نسخة مقاومة للأخطاء)
#  Ubuntu 22.04 / 24.04 | WSL2
#  الاستخدام: bash wsl-setup.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'; BOLD=$'\033[1m'; NC=$'\033[0m'

step() { printf "\n${CYAN}${BOLD}[%s/%s]${NC} %s\n" "$1" "$TOTAL_STEPS" "$2"; }
ok()   { printf "  ${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "  ${YELLOW}⚠️  %s${NC}\n" "$*"; }
info() { printf "  ${CYAN}→  %s${NC}\n" "$*"; }
fail() { printf "  ${RED}❌ %s${NC}\n" "$*" >&2; }

TOTAL_STEPS=8

# ── تحقق WSL ─────────────────────────────────────────────────
grep -qi "microsoft\|wsl" /proc/version 2>/dev/null \
  && ok "WSL2 مكتشف" \
  || warn "لا يبدو WSL — متابعة على أي حال"

# تحقق مبكر: هل المشروع على /mnt/ (Windows drive)؟
if [[ "$ROOT" == /mnt/* ]]; then
  warn "المشروع على Windows drive ($ROOT)"
  warn "إذا فشلت السكريبتات لاحقاً: انسخ المشروع لـ ~/alazab-rasa"
  warn "cp -r $ROOT ~/alazab-rasa && cd ~/alazab-rasa && bash wsl-setup.sh"
fi

# ══════════════════════════════════════════════════════════════
step "1" "إصلاح apt وتثبيت الأدوات"
# ══════════════════════════════════════════════════════════════

# أصلح cnf-update-db إذا كان مكسوراً (apt_pkg error)
if python3 -c "import apt_pkg" 2>/dev/null; then
  ok "apt_pkg سليم"
else
  warn "apt_pkg مكسور — إصلاح..."
  sudo apt-get install -y --reinstall python3-apt -qq 2>/dev/null || true
  # إذا لم يُصلح، أوقف الـ hook بدلاً من إيقاف الإعداد
  sudo chmod -x /usr/lib/cnf-update-db 2>/dev/null || true
  ok "cnf-update-db معطّل مؤقتاً"
fi

# أوقف PPAs الفاشلة قبل update
for f in /etc/apt/sources.list.d/*.list /etc/apt/sources.list.d/*.sources; do
  [[ -f "$f" ]] || continue
  if grep -q "launchpadcontent\|deadsnakes" "$f" 2>/dev/null; then
    sudo mv "$f" "${f}.disabled" 2>/dev/null || true
    warn "PPA فاشل عُطِّل: $(basename $f)"
  fi
done

# apt update — نتجاهل تحذيرات W: ونوقف فقط عند E:
if ! sudo apt-get update -qq 2>&1 | grep -E "^E:" | head -3; then
  ok "apt update اكتمل"
fi

# تثبيت الحزم الأساسية
PKGS=(
  curl wget git build-essential
  python3-venv python3-dev
  libpq-dev pkg-config
  redis-server redis-tools
  postgresql postgresql-contrib
  lsof net-tools jq dos2unix
)
sudo apt-get install -y -qq "${PKGS[@]}" 2>/dev/null
ok "الحزم الأساسية مثبّتة"

# ── اختار أفضل Python متاح ─────────────────────────────────
PYTHON_BIN=""
for pyver in python3.11 python3.12 python3.10 python3; do
  if command -v "$pyver" >/dev/null 2>&1; then
    PYTHON_BIN="$pyver"
    ok "Python: $($PYTHON_BIN --version)"
    break
  fi
done
[[ -z "$PYTHON_BIN" ]] && { fail "لا يوجد Python — أعد تثبيت Ubuntu"; exit 1; }

# إذا python3.11 غير موجود حاول تثبيته من الـ repos الرسمية
if ! command -v python3.11 >/dev/null 2>&1; then
  info "تثبيت python3.11 من repos الرسمية..."
  sudo apt-get install -y -qq python3.11 python3.11-venv python3.11-dev 2>/dev/null \
    && PYTHON_BIN=python3.11 && ok "python3.11 مثبّت" \
    || warn "python3.11 غير متاح — سنستخدم $PYTHON_BIN"
fi

# ══════════════════════════════════════════════════════════════
step "2" "تثبيت Node.js 22 + pnpm"
# ══════════════════════════════════════════════════════════════
if command -v node >/dev/null 2>&1 && [[ "$(node -v | cut -d. -f1 | tr -d 'v')" -ge 20 ]]; then
  ok "Node.js $(node -v) موجود بالفعل"
else
  info "تثبيت Node.js 22..."
  # استخدام NodeSource بدون -E (أكثر أماناً في WSL)
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash - -q 2>/dev/null || true
  sudo apt-get install -y -qq nodejs 2>/dev/null
  command -v node >/dev/null 2>&1 \
    && ok "Node.js $(node -v) مثبّت" \
    || warn "فشل تثبيت Node.js — الفرونت لن يعمل"
fi

if command -v pnpm >/dev/null 2>&1; then
  ok "pnpm $(pnpm -v) موجود"
else
  sudo npm install -g pnpm -q 2>/dev/null && ok "pnpm مثبّت" || warn "فشل تثبيت pnpm"
fi

# ══════════════════════════════════════════════════════════════
step "3" "إعداد Redis"
# ══════════════════════════════════════════════════════════════

# تشغيل Redis — يدعم systemd و service
start_redis() {
  if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
    sudo systemctl enable redis-server -q 2>/dev/null || true
    sudo systemctl start redis-server 2>/dev/null || true
  else
    sudo service redis-server start 2>/dev/null || true
  fi
}

start_redis; sleep 1
if redis-cli ping 2>/dev/null | grep -q PONG; then
  ok "Redis يعمل على 127.0.0.1:6379"
else
  warn "Redis لم يبدأ — ستحتاج تشغيله يدوياً: sudo service redis-server start"
fi

# ══════════════════════════════════════════════════════════════
step "4" "إعداد PostgreSQL"
# ══════════════════════════════════════════════════════════════

start_postgres() {
  if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
    sudo systemctl enable postgresql -q 2>/dev/null || true
    sudo systemctl start postgresql 2>/dev/null || true
  else
    sudo service postgresql start 2>/dev/null || true
  fi
}

start_postgres; sleep 2

if sudo -u postgres psql -c "SELECT 1" -q >/dev/null 2>&1; then
  ok "PostgreSQL يعمل"

  # إنشاء user
  sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='azab_user'" \
    | grep -q 1 2>/dev/null \
    || sudo -u postgres psql -c "CREATE USER azab_user WITH PASSWORD 'devpassword123';" -q

  # إنشاء database
  sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='alazab_core'" \
    | grep -q 1 2>/dev/null \
    || sudo -u postgres psql -c "CREATE DATABASE alazab_core OWNER azab_user;" -q

  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE alazab_core TO azab_user;" -q 2>/dev/null || true

  # إنشاء الجداول
  PGPASSWORD=devpassword123 psql -h 127.0.0.1 -U azab_user -d alazab_core -q << 'SQL' 2>/dev/null || true
CREATE TABLE IF NOT EXISTS leads (
  id SERIAL PRIMARY KEY, name TEXT, phone TEXT, location TEXT,
  service_type TEXT, brand TEXT, sender_id TEXT,
  created_at TEXT, source TEXT DEFAULT 'chatbot', status TEXT DEFAULT 'new'
);
CREATE TABLE IF NOT EXISTS feedback (
  id SERIAL PRIMARY KEY, sender_id TEXT, service TEXT,
  rating REAL, feedback_text TEXT, brand TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS suggestions (
  id SERIAL PRIMARY KEY, sender_id TEXT, suggestion TEXT,
  brand TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS escalation_tickets (
  id SERIAL PRIMARY KEY, sender_id TEXT, details TEXT,
  brand TEXT, status TEXT DEFAULT 'open', created_at TEXT
);
SQL
  ok "PostgreSQL: user=azab_user | db=alazab_core | 4 جداول"
else
  warn "PostgreSQL لم يبدأ — تشغيل يدوي: sudo service postgresql start"
fi

# ══════════════════════════════════════════════════════════════
step "5" "إنشاء .env للـ dev"
# ══════════════════════════════════════════════════════════════
if [[ -f "$ROOT/.env" ]]; then
  ok ".env موجود — تم تخطيه"
else
  cat > "$ROOT/.env" << 'ENVFILE'
# ── AzaBot — WSL Dev .env ─────────────────────────────────────
# ⚠️  عدّل هذين قبل التشغيل:
RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY

# Admin
ADMIN_EMAIL=admin@alazab.local
ADMIN_PASSWORD=AdminDev2024!
ADMIN_SESSION_SECRET=ZGV2c2Vzc2lvbnNlY3JldGtleWZvcnRlc3Rpbmc=

# Database (WSL local)
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=alazab_core
DB_USER=azab_user
DB_PASSWORD=devpassword123

# Redis (WSL local)
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USE_SSL=false
REDIS_DB=0
REDIS_LOCK_DB=1
REDIS_KEY_PREFIX=azabot_dev

# Rasa
RASA_URL=http://127.0.0.1:5005
ACTION_SERVER_URL=http://127.0.0.1:5055/webhook
RASA_TELEMETRY_ENABLED=false

# Frontend
ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080,http://localhost:5173
PUBLIC_BASE_URL=http://localhost:8000

# Audio
AUDIO_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
AUDIO_TTS_MODEL=gpt-4o-mini-tts
AUDIO_TTS_VOICE=nova

# Optional (فارغة في dev)
FB_VERIFY_TOKEN=dev_token
FB_APP_ID=
FB_APP_SECRET=
FB_PAGE_ACCESS_TOKEN=
WHATSAPP_TOKEN=
NOTIFY_PHONE=
WHATSAPP_API_URL=
TELEGRAM_BOT_TOKEN=
NOTIFY_TG_CHAT_ID=
UBERFIX_API_KEY=
MAINTENANCE_GETEWAY_API=

# Security
JWT_SECRET=ZGV2andzZWNyZXRrZXlmb3JhemFib3RkZXZlbG9wbWVudA==
ENCRYPTION_KEY=ZGV2ZW5jcnlwdGlvbmtleWZvcmF6YWJvdGRldg==
ADMIN_API_KEY=ZGV2YWRtaW5hcGlrZXlmb3JhemFib3Q=

# Server
NODE_ENV=development
PUBLIC_IP=127.0.0.1
LOCAL_IP=127.0.0.1

# Ports
RASA_PORT=5005
ACTIONS_PORT=5055
WEBHOOK_PORT=8000
FRONTEND_PORT=8080
ENVFILE
  ok ".env للـ dev أُنشئ"
  warn "لا تنسَ: RASA_PRO_LICENSE و OPENAI_API_KEY"
fi

# ══════════════════════════════════════════════════════════════
step "6" "Python venv + packages"
# ══════════════════════════════════════════════════════════════

# مهم: إذا كنا على /mnt/ نبني venv في home أولاً
VENV_DIR="$ROOT/.venv"
if [[ "$ROOT" == /mnt/* ]]; then
  warn "المشروع على Windows drive — venv قد يكون بطيئاً جداً"
  warn "يُنصح بنسخ المشروع لـ ~/alazab-rasa"
fi

if [[ ! -d "$VENV_DIR" ]]; then
  $PYTHON_BIN -m venv "$VENV_DIR"
  ok "venv أُنشئ ($PYTHON_BIN)"
else
  ok "venv موجود"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip setuptools wheel -q

# تثبيت المشروع
if pip install -e "$ROOT/.[dev]" -q 2>/dev/null; then
  ok "Python packages مثبّتة"
else
  warn "فشل pip install -e . — محاولة بدون [dev]..."
  pip install -e "$ROOT/." -q 2>/dev/null && ok "packages مثبّتة (بدون dev extras)" \
    || warn "فشل تثبيت packages — شغّل يدوياً: pip install -r requirements.txt"
fi

# ══════════════════════════════════════════════════════════════
step "7" "Frontend packages"
# ══════════════════════════════════════════════════════════════
if command -v pnpm >/dev/null 2>&1 && [[ -d "$ROOT/azabot" ]]; then
  info "تثبيت packages الفرونت..."
  (cd "$ROOT/azabot" && pnpm install --frozen-lockfile -s 2>/dev/null) \
    && ok "Frontend packages مثبّتة" \
    || warn "فشل pnpm install — شغّل يدوياً: cd azabot && pnpm install"
else
  warn "pnpm غير موجود أو azabot/ مفقود — تخطي"
fi

# ══════════════════════════════════════════════════════════════
step "8" "إعداد /etc/wsl.conf (execute permissions لـ /mnt/)"
# ══════════════════════════════════════════════════════════════
WSL_CONF="/etc/wsl.conf"
NEEDS_RESTART=false

if ! grep -q "metadata" "$WSL_CONF" 2>/dev/null; then
  sudo tee "$WSL_CONF" > /dev/null << 'WSLCONF'
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"

[interop]
enabled = true
appendWindowsPath = false

[boot]
systemd = true
WSLCONF
  NEEDS_RESTART=true
  ok "/etc/wsl.conf أُنشئ — يلزم restart"
else
  ok "/etc/wsl.conf جاهز"
fi

# ══════════════════════════════════════════════════════════════
# ملخص نهائي
# ══════════════════════════════════════════════════════════════
echo ""
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
printf "${GREEN}${BOLD} ✅ الإعداد اكتمل!${NC}\n"
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
echo ""

if [[ "$NEEDS_RESTART" == "true" ]]; then
  printf "  ${RED}${BOLD}مطلوب: أعد تشغيل WSL أولاً${NC}\n"
  printf "  في PowerShell:\n"
  printf "    ${CYAN}wsl --shutdown${NC}\n"
  printf "  ثم افتح WSL من جديد واكمل:\n\n"
fi

printf "  1️⃣  عدّل الـ license والـ key:\n"
printf "     ${CYAN}nano .env${NC}\n"
printf "     RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
printf "     OPENAI_API_KEY=...\n\n"
printf "  2️⃣  درّب الموديل:\n"
printf "     ${CYAN}bash scripts/botctl.sh train${NC}\n\n"
printf "  3️⃣  شغّل كل شيء:\n"
printf "     ${CYAN}bash dev.sh${NC}\n\n"
printf "  أو اختبر أولاً:\n"
printf "     ${CYAN}bash wsl-test.sh --quick${NC}\n"
echo ""
