#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  azabot-doctor.sh — فحص بيئة AzaBot وإصلاحها
#  الاستخدام:
#    bash azabot-doctor.sh          ← فحص فقط
#    bash azabot-doctor.sh --fix    ← فحص + إصلاح تلقائي
#    bash azabot-doctor.sh --quiet  ← نتائج فقط (بدون تفاصيل)
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# ── CLI args ──────────────────────────────────────────────────
FIX=false; QUIET=false; SECTION=""
for arg in "$@"; do
  case "$arg" in
    --fix)     FIX=true  ;;
    --quiet)   QUIET=true ;;
    --fix-env) # إصلاح CRLF في .env قبل أي شيء
      if [[ -f ".env" ]]; then
        sed -i 's/\r$//' .env
        echo "✅ .env: تم إزالة CRLF (\\r)"
      fi
      exit 0
      ;;
    --tools|--env|--paths|--api|--all) SECTION="$arg" ;;
  esac
done
[[ -z "$SECTION" ]] && SECTION="--all"

# ── ألوان ─────────────────────────────────────────────────────
G=$'\033[1;32m'; R=$'\033[1;31m'; Y=$'\033[1;33m'
C=$'\033[1;36m'; B=$'\033[1m';    D=$'\033[0;90m'; N=$'\033[0m'

# ── متغيرات عدّادة ────────────────────────────────────────────
PASS=0; FAIL=0; WARN=0; FIXED=0

# ── helpers ───────────────────────────────────────────────────
pass()  { PASS=$((PASS+1)); $QUIET || printf "  ${G}✅ PASS${N}  %s\n" "$*"; }
fail()  { FAIL=$((FAIL+1));          printf "  ${R}❌ FAIL${N}  %s\n" "$*"; }
warn()  { WARN=$((WARN+1)); $QUIET || printf "  ${Y}⚠️  WARN${N}  %s\n" "$*"; }
fixed() { FIXED=$((FIXED+1));         printf "  ${C}🔧 FIXED${N} %s\n" "$*"; }
info()  { $QUIET || printf "  ${D}ℹ  %s${N}\n" "$*"; }
section(){ printf "\n${B}${C}▶  %s${N}\n  %s\n" "$1" "$(printf '─%.0s' {1..55})"; }

# ── تحميل .env ───────────────────────────────────────────────
load_env() {
  if [[ -f "$ROOT/.env" ]]; then
    # ── إزالة \r (CRLF) قبل التحميل ──────────────────────
    ENV_CLEAN=$(grep -v '^\s*#' "$ROOT/.env" | grep -v '^\s*$' | sed 's/\r$//')
    set -a
    # shellcheck disable=SC1090
    source <(echo "$ENV_CLEAN")
    set +a
  fi
}
load_env

