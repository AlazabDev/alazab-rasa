#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  server-setup.sh — إعداد السيرفر كاملاً (مرة واحدة)
#  Ubuntu 22.04/24.04 | 2 vCPU | 8 GB RAM
#  الاستخدام: sudo bash deploy/production/server-setup.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; YELLOW=$'\033[1;33m'; NC=$'\033[0m'
ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
info() { printf "${CYAN}[setup]${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }

[[ $EUID -eq 0 ]] || { echo "شغّل بـ sudo"; exit 1; }

DOMAIN="bot.alazab.com"

# ══════════════════════════════════════════════════════════════
info "1/8 — تحديث النظام"
# ══════════════════════════════════════════════════════════════
apt-get update -qq
apt-get upgrade -y -qq
apt-get install -y -qq \
  curl wget git build-essential software-properties-common \
  ufw fail2ban \
  python3.11 python3.11-venv python3.11-dev \
  libpq-dev pkg-config \
  redis-server \
  postgresql postgresql-contrib \
  nginx \
  certbot python3-certbot-nginx \
  lsof net-tools htop iotop \
  dos2unix jq
ok "حزم النظام مثبّتة"

# ══════════════════════════════════════════════════════════════
info "2/8 — Node.js 22 + pnpm"
# ══════════════════════════════════════════════════════════════
if ! command -v node >/dev/null 2>&1 || [[ "$(node -v | cut -d. -f1 | tr -d 'v')" -lt 20 ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash - -q
  apt-get install -y -qq nodejs
fi
command -v pnpm >/dev/null 2>&1 || npm install -g pnpm -q
ok "Node.js $(node -v) + pnpm $(pnpm -v)"

# ══════════════════════════════════════════════════════════════
info "3/8 — Swap 4GB (مهم لـ Rasa على 2 vCPU)"
# ══════════════════════════════════════════════════════════════
if ! swapon --show | grep -q swapfile; then
  bash /opt/azabot/deploy/production/setup-swap.sh 2>/dev/null || \
  bash "$(dirname "$0")/setup-swap.sh" 2>/dev/null || \
  { fallocate -l 4G /swapfile; chmod 600 /swapfile; mkswap /swapfile; swapon /swapfile; }
fi
ok "Swap: $(free -h | awk '/Swap/{print $2}')"

# ══════════════════════════════════════════════════════════════
info "4/8 — Redis"
# ══════════════════════════════════════════════════════════════
# تحسين Redis لـ 2 vCPU
cat >> /etc/redis/redis.conf << 'REDIS_CONF'

# ── AzaBot Redis Tuning ───────────────────────────────────────
maxmemory 256mb
maxmemory-policy allkeys-lru
save ""
appendonly no
REDIS_CONF
systemctl enable redis-server -q
systemctl restart redis-server
sleep 1
redis-cli ping | grep -q PONG && ok "Redis يعمل" || warn "Redis: تحقق يدوياً"

# ══════════════════════════════════════════════════════════════
info "5/8 — PostgreSQL"
# ══════════════════════════════════════════════════════════════
systemctl enable postgresql -q
systemctl start postgresql
sleep 2

# إنشاء user + DB
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='azab_user'" | grep -q 1 || \
  sudo -u postgres createuser --no-superuser --no-createdb --no-createrole azab_user

PROD_DB_PASS="${DB_PASSWORD:-$(openssl rand -base64 24)}"
sudo -u postgres psql -c "ALTER USER azab_user WITH PASSWORD '$PROD_DB_PASS';" -q
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='alazab_core'" | grep -q 1 || \
  sudo -u postgres createdb -O azab_user alazab_core

ok "PostgreSQL: azab_user@alazab_core"
echo "  DB_PASSWORD=$PROD_DB_PASS  ← احفظ هذا في .env"

# ══════════════════════════════════════════════════════════════
info "6/8 — Nginx"
# ══════════════════════════════════════════════════════════════
# نسخ nginx.conf المُحسَّن
cp "$(dirname "$0")/nginx/nginx.conf" /etc/nginx/nginx.conf 2>/dev/null || true
cp "$(dirname "$0")/nginx/bot.alazab.com.conf" \
   /etc/nginx/sites-available/bot.alazab.com.conf
ln -sf /etc/nginx/sites-available/bot.alazab.com.conf \
       /etc/nginx/sites-enabled/bot.alazab.com.conf
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl enable nginx -q && systemctl reload nginx
ok "Nginx جاهز"

# ══════════════════════════════════════════════════════════════
info "7/8 — Firewall (UFW)"
# ══════════════════════════════════════════════════════════════
ufw --force reset >/dev/null 2>&1
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow ssh >/dev/null
ufw allow 80/tcp >/dev/null
ufw allow 443/tcp >/dev/null
# المنافذ الداخلية مغلقة من الخارج
ufw --force enable >/dev/null
ok "Firewall: SSH+80+443 فقط مفتوحة"

# ══════════════════════════════════════════════════════════════
info "8/8 — SSL (Let's Encrypt)"
# ══════════════════════════════════════════════════════════════
if [[ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]]; then
  warn "تشغيل certbot..."
  certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" \
    --non-interactive --agree-tos \
    --email "admin@alazab.com" \
    --redirect 2>/dev/null || \
  warn "certbot: شغّله يدوياً: certbot --nginx -d $DOMAIN"
else
  ok "SSL موجود: $DOMAIN"
fi

echo ""
printf "${GREEN}══════════════════════════════════════════════${NC}\n"
printf "${GREEN} ✅ السيرفر جاهز!${NC}\n"
printf "${GREEN}══════════════════════════════════════════════${NC}\n"
echo ""
echo "  الخطوة التالية:"
echo "  sudo bash deploy/production/deploy-production.sh"
echo ""
