#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  scripts/prod-check.sh — فحص جاهزية الإنتاج
#  الاستخدام:  bash scripts/prod-check.sh
# ══════════════════════════════════════════════════════════════
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'

PASS=0; FAIL=0; WARN=0

ok()   { echo -e "  ${GREEN}✅ PASS${NC}  $*"; ((PASS++)); }
fail() { echo -e "  ${RED}❌ FAIL${NC}  $*"; ((FAIL++)); }
warn() { echo -e "  ${YELLOW}⚠️  WARN${NC}  $*"; ((WARN++)); }

echo -e "\n${BLUE}══ فحص جاهزية الإنتاج — AzaBot v4.1 ══${NC}\n"

# ── .env موجود ────────────────────────────────────────────────
echo -e "${BLUE}[1] ملفات البيئة${NC}"
[[ -f .env ]] && ok ".env موجود" || fail ".env مفقود — انسخ .env.example وأكمل القيم"
[[ ! -f ssl/privkey.pem ]] && ok "ssl/ غير موجود في الريبو" || fail "ssl/privkey.pem مكشوف في الريبو — احذفه!"

# ── المتغيرات الحرجة ──────────────────────────────────────────
echo -e "\n${BLUE}[2] متغيرات البيئة الحرجة${NC}"
if [[ -f .env ]]; then
  source <(grep -v '^#' .env | grep '=' | sed 's/^/export /')

  [[ -n "${ADMIN_SESSION_SECRET:-}" ]] && [[ "${#ADMIN_SESSION_SECRET}" -ge 32 ]] \
    && ok "ADMIN_SESSION_SECRET (${#ADMIN_SESSION_SECRET} حرف)" \
    || fail "ADMIN_SESSION_SECRET مفقود أو قصير (يجب ≥ 32 حرف)"

  [[ -n "${ADMIN_PASSWORD_HASH_ADMIN:-}" ]] && [[ "${ADMIN_PASSWORD_HASH_ADMIN}" =~ ^\$2b\$ ]] \
    && ok "ADMIN_PASSWORD_HASH_ADMIN (bcrypt ✓)" \
    || fail "ADMIN_PASSWORD_HASH_ADMIN مفقود أو ليس bcrypt — شغّل: python scripts/gen_password_hash.py"

  for user in DEVOPS CEO MOHAMED; do
    var="ADMIN_PASSWORD_HASH_${user}"
    [[ -n "${!var:-}" ]] && [[ "${!var}" =~ ^\$2b\$ ]] \
      && ok "${var} (bcrypt ✓)" \
      || warn "${var} مفقود — المستخدم معطَّل"
  done

  [[ -n "${OPENAI_API_KEY:-}" ]] && [[ "${OPENAI_API_KEY}" != "sk-proj-REPLACE_ME" ]] \
    && ok "OPENAI_API_KEY مضبوط" \
    || fail "OPENAI_API_KEY مفقود أو افتراضي"

  [[ -n "${SUPABASE_URL:-}" ]] && [[ "${SUPABASE_URL}" != *"REPLACE"* ]] \
    && ok "SUPABASE_URL مضبوط" \
    || fail "SUPABASE_URL مفقود"

  [[ -n "${SUPABASE_SERVICE_ROLE_KEY:-}" ]] && [[ "${SUPABASE_SERVICE_ROLE_KEY}" != *"REPLACE"* ]] \
    && ok "SUPABASE_SERVICE_ROLE_KEY مضبوط" \
    || fail "SUPABASE_SERVICE_ROLE_KEY مفقود"

  [[ "${NODE_ENV:-}" == "production" ]] \
    && ok "NODE_ENV=production" \
    || warn "NODE_ENV ليس production"

  # تحقق من كلمة المرور القديمة
  [[ -z "${ADMIN_PASSWORD:-}" ]] \
    && ok "ADMIN_PASSWORD غير موجود (جيد — يستخدم bcrypt الآن)" \
    || warn "ADMIN_PASSWORD لا يزال موجوداً — احذفه من .env"
fi

