#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

log() { printf '[train-prod] %s\n' "$*"; }
fail() { printf '[train-prod][FAIL] %s\n' "$*" >&2; exit 1; }

if [[ -z "${VIRTUAL_ENV:-}" ]] && ! command -v rasa >/dev/null 2>&1 && [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

command -v rasa >/dev/null 2>&1 || fail "rasa is not available on PATH"

log "Validating Rasa data"
rasa data validate

log "Training production model"
rasa train --force

log "Training completed; model artifact stored in models/"
