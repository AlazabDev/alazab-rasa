#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  az.sh — AzaBot local production controller
#  الهدف:
#    - نقطة تشغيل واحدة للمشروع محلياً قبل GitHub/Production.
#    - لا يستخدم source .venv حتى لا يتأثر بـ set -u في جلسة المستخدم.
#    - كل تدريب/تحقق يعمل على .runtime/domain.generated.yml وليس domain.yml الخام.
#    - يمنع التدريب في production إلا بتجاوز صريح.
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

BLUE=$'\033[1;34m'
GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'
CYAN=$'\033[1;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

log()  { printf "%s[az]%s %s\n" "$BLUE" "$NC" "$*"; }
ok()   { printf "%s[ok]%s %s\n" "$GREEN" "$NC" "$*"; }
warn() { printf "%s[warn]%s %s\n" "$YELLOW" "$NC" "$*"; }
fail() { printf "%s[fail]%s %s\n" "$RED" "$NC" "$*" >&2; exit 1; }

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_VERSION="${PYTHON_VERSION:-3.11}"
RASA_PORT="${RASA_PORT:-5005}"
ACTIONS_PORT="${ACTIONS_PORT:-5055}"
WEBHOOK_HOST="${WEBHOOK_HOST:-0.0.0.0}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"
RASA_HOST="${RASA_HOST:-127.0.0.1}"
PID_DIR="${PID_DIR:-.runtime/pids}"
DOMAIN_FILE="${DOMAIN_FILE:-.runtime/domain.generated.yml}"
ENDPOINTS_FILE="${ENDPOINTS_FILE:-.runtime/endpoints.generated.yml}"
LOG_DIR="${LOG_DIR:-logs}"

mkdir -p "$PID_DIR" "$LOG_DIR" .runtime models

command_exists() { command -v "$1" >/dev/null 2>&1; }

_trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