# ══════════════════════════════════════════════════════════════
# SECTION 1: الأدوات المطلوبة
# ══════════════════════════════════════════════════════════════
check_tools() {
  section "1/4  الأدوات المطلوبة"

  # ── Python ─────────────────────────────────────────────────
  REQUIRED_PY="3.11"
  PYTHON_BIN=""
  for py in python3.11 python3.12 python3.10 python3; do
    command -v "$py" &>/dev/null && { PYTHON_BIN="$py"; break; }
  done

  if [[ -z "$PYTHON_BIN" ]]; then
    fail "Python غير موجود"
    if $FIX; then
      info "تثبيت Python 3.11..."
      sudo apt-get install -y python3.11 python3.11-venv python3.11-dev -qq 2>/dev/null \
        && PYTHON_BIN=python3.11 && fixed "Python 3.11 مثبّت" \
        || fail "فشل تثبيت Python"
    fi
  else
    PY_VER=$($PYTHON_BIN --version 2>&1 | grep -oP '\d+\.\d+')
    MAJOR=${PY_VER%%.*}; MINOR=${PY_VER##*.}
    if [[ "$MAJOR" -ge 3 && "$MINOR" -ge 10 ]]; then
      pass "Python $($PYTHON_BIN --version 2>&1)"
    else
      fail "Python $PY_VER — يلزم 3.10+"
    fi
  fi

  # ── Virtual Env ────────────────────────────────────────────
  if [[ -d "$ROOT/.venv" ]]; then
    VENV_PY="$ROOT/.venv/bin/python"
    [[ -f "$VENV_PY" ]] && pass ".venv موجود: $($VENV_PY --version 2>&1)" \
                        || fail ".venv/bin/python مفقود"
  else
    fail ".venv غير موجود"
    if $FIX && [[ -n "$PYTHON_BIN" ]]; then
      $PYTHON_BIN -m venv "$ROOT/.venv" && fixed ".venv أُنشئ"
      "$ROOT/.venv/bin/pip" install --upgrade pip setuptools wheel -q
      "$ROOT/.venv/bin/pip" install -e "$ROOT/." -q && fixed "packages مثبّتة"
    fi
  fi

  # ── Node.js ────────────────────────────────────────────────
  if command -v node &>/dev/null; then
    NODE_MAJ=$(node -v | cut -d. -f1 | tr -d 'v')
    [[ "$NODE_MAJ" -ge 20 ]] \
      && pass "Node.js $(node -v)" \
      || fail "Node.js $(node -v) — يلزم v20+"
  else
    fail "Node.js غير موجود"
    if $FIX; then
      curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - -q 2>/dev/null
      sudo apt-get install -y nodejs -qq 2>/dev/null && fixed "Node.js مثبّت"
    fi
  fi

  # ── pnpm ──────────────────────────────────────────────────
  if command -v pnpm &>/dev/null; then
    pass "pnpm $(pnpm -v)"
  else
    fail "pnpm غير موجود"
    $FIX && sudo npm install -g pnpm -q && fixed "pnpm مثبّت" || true
  fi

  # ── Nginx ─────────────────────────────────────────────────
  if command -v nginx &>/dev/null; then
    pass "Nginx $(nginx -v 2>&1 | grep -oP '\d+\.\d+\.\d+')"
  else
    warn "Nginx غير موجود (مطلوب في الإنتاج فقط)"
    $FIX && sudo apt-get install -y nginx -qq 2>/dev/null && fixed "Nginx مثبّت" || true
  fi

  # ── Redis ─────────────────────────────────────────────────
  if command -v redis-cli &>/dev/null; then
    REDIS_VER=$(redis-cli --version | grep -oP '\d+\.\d+')
    pass "Redis $REDIS_VER"
    # فحص الاتصال الفعلي
    REDIS_H="${REDIS_HOST:-127.0.0.1}"
    REDIS_P="${REDIS_PORT:-6379}"
    REDIS_PW="${REDIS_PASSWORD:-}"
    if redis-cli -h "$REDIS_H" -p "$REDIS_P" ${REDIS_PW:+-a "$REDIS_PW"} ping \
        2>/dev/null | grep -q PONG; then
      pass "Redis اتصال: $REDIS_H:$REDIS_P"
    else
      fail "Redis لا يستجيب على $REDIS_H:$REDIS_P"
      if $FIX; then
        sudo service redis-server start 2>/dev/null || \
        sudo systemctl start redis-server 2>/dev/null || true
        sleep 1
        redis-cli ping 2>/dev/null | grep -q PONG \
          && fixed "Redis تم تشغيله" \
          || fail "فشل تشغيل Redis"
      fi
    fi
  else
    fail "redis-cli غير موجود"
    $FIX && sudo apt-get install -y redis-server -qq 2>/dev/null && fixed "Redis مثبّت" || true
  fi

  # ── PostgreSQL ────────────────────────────────────────────
  if command -v psql &>/dev/null; then
    PG_VER=$(psql --version | grep -oP '\d+\.\d+' | head -1)
    pass "PostgreSQL $PG_VER"
    # فحص الاتصال
    DB_H="${DB_HOST:-127.0.0.1}"; DB_P="${DB_PORT:-5432}"
    DB_N="${DB_NAME:-alazab_core}"; DB_U="${DB_USER:-azab_user}"; DB_PW="${DB_PASSWORD:-}"
    if PGPASSWORD="$DB_PW" psql -h "$DB_H" -p "$DB_P" -U "$DB_U" \
        -d "$DB_N" -c "SELECT 1" -q &>/dev/null; then
      pass "PostgreSQL اتصال: $DB_U@$DB_N"
    else
      fail "PostgreSQL لا يستجيب: $DB_U@$DB_N@$DB_H:$DB_P"
      if $FIX; then
        sudo service postgresql start 2>/dev/null || \
        sudo systemctl start postgresql 2>/dev/null || true
        sleep 2
        PGPASSWORD="$DB_PW" psql -h "$DB_H" -p "$DB_P" -U "$DB_U" \
          -d "$DB_N" -c "SELECT 1" -q &>/dev/null \
          && fixed "PostgreSQL يعمل" || warn "قد تحتاج إعداد قاعدة البيانات أولاً"
      fi
    fi
  else
    warn "psql غير موجود (قد تستخدم Supabase Cloud)"
  fi

  # ── certbot ───────────────────────────────────────────────
  command -v certbot &>/dev/null \
    && pass "certbot $(certbot --version 2>&1 | grep -oP '\d+\.\d+')" \
    || warn "certbot غير موجود (مطلوب للـ SSL في الإنتاج)"

  # ── dos2unix ──────────────────────────────────────────────
  if ! command -v dos2unix &>/dev/null; then
    warn "dos2unix غير موجود"
    $FIX && sudo apt-get install -y dos2unix -qq 2>/dev/null && fixed "dos2unix مثبّت" || true
  else
    pass "dos2unix موجود"
  fi

  # ── systemd ───────────────────────────────────────────────
  if command -v systemctl &>/dev/null && systemctl is-system-running &>/dev/null; then
    pass "systemd يعمل"
  else
    warn "systemd غير نشط (WSL؟ — أضف 'systemd=true' في .wslconfig)"
  fi
}

# ══════════════════════════════════════════════════════════════
# SECTION 2: متغيرات البيئة
# ══════════════════════════════════════════════════════════════
check_env() {
  section "2/4  متغيرات البيئة"

  # ── فحص وجود .env ─────────────────────────────────────────
  if [[ ! -f "$ROOT/.env" ]]; then
    fail ".env غير موجود"
    if $FIX; then
      cp "$ROOT/.env.example" "$ROOT/.env" 2>/dev/null \
        && fixed ".env نُسخ من .env.example — عدّل القيم الحقيقية" \
        || fail ".env.example غير موجود أيضاً"
    fi
    return
  fi
  pass ".env موجود"

  # ── تعريف المتغيرات وأوزانها ──────────────────────────────
  # صيغة: "VAR_NAME|CRITICAL|DESCRIPTION"
  # CRITICAL: c=حرج، w=تحذير، o=اختياري
  declare -A ENV_DEFS=(
    # ── إلزامي حرج ────────────────────────────────────────
    ["RASA_PRO_LICENSE"]="c|ترخيص Rasa Pro CALM"
    ["OPENAI_API_KEY"]="c|مفتاح OpenAI API"
    ["ADMIN_EMAIL"]="c|بريد مدير النظام"
    ["ADMIN_PASSWORD"]="c|كلمة سر لوحة الإدارة"
    ["ADMIN_SESSION_SECRET"]="c|سر توقيع الـ JWT"
    ["DB_HOST"]="c|عنوان PostgreSQL"
    ["DB_PORT"]="c|منفذ PostgreSQL"
    ["DB_NAME"]="c|اسم قاعدة البيانات"
    ["DB_USER"]="c|مستخدم قاعدة البيانات"
    ["DB_PASSWORD"]="c|كلمة سر قاعدة البيانات"
    ["REDIS_HOST"]="c|عنوان Redis"
    ["REDIS_PORT"]="c|منفذ Redis"
    ["RASA_URL"]="c|عنوان Rasa Server"
    ["ACTION_SERVER_URL"]="c|عنوان Actions Server"
    ["ALLOWED_ORIGINS"]="c|CORS origins"
    ["PUBLIC_BASE_URL"]="c|الـ URL العام للموقع"
    # ── مهم لكن اختياري ────────────────────────────────────
    ["ADMIN_API_KEY"]="w|مفتاح API الإدارة"
    ["JWT_SECRET"]="w|سر JWT العام"
    ["ENCRYPTION_KEY"]="w|مفتاح التشفير"
    ["REDIS_PASSWORD"]="w|كلمة سر Redis"
    ["NODE_ENV"]="w|وضع التشغيل (production/development)"
    ["AUDIO_TRANSCRIPTION_MODEL"]="w|موديل Whisper"
    ["AUDIO_TTS_MODEL"]="w|موديل TTS"
    ["AUDIO_TTS_VOICE"]="w|صوت TTS"
    # ── اختياري ────────────────────────────────────────────
    ["WHATSAPP_TOKEN"]="o|WhatsApp Business API"
    ["WHATSAPP_API_URL"]="o|WhatsApp API URL"
    ["NOTIFY_PHONE"]="o|هاتف الإشعارات"
    ["TELEGRAM_BOT_TOKEN"]="o|Telegram Bot"
    ["TELEGRAM_WEBHOOK_SECRET"]="o|Telegram Webhook Secret"
    ["FB_PAGE_ACCESS_TOKEN"]="o|Facebook Page Token"
    ["FB_VERIFY_TOKEN"]="o|Facebook Verify Token"
    ["UBERFIX_API_KEY"]="o|UberFix API Key"
    ["UBERFIX_API_URL"]="o|UberFix API URL"
    ["SUPABASE_URL"]="o|Supabase URL"
    ["SUPABASE_ANON_KEY"]="o|Supabase Anon Key"
  )

  MISSING_CRITICAL=0
  REPLACE_COUNT=0

  for var in "${!ENV_DEFS[@]}"; do
    IFS="|" read -r level desc <<< "${ENV_DEFS[$var]}"
    val="${!var:-}"

    if [[ -z "$val" ]]; then
      case "$level" in
        c) fail "CRITICAL  $var  ← $desc"; MISSING_CRITICAL=$((MISSING_CRITICAL+1)) ;;
        w) warn "MISSING   $var  ← $desc" ;;
        o) $QUIET || info "OPTIONAL  $var  ← $desc" ;;
      esac
    elif [[ "$val" == REPLACE_* || "$val" == "replace-"* ]]; then
      fail "NOT_SET   $var = '${val:0:30}'  ← يجب التعديل"; REPLACE_COUNT=$((REPLACE_COUNT+1))
    else
      # إخفاء القيم الحساسة في العرض
      case "$var" in
        *PASSWORD*|*SECRET*|*KEY*|*TOKEN*|*LICENSE*)
          $QUIET || pass "$var = '${val:0:8}…'"
          ;;
        *)
          $QUIET || pass "$var = '${val:0:50}'"
          ;;
      esac
    fi
  done

  [[ "$MISSING_CRITICAL" -gt 0 ]] && \
    printf "\n  ${R}${B}⚠  %d متغير حرج مفقود — البوت لن يعمل!${N}\n" "$MISSING_CRITICAL"
  [[ "$REPLACE_COUNT" -gt 0 ]] && \
    printf "\n  ${R}${B}⚠  %d متغير لم يُعدَّل بعد (REPLACE_...)${N}\n" "$REPLACE_COUNT"

  # ── فحص .env في مجلد الفرونت (يجب أن يكون نظيفاً) ─────────
  FRONT_ENV="$ROOT/azabot/.env"
  if [[ -f "$FRONT_ENV" ]]; then
    if grep -qE "eyJ|supabase\.co|postgres|pass" "$FRONT_ENV" 2>/dev/null; then
      fail "azabot/.env يحتوي credentials حقيقية! (خطر أمني)"
      if $FIX; then
        cp "$FRONT_ENV" "${FRONT_ENV}.bak"
        cat > "$FRONT_ENV" << 'CLEANENV'
