#!/usr/bin/env bash
set -euo pipefail

failed=0

check_any() {
  local label="$1"
  shift

  local name
  for name in "$@"; do
    if [[ -n "${!name:-}" ]]; then
      echo "[ok] $label"
      return 0
    fi
  done

  echo "[missing] $label: $*" >&2
  failed=1
}

check_any "Admin password" ADMIN_PASSWORD
check_any "Admin session secret" ADMIN_SESSION_SECRET
check_any "Maintenance gateway URL" MAINTENANCE_GATEWAY_URL UBERFIX_API_URL UBERFIX_BOT_GATEWAY_URL
check_any "Maintenance API key" MAINTENANCE_API_KEY UBERFIX_API_KEY
check_any "Allowed CORS origins" ALLOWED_ORIGINS

if [[ "$failed" -ne 0 ]]; then
  echo "Backend environment is incomplete." >&2
  exit 1
fi

echo "Backend environment is ready."
