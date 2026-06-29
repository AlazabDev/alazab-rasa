#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -z "${VIRTUAL_ENV:-}" ]] && ! python -c "import rasa_sdk" >/dev/null 2>&1 && [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

ACTION_HOST="${ACTION_HOST:-127.0.0.1}"
ACTION_PORT="${ACTION_PORT:-5055}"
export SANIC_HOST="$ACTION_HOST"

printf '[run-actions-prod] Starting Rasa action server on %s:%s\n' "$ACTION_HOST" "$ACTION_PORT"
exec python -m rasa_sdk.endpoint --actions actions --port "$ACTION_PORT"