_load_env() {
  # يحمّل .env بأمان بدون source حتى لا تتكسر قيم bcrypt/JWT التي تحتوي على $.
  [[ ! -f .env ]] && return 0

  local line key value
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="$(_trim "$line")"
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue

    key="$(_trim "${line%%=*}")"
    value="${line#*=}"
    value="$(_trim "$value")"

    # إزالة quotes المحيطة فقط، بدون تفسير داخلي للقيمة.
    if [[ "$value" == \"*\" && "$value" == *\" ]]; then
      value="${value#\"}"
      value="${value%\"}"
    elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
      value="${value#\'}"
      value="${value%\'}"
    fi

    [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
    export "$key=$value"
  done < .env
}

_venv_python() {
  if [[ -x "$VENV_DIR/bin/python" ]]; then
    printf '%s\n' "$VENV_DIR/bin/python"
  elif command_exists python3; then
    command -v python3
  else
    return 1
  fi
}

_venv_pip() {
  [[ -x "$VENV_DIR/bin/pip" ]] || fail "pip داخل $VENV_DIR غير موجود — شغّل: bash az.sh setup"
  "$VENV_DIR/bin/pip" "$@"
}

_venv_rasa() {
  if [[ -x "$VENV_DIR/bin/rasa" ]]; then
    printf '%s\n' "$VENV_DIR/bin/rasa"
  elif command_exists rasa; then
    command -v rasa
  else
    return 1
  fi
}

_python() {
  local py
  py="$(_venv_python)" || fail "python3 غير موجود"
  "$py" "$@"
}

_rasa() {
  local rasa_bin
  rasa_bin="$(_venv_rasa)" || fail "Rasa غير مثبت — شغّل: bash az.sh setup"
  "$rasa_bin" "$@"
}

_has_systemd_units() {
  command_exists systemctl || return 1
  systemctl list-unit-files 2>/dev/null | grep -q '^azabot-webhook\.service'
}

_require_file() {
  [[ -f "$1" ]] || fail "ملف مطلوب غير موجود: $1"
}

_require_dir() {
  [[ -d "$1" ]] || fail "مجلد مطلوب غير موجود: $1"
}

_runtime_render() {
  _require_file scripts/render_runtime_domain.py
  log "توليد ملفات Rasa runtime..."
  _python scripts/render_runtime_domain.py >/dev/null
  _require_file "$DOMAIN_FILE"
  _require_file "$ENDPOINTS_FILE"
  ok "runtime جاهز: $DOMAIN_FILE + $ENDPOINTS_FILE"
}

_yaml_check() {
  log "فحص YAML لكل ملفات المشروع المهمة..."
  _python - <<'PY'
from pathlib import Path
import sys

try:
    import yaml
except Exception as exc:
    print(f"[warn] PyYAML غير متاح: {exc}")
    sys.exit(0)

skip = {'.git', '.venv', 'venv', 'node_modules', 'models', '__pycache__'}
files = []

for pattern in ('*.yml', '*.yaml'):
    for p in Path('.').rglob(pattern):
        if any(part in skip for part in p.parts):
            continue
        files.append(p)

errors = []
for p in sorted(files):
    try:
        yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append((p, exc))

if errors:
    print(f"[fail] YAML errors: {len(errors)}")
    for p, exc in errors:
        print(f"- {p}: {exc}")
    sys.exit(1)

print(f"[ok] YAML files valid: {len(files)}")
PY
}

_training_audit() {
  if [[ -f scripts/audit-rasa-training.py ]]; then
    log "مراجعة ملفات التدريب/domain/data..."
    _python scripts/audit-rasa-training.py
  else
    warn "scripts/audit-rasa-training.py غير موجود — تخطي مراجعة التدريب المتقدمة"
  fi
}

_assert_not_production_training() {
  local force="${1:-false}"
  _load_env

  if [[ "${NODE_ENV:-}" == "production" && "$force" != "true" ]]; then
    cat >&2 <<MSG
${RED}تم منع التدريب لأن NODE_ENV=production.${NC}
التدريب يجب أن يتم محلياً أو في بيئة staging، ثم يتم نشر model جاهز.
للتجاوز القسري غير المفضل: bash az.sh train --force
MSG
    exit 1
  fi

  if [[ "${TRAIN_ON_DEPLOY:-false}" == "true" && "$force" != "true" ]]; then
    fail "TRAIN_ON_DEPLOY=true مرفوض. اجعله false أو استخدم --force بمسؤوليتك."
  fi
}

_latest_model() {
  ls -t models/*.tar.gz 2>/dev/null | head -1 || true
}

_port_pid() {
  local port="$1"

  if command_exists lsof; then
    lsof -ti tcp:"$port" 2>/dev/null | head -1 || true
  elif command_exists ss; then
    ss -ltnp 2>/dev/null \
      | awk -v p=":$port" '$4 ~ p {print $NF}' \
      | sed -n 's/.*pid=\([0-9]*\).*/\1/p' \
      | head -1
  else
    true
  fi
}

_http_code() {
  local url="$1"
  curl -sS -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || printf '000'
}

_start_one() {
  local name="$1"
  shift

  local pidfile="$PID_DIR/${name}.pid"

  if [[ -f "$pidfile" ]]; then
    local oldpid
    oldpid="$(cat "$pidfile" 2>/dev/null || true)"
    if [[ -n "$oldpid" ]] && kill -0 "$oldpid" 2>/dev/null; then
      warn "$name يعمل بالفعل PID=$oldpid"
      return 0
    fi
    rm -f "$pidfile"
  fi

  log "تشغيل $name..."
  nohup "$@" >> "$LOG_DIR/${name}.out.log" 2>> "$LOG_DIR/${name}.err.log" &
  echo $! > "$pidfile"
  sleep 1

  local pid
  pid="$(cat "$pidfile")"

  if kill -0 "$pid" 2>/dev/null; then
    ok "$name يعمل PID=$pid"
  else
    rm -f "$pidfile"
    fail "$name فشل في التشغيل — راجع $LOG_DIR/${name}.err.log"
  fi
}

_stop_one() {
  local name="$1"
  local pidfile="$PID_DIR/${name}.pid"

  if [[ ! -f "$pidfile" ]]; then
    warn "$name: لا يوجد pidfile"
    return 0
  fi

  local pid
  pid="$(cat "$pidfile" 2>/dev/null || true)"
  rm -f "$pidfile"

  if [[ -z "$pid" ]]; then
    warn "$name: pidfile فارغ"
    return 0
  fi

  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1

    if kill -0 "$pid" 2>/dev/null; then
      warn "$name لم يتوقف بلطف — kill -9 PID=$pid"
      kill -9 "$pid" 2>/dev/null || true
    fi

    ok "$name توقف"
  else
    warn "$name: العملية غير موجودة PID=$pid"
  fi
}

# ══════════════════════════════════════════════════════════════
#  setup/install
# ══════════════════════════════════════════════════════════════

cmd_install() {
  log "إعداد Python venv وتثبيت المتطلبات..."

  if command_exists uv; then
    ok "uv متاح: $(uv --version)"
    [[ -d "$VENV_DIR" ]] || uv venv "$VENV_DIR" --python "$PYTHON_VERSION"

    [[ -f requirements/01-rasa.txt ]] || fail "requirements/01-rasa.txt غير موجود"
    [[ -f requirements/02-extra.txt ]] || fail "requirements/02-extra.txt غير موجود"

    log "[1/2] تثبيت Rasa Pro requirements..."
    VIRTUAL_ENV="$ROOT_DIR/$VENV_DIR" uv pip install -p "$VENV_DIR/bin/python" -r requirements/01-rasa.txt

    log "[2/2] تثبيت extra requirements..."
    VIRTUAL_ENV="$ROOT_DIR/$VENV_DIR" uv pip install -p "$VENV_DIR/bin/python" -r requirements/02-extra.txt
  else
    warn "uv غير موجود — استخدام python venv + pip"
    [[ -d "$VENV_DIR" ]] || python3 -m venv "$VENV_DIR"

    _venv_pip install --upgrade pip setuptools wheel
    _venv_pip install -r requirements/01-rasa.txt
    _venv_pip install -r requirements/02-extra.txt
  fi

  ok "انتهى تثبيت Python"
}

cmd_setup() {
  cmd_install

  if [[ ! -f .env ]]; then
    [[ -f .env.example ]] || fail ".env.example غير موجود"
    cp .env.example .env
    warn "تم إنشاء .env من .env.example — أكمل القيم السرية قبل التشغيل"
  fi

  mkdir -p .runtime/uploads .runtime/kb "$PID_DIR" "$LOG_DIR" models
  _runtime_render

  if [[ -d azabot ]]; then
    if command_exists pnpm; then
      log "تثبيت frontend dependencies..."
      (cd azabot && pnpm install) || warn "فشل pnpm install — راجع azabot/package.json"
    else
      warn "pnpm غير موجود — تخطي frontend install"
    fi
  fi

  ok "setup اكتمل. التالي: bash az.sh doctor"
}

# ══════════════════════════════════════════════════════════════
#  doctor/audit/check
# ══════════════════════════════════════════════════════════════

cmd_doctor() {
  log "فحص البيئة والمسارات..."
  echo ""

  command_exists python3 && ok "python3: $(python3 --version)" || fail "python3 غير موجود"
  command_exists uv && ok "uv: $(uv --version)" || warn "uv غير مثبت"

  [[ -x "$VENV_DIR/bin/python" ]] \
    && ok "venv python: $($VENV_DIR/bin/python --version)" \
    || warn "venv غير موجود: $VENV_DIR"

  [[ -x "$VENV_DIR/bin/rasa" ]] \
    && ok "rasa: $($VENV_DIR/bin/rasa --version 2>/dev/null | head -1)" \
    || warn "rasa CLI غير موجود داخل venv"

  command_exists node && ok "node: $(node --version)" || warn "node غير موجود"
  command_exists pnpm && ok "pnpm: $(pnpm --version)" || warn "pnpm غير موجود"
  command_exists redis-cli && ok "redis-cli موجود" || warn "redis-cli غير موجود"

  if command_exists redis-cli; then
    redis-cli ping >/dev/null 2>&1 && ok "Redis يستجيب" || warn "Redis لا يستجيب"
  fi

  [[ -f .env ]] && ok ".env موجود" || warn ".env غير موجود"

  if [[ -f .env ]]; then
    _load_env

    [[ -n "${ADMIN_SESSION_SECRET:-}" && "${#ADMIN_SESSION_SECRET}" -ge 32 ]] \
      && ok "ADMIN_SESSION_SECRET مضبوط" \
      || warn "ADMIN_SESSION_SECRET مفقود/قصير"

    [[ "${ADMIN_PASSWORD_HASH_ADMIN:-}" == \$2*\$* ]] \
      && ok "ADMIN_PASSWORD_HASH_ADMIN bcrypt موجود" \
      || warn "ADMIN_PASSWORD_HASH_ADMIN غير مضبوط"

    [[ -n "${SUPABASE_URL:-}" ]] \
      && ok "SUPABASE_URL موجود" \
      || warn "SUPABASE_URL مفقود"

    [[ -n "${OPENAI_API_KEY:-}" ]] \
      && ok "OPENAI_API_KEY موجود" \
      || warn "OPENAI_API_KEY مفقود"
  fi

  [[ -f domain.yml ]] && ok "domain.yml موجود" || fail "domain.yml مفقود"
  [[ -d domain ]] && ok "domain/ موجود" || fail "domain/ مفقود"
  [[ -d data ]] && ok "data/ موجود" || fail "data/ مفقود"
  [[ -f config.yml ]] && ok "config.yml موجود" || fail "config.yml مفقود"

  _runtime_render

  local model
  model="$(_latest_model)"
  [[ -n "$model" ]] && ok "آخر model: $model" || warn "لا يوجد model مدرب داخل models/"

  echo ""
  ok "doctor اكتمل"
}

cmd_audit() {
  _runtime_render
  _yaml_check
  _training_audit
}

cmd_check() {
  if [[ -f scripts/prod-check.sh ]]; then
    bash scripts/prod-check.sh
  else
    warn "scripts/prod-check.sh غير موجود — تشغيل audit بدلاً منه"
    cmd_audit
  fi
}

# ══════════════════════════════════════════════════════════════
#  validate/train/test
# ══════════════════════════════════════════════════════════════

cmd_validate() {
  _load_env
  _runtime_render
  _yaml_check
  _training_audit

  log "تشغيل rasa data validate على الدومين النهائي..."
  _rasa data validate --domain "$DOMAIN_FILE" --data data/ --endpoints "$ENDPOINTS_FILE"

  ok "rasa data validate نجح"
}

cmd_train() {
  local force=false
  local args=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force)
        force=true
        args+=("$1")
        shift
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done

  _assert_not_production_training "$force"
  cmd_validate

  if [[ -x scripts/train-prod.sh ]]; then
    log "تشغيل سكربت التدريب الرسمي scripts/train-prod.sh..."
    bash scripts/train-prod.sh "${args[@]}"
  else
    warn "scripts/train-prod.sh غير موجود/غير تنفيذي — تشغيل rasa train مباشرة"

    mkdir -p models
    _rasa train \
      --domain "$DOMAIN_FILE" \
      --data data/ \
      --config config.yml \
      --out models/ \
      --fixed-model-name "alazab-$(date +%Y%m%d-%H%M)"
  fi

  local model
  model="$(_latest_model)"
  [[ -n "$model" ]] && ok "تم إنتاج model: $model" || fail "التدريب انتهى بدون model داخل models/"
}

cmd_test() {
  _load_env
  _runtime_render

  log "تشغيل rasa test بالدومين النهائي..."

  if [[ -d tests ]]; then
    _rasa test --domain "$DOMAIN_FILE" --config config.yml
  else
    warn "مجلد tests غير موجود — تشغيل test عام قد لا يفحص قصص حقيقية"
    _rasa test --domain "$DOMAIN_FILE" --config config.yml \
      || warn "rasa test فشل أو لا توجد بيانات اختبار كافية"
  fi
}

cmd_release() {
  _assert_not_production_training false

  log "Local production candidate: validate → train → test → frontend → check"

  cmd_validate
  cmd_train
  cmd_test
  cmd_frontend_preflight || warn "frontend preflight فشل — لا تعتبر النسخة جاهزة للرفع"
  cmd_check || warn "production check فيه مشاكل — راجع التقرير"

  ok "release المحلي انتهى. لا ترفع GitHub إلا بعد مراجعة التحذيرات أعلاه."
}

# ══════════════════════════════════════════════════════════════
#  local services
# ══════════════════════════════════════════════════════════════

cmd_on() {
  _load_env
  _runtime_render

  if _has_systemd_units && [[ "${AZ_FORCE_LOCAL:-false}" != "true" ]]; then
    log "systemd مكتشف — تشغيل services"
    sudo systemctl start azabot-actions azabot-rasa azabot-webhook
    sleep 2
    cmd_status
    return 0
  fi

  local py rasa_bin
  py="$(_venv_python)" || fail "python غير موجود"
  rasa_bin="$(_venv_rasa)" || fail "rasa غير مثبت"

  local rasa_pid actions_pid webhook_pid
  actions_pid="$(_port_pid "$ACTIONS_PORT")"
  rasa_pid="$(_port_pid "$RASA_PORT")"
  webhook_pid="$(_port_pid "$WEBHOOK_PORT")"

  [[ -n "$actions_pid" ]] && warn "بورت actions $ACTIONS_PORT مستخدم PID=$actions_pid"
  [[ -n "$rasa_pid" ]] && warn "بورت rasa $RASA_PORT مستخدم PID=$rasa_pid"
  [[ -n "$webhook_pid" ]] && warn "بورت webhook $WEBHOOK_PORT مستخدم PID=$webhook_pid"

  _start_one actions "$rasa_bin" run actions --port "$ACTIONS_PORT"
  sleep 2

  _start_one rasa "$rasa_bin" run \
    --interface "$RASA_HOST" \
    --port "$RASA_PORT" \
    --endpoints "$ENDPOINTS_FILE" \
    --credentials credentials.yml \
    --enable-api

  sleep 3

  _start_one webhook "$py" -m uvicorn webhook.server:app \
    --host "$WEBHOOK_HOST" \
    --port "$WEBHOOK_PORT"

  sleep 2

  cmd_status
}

cmd_off() {
  if _has_systemd_units && [[ "${AZ_FORCE_LOCAL:-false}" != "true" ]]; then
    log "systemd مكتشف — إيقاف services"
    sudo systemctl stop azabot-webhook azabot-rasa azabot-actions
    ok "تم إيقاف systemd services"
    return 0
  fi

  _stop_one webhook
  _stop_one rasa
  _stop_one actions
}

cmd_restart() {
  cmd_off
  sleep 1
  cmd_on
}

cmd_status() {
  if _has_systemd_units && [[ "${AZ_FORCE_LOCAL:-false}" != "true" ]]; then
    for svc in azabot-actions azabot-rasa azabot-webhook; do
      if systemctl is-active --quiet "$svc"; then
        ok "$svc يعمل"
      else
        warn "$svc متوقف"
      fi
    done
  else
    for name in actions rasa webhook; do
      local pidfile="$PID_DIR/${name}.pid"

      if [[ -f "$pidfile" ]]; then
        local pid
        pid="$(cat "$pidfile" 2>/dev/null || true)"

        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
          ok "$name يعمل PID=$pid"
        else
          warn "$name متوقف pidfile قديم"
        fi
      else
        warn "$name متوقف"
      fi
    done
  fi

  echo ""
  printf '  rasa     /version → HTTP %s\n' "$(_http_code "http://127.0.0.1:${RASA_PORT}/version")"
  printf '  webhook  /health  → HTTP %s\n' "$(_http_code "http://127.0.0.1:${WEBHOOK_PORT}/health")"
}

cmd_logs() {
  local svc="${1:-webhook}"

  if _has_systemd_units && [[ "${AZ_FORCE_LOCAL:-false}" != "true" ]]; then
    [[ "$svc" == azabot-* ]] || svc="azabot-$svc"
    sudo journalctl -u "$svc" -f
    return 0
  fi

  case "$svc" in
    actions|rasa|webhook)
      ;;
    *)
      fail "service غير معروف: $svc — استخدم actions أو rasa أو webhook"
      ;;
  esac

  touch "$LOG_DIR/${svc}.out.log" "$LOG_DIR/${svc}.err.log"
  tail -f "$LOG_DIR/${svc}.out.log" "$LOG_DIR/${svc}.err.log"
}

