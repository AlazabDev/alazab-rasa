#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  deploy-production.sh — AzaBot v3 Full Production Deploy
#  الخادم: Ubuntu 22.04/24.04 | بدون Docker
#  الاستخدام: sudo bash deploy/production/deploy-production.sh
#
#  ما يفعله:
#    1. إنشاء system user
#    2. مزامنة ملفات المشروع
#    3. Python venv + packages
#    4. بناء React frontend
#    5. تثبيت systemd services
#    6. تثبيت Nginx config
#    7. إعادة تشغيل الخدمات
#    8. Smoke test
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

DEPLOY_DIR="/opt/azabot"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE_USER="azab"
NGINX_CONF_DEST="/etc/nginx/sites-available/bot.alazab.com.conf"
NGINX_LINK="/etc/nginx/sites-enabled/bot.alazab.com.conf"

BLUE=$'\033[1;34m'; GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; NC=$'\033[0m'

log()  { printf "${BLUE}[deploy]${NC} %s\n" "$*"; }
ok()   { printf "${GREEN}[ok]${NC}    %s\n" "$*"; }
warn() { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
fail() { printf "${RED}[fail]${NC}  %s\n" "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || fail "شغّل بـ sudo"

# ── 1. Python ──────────────────────────────────────────────────
log "اختيار Python"
PYTHON_BIN=""
for py in python3.11 python3.12 python3.10 python3; do
  command -v "$py" >/dev/null 2>&1 && { PYTHON_BIN="$py"; break; }
done
[[ -z "$PYTHON_BIN" ]] && fail "Python غير موجود — sudo apt install python3.11"
ok "Python: $($PYTHON_BIN -V)"

# ── 2. System user ─────────────────────────────────────────────
log "System user: $SERVICE_USER"
id "$SERVICE_USER" &>/dev/null || \
  useradd --system --shell /bin/bash --home "$DEPLOY_DIR" --create-home "$SERVICE_USER"
ok "User: $SERVICE_USER"

# ── 3. Sync files ──────────────────────────────────────────────
log "مزامنة الملفات إلى $DEPLOY_DIR"
rsync -a --delete \
  --exclude='.git' --exclude='.venv' --exclude='venv' \
  --exclude='**/__pycache__' --exclude='*.pyc' \
  --exclude='models/*.tar.gz' \
  --exclude='logs/*' --exclude='.runtime/*' \
  --exclude='azabot/node_modules' --exclude='azabot/.pnpm-store' \
  --exclude='azabot/dist' \
  --exclude='azabot/.env.local' \
  "$REPO_DIR/" "$DEPLOY_DIR/"
ok "ملفات منقولة"

# ── 4. Directories ────────────────────────────────────────────
mkdir -p "$DEPLOY_DIR"/{logs,.runtime/pids,models,webhook/static/uploads}
chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR"
chmod 750 "$DEPLOY_DIR"
chmod 755 "$DEPLOY_DIR/webhook/static/uploads"
ok "المجلدات جاهزة"

# ── 5. Python venv ────────────────────────────────────────────
log "Python venv"
[[ ! -d "$DEPLOY_DIR/.venv" ]] && \
  sudo -u "$SERVICE_USER" "$PYTHON_BIN" -m venv "$DEPLOY_DIR/.venv"
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip setuptools wheel -q
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install -e "$DEPLOY_DIR/.[dev]" -q
ok "Python env جاهز"

# ── 6. Frontend build ─────────────────────────────────────────
log "بناء الفرونت"
if command -v pnpm >/dev/null 2>&1; then
  cd "$DEPLOY_DIR"
  bash azabot/scripts/build-production.sh
  chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR/azabot/dist"
  ok "الفرونت مبني: azabot/dist"
else
  warn "pnpm غير موجود — تخطي الفرونت (curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -)"
fi

# ── 7. Systemd services ───────────────────────────────────────
log "تثبيت systemd units"
for unit in azabot-actions azabot-rasa azabot-webhook; do
  src="$DEPLOY_DIR/deploy/systemd/${unit}.service"
  [[ -f "$src" ]] || fail "مفقود: $src"
  cp "$src" "/etc/systemd/system/${unit}.service"
  chmod 644 "/etc/systemd/system/${unit}.service"
  ok "مثبّت: ${unit}.service"
done
systemctl daemon-reload
ok "daemon-reload"

# ── 8. Nginx ──────────────────────────────────────────────────
log "تثبيت Nginx config"
NGINX_SRC="$DEPLOY_DIR/deploy/production/nginx/bot.alazab.com.conf"
[[ -f "$NGINX_SRC" ]] || fail "مفقود: $NGINX_SRC"

# تحديث dist_root في config
sed "s|/opt/azabot/azabot/dist|$DEPLOY_DIR/azabot/dist|g" \
  "$NGINX_SRC" > "$NGINX_CONF_DEST"

ln -sf "$NGINX_CONF_DEST" "$NGINX_LINK"
nginx -t && ok "Nginx config صالح" || fail "Nginx config خاطئ"

# ── 9. Enable + restart services ─────────────────────────────
log "تشغيل الخدمات"
for unit in azabot-actions azabot-rasa azabot-webhook; do
  systemctl enable "$unit" -q
  systemctl restart "$unit"
  sleep 3
  systemctl is-active --quiet "$unit" \
    && ok "$unit: يعمل" \
    || warn "$unit: تحقق → journalctl -u $unit -n 30"
done

# ── 10. Nginx reload ──────────────────────────────────────────
systemctl reload nginx && ok "Nginx reload"

# ── 11. SSL check ─────────────────────────────────────────────
SSL_CERT="/etc/letsencrypt/live/bot.alazab.com/fullchain.pem"
if [[ ! -f "$SSL_CERT" ]]; then
  warn "شهادة SSL غير موجودة — شغّل:"
  warn "  certbot --nginx -d bot.alazab.com -d www.bot.alazab.com"
fi

# ── 12. Smoke test ────────────────────────────────────────────
log "Smoke test"
sleep 6
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health)
[[ "$STATUS" == "200" ]] \
  && ok "Webhook: HTTP $STATUS ✅" \
  || warn "Webhook: HTTP $STATUS — الخدمة قد تحتاج وقتاً"

echo ""
ok "══════════════════════════════════════════════"
ok " 🎉 AzaBot نُشر على bot.alazab.com"
ok "══════════════════════════════════════════════"
ok " API    : https://bot.alazab.com/health"
ok " Admin  : https://bot.alazab.com/admin"
ok " Logs   : journalctl -u azabot-webhook -f"
ok " Status : bash scripts/botctl.sh status"
ok "══════════════════════════════════════════════"