# ── Redis ─────────────────────────────────────────────────────
echo -e "\n${BLUE}[3] Redis${NC}"
if command -v redis-cli &>/dev/null; then
  REDIS_HOST_VAL="${REDIS_HOST:-127.0.0.1}"
  REDIS_PORT_VAL="${REDIS_PORT:-6379}"
  redis-cli -h "$REDIS_HOST_VAL" -p "$REDIS_PORT_VAL" ping 2>/dev/null | grep -q "PONG" \
    && ok "Redis يستجيب على $REDIS_HOST_VAL:$REDIS_PORT_VAL" \
    || fail "Redis لا يستجيب — Rate limiting وجلسات لن تعمل"
else
  warn "redis-cli غير مثبَّت — لا يمكن فحص Redis"
fi

# ── الملفات الحرجة ────────────────────────────────────────────
echo -e "\n${BLUE}[4] ملفات الكود${NC}"
for f in webhook/auth.py webhook/server.py webhook/middleware.py \
          webhook/services/rasa_client.py webhook/services/integrations.py; do
  [[ -f "$f" ]] && ok "$f موجود" || fail "$f مفقود"
done

# تحقق من bcrypt في auth.py
grep -q "bcrypt.checkpw" webhook/auth.py \
  && ok "auth.py يستخدم bcrypt ✓" \
  || fail "auth.py لا يستخدم bcrypt — راجع الإصلاحات"

# تحقق من Redis sessions
grep -q "redis" webhook/auth.py \
  && ok "auth.py يستخدم Redis sessions ✓" \
  || warn "auth.py لا يزال يستخدم file sessions"

# تحقق من RateLimitMiddleware
grep -q "RateLimitMiddleware" webhook/server.py \
  && ok "RateLimitMiddleware مُفعَّل ✓" \
  || fail "RateLimitMiddleware غير مُفعَّل في server.py"

# تحقق من إغلاق /docs
grep -q "docs_url=None" webhook/server.py \
  && ok "/docs مغلق في الإنتاج ✓" \
  || warn "/docs قد يكون مفتوحاً"

# تحقق من SSRF protection
grep -q "_validate_webhook_url\|_BLOCKED_NETS" webhook/services/integrations.py \
  && ok "SSRF protection مُفعَّل ✓" \
  || fail "SSRF protection مفقود في integrations.py"

# تحقق من X-Powered-By
grep -q "X-Powered-By" webhook/middleware.py \
  && fail "X-Powered-By لا يزال موجوداً في middleware.py" \
  || ok "X-Powered-By محذوف ✓"

# ── .gitignore ────────────────────────────────────────────────
echo -e "\n${BLUE}[5] .gitignore${NC}"
for item in ".env" "ssl/" "*.pem" ".runtime/" "scratch/"; do
  grep -q "^${item%/}" .gitignore 2>/dev/null \
    && ok ".gitignore يحجب: $item" \
    || fail ".gitignore لا يحجب: $item"
done

# ── Systemd services ──────────────────────────────────────────
echo -e "\n${BLUE}[6] Systemd Services${NC}"
for svc in azabot-webhook azabot-rasa azabot-actions; do
  [[ -f "deploy/systemd/${svc}.service" ]] \
    && ok "deploy/systemd/${svc}.service موجود" \
    || warn "deploy/systemd/${svc}.service مفقود"
done

# ── ملخص ──────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}══════════════════════════════════════${NC}"
echo -e "  ${GREEN}PASS: $PASS${NC}  |  ${YELLOW}WARN: $WARN${NC}  |  ${RED}FAIL: $FAIL${NC}"
echo -e "${BLUE}══════════════════════════════════════${NC}"

if [[ $FAIL -gt 0 ]]; then
  echo -e "  ${RED}❌ غير جاهز للإنتاج — أصلح الـ FAILs أولاً${NC}"
  exit 1
elif [[ $WARN -gt 0 ]]; then
  echo -e "  ${YELLOW}⚠️  جاهز مع تحفظات — راجع الـ WARNs${NC}"
else
  echo -e "  ${GREEN}🎉 جاهز للإنتاج!${NC}"
fi
