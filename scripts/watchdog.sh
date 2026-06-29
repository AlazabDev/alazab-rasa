#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

RASA_PORT="${RASA_PORT:-5005}"
ACTIONS_PORT="${ACTIONS_PORT:-5055}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"
CHECK_INTERVAL="${CHECK_INTERVAL:-30}"
CPU_WARN="${CPU_WARN:-85}"
MEM_WARN="${MEM_WARN:-80}"
LOG_DIR="${LOG_DIR:-logs}"
WATCHDOG_LOG="$LOG_DIR/watchdog.log"
BOTCTL="bash scripts/botctl.sh"

BLUE=$'\033[1;34m'; GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; PURPLE=$'\033[1;35m'; NC=$'\033[0m'
info(){ printf '%s🔵 [watchdog]%s %s\n' "$BLUE" "$NC" "$*" | tee -a "$WATCHDOG_LOG"; }
ok(){ printf '%s🟢 [watchdog]%s %s\n' "$GREEN" "$NC" "$*" | tee -a "$WATCHDOG_LOG"; }
warn(){ printf '%s🟡 [watchdog]%s %s\n' "$YELLOW" "$NC" "$*" | tee -a "$WATCHDOG_LOG"; }
err(){ printf '%s🔴 [watchdog]%s %s\n' "$RED" "$NC" "$*" | tee -a "$WATCHDOG_LOG"; }
work(){ printf '%s🟣 [watchdog]%s %s\n' "$PURPLE" "$NC" "$*" | tee -a "$WATCHDOG_LOG"; }

mkdir -p "$LOG_DIR" .runtime

health_url(){
  case "$1" in
    rasa) echo "http://127.0.0.1:${RASA_PORT}/" ;;
    actions) echo "http://127.0.0.1:${ACTIONS_PORT}/health" ;;
    webhook) echo "http://127.0.0.1:${WEBHOOK_PORT}/health" ;;
    frontend) echo "http://127.0.0.1:${FRONTEND_PORT}" ;;
  esac
}

service_healthy(){ curl -fsS --max-time 5 "$(health_url "$1")" >/dev/null 2>&1; }
port_listening(){ ss -ltn "( sport = :$1 )" 2>/dev/null | grep -q ":$1" || lsof -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1; }

restart_stack(){
  work "إعادة تشغيل تلقائية بعد فشل health/port check"
  $BOTCTL restart --heal >> "$WATCHDOG_LOG" 2>&1 || err "فشل restart --heal"
}

resource_check(){
  local mem_used cpu_idle cpu_used
  mem_used=$(free | awk '/Mem:/ {printf "%d", ($3/$2)*100}' 2>/dev/null || echo 0)
  cpu_idle=$(top -bn1 | awk -F'id,' '/Cpu\(s\)/ {split($1,a,","); print a[length(a)]}' | awk '{print int($NF)}' 2>/dev/null || echo 100)
  cpu_used=$((100 - cpu_idle))
  (( mem_used >= MEM_WARN )) && warn "Memory usage high: ${mem_used}%"
  (( cpu_used >= CPU_WARN )) && warn "CPU usage high: ${cpu_used}%"
}

scan_errors(){
  grep -Eih "(error|exception|traceback|failed|critical|fatal|connection refused|timeout)" \
    "$LOG_DIR"/*.out.log 2>/dev/null | tail -n 20 > .runtime/watchdog_errors.last || true
  if [[ -s .runtime/watchdog_errors.last ]]; then
    warn "أخطاء حديثة في logs: .runtime/watchdog_errors.last"
  fi
}

run_once(){
  local failed=false
  service_healthy actions || { err "Actions health failed"; failed=true; }
  service_healthy rasa || { err "Rasa health failed"; failed=true; }
  service_healthy webhook || { err "Webhook health failed"; failed=true; }
  port_listening "$ACTIONS_PORT" || { err "Port $ACTIONS_PORT not listening"; failed=true; }
  port_listening "$RASA_PORT" || { err "Port $RASA_PORT not listening"; failed=true; }
  port_listening "$WEBHOOK_PORT" || { err "Port $WEBHOOK_PORT not listening"; failed=true; }
  port_listening "$FRONTEND_PORT" || warn "Port $FRONTEND_PORT not listening"
  resource_check
  scan_errors
  $failed && restart_stack || ok "كل الخدمات الأساسية سليمة"
}

case "${1:-run}" in
  once) run_once ;;
  run) info "بدء المراقبة كل ${CHECK_INTERVAL}s"; while true; do run_once; sleep "$CHECK_INTERVAL"; done ;;
  *) echo "Usage: $0 [run|once]"; exit 2 ;;
esac
