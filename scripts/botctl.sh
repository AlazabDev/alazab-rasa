#!/usr/bin/env bash
# Unified operations helper for Alazab Rasa/AzaBot on Ubuntu/WSL.
# Usage: bash scripts/botctl.sh <command> [options]
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ENV_FILE="${ENV_FILE:-.env}"
VENV_DIR="${VENV_DIR:-.venv}"
RUNTIME_DIR="${RUNTIME_DIR:-.runtime}"
ENDPOINTS_FILE="${ENDPOINTS_FILE:-$RUNTIME_DIR/endpoints.generated.yml}"
RUNTIME_DOMAIN_FILE="${RUNTIME_DOMAIN_FILE:-$RUNTIME_DIR/domain.generated.yml}"
LOG_DIR="${LOG_DIR:-logs}"
PID_DIR="$RUNTIME_DIR/pids"

PYTHON_BIN="${PYTHON_BIN:-}"
WEBHOOK_WORKERS="${WEBHOOK_WORKERS:-1}"
RASA_PORT="${RASA_PORT:-5005}"
ACTIONS_PORT="${ACTIONS_PORT:-5055}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"
HOST="${HOST:-127.0.0.1}"

BLUE=$'\033[1;34m'
GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'
PURPLE=$'\033[1;35m'
NC=$'\033[0m'

log() { printf '%s🔵 [info]%s %s\n' "$BLUE" "$NC" "$*"; }
ok() { printf '%s🟢 [ok]%s %s\n' "$GREEN" "$NC" "$*"; }
warn() { printf '%s🟡 [warn]%s %s\n' "$YELLOW" "$NC" "$*"; }
work() { printf '%s🟣 [work]%s %s\n' "$PURPLE" "$NC" "$*"; }
fail() { printf '%s🔴 [fail]%s %s\n' "$RED" "$NC" "$*" >&2; exit 1; }

usage() {
  cat <<'USAGE'
Alazab bot operations helper.

Commands:
  doctor              Check local tools, env file, Python syntax, and optional Docker.
  setup               Create venv and install Python dependencies.
  frontend            Install/build AzaBot frontend with pnpm.
  validate            Run rasa data validate.
  train               Train the Rasa model.
  test                Run Rasa E2E tests.
  preflight           Run doctor + validate + Python syntax check.
  dev                 Start everything: backend + frontend dev server (single command).
  start [--force]     Start actions, rasa, and webhook. --force frees ports first.
  stop                Stop background processes started by this script.
  restart [--heal]    Stop then start. --heal runs automatic repair first.
  status [--verbose]  Show process and HTTP health status; verbose adds ports/resources.
  logs [--errors] [service]  Tail logs, optionally only important errors.
  smoke               Hit health, brands, and chat endpoints.
  heal                Render endpoints fallback, validate YAML, and clear stale ports.
  docker-up           Start docker/docker-compose.yaml.
  docker-down         Stop docker/docker-compose.yaml.
  prod-preflight      Validate production compose and required env values.
  prod-readiness      Run static production readiness checks.
  prod-up             Start docker/docker-compose.prod.yaml.
  prod-down           Stop docker/docker-compose.prod.yaml.

Options via environment:
  ENV_FILE=.env
  VENV_DIR=.venv
  PYTHON_BIN=python3.10
  HOST=127.0.0.1
  RASA_PORT=5005
  ACTIONS_PORT=5055
  WEBHOOK_PORT=8000
  WEBHOOK_WORKERS=1

Examples:
  bash scripts/botctl.sh setup
  bash scripts/botctl.sh train
  bash scripts/botctl.sh start
  bash scripts/botctl.sh status
  bash scripts/botctl.sh logs webhook
USAGE
}

ensure_dirs() {
  mkdir -p "$RUNTIME_DIR" "$PID_DIR" "$LOG_DIR" models
}

