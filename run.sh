#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "scripts/start-backend-nodocker.sh" ]]; then
  echo "Missing script: scripts/start-backend-nodocker.sh" >&2
  exit 1
fi

if [[ -z "${ALLOWED_ORIGINS:-}" ]]; then
  export ALLOWED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
fi

bash scripts/start-backend-nodocker.sh
