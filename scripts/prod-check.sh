#!/usr/bin/env bash
set -euo pipefail
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
PASS=0; FAIL=0; WARN=0
ok()   { echo -e "  ${GREEN}✅ PASS${NC}  $*"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}❌ FAIL${NC}  $*"; FAIL=$((FAIL + 1)); }
warn() { echo -e "  ${YELLOW}⚠️  WARN${NC}  $*"; WARN=$((WARN + 1)); }

echo -e "\n${BLUE}══ فحص جاهزية الإنتاج — AzaBot v4.1 ══${NC}\n"

[[ -f .env ]] && ok ".env موجود" || fail ".env مفقود"
[[ ! -d ssl ]] && ok "ssl/ غير موجود في الريبو" || fail "ssl/ مكشوف"
[[ ! -f RASA_LICENSE1 ]] && ok "RASA_LICENSE* غير موجودة في الريبو" || fail "RASA_LICENSE* مكشوفة"

if [[ -f .env ]]; then
  set +u
  line=""; key=""; value=""
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue
    key="${line%%=*}"; value="${line#*=}"
    key="$(echo "$key" | xargs)"
    value="${value%\"}"; value="${value#\"}"
    export "$key=$value"
  done < .env
  set -u
  [[ -n "${ADMIN_SESSION_SECRET:-}" && "${#ADMIN_SESSION_SECRET}" -ge 32 ]] && ok "ADMIN_SESSION_SECRET" || fail "ADMIN_SESSION_SECRET مفقود/قصير"
  [[ "${ADMIN_PASSWORD_HASH_ADMIN:-}" =~ ^\$2b\$ ]] && ok "ADMIN_PASSWORD_HASH_ADMIN bcrypt ✓" || fail "ADMIN_PASSWORD_HASH_ADMIN — شغّل scripts/gen_password_hash.py"
  [[ "${OPENAI_API_KEY:-}" != *REPLACE* && -n "${OPENAI_API_KEY:-}" ]] && ok "OPENAI_API_KEY" || fail "OPENAI_API_KEY مفقود"
  [[ "${SUPABASE_URL:-}" != *REPLACE* && -n "${SUPABASE_URL:-}" ]] && ok "SUPABASE_URL" || fail "SUPABASE_URL مفقود"
  [[ "${NODE_ENV:-}" == "production" ]] && ok "NODE_ENV=production" || warn "NODE_ENV ليس production"
  [[ -z "${ADMIN_PASSWORD:-}" ]] && ok "ADMIN_PASSWORD غير موجود (bcrypt الآن)" || warn "ADMIN_PASSWORD لا يزال موجوداً — احذفه"
fi

grep -q "bcrypt.checkpw" webhook/auth.py && ok "auth.py bcrypt ✓" || fail "auth.py بلا bcrypt"
grep -q "RateLimitMiddleware" webhook/server.py && ok "RateLimitMiddleware مُفعَّل" || fail "RateLimitMiddleware غائب"
grep -q "docs_url=None" webhook/server.py && ok "/docs مغلق في prod" || warn "/docs قد يكون مفتوحاً"
grep -q "_validate_webhook_url" webhook/services/integrations.py && ok "SSRF protection ✓" || fail "SSRF protection غائب"
grep -q "DB_HOST.*pooler.supabase" endpoints.yml && fail "endpoints.yml لا يزال به project ID مكتوب" || ok "endpoints.yml نظيف"

for item in ".env" "ssl/" "RASA_LICENSE" ".runtime/"; do
  grep -q "${item%/}" .gitignore && ok ".gitignore يحجب: $item" || fail ".gitignore لا يحجب: $item"
done

echo -e "\n${BLUE}══════════════════════${NC}"
echo -e "  ${GREEN}PASS: $PASS${NC} | ${YELLOW}WARN: $WARN${NC} | ${RED}FAIL: $FAIL${NC}"
[[ $FAIL -gt 0 ]] && { echo -e "${RED}❌ غير جاهز${NC}"; exit 1; }
echo -e "${GREEN}🎉 جاهز للإنتاج${NC}"