choose_python() {
  if [[ -n "$PYTHON_BIN" ]]; then
    command -v "$PYTHON_BIN" >/dev/null 2>&1 || fail "Python not found: $PYTHON_BIN"
    return
  fi
  if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN=python3.11
  elif command -v python3.10 >/dev/null 2>&1; then
    PYTHON_BIN=python3.10
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  else
    fail "Missing python3.11/python3.10/python3"
  fi
}

load_env() {
  [[ -f "$ENV_FILE" ]] || fail "Missing env file: $ENV_FILE"

  # Export simple KEY=VALUE lines without evaluating shell code.
  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    raw_line="${raw_line%$'\r'}"
    [[ -z "${raw_line//[[:space:]]/}" || "$raw_line" =~ ^[[:space:]]*# ]] && continue
    [[ "$raw_line" == *"="* ]] || continue

    local key="${raw_line%%=*}"
    local value="${raw_line#*=}"
    key="$(printf '%s' "$key" | xargs)"
    [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue

    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    if [[ "$value" == \"*\" && "$value" == *\" ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
      value="${value:1:${#value}-2}"
    fi
    export "$key=$value"
  done < "$ENV_FILE"

  export PYTHONUTF8=1
  export PYTHONIOENCODING=utf-8
  export RASA_TELEMETRY_ENABLED=false

  if [[ "${RASA_URL:-}" == "http://rasa:5005" || -z "${RASA_URL:-}" ]]; then
    export RASA_URL="http://127.0.0.1:${RASA_PORT}"
  fi
  if [[ "${ACTION_SERVER_URL:-}" == "http://rasa-actions:5055/webhook" || -z "${ACTION_SERVER_URL:-}" ]]; then
    export ACTION_SERVER_URL="http://127.0.0.1:${ACTIONS_PORT}/webhook"
  fi
  if [[ "${DB_HOST:-}" == "postgres" ]]; then
    export DB_HOST=127.0.0.1
  fi
  if [[ "${REDIS_HOST:-}" == "redis" ]]; then
    export REDIS_HOST=127.0.0.1
  fi
  export REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
  export REDIS_PORT="${REDIS_PORT:-6379}"
  export REDIS_DB="${REDIS_DB:-0}"
  export REDIS_LOCK_DB="${REDIS_LOCK_DB:-1}"
  export REDIS_PASSWORD="${REDIS_PASSWORD:-}"
  export REDIS_KEY_PREFIX="${REDIS_KEY_PREFIX:-alazab}"
  export REDIS_USE_SSL="${REDIS_USE_SSL:-false}"
  # endpoints.yml uses REDIS_HOST directly now - also export for legacy compat.
  export REDIS_URL="$REDIS_HOST"
}

require_env() {
  local missing=()
  for name in "$@"; do
    local value="${!name:-}"
    if [[ -z "$value" || "$value" == *"replace-with"* || "$value" == *"change-this"* ]]; then
      missing+=("$name")
    fi
  done
  if (( ${#missing[@]} > 0 )); then
    printf '%s\n' "${missing[@]}" | sed 's/^/  - /'
    fail "Required environment variables are missing or placeholders."
  fi
}

activate_venv() {
  choose_python
  [[ -d "$VENV_DIR" ]] || fail "Virtualenv not found: $VENV_DIR. Run: bash scripts/botctl.sh setup"
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
}

run_checked() {
  log "$*"
  "$@"
}

port_busy() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn "( sport = :$port )" | grep -q ":$port"
  elif command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
  else
    return 1
  fi
}

wait_http() {
  local name="$1" url="$2" attempts="${3:-45}"
  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      ok "$name ready: $url"
      return 0
    fi
    sleep 2
  done
  fail "$name did not become ready: $url"
}

write_pid() {
  local service="$1" pid="$2"
  printf '%s\n' "$pid" > "$PID_DIR/$service.pid"
}

read_pid() {
  local service="$1"
  [[ -f "$PID_DIR/$service.pid" ]] && cat "$PID_DIR/$service.pid"
}

is_running() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" >/dev/null 2>&1
}

cmd_doctor() {
  ensure_dirs
  choose_python
  log "Project: $ROOT_DIR"
  ok "Python: $("$PYTHON_BIN" --version 2>&1)"
  command -v curl >/dev/null 2>&1 && ok "curl available" || warn "curl is missing"
  command -v docker >/dev/null 2>&1 && ok "docker available" || warn "docker is not installed or not in PATH"
  command -v pnpm >/dev/null 2>&1 && ok "pnpm available" || warn "pnpm is missing; frontend build will need corepack/pnpm"
  [[ -f "$ENV_FILE" ]] && ok "$ENV_FILE exists" || warn "$ENV_FILE is missing"
  [[ -f "$ENDPOINTS_FILE" ]] && ok "$ENDPOINTS_FILE exists" || warn "$ENDPOINTS_FILE is missing"
  "$PYTHON_BIN" -m compileall actions webhook >/dev/null
  ok "Python syntax check passed"
}

cmd_setup() {
  ensure_dirs
  choose_python
  [[ -f "$ENV_FILE" ]] || warn "$ENV_FILE is missing. Create it from .env.example before running the bot."
  if [[ ! -d "$VENV_DIR" ]]; then
    run_checked "$PYTHON_BIN" -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  run_checked python -m pip install --upgrade pip setuptools wheel
  if [[ -f pyproject.toml ]]; then
    run_checked pip install -e ".[dev]"
  else
    run_checked pip install -r requirements.txt
  fi
  ok "Python environment is ready: $VENV_DIR"
}

cmd_frontend() {
  if ! command -v pnpm >/dev/null 2>&1; then
    if command -v corepack >/dev/null 2>&1; then
      run_checked corepack enable
    else
      fail "pnpm/corepack is missing. Install Node.js 22+ then rerun."
    fi
  fi
  (cd azabot && run_checked pnpm install --frozen-lockfile)
  (cd azabot && run_checked pnpm lint)
  (cd azabot && run_checked pnpm test)
  (cd azabot && run_checked pnpm build)
  ok "Frontend build is ready: azabot/dist"
}

cmd_validate() {
  ensure_dirs
  load_env
  python3 scripts/render_runtime_domain.py >/dev/null
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa data validate --domain "$RUNTIME_DOMAIN_FILE"
}

cmd_train() {
  ensure_dirs
  load_env
  python3 scripts/render_runtime_domain.py >/dev/null
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa train --domain "$RUNTIME_DOMAIN_FILE" --force
  ok "Rasa model trained."
}

cmd_test() {
  ensure_dirs
  load_env
  python3 scripts/render_runtime_domain.py >/dev/null
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa test e2e tests/e2e_test_cases/ --domain "$RUNTIME_DOMAIN_FILE"
}

cmd_preflight() {
  cmd_doctor
  load_env
  require_env RASA_PRO_LICENSE OPENAI_API_KEY DB_NAME DB_USER DB_PASSWORD REDIS_PASSWORD
  cmd_validate
}

start_one() {
  local service="$1"
  local logfile="$2"
  shift 2
  local old_pid
  old_pid="$(read_pid "$service" || true)"
  if is_running "$old_pid"; then
    warn "$service already running: $old_pid"
    return
  fi
  log "Starting $service"
  nohup "$@" > "$logfile" 2>&1 &
  write_pid "$service" "$!"
  ok "$service started: $!"
}


# ── تحرير المنافذ بالقوة ─────────────────────────────────────────
force_free_port() {
  local port="$1"
  local pid
  pid=$(lsof -ti ":$port" 2>/dev/null | head -1 || true)
  if [[ -n "$pid" ]]; then
    local pname; pname=$(ps -p "$pid" -o comm= 2>/dev/null || echo "?")
    warn "Port $port مشغول بـ $pname (PID $pid) — إيقاف..."
    kill -TERM "$pid" 2>/dev/null || true
    sleep 2; kill -KILL "$pid" 2>/dev/null || true
    ok "Port $port محرر"
  fi
}
redis_available() {
  local host="${REDIS_HOST:-127.0.0.1}" port="${REDIS_PORT:-6379}"
  if command -v redis-cli >/dev/null 2>&1; then
    redis-cli -h "$host" -p "$port" ${REDIS_PASSWORD:+-a "$REDIS_PASSWORD"} ping 2>/dev/null | grep -qi PONG
    return
  fi
  timeout 1 bash -c "</dev/tcp/$host/$port" >/dev/null 2>&1
}

render_runtime_endpoints() {
  ensure_dirs
  if redis_available; then
    cp endpoints.yml "$ENDPOINTS_FILE"
    ok "Redis tracker/lock store selected: $ENDPOINTS_FILE"
  else
    cp endpoints.sqlite.yml "$ENDPOINTS_FILE"
    warn "Redis unavailable; using SQLite fallback: $ENDPOINTS_FILE"
  fi
}

cmd_heal() {
  ensure_dirs
  work "Running auto-heal checks"
  for port in "$ACTIONS_PORT" "$RASA_PORT" "$WEBHOOK_PORT" "$FRONTEND_PORT"; do
    force_free_port "$port" 2>/dev/null || true
  done
  load_env
  render_runtime_endpoints
  python3 scripts/render_runtime_domain.py >/dev/null
  python3 scripts/deep_clean.py --validate-only || fail "YAML/domain validation failed"
  ok "Auto-heal completed"
}

cmd_start() {
  ensure_dirs
  local force=false
  if [[ "${1:-}" == "--force" ]]; then
    force=true
    shift || true
  fi
  load_env
  if $force; then
    work "Freeing service ports before start"
    for _port in "${ACTIONS_PORT}" "${RASA_PORT}" "${WEBHOOK_PORT}" "${FRONTEND_PORT}"; do
      force_free_port "$_port" 2>/dev/null || true
    done
  fi
  render_runtime_endpoints
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  [[ -f "$ENDPOINTS_FILE" ]] || fail "Missing endpoints file: $ENDPOINTS_FILE"

  for port in "$ACTIONS_PORT" "$RASA_PORT" "$WEBHOOK_PORT"; do
    if port_busy "$port"; then
      fail "Port $port is already in use. Run: bash scripts/botctl.sh start --force"
    fi
  done

  start_one actions "$LOG_DIR/actions.out.log" rasa run actions --port "$ACTIONS_PORT"
  wait_http "Actions" "http://127.0.0.1:${ACTIONS_PORT}/health" 30

  start_one rasa "$LOG_DIR/rasa.out.log" rasa run \
    --enable-api \
    --cors "${ALLOWED_ORIGINS:-http://127.0.0.1:${WEBHOOK_PORT}}" \
    --port "$RASA_PORT" \
    --endpoints "$ENDPOINTS_FILE"
  wait_http "Rasa" "http://127.0.0.1:${RASA_PORT}/" 60

  start_one webhook "$LOG_DIR/webhook.out.log" uvicorn webhook.server:app \
    --host "$HOST" \
    --port "$WEBHOOK_PORT" \
    --workers "$WEBHOOK_WORKERS"
  wait_http "Webhook" "http://127.0.0.1:${WEBHOOK_PORT}/health" 45

  ok "Bot is running at http://127.0.0.1:${WEBHOOK_PORT}"
}


cmd_dev() {
  # ── 1. تشغيل الباك اند ──────────────────────────────────────
  cmd_start

  # ── 2. تحقق من pnpm ─────────────────────────────────────────
  if ! command -v pnpm >/dev/null 2>&1; then
    warn "pnpm غير موجود — الفرونت لن يُشغَّل"
    warn "لتثبيته: npm install -g pnpm  ثم أعد التشغيل"
    ok "الباك اند يعمل على http://127.0.0.1:${WEBHOOK_PORT}"
    return 0
  fi

  # ── 3. تثبيت deps الفرونت إن لزم ───────────────────────────
  if [[ ! -d "azabot/node_modules" ]]; then
    log "تثبيت packages الفرونت..."
    (cd azabot && pnpm install --frozen-lockfile)
  fi

  # ── 4. تشغيل Vite dev server ────────────────────────────────
  log "تشغيل الفرونت (Vite dev) على port ${FRONTEND_PORT:-8080}..."
  FRONTEND_LOGFILE="$LOG_DIR/frontend.out.log"
  local old_pid
  old_pid="$(read_pid "frontend" || true)"
  if is_running "$old_pid"; then
    warn "الفرونت يعمل بالفعل: $old_pid"
  else
    nohup bash -c "cd azabot && VITE_DEV_BACKEND_URL=http://127.0.0.1:${WEBHOOK_PORT} pnpm dev"       > "$FRONTEND_LOGFILE" 2>&1 &
    write_pid "frontend" "$!"
    ok "الفرونت شغّال: PID $!"
  fi

  # ── 5. انتظر الفرونت ─────────────────────────────────────────
  wait_http "Frontend" "http://127.0.0.1:${FRONTEND_PORT:-8080}" 30

  echo ""
  ok "══════════════════════════════════════════"
  ok " 🚀 كل الخدمات شغّالة!"
  ok " Frontend : http://localhost:${FRONTEND_PORT:-8080}"
  ok " Backend  : http://localhost:${WEBHOOK_PORT}"
  ok " Rasa     : http://localhost:${RASA_PORT}"
  ok " Actions  : http://localhost:${ACTIONS_PORT}"
  ok "══════════════════════════════════════════"
  ok " لوقف كل شيء: bash scripts/botctl.sh stop"
  ok " للسجلات:     bash scripts/botctl.sh logs all"
  ok "══════════════════════════════════════════"
}

cmd_stop() {
  ensure_dirs
  local stopped=false
  for service in frontend webhook rasa actions; do
    local pid
    pid="$(read_pid "$service" || true)"
    if is_running "$pid"; then
      log "Stopping $service ($pid)"
      kill "$pid" || true
      stopped=true
    fi
    rm -f "$PID_DIR/$service.pid"
  done
  $stopped && ok "Stopped bot services." || warn "No botctl-managed services were running."
}

cmd_status() {
  ensure_dirs
  local verbose=false
  if [[ "${1:-}" == "--verbose" ]]; then verbose=true; fi
  echo ""
  printf "%-20s %-10s %-12s %s\n" "الخدمة" "PID" "Process" "HTTP"
  printf "%-20s %-10s %-12s %s\n" "────────────────" "────────" "────────" "────────────────────────────"

  for service in actions rasa webhook frontend; do
    local pid url label
    pid="$(read_pid "$service" || true)"
    case "$service" in
      actions)  url="http://127.0.0.1:${ACTIONS_PORT}/health"; label="Actions  :${ACTIONS_PORT}" ;;
      rasa)     url="http://127.0.0.1:${RASA_PORT}/";          label="Rasa     :${RASA_PORT}" ;;
      webhook)  url="http://127.0.0.1:${WEBHOOK_PORT}/health"; label="Webhook  :${WEBHOOK_PORT}" ;;
      frontend) url="http://127.0.0.1:${FRONTEND_PORT}";       label="Frontend :${FRONTEND_PORT}" ;;
    esac
    local proc_status http_status
    if is_running "$pid"; then proc_status="${GREEN}● running${NC}"; else proc_status="${RED}○ stopped${NC}"; pid="-"; fi
    if curl -fsS "$url" >/dev/null 2>&1; then http_status="${GREEN}🟢 healthy${NC}"; else http_status="${YELLOW}🟡 offline${NC}"; fi
    printf "%-20s %-10s " "$label" "$pid"
    printf "$proc_status"
    printf "  "
    printf "$http_status\n"
    if $verbose && [[ "$pid" != "-" ]]; then
      ps -p "$pid" -o pid,ppid,%cpu,%mem,etime,cmd --no-headers 2>/dev/null || true
    fi
  done
  if $verbose; then
    echo ""
    log "Runtime endpoints: $ENDPOINTS_FILE"
    log "Runtime domain: $RUNTIME_DOMAIN_FILE"
    for port in "$RASA_PORT" "$ACTIONS_PORT" "$WEBHOOK_PORT" "$FRONTEND_PORT"; do
      if port_busy "$port"; then ok "Port $port is listening"; else warn "Port $port is not listening"; fi
    done
    free -h 2>/dev/null || true
  fi
  echo ""
}

cmd_logs() {
  ensure_dirs
  local errors_only=false service="all"
  if [[ "${1:-}" == "--errors" ]]; then errors_only=true; shift || true; fi
  service="${1:-all}"
  local files=()
  case "$service" in
    actions|rasa|webhook|frontend) files=("$LOG_DIR/$service.out.log") ;;
    all) files=("$LOG_DIR/actions.out.log" "$LOG_DIR/rasa.out.log" "$LOG_DIR/webhook.out.log" "$LOG_DIR/frontend.out.log") ;;
    *) fail "Unknown log service: $service" ;;
  esac
  if $errors_only; then
    grep -Eih "(error|exception|traceback|failed|critical|fatal|connection refused|timeout)" "${files[@]}" 2>/dev/null | tail -n 200 || true
  else
    tail -n 120 -f "${files[@]}" 2>/dev/null
  fi
}

