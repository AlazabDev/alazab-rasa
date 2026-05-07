#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

HOST_ADDRESS="${HOST_ADDRESS:-127.0.0.1}"
RASA_PORT="${RASA_PORT:-5005}"
ACTION_PORT="${ACTION_PORT:-5055}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8080}"
ENDPOINTS_FILE="endpoints.yml"

require_file() {
  local path="$1"
  [[ -f "$path" ]] || {
    echo "Required file is missing: $path" >&2
    exit 1
  }
}

require_env_any() {
  local found=""
  local name
  for name in "$@"; do
    if [[ -n "${!name:-}" ]]; then
      found="yes"
      break
    fi
  done

  if [[ -z "$found" ]]; then
    echo "Missing required environment variable. Set one of: $*" >&2
    exit 1
  fi
}

require_file "domain.yml"
require_file "config.yml"
require_file "credentials.yml"
require_file "actions/__init__.py"
require_file "webhook/server.py"
require_file "$ENDPOINTS_FILE"

export PYTHONUTF8=1
export PYTHONUNBUFFERED=1
export ALLOWED_ORIGINS="${ALLOWED_ORIGINS:-http://localhost:8080,http://127.0.0.1:8080,http://localhost:5173,http://127.0.0.1:5173}"

require_env_any ADMIN_PASSWORD
require_env_any ADMIN_SESSION_SECRET
require_env_any MAINTENANCE_GATEWAY_URL UBERFIX_API_URL UBERFIX_BOT_GATEWAY_URL
require_env_any MAINTENANCE_API_KEY UBERFIX_API_KEY

pids=()

cleanup() {
  for pid in "${pids[@]:-}"; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
    fi
  done
}
trap cleanup EXIT INT TERM

echo "Starting backend without Docker..."
echo "Rasa endpoint file: $ENDPOINTS_FILE"
echo "Allowed origins: $ALLOWED_ORIGINS"

python -m rasa_sdk.endpoint --actions actions --port "$ACTION_PORT" &
pids+=("$!")

sleep 2

rasa run \
  --enable-api \
  --host "$HOST_ADDRESS" \
  --port "$RASA_PORT" \
  --credentials credentials.yml \
  --endpoints "$ENDPOINTS_FILE" \
  --cors "$ALLOWED_ORIGINS" &
pids+=("$!")

sleep 2

python -m uvicorn webhook.server:app --host "$HOST_ADDRESS" --port "$WEBHOOK_PORT" &
pids+=("$!")

echo "Action server: http://$HOST_ADDRESS:$ACTION_PORT"
echo "Rasa server:   http://$HOST_ADDRESS:$RASA_PORT"
echo "Webhook API:   http://$HOST_ADDRESS:$WEBHOOK_PORT"

# انتظر أي process تنتهي ثم أوقف الباقين
wait "${pids[@]}" 2>/dev/null || true
echo "A backend process exited; stopping the remaining processes." >&2
exit 1
