#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  wsl-test.sh — اختبار شامل لكل مكونات AzaBot على WSL
#  الاستخدام: bash wsl-test.sh
#  الاستخدام المتقدم: bash wsl-test.sh --quick   (بدون rasa)
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# ── ألوان وhelpers ────────────────────────────────────────────
GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'; BOLD=$'\033[1m'; GRAY=$'\033[0;90m'; NC=$'\033[0m'

PASS=0; FAIL=0; WARN=0
QUICK="${1:-}"

pass() { ((PASS++)); printf "  ${GREEN}✅ PASS${NC}  %s\n" "$*"; }
fail() { ((FAIL++)); printf "  ${RED}❌ FAIL${NC}  %s\n" "$*"; }
warn() { ((WARN++)); printf "  ${YELLOW}⚠️  WARN${NC}  %s\n" "$*"; }
section() { echo; printf "${CYAN}${BOLD}▶ %s${NC}\n" "$*"; echo "  $(printf '─%.0s' {1..50})"; }

# ══════════════════════════════════════════════════════════════
section "1. بيئة النظام"
# ══════════════════════════════════════════════════════════════

# WSL
grep -qi "microsoft\|wsl" /proc/version 2>/dev/null \
  && pass "WSL2 detected" \
  || warn "Not WSL — running anyway"

# Python 3.11
if command -v python3.11 >/dev/null 2>&1; then
  PY_VER=$(python3.11 -V 2>&1)
  pass "Python: $PY_VER"
else
  fail "Python 3.11 not found → sudo apt install python3.11"
fi

# bash version (>= 5 for wait -n support)
BASH_MAJOR="${BASH_VERSINFO[0]}"
if [[ "$BASH_MAJOR" -ge 5 ]]; then
  pass "Bash $BASH_VERSION (wait -n supported)"
else
  warn "Bash $BASH_VERSION — wait -n not supported (أُصلح في start-backend-nodocker.sh)"
fi

# Node + pnpm
command -v node >/dev/null 2>&1 \
  && pass "Node.js $(node -v)" \
  || fail "Node.js not found → curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -"
command -v pnpm >/dev/null 2>&1 \
  && pass "pnpm $(pnpm -v)" \
  || fail "pnpm not found → npm install -g pnpm"

# dos2unix (تحقق من LF)
command -v dos2unix >/dev/null 2>&1 \
  && pass "dos2unix available" \
  || warn "dos2unix not found → sudo apt install dos2unix"

# ══════════════════════════════════════════════════════════════
section "2. ملفات المشروع"
# ══════════════════════════════════════════════════════════════

for f in .env config.yml domain.yml endpoints.yml credentials.yml \
          actions/__init__.py webhook/server.py dev.sh scripts/botctl.sh \
          azabot/package.json azabot/vite.config.ts; do
  [[ -f "$f" ]] && pass "موجود: $f" || fail "مفقود: $f"
done

# venv
[[ -d ".venv" ]] && pass ".venv موجود" || fail ".venv غير موجود → bash scripts/botctl.sh setup"

# موديل Rasa
MODEL=$(ls models/*.tar.gz 2>/dev/null | head -1 || true)
[[ -n "$MODEL" ]] \
  && pass "Rasa model: $(basename $MODEL)" \
  || warn "لا يوجد موديل → bash scripts/botctl.sh train"

# storie.yml typo check
[[ -f "data/brands/uberfix/storie.yml" ]] \
  && fail "storie.yml موجود (اسم خاطئ) — يجب حذفه" \
  || pass "stories.yml — الاسم صحيح"

# LF line endings
CRLF_FILES=$(find . -name "*.sh" -not -path "./.venv/*" | xargs file 2>/dev/null | grep CRLF | wc -l)
[[ "$CRLF_FILES" -eq 0 ]] \
  && pass "كل الـ scripts بـ LF endings" \
  || fail "$CRLF_FILES ملف بـ CRLF → dos2unix scripts/*.sh dev.sh"

# ══════════════════════════════════════════════════════════════
section "3. متغيرات البيئة .env"
# ══════════════════════════════════════════════════════════════

source_env() {
  [[ -f ".env" ]] && export $(grep -v '^#' .env | grep -v '^$' | xargs) 2>/dev/null || true
}
source_env

REQUIRED_VARS=(
  RASA_PRO_LICENSE OPENAI_API_KEY
  ADMIN_EMAIL ADMIN_PASSWORD ADMIN_SESSION_SECRET
  DB_HOST DB_PORT DB_NAME DB_USER DB_PASSWORD
  REDIS_HOST REDIS_PORT
  RASA_URL ACTION_SERVER_URL
  ALLOWED_ORIGINS PUBLIC_BASE_URL
)

OPTIONAL_VARS=(
  WHATSAPP_TOKEN TELEGRAM_BOT_TOKEN
  UBERFIX_API_KEY FB_PAGE_ACCESS_TOKEN
)

for var in "${REQUIRED_VARS[@]}"; do
  val="${!var:-}"
  if [[ -z "$val" ]]; then
    fail ".env: $var فارغ أو مفقود"
  elif [[ "$val" == REPLACE_* ]]; then
    fail ".env: $var لم يُعدَّل بعد (REPLACE_...)"
  else
    # إخفاء القيم الحساسة
    if [[ "$var" == *PASSWORD* || "$var" == *SECRET* || "$var" == *KEY* || "$var" == *LICENSE* || "$var" == *TOKEN* ]]; then
      pass ".env: $var = ${val:0:6}***"
    else
      pass ".env: $var = $val"
    fi
  fi
done

for var in "${OPTIONAL_VARS[@]}"; do
  val="${!var:-}"
  [[ -n "$val" ]] \
    && pass ".env (optional): $var مضبوط" \
    || warn ".env (optional): $var فارغ — بعض الـ notifications لن تعمل"
done

# ══════════════════════════════════════════════════════════════
section "4. قاعدة البيانات PostgreSQL"
# ══════════════════════════════════════════════════════════════

source_env
DB_H="${DB_HOST:-127.0.0.1}"; DB_P="${DB_PORT:-5432}"
DB_N="${DB_NAME:-alazab_core}"; DB_U="${DB_USER:-azab_user}"; DB_PW="${DB_PASSWORD:-}"

# PostgreSQL service
sudo service postgresql status >/dev/null 2>&1 || sudo service postgresql start 2>/dev/null || true

if command -v psql >/dev/null 2>&1; then
  if PGPASSWORD="$DB_PW" psql -h "$DB_H" -p "$DB_P" -U "$DB_U" -d "$DB_N" -c "SELECT 1" -q >/dev/null 2>&1; then
    pass "PostgreSQL: اتصال ناجح بـ $DB_N"

    # تحقق من الجداول
    TABLES=$(PGPASSWORD="$DB_PW" psql -h "$DB_H" -p "$DB_P" -U "$DB_U" -d "$DB_N" \
      -tc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'" 2>/dev/null | tr -d ' ')
    pass "PostgreSQL: $TABLES جدول موجود"
  else
    fail "PostgreSQL: فشل الاتصال → تحقق من DB_HOST/USER/PASSWORD في .env"
  fi
else
  warn "psql غير موجود — تخطي فحص DB"
fi

# ══════════════════════════════════════════════════════════════
section "5. Redis"
# ══════════════════════════════════════════════════════════════

source_env
REDIS_H="${REDIS_HOST:-127.0.0.1}"; REDIS_P="${REDIS_PORT:-6379}"
REDIS_PW="${REDIS_PASSWORD:-}"

# start redis if local
if [[ "$REDIS_H" == "127.0.0.1" || "$REDIS_H" == "localhost" ]]; then
  sudo service redis-server status >/dev/null 2>&1 || sudo service redis-server start 2>/dev/null || true
  sleep 1
fi

if command -v redis-cli >/dev/null 2>&1; then
  if [[ -n "$REDIS_PW" ]]; then
    RESULT=$(redis-cli -h "$REDIS_H" -p "$REDIS_P" -a "$REDIS_PW" ping 2>/dev/null || true)
  else
    RESULT=$(redis-cli -h "$REDIS_H" -p "$REDIS_P" ping 2>/dev/null || true)
  fi

  if [[ "$RESULT" == "PONG" ]]; then
    pass "Redis: يعمل على $REDIS_H:$REDIS_P"
    # كتابة/قراءة اختبار
    redis-cli -h "$REDIS_H" -p "$REDIS_P" ${REDIS_PW:+-a "$REDIS_PW"} SET azabot:test "ok" EX 5 >/dev/null 2>&1
    VAL=$(redis-cli -h "$REDIS_H" -p "$REDIS_P" ${REDIS_PW:+-a "$REDIS_PW"} GET azabot:test 2>/dev/null || true)
    [[ "$VAL" == "ok" ]] && pass "Redis: قراءة/كتابة ناجحة" || fail "Redis: فشل read/write"
  else
    fail "Redis: لا يستجيب → sudo service redis-server start"
  fi
else
  warn "redis-cli غير موجود — تخطي فحص Redis"
fi

# ══════════════════════════════════════════════════════════════
section "6. Python packages"
# ══════════════════════════════════════════════════════════════

VENV_PY="$ROOT/.venv/bin/python"
if [[ -f "$VENV_PY" ]]; then
  for pkg in fastapi uvicorn rasa_sdk pydantic aiohttp; do
    $VENV_PY -c "import $pkg; print($pkg.__version__)" >/dev/null 2>&1 \
      && pass "Python: $pkg installed" \
      || fail "Python: $pkg مفقود → source .venv/bin/activate && pip install -e ."
  done

  # فحص server.py syntax
  $VENV_PY -c "import ast; ast.parse(open('webhook/server.py').read()); print('ok')" >/dev/null 2>&1 \
    && pass "webhook/server.py: syntax سليم" \
    || fail "webhook/server.py: syntax error"

  # فحص actions syntax
  $VENV_PY -c "import ast; ast.parse(open('actions/action_general.py').read())" >/dev/null 2>&1 \
    && pass "actions/action_general.py: syntax سليم" \
    || fail "actions/action_general.py: syntax error"
else
  fail ".venv/bin/python غير موجود → bash wsl-setup.sh"
fi

# ══════════════════════════════════════════════════════════════
section "7. Frontend packages"
# ══════════════════════════════════════════════════════════════

if [[ -d "azabot/node_modules" ]]; then
  PKGS=$(ls azabot/node_modules | wc -l)
  pass "node_modules: $PKGS package"
else
  fail "node_modules غير موجود → cd azabot && pnpm install"
fi

# تحقق من vite config proxy
grep -q "/chat" azabot/vite.config.ts \
  && pass "vite.config.ts: proxy مضبوط" \
  || fail "vite.config.ts: proxy مفقود"

# ══════════════════════════════════════════════════════════════
section "8. منافذ الشبكة"
# ══════════════════════════════════════════════════════════════

for port in 5005 5055 8000 8080; do
  if lsof -i ":$port" >/dev/null 2>&1; then
    PROC=$(lsof -i ":$port" 2>/dev/null | awk 'NR==2{print $1}')
    warn "Port $port مشغول بـ $PROC — قد يسبب تعارض"
  else
    pass "Port $port متاح"
  fi
done

# ══════════════════════════════════════════════════════════════
section "9. اختبار تشغيل الباك اند (الخدمات)"
# ══════════════════════════════════════════════════════════════

if [[ "$QUICK" == "--quick" ]]; then
  warn "وضع --quick: تخطي اختبار تشغيل الخدمات"
else
  source_env
  source "$ROOT/.venv/bin/activate" 2>/dev/null || true

  # تشغيل Actions server
  echo "  → تشغيل Actions server..."
  nohup .venv/bin/python -m rasa_sdk.endpoint --actions actions --port 5055 \
    > /tmp/azabot_test_actions.log 2>&1 &
  ACTIONS_PID=$!

  # تشغيل Webhook server
  echo "  → تشغيل Webhook server..."
  nohup .venv/bin/python -m uvicorn webhook.server:app \
    --host 127.0.0.1 --port 8000 \
    > /tmp/azabot_test_webhook.log 2>&1 &
  WEBHOOK_PID=$!

  # انتظر وافحص
  sleep 6

  # Actions health
  if curl -fsS "http://127.0.0.1:5055/health" >/dev/null 2>&1; then
    pass "Actions server: يستجيب على :5055"
  else
    fail "Actions server: لا يستجيب → cat /tmp/azabot_test_actions.log"
    cat /tmp/azabot_test_actions.log | tail -5 | sed 's/^/     /'
  fi

  # Webhook health
  if curl -fsS "http://127.0.0.1:8000/health" >/dev/null 2>&1; then
    pass "Webhook server: يستجيب على :8000"

    # فحص أوضاع الـ API
    STATUS=$(curl -s "http://127.0.0.1:8000/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "ok")
    pass "Webhook /health: status=$STATUS"

    # فحص CORS
    CORS=$(curl -s -I -X OPTIONS "http://127.0.0.1:8000/chat/alazab" \
      -H "Origin: http://localhost:8080" 2>/dev/null | grep -i "access-control" | head -1 || true)
    [[ -n "$CORS" ]] \
      && pass "CORS headers موجودة" \
      || warn "CORS headers غير موجودة — تحقق من ALLOWED_ORIGINS"

    # فحص admin login
    LOGIN=$(curl -s -X POST "http://127.0.0.1:8000/admin/login" \
      -H "Content-Type: application/json" \
      -d "{\"email\":\"${ADMIN_EMAIL:-}\",\"password\":\"${ADMIN_PASSWORD:-}\"}" 2>/dev/null || true)
    echo "$LOGIN" | python3 -c "import sys,json; d=json.load(sys.stdin); print('token' in d)" 2>/dev/null | grep -q True \
      && pass "Admin login: يعمل ✅" \
      || fail "Admin login: فشل ← تحقق من ADMIN_EMAIL و ADMIN_PASSWORD"
  else
    fail "Webhook server: لا يستجيب → cat /tmp/azabot_test_webhook.log"
    cat /tmp/azabot_test_webhook.log | tail -10 | sed 's/^/     /'
  fi

  # إيقاف خدمات الاختبار
  kill "$ACTIONS_PID" "$WEBHOOK_PID" 2>/dev/null || true
  wait "$ACTIONS_PID" "$WEBHOOK_PID" 2>/dev/null || true
  ok "خدمات الاختبار أُوقفت"
fi

# ══════════════════════════════════════════════════════════════
section "10. فحص YAML صحة ملفات Rasa"
# ══════════════════════════════════════════════════════════════

VENV_PY="$ROOT/.venv/bin/python"
if [[ -f "$VENV_PY" ]]; then
  $VENV_PY << 'PYCHECK'
import yaml, sys
from pathlib import Path

ROOT = Path(".")
errors = []

for f in list(ROOT.glob("domain/*.yml")) + \
         list((ROOT/"data").rglob("*.yml")) + \
         [ROOT/"domain.yml", ROOT/"config.yml", ROOT/"endpoints.yml"]:
    if not f.exists(): continue
    try:
        yaml.safe_load(f.read_text())
    except yaml.YAMLError as e:
        errors.append(f"  ❌ YAML error: {f}: {e}")

if errors:
    for e in errors: print(e)
    sys.exit(1)
else:
    print(f"  ✅ كل ملفات YAML سليمة ({sum(1 for _ in ROOT.rglob('*.yml'))} ملف)")
PYCHECK
  [[ $? -eq 0 ]] && pass "YAML validation" || fail "YAML validation — راجع الأخطاء أعلاه"
else
  warn "تخطي YAML check"
fi

# ══════════════════════════════════════════════════════════════
# التقرير النهائي
# ══════════════════════════════════════════════════════════════
echo ""
printf "${BOLD}══════════════════════════════════════════════${NC}\n"
printf "${BOLD} 📊 نتائج الاختبار${NC}\n"
printf "${BOLD}══════════════════════════════════════════════${NC}\n"
printf "  ${GREEN}PASS: $PASS${NC}\n"
printf "  ${YELLOW}WARN: $WARN${NC}\n"
printf "  ${RED}FAIL: $FAIL${NC}\n"
echo ""

if [[ "$FAIL" -eq 0 ]]; then
  printf "${GREEN}${BOLD} 🎉 المشروع جاهز على WSL!${NC}\n"
  echo ""
  printf "  الخطوة التالية:\n"
  printf "  ${CYAN}bash dev.sh${NC}\n"
elif [[ "$FAIL" -le 2 ]]; then
  printf "${YELLOW}${BOLD} ⚠️  اصلح الـ $FAIL مشكلة أعلاه ثم شغّل مجدداً${NC}\n"
else
  printf "${RED}${BOLD} ❌ $FAIL مشكلة تحتاج إصلاح قبل التشغيل${NC}\n"
  printf "  جرب: ${CYAN}bash wsl-setup.sh${NC} لإعداد كل شيء تلقائياً\n"
fi

echo ""
