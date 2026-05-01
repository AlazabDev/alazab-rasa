#!/usr/bin/env bash
# Unified operations helper for Alazab Rasa/AzaBot on Ubuntu/WSL.
# Usage: bash scripts/botctl.sh <command> [options]
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ENV_FILE="${ENV_FILE:-.env}"
ENDPOINTS_FILE="${ENDPOINTS_FILE:-endpoints.nodocker.yml}"
VENV_DIR="${VENV_DIR:-.venv}"
RUNTIME_DIR="${RUNTIME_DIR:-.runtime}"
LOG_DIR="${LOG_DIR:-logs}"
PID_DIR="$RUNTIME_DIR/pids"

PYTHON_BIN="${PYTHON_BIN:-}"
WEBHOOK_WORKERS="${WEBHOOK_WORKERS:-1}"
RASA_PORT="${RASA_PORT:-5005}"
ACTIONS_PORT="${ACTIONS_PORT:-5055}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"
HOST="${HOST:-127.0.0.1}"

BLUE=$'\033[1;34m'
GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'
NC=$'\033[0m'

log() { printf '%s[botctl]%s %s\n' "$BLUE" "$NC" "$*"; }
ok() { printf '%s[ok]%s %s\n' "$GREEN" "$NC" "$*"; }
warn() { printf '%s[warn]%s %s\n' "$YELLOW" "$NC" "$*"; }
fail() { printf '%s[fail]%s %s\n' "$RED" "$NC" "$*" >&2; exit 1; }

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
  start               Start actions, rasa, and webhook as background processes.
  stop                Stop background processes started by this script.
  restart             Stop then start.
  status              Show process and HTTP health status.
  logs [service]      Tail logs. service: actions, rasa, webhook, or all.
  smoke               Hit health, brands, and chat endpoints.
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
  load_env
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa data validate
}

cmd_train() {
  load_env
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa train --force
  ok "Rasa model trained."
}

cmd_test() {
  load_env
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  run_checked rasa test e2e tests/e2e_test_cases/
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

cmd_start() {
  ensure_dirs
  load_env
  activate_venv
  require_env RASA_PRO_LICENSE OPENAI_API_KEY
  [[ -f "$ENDPOINTS_FILE" ]] || fail "Missing endpoints file: $ENDPOINTS_FILE"

  for port in "$ACTIONS_PORT" "$RASA_PORT" "$WEBHOOK_PORT"; do
    if port_busy "$port"; then
      fail "Port $port is already in use. Run status/stop or free the port."
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

cmd_stop() {
  ensure_dirs
  local stopped=false
  for service in webhook rasa actions; do
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
  for service in actions rasa webhook; do
    local pid
    pid="$(read_pid "$service" || true)"
    if is_running "$pid"; then
      ok "$service running: $pid"
    else
      warn "$service stopped"
    fi
  done
  curl -fsS "http://127.0.0.1:${ACTIONS_PORT}/health" >/dev/null 2>&1 && ok "Actions HTTP healthy" || warn "Actions HTTP unavailable"
  curl -fsS "http://127.0.0.1:${RASA_PORT}/" >/dev/null 2>&1 && ok "Rasa HTTP healthy" || warn "Rasa HTTP unavailable"
  curl -fsS "http://127.0.0.1:${WEBHOOK_PORT}/health" >/dev/null 2>&1 && ok "Webhook HTTP healthy" || warn "Webhook HTTP unavailable"
}

cmd_logs() {
  ensure_dirs
  local service="${1:-all}"
  case "$service" in
    actions|rasa|webhook) tail -n 120 -f "$LOG_DIR/$service.out.log" ;;
    all) tail -n 80 -f "$LOG_DIR/actions.out.log" "$LOG_DIR/rasa.out.log" "$LOG_DIR/webhook.out.log" ;;
    *) fail "Unknown log service: $service" ;;
  esac
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
  stop) cmd_stop "$@" ;;
  restart) cmd_stop; cmd_start "$@" ;;
  status) cmd_status "$@" ;;
  logs) cmd_logs "$@" ;;
  smoke) cmd_smoke "$@" ;;
  docker-up) cmd_docker_up "$@" ;;
  docker-down) cmd_docker_down "$@" ;;
  prod-preflight) cmd_prod_preflight "$@" ;;
  prod-readiness) cmd_prod_readiness "$@" ;;
  prod-up) cmd_prod_up "$@" ;;
  prod-down) cmd_prod_down "$@" ;;
  *) usage; fail "Unknown command: $cmd" ;;
esac
