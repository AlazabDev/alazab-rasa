#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  AzaBot — Production Deploy Script
#  الخادم: Ubuntu 22.04+ | بدون Docker (Python مباشر)
#  الاستخدام: sudo bash deploy/production/deploy-production.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

DEPLOY_DIR="/opt/azabot"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE_USER="azab"
PYTHON_BIN="python3.11"
BLUE=$'\033[1;34m'; GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; NC=$'\033[0m'

log()  { printf '%s[deploy]%s %s\n' "$BLUE"   "$NC" "$*"; }
ok()   { printf '%s[ok]%s    %s\n' "$GREEN"  "$NC" "$*"; }
warn() { printf '%s[warn]%s  %s\n' "$YELLOW" "$NC" "$*"; }
fail() { printf '%s[fail]%s  %s\n' "$RED"    "$NC" "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || fail "Run with sudo or as root"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || fail "Python 3.11 not found. Run server-setup.sh first."

# ── 1. Create system user ─────────────────────────────────────
log "Creating system user: $SERVICE_USER"
id "$SERVICE_USER" &>/dev/null || useradd --system --shell /bin/bash --home-dir "$DEPLOY_DIR" --create-home "$SERVICE_USER"
ok "User: $SERVICE_USER"

# ── 2. Sync project files ─────────────────────────────────────
log "Syncing project to $DEPLOY_DIR"
rsync -a --delete \
  --exclude='.git' --exclude='.venv' --exclude='venv' \
  --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='models/*.tar.gz' \
  --exclude='logs/*' --exclude='.runtime/*' \
  --exclude='azabot/node_modules' --exclude='azabot/.pnpm-store' \
  "$REPO_DIR/" "$DEPLOY_DIR/"
ok "Files synced"

# ── 3. Create required directories ───────────────────────────
mkdir -p "$DEPLOY_DIR"/{logs,.runtime/pids,webhook/static/uploads}
chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR"
chmod 750 "$DEPLOY_DIR"
chmod 755 "$DEPLOY_DIR/webhook/static/uploads"
ok "Directories ready"

# ── 4. Python virtualenv + dependencies ──────────────────────
log "Setting up Python virtualenv"
if [[ ! -d "$DEPLOY_DIR/.venv" ]]; then
  sudo -u "$SERVICE_USER" "$PYTHON_BIN" -m venv "$DEPLOY_DIR/.venv"
fi
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip setuptools wheel -q
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install -e "$DEPLOY_DIR/.[dev]" -q
ok "Python environment ready"

# ── 5. Build frontend ─────────────────────────────────────────
log "Building AzaBot frontend"
if command -v pnpm >/dev/null 2>&1; then
  (cd "$DEPLOY_DIR/azabot" && pnpm install --frozen-lockfile && pnpm build)
  ok "Frontend built: azabot/dist"
else
  warn "pnpm not found — skipping frontend build. Install Node.js 22+ and pnpm."
fi

# ── 6. Install/update systemd services ───────────────────────
log "Installing systemd service units"
for unit in azabot-actions azabot-rasa azabot-webhook; do
  src="$DEPLOY_DIR/deploy/systemd/${unit}.service"
  dst="/etc/systemd/system/${unit}.service"
  [[ -f "$src" ]] || fail "Missing unit file: $src"
  cp "$src" "$dst"
  chmod 644 "$dst"
  ok "Installed: $dst"
done
systemctl daemon-reload

# ── 7. Install nginx config ───────────────────────────────────
log "Installing Nginx config"
NGINX_CONF_SRC="$DEPLOY_DIR/deploy/production/nginx/bot.alazab.com.conf"
NGINX_CONF_DST="/etc/nginx/sites-available/bot.alazab.com.conf"
NGINX_LINK="/etc/nginx/sites-enabled/bot.alazab.com.conf"
if [[ -f "$NGINX_CONF_SRC" ]]; then
  cp "$NGINX_CONF_SRC" "$NGINX_CONF_DST"
  ln -sf "$NGINX_CONF_DST" "$NGINX_LINK"
  nginx -t && ok "Nginx config installed and validated"
else
  warn "Nginx config not found — skipping"
fi

# ── 8. Restart services ───────────────────────────────────────
log "Restarting AzaBot services"
for unit in azabot-actions azabot-rasa azabot-webhook; do
  systemctl enable "$unit"
  systemctl restart "$unit"
  sleep 2
  systemctl is-active --quiet "$unit" && ok "$unit is running" || warn "$unit failed to start — check: journalctl -u $unit -n 50"
done

# ── 9. Reload nginx ───────────────────────────────────────────
systemctl reload nginx && ok "Nginx reloaded"

# ── 10. Smoke test ───────────────────────────────────────────
log "Running smoke test"
sleep 5
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health)
if [[ "$HTTP_STATUS" == "200" ]]; then
  ok "Webhook health check: HTTP $HTTP_STATUS ✅"
else
  warn "Webhook health check returned HTTP $HTTP_STATUS — services may still be warming up"
fi

echo ""
ok "═══════════════════════════════════════════════"
ok " AzaBot deployed successfully 🎉"
ok " Webhook : http://127.0.0.1:8000"
ok " Public  : https://bot.alazab.com"
ok " Logs    : journalctl -u azabot-webhook -f"
ok " Status  : bash scripts/botctl.sh status"
ok "═══════════════════════════════════════════════"
