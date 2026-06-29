#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
# sync-deploy.sh — مزامنة ونشر كامل
# يُشغَّل من: D:\Dev\AzBot\alazab-rasa\azabot\
# ══════════════════════════════════════════════════════════════

set -euo pipefail
cd "$(dirname "$0")"

GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }
step() { printf "\n${GREEN}══ %s ══${NC}\n" "$*"; }

# ══════════════════════════════════════════════════════════════
step "1. Supabase DB — مزامنة الـ Schema"
# ══════════════════════════════════════════════════════════════

# فحص الفرق بين local و remote
echo "→ جارٍ فحص الـ schema..."
supabase db diff --linked 2>&1 | head -20

# رفع migration الجداول الجديدة
echo "→ رفع migrations..."
supabase db push --linked
ok "Schema synced"

# ══════════════════════════════════════════════════════════════
step "2. Edge Functions — نشر"
# ══════════════════════════════════════════════════════════════

FUNCTIONS=(
  "admin-api"
  "admin-login"
  "azabot-chat"
  "chat"
  "chat-v2"
  "bot-public-settings"
  "elevenlabs-tts"
  "elevenlabs-stt"
)

for fn in "${FUNCTIONS[@]}"; do
  if [[ -d "supabase/functions/$fn" ]]; then
    echo "→ deploying $fn..."
    supabase functions deploy "$fn" --no-verify-jwt 2>/dev/null \
      && ok "$fn deployed" \
      || warn "$fn failed — check logs"
  fi
done

# ══════════════════════════════════════════════════════════════
step "3. Environment Variables → Supabase Secrets"
# ══════════════════════════════════════════════════════════════

ENV_FILE="../.env"
if [[ -f "$ENV_FILE" ]]; then
  echo "→ رفع الـ secrets للـ Edge Functions..."

  # المتغيرات المطلوبة للـ Edge Functions
  SECRETS=(
    OPENAI_API_KEY
    SUPABASE_SERVICE_ROLE_KEY
    SUPABASE_ANON_KEY
    BOT_API_KEY
    BOT_GATEWAY_URL
    UBERFIX_API_KEY
    UBERFIX_API_URL
    WHATSAPP_TOKEN
    META_TOKEN
    TELEGRAM_BOT_TOKEN
    ELEVENLABS_API_KEY
    ELEVENLABS_AGENT_ID
    ADMIN_EMAIL
    ADMIN_PASSWORD
    ADMIN_SESSION_SECRET
    JWT_SECRET
    ENCRYPTION_KEY
  )

  for var in "${SECRETS[@]}"; do
    val=$(grep "^${var}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-)
    if [[ -n "$val" ]]; then
      echo "$val" | supabase secrets set "${var}=-" 2>/dev/null \
        && echo "  ✅ $var" \
        || echo "  ⚠️  $var (skip)"
    fi
  done
  ok "Secrets updated"
else
  warn ".env not found at $ENV_FILE"
fi

# ══════════════════════════════════════════════════════════════
step "4. Supabase Storage — إنشاء Buckets"
# ══════════════════════════════════════════════════════════════

# يتم عبر SQL مباشر
supabase db execute --linked << 'SQL'
-- Uploads bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('uploads', 'uploads', false, 52428800,
  ARRAY['image/jpeg','image/png','image/webp','audio/webm','audio/mp4','application/pdf'])
ON CONFLICT (id) DO NOTHING;

-- Audio bucket (TTS outputs)
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('audio', 'audio', true, 10485760)
ON CONFLICT (id) DO NOTHING;

-- KB documents bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('kb-documents', 'kb-documents', false)
ON CONFLICT (id) DO NOTHING;
SQL
ok "Storage buckets ready"

# ══════════════════════════════════════════════════════════════
step "5. RLS Policies — تفعيل"
# ══════════════════════════════════════════════════════════════

supabase db execute --linked << 'SQL'
-- Storage policies
CREATE POLICY IF NOT EXISTS "service_role_uploads"
  ON storage.objects FOR ALL TO service_role USING (true);

CREATE POLICY IF NOT EXISTS "service_role_audio"
  ON storage.objects FOR ALL TO service_role USING (true);

-- Bot settings — قراءة عامة
CREATE POLICY IF NOT EXISTS "anon_read_settings"
  ON public.bot_settings FOR SELECT TO anon USING (true);
SQL
ok "RLS policies applied"

# ══════════════════════════════════════════════════════════════
step "6. تحقق نهائي"
# ══════════════════════════════════════════════════════════════

echo ""
echo "→ Edge Functions المنشورة:"
supabase functions list 2>/dev/null | head -20

echo ""
ok "══════════════════════════════════════"
ok "  المزامنة والنشر اكتملا!"
ok "══════════════════════════════════════"
echo ""
echo "الخطوة التالية — على السيرفر:"
echo "  bash scripts/botctl.sh train"
echo "  bash run.sh"
