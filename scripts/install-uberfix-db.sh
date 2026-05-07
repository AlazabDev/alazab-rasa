#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Required env:
# - UBERFIX_DB_URL: postgres connection string
# - UBERFIX_API_KEY: maintenance service key
# Optional:
# - UBERFIX_DB_SQL_FILE: custom SQL file path

if [[ -z "${UBERFIX_DB_URL:-}" ]]; then
  echo "Missing UBERFIX_DB_URL" >&2
  exit 1
fi

if [[ -z "${UBERFIX_API_KEY:-}" ]]; then
  echo "Missing UBERFIX_API_KEY" >&2
  exit 1
fi

SQL_FILE="${UBERFIX_DB_SQL_FILE:-deploy/production/sql/uberfix.sql}"
if [[ ! -f "$SQL_FILE" ]]; then
  echo "SQL file not found: $SQL_FILE" >&2
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required but not installed." >&2
  exit 1
fi

echo "Applying UberFix schema from: $SQL_FILE"
psql "$UBERFIX_DB_URL" -v ON_ERROR_STOP=1 -f "$SQL_FILE"

echo "Schema applied."
echo "Reminder: keep UBERFIX_API_KEY in environment only; never hardcode in scripts."
