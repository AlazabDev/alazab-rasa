#!/usr/bin/env bash
set -Eeuo pipefail

APP_USER="${APP_USER:-alazab}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_BASE="${APP_BASE:-/opt/alazab-rasa}"
APP_ROOT="${APP_ROOT:-$APP_BASE/app}"
UPLOADS_DIR="${UPLOADS_DIR:-$APP_BASE/uploads}"
RUNTIME_DIR="${RUNTIME_DIR:-$APP_BASE/runtime}"
ENV_DIR="${ENV_DIR:-/etc/opt/alazab-rasa}"
LOG_DIR="${LOG_DIR:-/var/log/alazab-rasa}"
NODE_MAJOR="${NODE_MAJOR:-22}"
PNPM_VERSION="${PNPM_VERSION:-10.33.0}"

log() { printf '\033[1;34m[bootstrap]\033[0m %s\n' "$*"; }
ok() { printf '\033[1;32m[ok]\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31m[fail]\033[0m %s\n' "$*" >&2; exit 1; }

require_root() {
  [[ "${EUID}" -eq 0 ]] || fail "Run this script as root."
}

install_packages() {
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    gnupg \
    unzip \
    build-essential \
    ffmpeg \
    libpq-dev \
    nginx \
    redis-server \
    postgresql \
    postgresql-contrib \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    certbot \
    python3-certbot-nginx
}

install_node() {
  local current_major=""
  if command -v node >/dev/null 2>&1; then
    current_major="$(node -p 'process.versions.node.split(".")[0]')"
  fi

  if [[ -n "$current_major" && "$current_major" -ge "$NODE_MAJOR" ]]; then
    log "Node.js $current_major already installed"
  else
    log "Installing Node.js ${NODE_MAJOR}.x"
    curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
    apt-get install -y nodejs
  fi

  corepack enable
  corepack prepare "pnpm@${PNPM_VERSION}" --activate
}

ensure_user() {
  if id -u "$APP_USER" >/dev/null 2>&1; then
    log "User $APP_USER already exists"
    usermod -g "$APP_GROUP" "$APP_USER"
  else
    log "Creating user $APP_USER"
    useradd --create-home --shell /bin/bash --gid "$APP_GROUP" "$APP_USER"
  fi
}

ensure_group() {
  if getent group "$APP_GROUP" >/dev/null 2>&1; then
    return
  fi
  log "Creating group $APP_GROUP"
  groupadd "$APP_GROUP"
}

prepare_directories() {
  install -d -m 0755 "$APP_BASE"
  install -d -m 0755 "$APP_ROOT"
  install -d -m 0755 "$UPLOADS_DIR"
  install -d -m 0755 "$RUNTIME_DIR"
  install -d -m 0755 "$LOG_DIR"
  install -d -m 0750 "$ENV_DIR"
  chown -R "$APP_USER:$APP_GROUP" "$APP_BASE" "$LOG_DIR"
  chown root:"$APP_GROUP" "$ENV_DIR"
}

enable_services() {
  systemctl enable --now postgresql
  systemctl enable --now redis-server
  systemctl enable --now nginx
}

main() {
  require_root
  ensure_group
  install_packages
  install_node
  ensure_user
  prepare_directories
  enable_services

  ok "Base server packages are ready."
  echo ""
  echo "Next:"
  echo "  1. Clone the repo into: $APP_ROOT"
  echo "  2. Copy deploy/production/.env.example to: $ENV_DIR/.env"
  echo "  3. Create PostgreSQL DB/user and set Redis password"
  echo "  4. Run scripts/deploy-server-nodocker.sh as user: $APP_USER"
}

main "$@"
