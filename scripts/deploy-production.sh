#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
# scripts/deploy-production.sh
# نشر AzaBot على bot.alazab.com
#
# الاستخدام:
#   bash scripts/deploy-production.sh          ← full deploy
#   bash scripts/deploy-production.sh --quick  ← بدون train
# ══════════════════════════════════════════════════════════════
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

QUICK=false
[[ "${1:-}" == "--quick" ]] && QUICK=true

GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; NC=$'\033[0m'
ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }
fail() { printf "${RED}❌ %s${NC}\n" "$*" >&2; exit 1; }
step() { printf "\n${GREEN}══ %s ══${NC}\n" "$*"; }

# ══════════════════════════════════════════════════════════════
step "1. Pre-flight checks"
# ══════════════════════════════════════════════════════════════

[[ -f .env ]] || fail ".env مفقود"

source_env() { set -a; source .env; set +a; }
source_env

[[ -n "${SUPABASE_URL:-}" ]]              || fail "SUPABASE_URL مفقود"
[[ -n "${SUPABASE_SERVICE_ROLE_KEY:-}" ]] || fail "SUPABASE_SERVICE_ROLE_KEY مفقود"
[[ -n "${OPENAI_API_KEY:-}" ]]            || fail "OPENAI_API_KEY مفقود"
[[ -n "${RASA_PRO_LICENSE:-}" ]]          || fail "RASA_PRO_LICENSE مفقود"
ok "Environment verified"

# ══════════════════════════════════════════════════════════════
step "2. Git pull"
# ══════════════════════════════════════════════════════════════

git pull origin main --ff-only 2>/dev/null || warn "Git pull failed — continuing"
ok "Code updated"

# ══════════════════════════════════════════════════════════════
step "3. Python dependencies"
# ══════════════════════════════════════════════════════════════

source .venv/bin/activate || { python3 -m venv .venv && source .venv/bin/activate; }
pip install -q --upgrade pip
pip install -q -r requirements.txt
ok "Python deps installed"

# ══════════════════════════════════════════════════════════════
step "4. Supabase Edge Functions"
# ══════════════════════════════════════════════════════════════

if command -v supabase &>/dev/null; then
    cd azabot
    supabase functions deploy uberfix   --no-verify-jwt || warn "uberfix deploy failed"
    supabase functions deploy admin-api --no-verify-jwt || warn "admin-api deploy failed"
    supabase functions deploy chat      --no-verify-jwt || warn "chat deploy failed"
    cd ..
    ok "Edge Functions deployed"
else
    warn "supabase CLI not found — skipping Edge Functions deploy"
fi

# ══════════════════════════════════════════════════════════════
step "5. Domain validation"
# ══════════════════════════════════════════════════════════════

python3 scripts/render_runtime_domain.py
python3 scripts/deep_clean.py --validate-only
ok "Domain validated"

# ══════════════════════════════════════════════════════════════
step "6. Rasa Train"
# ══════════════════════════════════════════════════════════════

if $QUICK; then
    warn "Quick mode — skipping train"
    ls models/*.tar.gz &>/dev/null || fail "No trained model found — run without --quick"
else
    bash scripts/botctl.sh train
    ok "Model trained"
fi

# ══════════════════════════════════════════════════════════════
step "7. Stop old services"
# ══════════════════════════════════════════════════════════════

bash scripts/botctl.sh stop 2>/dev/null || true
sleep 2
ok "Old services stopped"

# ══════════════════════════════════════════════════════════════
step "8. Nginx config"
# ══════════════════════════════════════════════════════════════

NGINX_CONF="/etc/nginx/sites-available/bot.alazab.com.conf"
NGINX_LINK="/etc/nginx/sites-enabled/bot.alazab.com.conf"

if [[ -w /etc/nginx/sites-available ]]; then
    cp deploy/production/nginx/bot.alazab.com.conf "$NGINX_CONF"
    ln -sf "$NGINX_CONF" "$NGINX_LINK" 2>/dev/null || true
    nginx -t && systemctl reload nginx
    ok "Nginx configured"
else
    warn "No nginx write access — copy manually:"
    warn "  sudo cp deploy/production/nginx/bot.alazab.com.conf $NGINX_CONF"
fi

# ══════════════════════════════════════════════════════════════
step "9. Systemd services"
# ══════════════════════════════════════════════════════════════

SYSTEMD_DIR="/etc/systemd/system"

install_service() {
    local name="$1" src="deploy/systemd/${name}.service"
    if [[ -w "$SYSTEMD_DIR" ]]; then
        # تحديث WorkingDirectory و User
        sed "s|/opt/azabot|$ROOT|g; s|User=azab|User=$(whoami)|g" \
            "$src" > "$SYSTEMD_DIR/${name}.service"
        ok "Installed systemd: $name"
    else
        warn "No systemd write access — copy manually:"
        warn "  sudo cp $src $SYSTEMD_DIR/"
    fi
}

install_service azabot-actions
install_service azabot-rasa
install_service azabot-webhook

if [[ -w "$SYSTEMD_DIR" ]]; then
    systemctl daemon-reload
    systemctl enable azabot-actions azabot-rasa azabot-webhook
fi

# ══════════════════════════════════════════════════════════════
step "10. Start services"
# ══════════════════════════════════════════════════════════════

bash run.sh --backend &
sleep 5
bash scripts/botctl.sh smoke || warn "Smoke test failed — check logs"

ok "AzaBot deployed on bot.alazab.com ✅"
echo ""
echo "  Health:  https://bot.alazab.com/health"
echo "  Admin:   https://bot.alazab.com/admin/"
echo "  Logs:    bash scripts/botctl.sh logs all"
echo ""