# AzaBot Frontend .env — آمن (بدون credentials)
VITE_APP_NAME=AzaBot
VITE_APP_VERSION=3.0.0
VITE_APP_ENV=production
CLEANENV
        fixed "azabot/.env نُظِّف — نسخة احتياطية في azabot/.env.bak"
      fi
    else
      pass "azabot/.env نظيف (بدون credentials)"
    fi
  fi

  # ── فحص ALLOWED_ORIGINS يشمل الدومين الصحيح ──────────────
  if [[ -n "${ALLOWED_ORIGINS:-}" ]]; then
    if echo "$ALLOWED_ORIGINS" | grep -q "localhost\|127.0.0.1"; then
      NODE_ENV_VAL="${NODE_ENV:-development}"
      [[ "$NODE_ENV_VAL" == "production" ]] \
        && warn "ALLOWED_ORIGINS يحتوي localhost وNODE_ENV=production" \
        || info "ALLOWED_ORIGINS يحتوي localhost (مناسب للـ dev)"
    fi
    if echo "$ALLOWED_ORIGINS" | grep -q "alazab.com\|bot.alazab.com"; then
      pass "ALLOWED_ORIGINS يشمل alazab.com"
    else
      warn "ALLOWED_ORIGINS لا يشمل alazab.com أو bot.alazab.com"
    fi
  fi
}