cmd_smoke() {
  local base="http://127.0.0.1:${WEBHOOK_PORT}"
  wait_http "Webhook" "$base/health" 10
  curl -fsS "$base/brands" >/dev/null
  ok "Brands endpoint returned success"
  curl -fsS \
    -H "Content-Type: application/json; charset=utf-8" \
    -d '{"sender_id":"botctl_smoke","message":"مرحبا","channel":"website","site_host":"bot.alazab.com","site_path":"/"}' \
    "$base/chat" >/dev/null
  ok "Chat endpoint returned success"
}

cmd_docker_up() {
  run_checked docker compose --env-file "$ENV_FILE" -f docker/docker-compose.yaml up -d --build
}

cmd_docker_down() {
  run_checked docker compose --env-file "$ENV_FILE" -f docker/docker-compose.yaml down --remove-orphans
}

cmd_prod_preflight() {
  load_env
  require_env RASA_PRO_LICENSE OPENAI_API_KEY ADMIN_EMAIL ADMIN_PASSWORD ADMIN_SESSION_SECRET DB_NAME DB_USER DB_PASSWORD REDIS_PASSWORD PUBLIC_BASE_URL ALLOWED_ORIGINS
  run_checked docker compose --env-file "$ENV_FILE" -f docker/docker-compose.prod.yaml config
  ok "Production compose config is valid."
}

