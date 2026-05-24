#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
# scripts/register-webhooks.sh
# تسجيل Webhooks — Telegram + Meta
# الاستخدام: bash scripts/register-webhooks.sh
# ══════════════════════════════════════════════════════════════
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

source .env 2>/dev/null || true

GREEN='\033[1;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }

BASE_URL="${PUBLIC_BASE_URL:-https://chat.alazab.com}"

# ══════════════════════════════════════════════════════════════
echo "🔗 تسجيل Webhooks لـ $BASE_URL"
echo ""

# ── Telegram ──────────────────────────────────────────────────
TG_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TG_SECRET="${TELEGRAM_WEBHOOK_SECRET:-azab_secure_tg_2025_v3}"

if [[ -n "$TG_TOKEN" ]]; then
  echo "→ Telegram..."
  RESULT=$(curl -sS -X POST \
    "https://api.telegram.org/bot${TG_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{
      \"url\": \"${BASE_URL}/webhook/telegram\",
      \"secret_token\": \"${TG_SECRET}\",
      \"allowed_updates\": [\"message\", \"callback_query\"],
      \"drop_pending_updates\": true
    }")
  if echo "$RESULT" | grep -q '"ok":true'; then
    ok "Telegram webhook: ${BASE_URL}/webhook/telegram"
  else
    warn "Telegram failed: $RESULT"
  fi

  # معلومات البوت
  BOT_INFO=$(curl -sS "https://api.telegram.org/bot${TG_TOKEN}/getMe")
  BOT_NAME=$(echo "$BOT_INFO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('result',{}).get('username','?'))" 2>/dev/null || echo "?")
  echo "  Bot: @${BOT_NAME}"
else
  warn "TELEGRAM_BOT_TOKEN غير موجود في .env"
fi

echo ""

# ── Meta / WhatsApp ───────────────────────────────────────────
# Meta webhook يُسجَّل يدوياً من Meta Developer Console
# لأنه يحتاج SSL وverification token

echo "→ Meta / WhatsApp:"
echo "  الـ webhook URL: ${BASE_URL}/webhook/meta"
echo "  Verify Token: ${FB_VERIFY_TOKEN:-QvacXnwH_5QWUTKsEsxEgtYd8kHpVcf3U}"
echo ""
echo "  📌 خطوات التسجيل في Meta:"
echo "  1. developers.facebook.com → تطبيقك (${FB_APP_ID:-889346333913449})"
echo "  2. WhatsApp → Configuration → Webhook"
echo "  3. Callback URL: ${BASE_URL}/webhook/meta"
echo "  4. Verify Token: ${FB_VERIFY_TOKEN:-QvacXnwH_5QWUTKsEsxEgtYd8kHpVcf3U}"
echo "  5. Subscribe: messages, messaging_postbacks"
echo ""

# اختبار Meta Verify Token
echo "→ اختبار Meta verify token..."
TEST=$(curl -sS "${BASE_URL}/webhook/meta?hub.mode=subscribe&hub.verify_token=${FB_VERIFY_TOKEN:-QvacXnwH_5QWUTKsEsxEgtYd8kHpVcf3U}&hub.challenge=TEST123" 2>/dev/null || echo "")
if [[ "$TEST" == "TEST123" ]]; then
  ok "Meta webhook endpoint يعمل ✅"
else
  warn "Meta webhook endpoint: تحقق أن السيرفر شغال أولاً"
fi

echo ""
ok "تم تسجيل الـ Webhooks!"