# ══════════════════════════════════════════════════════════════
# SECTION 3: المسارات والملفات
# ══════════════════════════════════════════════════════════════
check_paths() {
  section "3/4  المسارات والملفات المطلوبة"

  # ── ملفات داخل المشروع ────────────────────────────────────
  declare -A PROJ_FILES=(
    # Rasa
    ["config.yml"]="إعدادات Rasa pipeline"
    ["domain.yml"]="تعريف domain"
    ["endpoints.yml"]="إعدادات Redis وActions"
    ["credentials.yml"]="قنوات الاتصال"
    ["endpoints.nodocker.yml"]="endpoints للتشغيل بدون Docker"
    ["python-version"]="إصدار Python المحدد"
    ["pyproject.toml"]="إعدادات المشروع"
    # Actions
    ["actions/__init__.py"]="تهيئة actions package"
    ["actions/action_general.py"]="Actions عامة"
    ["actions/action_submit_lead.py"]="Action إرسال Lead"
    ["actions/action_human_handoff.py"]="Action التحويل البشري"
    ["actions/action_context_accumulator.py"]="محرك الذاكرة السياقية"
    # Webhook
    ["webhook/server.py"]="FastAPI server"
    # Data
    ["data/general/nlu.yml"]="NLU عام"
    ["data/general/rules.yml"]="Rules عامة"
    ["data/general/collect_lead.yml"]="Flow جمع البيانات"
    ["data/brands/uberfix.yml"]="UberFix flows"
    ["data/brands/uberfix/nlu.yml"]="UberFix NLU"
    ["data/brands/uberfix/stories.yml"]="UberFix stories"
    ["data/system/patterns/patterns.yml"]="CALM patterns"
    # Domain
    ["domain/general.yml"]="domain عام"
    ["domain/uberfix.yml"]="domain UberFix"
    # Frontend
    ["azabot/package.json"]="Frontend dependencies"
    ["azabot/vite.config.ts"]="Vite config"
    ["azabot/src/hooks/useAudioRecorder.ts"]="Audio recorder hook"
    # Deploy
    ["deploy/systemd/azabot-rasa.service"]="systemd Rasa"
    ["deploy/systemd/azabot-webhook.service"]="systemd Webhook"
    ["deploy/systemd/azabot-actions.service"]="systemd Actions"
    ["deploy/production/nginx/bot.alazab.com.conf"]="Nginx config"
    ["deploy/production/nginx/nginx.conf"]="Nginx main config"
    ["deploy/production/deploy-production.sh"]="سكريبت النشر"
    ["deploy/production/server-setup.sh"]="سكريبت إعداد السيرفر"
    # Scripts
    ["scripts/botctl.sh"]="أداة إدارة الخدمات"
    ["dev.sh"]="مشغّل التطوير"
    ["wsl-setup.sh"]="إعداد WSL"
    ["wsl-test.sh"]="اختبار WSL"
    # Config
    [".env.example"]="مثال متغيرات البيئة"
    ["piper/pronunciation_lexicon.yml"]="قاموس النطق العربي"
  )

  MISSING_FILES=0
  for fpath in "${!PROJ_FILES[@]}"; do
    desc="${PROJ_FILES[$fpath]}"
    full="$ROOT/$fpath"
    if [[ -f "$full" ]]; then
      # تحقق من أن الملف غير فارغ
      if [[ ! -s "$full" ]]; then
        fail "فارغ: $fpath  ← $desc"
        MISSING_FILES=$((MISSING_FILES+1))
      else
        pass "موجود: $fpath"
      fi
    else
      fail "مفقود: $fpath  ← $desc"
      MISSING_FILES=$((MISSING_FILES+1))
    fi
  done

  # ── المجلدات المطلوبة ─────────────────────────────────────
  declare -a REQ_DIRS=(
    "models"
    "logs"
    ".runtime/pids"
    "webhook/static/uploads"
    "data/brands"
    "domain"
    "actions/brand_actions"
    "piper"
  )
  for dir in "${REQ_DIRS[@]}"; do
    if [[ -d "$ROOT/$dir" ]]; then
      pass "مجلد: $dir"
    else
      warn "مجلد مفقود: $dir"
      if $FIX; then
        mkdir -p "$ROOT/$dir"
        fixed "مجلد أُنشئ: $dir"
      fi
    fi
  done

  # ── موديل Rasa ────────────────────────────────────────────
  MODEL=$(ls "$ROOT/models/"*.tar.gz 2>/dev/null | head -1 || true)
  if [[ -n "$MODEL" ]]; then
    MODEL_SIZE=$(du -sh "$MODEL" | cut -f1)
    MODEL_DATE=$(stat -c "%y" "$MODEL" 2>/dev/null | cut -d' ' -f1 || echo "غير معروف")
    pass "Rasa model: $(basename $MODEL) ($MODEL_SIZE) — $MODEL_DATE"
  else
    fail "لا يوجد موديل Rasa — شغّل: bash scripts/botctl.sh train"
  fi

  # ── frontend node_modules ─────────────────────────────────
  if [[ -d "$ROOT/azabot/node_modules" ]]; then
    PKG_COUNT=$(ls "$ROOT/azabot/node_modules" | wc -l)
    pass "node_modules: $PKG_COUNT package"
  else
    warn "node_modules مفقود"
    if $FIX && command -v pnpm &>/dev/null; then
      (cd "$ROOT/azabot" && pnpm install --frozen-lockfile -s 2>/dev/null) \
        && fixed "node_modules مثبّتة" || warn "فشل pnpm install"
    fi
  fi

  # ── مسارات خارج المشروع (للإنتاج فقط) ───────────────────
  if [[ "$NODE_ENV:-" == "production" ]] || \
     [[ -d "/etc/nginx/sites-available" ]]; then
    info "فحص مسارات الإنتاج..."

    IS_PROD_SERVER=true

    declare -a EXT_PATHS=(
      "/etc/nginx/sites-available/bot.alazab.com.conf|Nginx site config"
      "/etc/nginx/sites-enabled/bot.alazab.com.conf|Nginx site enabled"
      "/etc/systemd/system/azabot-rasa.service|systemd Rasa"
      "/etc/systemd/system/azabot-webhook.service|systemd Webhook"
      "/etc/systemd/system/azabot-actions.service|systemd Actions"
    )
    for entry in "${EXT_PATHS[@]}"; do
      IFS="|" read -r p d <<< "$entry"
      [[ -f "$p" ]] \
        && pass "خارجي: $p" \
        || warn "خارجي مفقود: $p  ← $d (شغّل deploy-production.sh)"
    done

    SSL_CERT="/etc/letsencrypt/live/bot.alazab.com/fullchain.pem"
    if [[ -f "$SSL_CERT" ]]; then
      # فحص انتهاء الصلاحية
      EXPIRY=$(openssl x509 -enddate -noout -in "$SSL_CERT" 2>/dev/null | cut -d= -f2)
      EXPIRY_TS=$(date -d "$EXPIRY" +%s 2>/dev/null || echo 0)
      NOW_TS=$(date +%s)
      DAYS_LEFT=$(( (EXPIRY_TS - NOW_TS) / 86400 ))
      if [[ "$DAYS_LEFT" -gt 14 ]]; then
        pass "SSL: bot.alazab.com — منتهي بعد $DAYS_LEFT يوم"
      elif [[ "$DAYS_LEFT" -gt 0 ]]; then
        warn "SSL: ينتهي خلال $DAYS_LEFT يوم — جدّد: sudo certbot renew"
        $FIX && sudo certbot renew --quiet && fixed "SSL جُدِّد" || true
      else
        fail "SSL: منتهي الصلاحية! — sudo certbot renew"
        $FIX && sudo certbot renew && fixed "SSL جُدِّد" || true
      fi
    else
      warn "SSL غير موجود — شغّل: sudo certbot --nginx -d bot.alazab.com"
    fi

    # فحص Swap
    SWAP=$(swapon --show --bytes 2>/dev/null | awk 'NR>1{sum+=$3} END{print sum}')
    if [[ "${SWAP:-0}" -gt 1000000000 ]]; then
      pass "Swap: $(free -h | awk '/Swap/{print $2}')"
    else
      fail "Swap صغير جداً — يجب 4GB+ مع Rasa"
      $FIX && bash "$ROOT/deploy/production/setup-swap.sh" && fixed "Swap 4GB أُضيف" || true
    fi
  fi

  # ── فحص CRLF line endings ────────────────────────────────
  CRLF=$(find "$ROOT" -maxdepth 3 -name "*.sh" \
    -not -path "*/.venv/*" -not -path "*/node_modules/*" \
    -exec file {} \; 2>/dev/null | grep CRLF | wc -l)
  if [[ "$CRLF" -gt 0 ]]; then
    fail "CRLF line endings في $CRLF سكريبت — ستفشل في Linux"
    if $FIX && command -v dos2unix &>/dev/null; then
      find "$ROOT" -maxdepth 3 -name "*.sh" \
        -not -path "*/.venv/*" -not -path "*/node_modules/*" \
        -exec dos2unix {} \; 2>/dev/null
      fixed "تحويل CRLF → LF في $CRLF ملف"
    fi
  else
    pass "كل الـ scripts بـ LF endings"
  fi

  # ── YAML syntax ──────────────────────────────────────────
  if [[ -f "$ROOT/.venv/bin/python" ]]; then
    YAML_ERR=$("$ROOT/.venv/bin/python" -c "
import yaml, sys
from pathlib import Path
errors=[]
for f in list(Path('$ROOT/data').rglob('*.yml')) + \
         list(Path('$ROOT/domain').glob('*.yml')) + \
         [Path('$ROOT/config.yml'),Path('$ROOT/domain.yml')]:
    if not f.exists(): continue
    try: yaml.safe_load(f.read_text())
    except yaml.YAMLError as e: errors.append(f'{f}: {e}')
if errors:
    for e in errors: print(e)
else:
    print('OK')
" 2>/dev/null || echo "SKIP")
    if [[ "$YAML_ERR" == "OK" ]]; then
      pass "كل ملفات YAML صالحة"
    elif [[ "$YAML_ERR" == "SKIP" ]]; then
      warn "تخطي YAML check (.venv غير مكتمل)"
    else
      fail "YAML errors:$'\n'$YAML_ERR"
    fi
  fi

  # ── Python syntax ────────────────────────────────────────
  if [[ -f "$ROOT/.venv/bin/python" ]]; then
    PY_ERRS=0
    while IFS= read -r -d '' pyf; do
      if ! "$ROOT/.venv/bin/python" -c \
          "import ast; ast.parse(open('$pyf').read())" 2>/dev/null; then
        fail "Python syntax error: ${pyf#$ROOT/}"
        PY_ERRS=$((PY_ERRS+1))
      fi
    done < <(find "$ROOT/actions" "$ROOT/webhook" -name "*.py" \
              -not -path "*/__pycache__/*" -print0 2>/dev/null)
    [[ "$PY_ERRS" -eq 0 ]] && pass "كل ملفات Python صالحة"
  fi

  [[ "$MISSING_FILES" -gt 0 ]] && \
    printf "\n  ${R}${B}⚠  %d ملف مطلوب مفقود${N}\n" "$MISSING_FILES"
}

# ══════════════════════════════════════════════════════════════
# SECTION 4: الرخصة ومفاتيح API
# ══════════════════════════════════════════════════════════════
check_api_keys() {
  section "4/4  صحة الرخصة ومفاتيح API"

  # ── Rasa Pro License ──────────────────────────────────────
  LICENSE="${RASA_PRO_LICENSE:-}"
  if [[ -z "$LICENSE" ]]; then
    fail "RASA_PRO_LICENSE فارغ"
  elif [[ "$LICENSE" == REPLACE_* ]]; then
    fail "RASA_PRO_LICENSE لم يُعدَّل بعد"
  elif [[ "${#LICENSE}" -lt 100 ]]; then
    fail "RASA_PRO_LICENSE يبدو قصيراً (${#LICENSE} حرف) — قد يكون خاطئاً"
  else
    # JWT format check: header.payload.signature
    PARTS=$(echo "$LICENSE" | tr '.' '\n' | wc -l)
    if [[ "$PARTS" -ge 3 ]]; then
      # استخراج expiry من payload
      PAYLOAD=$(echo "$LICENSE" | cut -d. -f2 | \
        awk '{n=length($0)%4; if(n==2) print $0"=="; else if(n==3) print $0"="; else print $0}' | \
        base64 -d 2>/dev/null | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(d.get('exp','?'))" 2>/dev/null || echo "?")
      if [[ "$PAYLOAD" != "?" ]] && [[ "$PAYLOAD" =~ ^[0-9]+$ ]]; then
        NOW=$(date +%s)
        DAYS_LEFT=$(( (PAYLOAD - NOW) / 86400 ))
        if [[ "$DAYS_LEFT" -gt 30 ]]; then
          pass "RASA_PRO_LICENSE: صالح — ينتهي بعد $DAYS_LEFT يوم"
        elif [[ "$DAYS_LEFT" -gt 0 ]]; then
          warn "RASA_PRO_LICENSE: ينتهي خلال $DAYS_LEFT يوم!"
        else
          fail "RASA_PRO_LICENSE: منتهي الصلاحية منذ $(( -DAYS_LEFT )) يوم!"
        fi
      else
        pass "RASA_PRO_LICENSE: صيغة JWT صالحة (${#LICENSE} حرف)"
      fi
    else
      fail "RASA_PRO_LICENSE: صيغة خاطئة (ليس JWT)"
    fi
  fi

  # ── OpenAI API ────────────────────────────────────────────
  OAPI="${OPENAI_API_KEY:-}"
  if [[ -z "$OAPI" || "$OAPI" == REPLACE_* ]]; then
    fail "OPENAI_API_KEY فارغ أو لم يُعدَّل"
  elif [[ ! "$OAPI" =~ ^sk- ]]; then
    fail "OPENAI_API_KEY صيغة خاطئة (يجب أن يبدأ بـ sk-)"
  else
    info "اختبار OpenAI API (اتصال حقيقي)..."
    OAI_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer $OAPI" \
      -H "Content-Type: application/json" \
      --max-time 10 \
      "https://api.openai.com/v1/models" 2>/dev/null || echo "000")

    case "$OAI_STATUS" in
      200) pass "OPENAI_API_KEY: صالح ✓ (HTTP 200)" ;;
      401) fail "OPENAI_API_KEY: غير صالح أو منتهي (HTTP 401)" ;;
      429) warn "OPENAI_API_KEY: حد الطلبات مُستنفَد (HTTP 429)" ;;
      000) warn "OPENAI_API_KEY: لا يمكن الاتصال بـ OpenAI (شبكة؟)" ;;
      *)   warn "OPENAI_API_KEY: استجابة غير متوقعة (HTTP $OAI_STATUS)" ;;
    esac
  fi

  # ── WhatsApp (اختياري) ─────────────────────────────────────
  WA_TOKEN="${WHATSAPP_TOKEN:-}"
  WA_URL="${WHATSAPP_API_URL:-}"
  if [[ -n "$WA_TOKEN" && "$WA_TOKEN" != REPLACE_* ]]; then
    info "اختبار WhatsApp API..."
    WA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer $WA_TOKEN" \
      --max-time 8 \
      "https://graph.facebook.com/v20.0/me" 2>/dev/null || echo "000")
    case "$WA_STATUS" in
      200) pass "WHATSAPP_TOKEN: صالح (HTTP 200)" ;;
      401) fail "WHATSAPP_TOKEN: غير صالح (HTTP 401)" ;;
      000) warn "WHATSAPP_TOKEN: لا اتصال بـ Facebook API" ;;
      *)   warn "WHATSAPP_TOKEN: HTTP $WA_STATUS" ;;
    esac
  else
    info "WHATSAPP_TOKEN: غير مضبوط (اختياري)"
  fi

  # ── Telegram (اختياري) ────────────────────────────────────
  TG_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
  if [[ -n "$TG_TOKEN" && "$TG_TOKEN" != REPLACE_* ]]; then
    info "اختبار Telegram Bot API..."
    TG_RESP=$(curl -s --max-time 8 \
      "https://api.telegram.org/bot${TG_TOKEN}/getMe" 2>/dev/null || echo "{}")
    TG_OK=$(echo "$TG_RESP" | python3 -c \
      "import sys,json; d=json.load(sys.stdin); print(d.get('ok','false'))" 2>/dev/null || echo "false")
    if [[ "$TG_OK" == "True" || "$TG_OK" == "true" ]]; then
      TG_NAME=$(echo "$TG_RESP" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('username','?'))" 2>/dev/null)
      pass "TELEGRAM_BOT_TOKEN: صالح — @$TG_NAME"
    else
      fail "TELEGRAM_BOT_TOKEN: غير صالح"
    fi
  else
    info "TELEGRAM_BOT_TOKEN: غير مضبوط (اختياري)"
  fi

  # ── UberFix API (اختياري) ─────────────────────────────────
  UF_KEY="${UBERFIX_API_KEY:-}"
  UF_URL="${UBERFIX_API_URL:-}"
  if [[ -n "$UF_KEY" && "$UF_KEY" != REPLACE_* && -n "$UF_URL" ]]; then
    info "اختبار UberFix API..."
    UF_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "x-api-key: $UF_KEY" \
      --max-time 8 \
      "$UF_URL" 2>/dev/null || echo "000")
    case "$UF_STATUS" in
      200|201|400) pass "UBERFIX_API_KEY: يستجيب (HTTP $UF_STATUS)" ;;
      401|403)     fail "UBERFIX_API_KEY: غير صالح (HTTP $UF_STATUS)" ;;
      000)         warn "UBERFIX_API_KEY: لا اتصال بـ UberFix API" ;;
      *)           warn "UBERFIX_API_KEY: HTTP $UF_STATUS" ;;
    esac
  else
    info "UBERFIX_API_KEY: غير مضبوط (اختياري)"
  fi

  # ── فحص المنافذ المستخدمة ─────────────────────────────────
  info "فحص المنافذ..."
  for port in 5005 5055 8000 8080; do
    if command -v lsof &>/dev/null; then
      PROC=$(lsof -ti ":$port" 2>/dev/null | head -1 || true)
    else
      PROC=$(ss -tlnp 2>/dev/null | grep ":$port " | grep -oP 'pid=\K\d+' | head -1 || true)
    fi

    if [[ -n "$PROC" ]]; then
      PROC_NAME=$(ps -p "$PROC" -o comm= 2>/dev/null || echo "unknown")
      case "$port" in
        5005) pass  "Port $port مستخدم: $PROC_NAME (Rasa)" ;;
        5055) pass  "Port $port مستخدم: $PROC_NAME (Actions)" ;;
        8000) pass  "Port $port مستخدم: $PROC_NAME (Webhook)" ;;
        8080) info  "Port $port مستخدم: $PROC_NAME (Frontend dev)" ;;
      esac
    else
      case "$port" in
        5005) warn "Port $port فارغ (Rasa لا يعمل)" ;;
        5055) warn "Port $port فارغ (Actions لا يعمل)" ;;
        8000) warn "Port $port فارغ (Webhook لا يعمل)" ;;
        8080) info "Port $port فارغ (Frontend dev)" ;;
      esac
    fi
  done
}

