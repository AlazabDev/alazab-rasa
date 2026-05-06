#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  build-production.sh — بناء الفرونت للإنتاج مع inject المتغيرات
#  الاستخدام: bash azabot/scripts/build-production.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONT="$ROOT/azabot"
ENV_ROOT="$ROOT/.env"

GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; NC=$'\033[0m'
ok() { printf "${GREEN}✅ %s${NC}\n" "$*"; }
info() { printf "${CYAN}→  %s${NC}\n" "$*"; }

# تحميل root .env
[[ -f "$ENV_ROOT" ]] || { echo "❌ .env غير موجود"; exit 1; }
export $(grep -v '^#' "$ENV_ROOT" | grep -v '^$' | xargs) 2>/dev/null || true

info "إنشاء azabot/.env.local من root .env..."
cat > "$FRONT/.env.local" << ENVLOCAL
# ── Auto-generated from root .env — DO NOT EDIT ──────────────
VITE_APP_NAME=AzaBot
VITE_APP_VERSION=3.0.0
VITE_APP_ENV=production

# Supabase
VITE_SUPABASE_URL=${SUPABASE_URL:-${VITE_SUPABASE_URL:-}}
VITE_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY:-${VITE_SUPABASE_ANON_KEY:-}}
VITE_SUPABASE_PROJECT_ID=${SUPABASE_PROJECT:-${VITE_SUPABASE_PROJECT_ID:-}}
VITE_SUPABASE_PUBLISHABLE_KEY=${SUPABASE_PUBLISHABLE_KEY:-${VITE_SUPABASE_PUBLISHABLE_KEY:-}}
ENVLOCAL

ok ".env.local أُنشئ"

info "تثبيت packages..."
cd "$FRONT"
pnpm install --frozen-lockfile -s

info "بناء الإنتاج..."
pnpm build

ok "البناء اكتمل: azabot/dist/"
ls -lh "$FRONT/dist/index.html" 2>/dev/null || true

# نظّف .env.local بعد البناء
rm -f "$FRONT/.env.local"
ok "تم حذف .env.local (credentials غير موجودة في dist)"
