#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -z "${VIRTUAL_ENV:-}" ]] && ! command -v rasa >/dev/null 2>&1 && [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

RASA_HOST="${RASA_HOST:-127.0.0.1}"
RASA_PORT="${RASA_PORT:-5005}"
RASA_CORS="${RASA_CORS:-}"

args=(
  run
  --interface "$RASA_HOST"
  --port "$RASA_PORT"
  --endpoints endpoints.yml
  --credentials credentials.yml
  --enable-api
)

if [[ -n "$RASA_CORS" ]]; then
  args+=(--cors "$RASA_CORS")
fi

printf '[run-rasa-prod] Starting Rasa on %s:%s\n' "$RASA_HOST" "$RASA_PORT"
exec rasa "${args[@]}"