# ══════════════════════════════════════════════════════════════
# التقرير النهائي
# ══════════════════════════════════════════════════════════════
print_report() {
  TOTAL=$((PASS + FAIL + WARN))
  echo ""
  printf "${B}%s${N}\n" "$(printf '═%.0s' {1..60})"
  printf "${B}  📊 نتائج azabot-doctor${N}\n"
  printf "${B}%s${N}\n" "$(printf '═%.0s' {1..60})"
  printf "  ${G}✅ PASS:  %3d${N}\n" "$PASS"
  printf "  ${R}❌ FAIL:  %3d${N}\n" "$FAIL"
  printf "  ${Y}⚠️  WARN:  %3d${N}\n" "$WARN"
  $FIX && printf "  ${C}🔧 FIXED: %3d${N}\n" "$FIXED"
  printf "  %s  TOTAL: %3d\n" "📋" "$TOTAL"
  printf "${B}%s${N}\n" "$(printf '─%.0s' {1..60})"

  if [[ "$FAIL" -eq 0 && "$WARN" -eq 0 ]]; then
    printf "\n  ${G}${B}🎉 المشروع جاهز تماماً!${N}\n"
  elif [[ "$FAIL" -eq 0 ]]; then
    printf "\n  ${Y}${B}⚠  المشروع يعمل مع %d تحذير — راجعها${N}\n" "$WARN"
  else
    printf "\n  ${R}${B}❌ %d مشكلة تحتاج إصلاح${N}\n" "$FAIL"
    if ! $FIX; then
      printf "  ${C}  شغّل:  bash azabot-doctor.sh --fix  لإصلاح ما يمكن إصلاحه تلقائياً${N}\n"
    fi
  fi
  echo ""

  return "$FAIL"
}

# ══════════════════════════════════════════════════════════════
# الدخول الرئيسي
# ══════════════════════════════════════════════════════════════
printf "${B}${C}\n  🩺 azabot-doctor — فحص بيئة AzaBot${N}\n"
printf "  المشروع: ${ROOT}\n"
printf "  الوضع:   %s\n" "$($FIX && echo '--fix (فحص + إصلاح)' || echo 'قراءة فقط')"
printf "  الوقت:   %s\n" "$(date '+%Y-%m-%d %H:%M:%S')"

case "$SECTION" in
  --tools) check_tools ;;
  --env)   check_env   ;;
  --paths) check_paths ;;
  --api)   check_api_keys ;;
  --all)
    check_tools
    check_env
    check_paths
    check_api_keys
    ;;
esac

print_report