cmd_prod_readiness() {
  run_checked node scripts/production-readiness.mjs
}

cmd_prod_up() {
  cmd_prod_preflight
  run_checked docker compose --env-file "$ENV_FILE" -f docker/docker-compose.prod.yaml up -d --build
}

cmd_prod_down() {
  run_checked docker compose --env-file "$ENV_FILE" -f docker/docker-compose.prod.yaml down --remove-orphans
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  help|-h|--help) usage ;;
  doctor) cmd_doctor "$@" ;;
  setup) cmd_setup "$@" ;;
  frontend) cmd_frontend "$@" ;;
  validate) cmd_validate "$@" ;;
  train) cmd_train "$@" ;;
  test) cmd_test "$@" ;;
  preflight) cmd_preflight "$@" ;;
  start) cmd_start "$@" ;;
  dev) cmd_dev "$@" ;;
  stop) cmd_stop "$@" ;;
  restart) if [[ "${1:-}" == "--heal" ]]; then cmd_heal; shift || true; fi; cmd_stop; cmd_start "$@" ;;
  status) cmd_status "$@" ;;
  logs) cmd_logs "$@" ;;
  smoke) cmd_smoke "$@" ;;
  heal) cmd_heal "$@" ;;
  docker-up) cmd_docker_up "$@" ;;
  docker-down) cmd_docker_down "$@" ;;
  prod-preflight) cmd_prod_preflight "$@" ;;
  prod-readiness) cmd_prod_readiness "$@" ;;
  prod-up) cmd_prod_up "$@" ;;
  prod-down) cmd_prod_down "$@" ;;
  *) usage; fail "Unknown command: $cmd" ;;
esac
