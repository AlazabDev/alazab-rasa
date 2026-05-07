#!/usr/bin/env bash
set -Eeuo pipefail

# Run this on a fresh Ubuntu server after DNS points to the machine.
# Edit the variables below first.

REPO_URL="git@github.com:YOUR_ORG/alazab-rasa.git"
DOMAIN="bot.alazab.com"
APP_USER="alazab"
APP_BASE="/opt/alazab-rasa"
APP_ROOT="$APP_BASE/app"
ENV_FILE="/etc/opt/alazab-rasa/.env"
DB_NAME="alazab_rasa"
DB_USER="alazab_bot"
DB_PASSWORD="CHANGE_ME_DB_PASSWORD"
REDIS_PASSWORD="CHANGE_ME_REDIS_PASSWORD"
ADMIN_PASSWORD="CHANGE_ME_ADMIN_PASSWORD"
ADMIN_SESSION_SECRET="CHANGE_ME_LONG_RANDOM_SECRET"
RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
OPENAI_API_KEY="CHANGE_ME_OPENAI_KEY"
ISSUE_SSL="false"

fail() { printf '\033[1;31m[fail]\033[0m %s\n' "$*" >&2; exit 1; }
log() { printf '\033[1;34m[deploy]\033[0m %s\n' "$*"; }

[[ "${EUID}" -eq 0 ]] || fail "Run this script as root."

for value in \
  "$REPO_URL" \
  "$DB_PASSWORD" \
  "$REDIS_PASSWORD" \
  "$ADMIN_PASSWORD" \
  "$ADMIN_SESSION_SECRET" \
  "$RASA_PRO_LICENSE" \
  "$OPENAI_API_KEY"
do
  [[ "$value" == CHANGE_ME* || "$value" == git@github.com:YOUR_ORG/* ]] && fail "Edit deploy/production/first-deploy.example.sh before running it."
done

log "Bootstrapping base server packages"
bash scripts/bootstrap-server-ubuntu.sh

if [[ -d "$APP_ROOT/.git" ]]; then
  log "Updating existing repo in $APP_ROOT"
  sudo -u "$APP_USER" git -C "$APP_ROOT" fetch origin main
  sudo -u "$APP_USER" git -C "$APP_ROOT" checkout main
  sudo -u "$APP_USER" git -C "$APP_ROOT" pull --ff-only origin main
else
  log "Cloning repo into $APP_ROOT"
  sudo -u "$APP_USER" git clone "$REPO_URL" "$APP_ROOT"
fi

log "Writing production env"
install -m 0640 -o root -g "$APP_USER" "$APP_ROOT/deploy/production/.env.bot.alazab.example" "$ENV_FILE"
sed -i "s|^RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
sed -i "s|^OPENAI_API_KEY=.*$|OPENAI_API_KEY=${OPENAI_API_KEY}|" "$ENV_FILE"
sed -i "s|^DB_PASSWORD=.*$|DB_PASSWORD=${DB_PASSWORD}|" "$ENV_FILE"
sed -i "s|^REDIS_PASSWORD=.*$|REDIS_PASSWORD=${REDIS_PASSWORD}|" "$ENV_FILE"
sed -i "s|^ADMIN_PASSWORD=.*$|ADMIN_PASSWORD=${ADMIN_PASSWORD}|" "$ENV_FILE"
sed -i "s|^ADMIN_SESSION_SECRET=.*$|ADMIN_SESSION_SECRET=${ADMIN_SESSION_SECRET}|" "$ENV_FILE"

log "Ensuring local PostgreSQL database and user"
sudo -u postgres psql <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${DB_USER}') THEN
    CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';
  ELSE
    ALTER ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}';
  END IF;
END
\$\$;
SQL
sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
  sudo -u postgres createdb -O "${DB_USER}" "${DB_NAME}"

log "Configuring Redis password"
cp /etc/redis/redis.conf /etc/redis/redis.conf.bak.$(date +%Y%m%d%H%M%S)
grep -qE '^#?\s*requirepass\s+' /etc/redis/redis.conf \
  && sed -Ei "s/^#?\s*requirepass\s+.*/requirepass ${REDIS_PASSWORD}/" /etc/redis/redis.conf \
  || echo "requirepass ${REDIS_PASSWORD}" >> /etc/redis/redis.conf
systemctl restart redis-server

log "Deploying application services"
sudo -u "$APP_USER" bash -lc "
  cd '$APP_ROOT' &&
  bash scripts/deploy-server-nodocker.sh \
    --env-file '$ENV_FILE' \
    --branch main \
    --configure-nginx \
    --domain '$DOMAIN'
"

if [[ "$ISSUE_SSL" == "true" ]]; then
  log "Issuing SSL certificate for $DOMAIN"
  certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "admin@alazab.com"
fi

log "Done"
echo "Health checks:"
echo "  curl -fsS http://127.0.0.1:5005/"
echo "  curl -fsS http://127.0.0.1:8000/health"
echo "  curl -I https://${DOMAIN}"
