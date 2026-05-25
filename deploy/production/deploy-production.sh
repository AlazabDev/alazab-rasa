#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  deploy-production.sh — AzaBot v4.1
#  Ubuntu 22.04/24.04 | بدون Docker
#  الاستخدام: sudo bash deploy/production/deploy-production.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

DEPLOY_DIR="/opt/azabot"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE_USER="azab"
NGINX_DEST="/etc/nginx/sites-available/bot.alazab.com.conf"
NGINX_LINK="/etc/nginx/sites-enabled/bot.alazab.com.conf"

BLUE=$'\033[1;34m'; GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'; NC=$'\033[0m'

log()  { printf "${BLUE}[deploy]${NC} %s\n" "$*"; }
ok()   { printf "${GREEN}[ok]${NC}    %s\n" "$*"; }
warn() { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
fail() { printf "${RED}[fail]${NC}  %s\n" "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || fail "شغّل بـ sudo"

# ── 1. فحص الجاهزية ────────────────────────────────────────────
log "فحص متطلبات الإنتاج"
[[ -f "$REPO_DIR/.env" ]] || fail ".env مفقود — انسخ .env.example وأكمل القيم"

# تحقق من bcrypt hashes
source <(grep -v '^#' "$REPO_DIR/.env" | grep '=' | sed 's/^/export /' 2>/dev/null || true)
[[ -n "${ADMIN_PASSWORD_HASH_ADMIN:-}" ]] && [[ "${ADMIN_PASSWORD_HASH_ADMIN}" =~ ^\$2b\$ ]] \
  || fail "ADMIN_PASSWORD_HASH_ADMIN مفقود أو غير bcrypt — شغّل: python scripts/gen_password_hash.py"
[[ -n "${ADMIN_SESSION_SECRET:-}" ]] && [[ "${#ADMIN_SESSION_SECRET}" -ge 32 ]] \
  || fail "ADMIN_SESSION_SECRET مفقود أو قصير جداً (≥ 32 حرف)"
[[ -n "${OPENAI_API_KEY:-}" ]] && [[ "${OPENAI_API_KEY}" != "sk-proj-REPLACE_ME" ]] \
  || fail "OPENAI_API_KEY مفقود أو افتراضي"
ok "فحص المتغيرات — ✓"

# ── 2. Python ──────────────────────────────────────────────────
log "اختيار Python"
PYTHON_BIN=""
for py in python3.11 python3.12 python3.10 python3; do
  command -v "$py" >/dev/null 2>&1 && { PYTHON_BIN="$py"; break; }
done
[[ -z "$PYTHON_BIN" ]] && fail "Python غير موجود — sudo apt install python3.11"
ok "Python: $($PYTHON_BIN -V)"

# ── 3. System user ─────────────────────────────────────────────
log "System user: $SERVICE_USER"
id "$SERVICE_USER" &>/dev/null || \
  useradd --system --shell /bin/bash --home "$DEPLOY_DIR" --create-home "$SERVICE_USER"
ok "User: $SERVICE_USER"

# ── 4. Sync files (بدون الملفات الحساسة) ─────────────────────
log "مزامنة الملفات إلى $DEPLOY_DIR"
rsync -a --delete \
  --exclude='.git' --exclude='.venv' --exclude='venv' \
  --exclude='**/__pycache__' --exclude='*.pyc' \
  --exclude='models/*.tar.gz' \
  --exclude='logs/*' --exclude='.runtime/*' \
  --exclude='azabot/node_modules' --exclude='azabot/.pnpm-store' \
  --exclude='azabot/dist' \
  --exclude='ssl/' \
  --exclude='scratch/' \
  --exclude='tools/dev.txt' \
  "$REPO_DIR/" "$DEPLOY_DIR/"
ok "ملفات منقولة (بدون ssl/ وscratch/)"

# ── 5. نسخ .env ────────────────────────────────────────────────
# .env لا يُنسَخ بـ rsync — ننسخه يدوياً إذا كان موجوداً في الريبو
if [[ -f "$REPO_DIR/.env" ]] && [[ ! -f "$DEPLOY_DIR/.env" ]]; then
  cp "$REPO_DIR/.env" "$DEPLOY_DIR/.env"
  chmod 600 "$DEPLOY_DIR/.env"
  ok ".env منسوخ"
elif [[ -f "$DEPLOY_DIR/.env" ]]; then
  ok ".env موجود مسبقاً (محفوظ)"
else
  fail ".env غير موجود في $DEPLOY_DIR — انسخه يدوياً"
fi
chown "$SERVICE_USER:" "$DEPLOY_DIR/.env"
chmod 600 "$DEPLOY_DIR/.env"

# ── 6. Directories ────────────────────────────────────────────
mkdir -p "$DEPLOY_DIR"/{logs,.runtime/pids,models,webhook/static/uploads}
chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR"
chmod 750 "$DEPLOY_DIR"
chmod 755 "$DEPLOY_DIR/webhook/static/uploads"
ok "المجلدات جاهزة"

# ── 7. Python venv ────────────────────────────────────────────
log "Python venv"
[[ ! -d "$DEPLOY_DIR/.venv" ]] && \
  sudo -u "$SERVICE_USER" "$PYTHON_BIN" -m venv "$DEPLOY_DIR/.venv"
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip setuptools wheel -q
sudo -u "$SERVICE_USER" "$DEPLOY_DIR/.venv/bin/pip" install -r "$DEPLOY_DIR/requirements.txt" -q
ok "Python env جاهز"

# ── 8. Redis (تثبيت إذا غير موجود) ───────────────────────────
log "فحص Redis"
if ! command -v redis-cli &>/dev/null; then
  warn "Redis غير مثبَّت — يُثبَّت الآن"
  apt-get install -y redis-server -q
  systemctl enable redis-server --now
  ok "Redis مُثبَّت وجارٍ"
else
  redis-cli ping 2>/dev/null | grep -q "PONG" && ok "Redis يعمل" || {
    systemctl start redis-server && ok "Redis بدأ" || warn "Redis لم يبدأ — تحقق يدوياً"
  }
fi

# ── 9. Frontend build ─────────────────────────────────────────
log "بناء الفرونت"
if command -v pnpm >/dev/null 2>&1; then
  cd "$DEPLOY_DIR"
  bash azabot/scripts/build-production.sh 2>/dev/null || \
    (cd azabot && pnpm install -q && pnpm build -q)
  chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR/azabot/dist"
  ok "الفرونت مبني: azabot/dist"
elif command -v npm >/dev/null 2>&1; then
  cd "$DEPLOY_DIR/azabot"
  npm install -q && npm run build -q
  chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR/azabot/dist"
  ok "الفرونت مبني (npm)"
else
  warn "pnpm/npm غير موجود — تخطي الفرونت"
fi

# ── 10. Systemd services ──────────────────────────────────────
log "تثبيت systemd units"

# تحديث WorkingDirectory و User في الـ unit files
for unit in azabot-actions azabot-rasa azabot-webhook; do
  src="$DEPLOY_DIR/deploy/systemd/${unit}.service"
  [[ -f "$src" ]] || fail "مفقود: $src"
  sed \
    -e "s|/mnt/apps/alazab-rasa|$DEPLOY_DIR|g" \
    -e "s|User=azureuser|User=$SERVICE_USER|g" \
    "$src" > "/etc/systemd/system/${unit}.service"
  chmod 644 "/etc/systemd/system/${unit}.service"
  ok "مثبَّت: ${unit}.service"
done
systemctl daemon-reload
ok "daemon-reload"

# ── 11. Nginx ─────────────────────────────────────────────────
log "تثبيت Nginx config"
NGINX_SRC="$DEPLOY_DIR/deploy/production/nginx/bot.alazab.com.conf"
[[ -f "$NGINX_SRC" ]] || fail "مفقود: $NGINX_SRC"
sed "s|/opt/azabot|$DEPLOY_DIR|g" "$NGINX_SRC" > "$NGINX_DEST"
ln -sf "$NGINX_DEST" "$NGINX_LINK"
nginx -t && ok "Nginx config صالح" || fail "Nginx config خاطئ"

# ── 12. Enable + restart services ────────────────────────────
log "تشغيل الخدمات"
for unit in azabot-actions azabot-rasa azabot-webhook; do
  systemctl enable "$unit" -q
  systemctl restart "$unit"
  sleep 3
  systemctl is-active --quiet "$unit" \
    && ok "$unit: يعمل ✅" \
    || warn "$unit: تحقق → journalctl -u $unit -n 30"
done

# ── 13. Nginx reload ──────────────────────────────────────────
systemctl reload nginx && ok "Nginx reload ✅"

# ── 14. SSL check ─────────────────────────────────────────────
SSL_CERT="/etc/letsencrypt/live/bot.alazab.com/fullchain.pem"
if [[ -f "$SSL_CERT" ]]; then
  ok "شهادة SSL موجودة ✅"
else
  warn "شهادة SSL غير موجودة — شغّل بعد تشغيل Nginx:"
  warn "  certbot --nginx -d bot.alazab.com -d www.bot.alazab.com"
fi

# ── 15. Smoke test ────────────────────────────────────────────
log "Smoke test"
sleep 6
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health 2>/dev/null || echo "000")
if [[ "$STATUS" == "200" ]]; then
  DETAIL=$(curl -s http://127.0.0.1:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "?")
  ok "Webhook: HTTP 200 | status=$DETAIL ✅"
else
  warn "Webhook: HTTP $STATUS — تحقق → journalctl -u azabot-webhook -n 50"
fi

# ── 16. ملخص ──────────────────────────────────────────────────
echo ""
ok "════════════════════════════════════════════"
ok " 🎉 AzaBot v4.1 نُشر على $DEPLOY_DIR"
ok "════════════════════════════════════════════"
ok " API    : https://bot.alazab.com/health"
ok " Admin  : https://bot.alazab.com/admin"
ok " Logs   : journalctl -u azabot-webhook -f"
ok " Check  : bash scripts/prod-check.sh"
ok " Status : bash scripts/botctl.sh status"
ok "════════════════════════════════════════════"