cmd_heal() {
  log "إصلاح التشغيل المحلي: إيقاف pidfiles وتحرير البورتات عند اللزوم"

  cmd_off || true

  for port in "$ACTIONS_PORT" "$RASA_PORT" "$WEBHOOK_PORT"; do
    local pid
    pid="$(_port_pid "$port")"

    if [[ -n "$pid" ]]; then
      warn "قتل عملية عالقة على port=$port PID=$pid"
      kill -9 "$pid" 2>/dev/null || true
    fi
  done

  rm -f "$PID_DIR"/*.pid
  ok "heal اكتمل"
}

cmd_smoke() {
  log "اختبار سريع للخدمات المحلية..."

  local health
  health="$(_http_code "http://127.0.0.1:${WEBHOOK_PORT}/health")"

  [[ "$health" == "200" ]] && ok "webhook /health OK" || fail "webhook /health HTTP=$health"

  log "اختبار /chat برسالة عربية بسيطة..."

  curl -sS -X POST "http://127.0.0.1:${WEBHOOK_PORT}/chat" \
    -H 'Content-Type: application/json' \
    -d '{"sender_id":"local-smoke","message":"مرحبا","brand":"uberfix"}' \
    | python3 -m json.tool || warn "رد /chat ليس JSON متوقع"
}

# ══════════════════════════════════════════════════════════════
#  frontend
# ══════════════════════════════════════════════════════════════

cmd_frontend_install() {
  [[ -d azabot ]] || fail "مجلد azabot غير موجود"
  command_exists pnpm || fail "pnpm غير مثبت"

  (cd azabot && pnpm install)
}

cmd_frontend_preflight() {
  [[ -d azabot ]] || {
    warn "مجلد azabot غير موجود — تخطي frontend"
    return 0
  }

  command_exists pnpm || {
    warn "pnpm غير موجود — تخطي frontend"
    return 1
  }

  log "frontend type-check..."
  (cd azabot && pnpm type-check)

  log "frontend test..."
  (cd azabot && pnpm test)

  log "frontend build..."
  (cd azabot && pnpm build)

  if (cd azabot && pnpm run | grep -q 'check:prod'); then
    log "frontend production check..."
    (cd azabot && pnpm check:prod)
  fi

  ok "frontend preflight نجح"
}

cmd_frontend_build() {
  [[ -d azabot ]] || fail "مجلد azabot غير موجود"
  command_exists pnpm || fail "pnpm غير مثبت"

  (cd azabot && pnpm build)
}

# ══════════════════════════════════════════════════════════════
#  misc
# ══════════════════════════════════════════════════════════════

cmd_db_init() {
  _load_env
  _require_file database/setup.sql

  local url="${DB_URL:-postgresql://${DB_USER:-postgres}:${SUPABASE_DB_PASSWORD:-}@${DB_HOST:-}:${DB_PORT:-5432}/${DB_NAME:-postgres}}"

  [[ "$url" == *':@'* || "$url" == *'@:5432'* ]] && warn "DB URL يبدو ناقصاً — راجع .env"
  command_exists psql || fail "psql غير مثبت"

  log "تنفيذ database/setup.sql..."
  psql "$url" -f database/setup.sql

  ok "db-init اكتمل"
}

cmd_passwd() {
  _require_file scripts/gen_password_hash.py
  _python scripts/gen_password_hash.py
}

cmd_untrack() {
  _require_file scripts/git-untrack-secrets.sh
  bash scripts/git-untrack-secrets.sh
}

cmd_clean() {
  log "تنظيف ملفات مؤقتة..."

  find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache \) -prune -exec rm -rf {} + 2>/dev/null || true
  find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete 2>/dev/null || true
  rm -rf .rasa 2>/dev/null || true

  ok "clean اكتمل"
}

cmd_models() {
  log "نماذج Rasa المتاحة:"
  ls -lh models/*.tar.gz 2>/dev/null || warn "لا يوجد models/*.tar.gz"
}

cmd_runtime() {
  _runtime_render

  echo ""
  wc -l "$DOMAIN_FILE" "$ENDPOINTS_FILE"
}

cmd_deploy() {
  [[ $EUID -eq 0 ]] || fail "deploy يحتاج root: sudo bash az.sh deploy"
  _require_file deploy/production/deploy-production.sh

  bash deploy/production/deploy-production.sh
}

# ══════════════════════════════════════════════════════════════
#  help/router
# ══════════════════════════════════════════════════════════════

cmd_help() {
  cat <<USAGE
${BOLD}az.sh — التحكم المحلي والإنتاجي في AzaBot${NC}

${CYAN}الإعداد والفحص${NC}
  setup                  تثبيت Python deps + إنشاء .env + runtime
  install                تثبيت Python deps فقط
  doctor                 فحص البيئة والمسارات والأسرار الأساسية
  runtime                توليد .runtime/domain.generated.yml و endpoints
  audit                  YAML + training audit
  check                  prod-check إن وجد، وإلا audit

${CYAN}Rasa / Training${NC}
  validate               runtime + yaml + audit + rasa data validate
  train [--force]        validate ثم تدريب model جديد
  test                   rasa test بالدومين النهائي
  models                 عرض النماذج الموجودة
  release                validate → train → test → frontend → check

${CYAN}التشغيل المحلي${NC}
  on                     تشغيل actions + rasa + webhook
  off                    إيقاف الخدمات
  restart                إعادة تشغيل الخدمات
  status                 حالة الخدمات و HTTP health
  logs [service]         logs actions|rasa|webhook
  smoke                  اختبار /health و /chat
  heal                   قتل العمليات العالقة وتنظيف pidfiles

${CYAN}Frontend${NC}
  frontend-install       pnpm install داخل azabot
  frontend-preflight     type-check + test + build + check:prod
  frontend-build         build فقط

${CYAN}DB / Security / Ops${NC}
  db-init                تنفيذ database/setup.sql
  passwd                 توليد password hashes
  untrack                تنظيف git من الملفات الحساسة
  deploy                 نشر production عبر deploy script، يحتاج sudo
  clean                  تنظيف cache/pyc

${YELLOW}أوامر العمل المحلي قبل GitHub:${NC}
  bash az.sh doctor
  NODE_ENV=dev bash az.sh validate
  NODE_ENV=dev bash az.sh train
  NODE_ENV=dev bash az.sh test
  bash az.sh on
  bash az.sh smoke
USAGE
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  setup)              cmd_setup "$@" ;;
  install)            cmd_install "$@" ;;
  doctor)             cmd_doctor "$@" ;;
  runtime)            cmd_runtime "$@" ;;
  audit)              cmd_audit "$@" ;;
  check)              cmd_check "$@" ;;

  validate)           cmd_validate "$@" ;;
  train)              cmd_train "$@" ;;
  test)               cmd_test "$@" ;;
  models)             cmd_models "$@" ;;
  release)            cmd_release "$@" ;;

  on)                 cmd_on "$@" ;;
  off)                cmd_off "$@" ;;
  restart)            cmd_restart "$@" ;;
  status)             cmd_status "$@" ;;
  logs)               cmd_logs "$@" ;;
  smoke)              cmd_smoke "$@" ;;
  heal)               cmd_heal "$@" ;;

  frontend-install)   cmd_frontend_install "$@" ;;
  frontend-preflight) cmd_frontend_preflight "$@" ;;
  frontend-build)     cmd_frontend_build "$@" ;;

  db-init)            cmd_db_init "$@" ;;
  passwd)             cmd_passwd "$@" ;;
  untrack)            cmd_untrack "$@" ;;
  deploy)             cmd_deploy "$@" ;;
  clean)              cmd_clean "$@" ;;

  help|-h|--help)     cmd_help ;;
  *)
    warn "أمر غير معروف: $cmd"
    echo ""
    cmd_help
    exit 1
    ;;
esac