#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  dev.sh — AzaBot Full Dev Stack Launcher
#
#  يشغّل كل شيء بأمر واحد:
#    ① Rasa Actions Server   → port 5055
#    ② Rasa Pro Server       → port 5005
#    ③ FastAPI Webhook       → port 8000
#    ④ Vite Frontend Dev     → port 8080
#
#  الاستخدام:
#    bash dev.sh              تشغيل كامل
#    bash dev.sh --backend    باك اند فقط
#    bash dev.sh --frontend   فرونت فقط
#    bash dev.sh stop         إيقاف كل شيء
#    bash dev.sh status       حالة الخدمات
#    bash dev.sh logs [svc]   السجلات (all|actions|rasa|webhook|frontend)
#    bash dev.sh restart      إعادة تشغيل كل شيء
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BOTCTL="bash scripts/botctl.sh"
LOG_DIR="${LOG_DIR:-logs}"
RUNTIME_DIR="${RUNTIME_DIR:-.runtime}"
PID_DIR="$RUNTIME_DIR/pids"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"

# ── ألوان ─────────────────────────────────────────────────────
CYAN=$'\033[1;36m'; GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'; BOLD=$'\033[1m'; NC=$'\033[0m'

# ── helpers ───────────────────────────────────────────────────
is_running() { local pid="$1"; [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; }
read_pid()   { local f="$PID_DIR/${1}.pid"; [[ -f "$f" ]] && cat "$f" || echo ""; }
write_pid()  { mkdir -p "$PID_DIR"; echo "$2" > "$PID_DIR/${1}.pid"; }

wait_http() {
  local name="$1" url="$2" tries="${3:-30}"
  for _ in $(seq 1 "$tries"); do
    curl -fsS "$url" >/dev/null 2>&1 && printf "${GREEN}✅ %s جاهز${NC}\n" "$name" && return 0
    sleep 2
  done
  printf "${YELLOW}⚠️  %s لم يستجب خلال %ss${NC}\n" "$name" "$((tries*2))"
  return 0
}

banner() {
  echo ""
  echo "${CYAN}${BOLD}╔══════════════════════════════════════════════╗${NC}"
  echo "${CYAN}${BOLD}║   🤖 AzaBot — Full Dev Stack Launcher        ║${NC}"
  echo "${CYAN}${BOLD}╚══════════════════════════════════════════════╝${NC}"
  echo ""
}

# ── تشغيل الفرونت ─────────────────────────────────────────────
_start_frontend() {
  if ! command -v pnpm >/dev/null 2>&1; then
    printf "${YELLOW}⚠️  pnpm غير موجود — الفرونت لن يُشغَّل${NC}\n"
    printf "   لتثبيته: npm install -g pnpm\n"
    return 0
  fi

  if [[ ! -d "azabot/node_modules" ]]; then
    printf "${CYAN}📦 تثبيت packages الفرونت...${NC}\n"
    (cd azabot && pnpm install --frozen-lockfile)
  fi

  local old_pid; old_pid="$(read_pid frontend || true)"
  if is_running "$old_pid"; then
    printf "${YELLOW}⚠️  الفرونت يعمل بالفعل (PID $old_pid)${NC}\n"
    return 0
  fi

  mkdir -p "$LOG_DIR"
  printf "${CYAN}🎨 تشغيل Vite dev server على port ${FRONTEND_PORT}...${NC}\n"
  nohup bash -c "cd azabot && VITE_DEV_BACKEND_URL=http://127.0.0.1:${WEBHOOK_PORT} pnpm dev --port ${FRONTEND_PORT}" \
    > "$LOG_DIR/frontend.out.log" 2>&1 &
  write_pid frontend "$!"
  printf "${GREEN}✅ الفرونت شغّال (PID $!)${NC}\n"
  wait_http "Frontend" "http://localhost:${FRONTEND_PORT}" 25
}

# ── إيقاف كل شيء ─────────────────────────────────────────────
_stop_all() {
  printf "${RED}🛑 إيقاف كل الخدمات...${NC}\n"
  # إيقاف الفرونت أولاً
  local fp; fp="$(read_pid frontend || true)"
  if is_running "$fp"; then
    kill "$fp" 2>/dev/null && printf "  stopped frontend (PID $fp)\n"
  fi
  rm -f "$PID_DIR/frontend.pid"
  # إيقاف الباك اند
  $BOTCTL stop
}

# ── الحالة ────────────────────────────────────────────────────
_show_status() {
  $BOTCTL status
}

# ── السجلات ──────────────────────────────────────────────────
_show_logs() {
  local svc="${1:-all}"
  if [[ "$svc" == "frontend" ]]; then
    tail -n 120 -f "$LOG_DIR/frontend.out.log"
  else
    $BOTCTL logs "$svc"
  fi
}

# ── التحقق من المتطلبات ───────────────────────────────────────
_preflight() {
  local ok=true

  if [[ ! -f ".env" ]]; then
    printf "${RED}❌ ملف .env غير موجود!${NC}\n"
    printf "   cp .env.example .env  ثم أضف بياناتك\n"
    ok=false
  fi

  if [[ ! -d ".venv" ]]; then
    printf "${YELLOW}⚠️  venv غير موجود — جاري الإعداد...${NC}\n"
    $BOTCTL setup
  fi

  if [[ -z "$(ls models/*.tar.gz 2>/dev/null || true)" ]]; then
    printf "${YELLOW}⚠️  لا يوجد موديل Rasa مدرّب.${NC}\n"
    read -r -p "   هل تريد التدريب الآن؟ [y/N] " answer
    if [[ "${answer,,}" == "y" ]]; then
      printf "${CYAN}🧠 جاري التدريب...${NC}\n"
      $BOTCTL train
    else
      printf "${RED}❌ يجب تدريب موديل أولاً: bash scripts/botctl.sh train${NC}\n"
      ok=false
    fi
  fi

  [[ "$ok" == "true" ]]
}

# ── إظهار الـ URLs النهائية ───────────────────────────────────
_print_urls() {
  echo ""
  printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
  printf "${GREEN}${BOLD} 🎉 كل الخدمات شغّالة!${NC}\n"
  printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
  printf "  🌐 الواجهة   : ${CYAN}http://localhost:${FRONTEND_PORT}${NC}\n"
  printf "  ⚙️  الباك اند : ${CYAN}http://localhost:${WEBHOOK_PORT}${NC}\n"
  printf "  🔗 API Docs  : ${CYAN}http://localhost:${WEBHOOK_PORT}/docs${NC}\n"
  printf "  📊 Admin     : ${CYAN}http://localhost:${WEBHOOK_PORT}/admin${NC}\n"
  printf "${GREEN}${BOLD}──────────────────────────────────────────────${NC}\n"
  printf "  للوقف:   ${YELLOW}bash dev.sh stop${NC}\n"
  printf "  للحالة:  ${YELLOW}bash dev.sh status${NC}\n"
  printf "  للسجلات: ${YELLOW}bash dev.sh logs [all|frontend|webhook|rasa|actions]${NC}\n"
  printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
  echo ""
}

# ══════════════════════════════════════════════════════════════
#  نقطة الدخول الرئيسية
# ══════════════════════════════════════════════════════════════
ARG="${1:-}"

case "$ARG" in
  stop)
    _stop_all
    exit 0
    ;;
  status)
    _show_status
    exit 0
    ;;
  logs)
    _show_logs "${2:-all}"
    exit 0
    ;;
  restart)
    _stop_all
    sleep 2
    exec bash "$0"
    ;;
  --backend)
    banner
    _preflight || exit 1
    printf "${YELLOW}⚙️  تشغيل الباك اند فقط...${NC}\n"
    $BOTCTL start
    echo ""
    printf "${GREEN}✅ الباك اند يعمل على: ${CYAN}http://localhost:${WEBHOOK_PORT}${NC}\n"
    exit 0
    ;;
  --frontend)
    banner
    printf "${YELLOW}🎨 تشغيل الفرونت فقط...${NC}\n"
    _start_frontend
    echo ""
    printf "${GREEN}✅ الفرونت يعمل على: ${CYAN}http://localhost:${FRONTEND_PORT}${NC}\n"
    exit 0
    ;;
  ""|--all|-a)
    : # تشغيل كامل — استمر
    ;;
  --help|-h)
    echo "الاستخدام: bash dev.sh [stop|status|logs|restart|--backend|--frontend]"
    exit 0
    ;;
  *)
    printf "${RED}أمر غير معروف: %s${NC}\n" "$ARG"
    echo "الاستخدام: bash dev.sh [stop|status|logs|restart|--backend|--frontend]"
    exit 1
    ;;
esac

# ── التشغيل الكامل ────────────────────────────────────────────
banner
_preflight || exit 1

printf "${CYAN}🚀 جاري تشغيل جميع الخدمات...${NC}\n\n"

# تشغيل الباك اند أولاً
$BOTCTL start

# ثم الفرونت
_start_frontend

# عرض URLs النهائية
_print_urls
