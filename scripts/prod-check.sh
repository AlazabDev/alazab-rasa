#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ok() { printf '[OK] %s\n' "$*"; }
fail() { printf '[FAIL] %s\n' "$*" >&2; exit 1; }
info() { printf '[INFO] %s\n' "$*"; }

if [[ -z "${VIRTUAL_ENV:-}" ]] && ! command -v rasa >/dev/null 2>&1 && [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

command -v python >/dev/null 2>&1 || fail "python is not available"
python --version
python - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ is required")
print(f"[OK] Python version is supported: {sys.version.split()[0]}")
PY

command -v rasa >/dev/null 2>&1 || fail "rasa is not available on PATH"
info "Rasa binary: $(command -v rasa)"
rasa --version

required_files=(
  "config.yml"
  "domain.yml"
  "credentials.yml"
  "endpoints.yml"
  "requirements.txt"
)
for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || fail "Missing required file: $file"
  ok "Found $file"
done

[[ -d "data" ]] || fail "Missing data directory"
[[ -d "actions" ]] || fail "Missing actions directory"

info "Validating Rasa domain and training data"
rasa data validate --domain domain.yml --data data
ok "Rasa domain and data validation passed"

info "Checking action imports"
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import importlib
import pkgutil
import actions

for module in pkgutil.walk_packages(actions.__path__, actions.__name__ + "."):
    importlib.import_module(module.name)

print("[OK] Action imports passed")
PY

SUPABASE_DIR="${SUPABASE_DIR:-}"
if [[ -z "$SUPABASE_DIR" ]]; then
  if [[ -d "supabase" ]]; then
    SUPABASE_DIR="supabase"
  elif [[ -d "azabot/supabase" ]]; then
    SUPABASE_DIR="azabot/supabase"
  fi
fi

if [[ -n "$SUPABASE_DIR" ]]; then
  [[ -f "$SUPABASE_DIR/.temp/project-ref" ]] || fail "Supabase project is not linked: $SUPABASE_DIR/.temp/project-ref missing"
  info "Supabase project ref: $(tr -d '[:space:]' < "$SUPABASE_DIR/.temp/project-ref")"

  info "Supabase functions:"
  if [[ -d "$SUPABASE_DIR/functions" ]]; then
    find "$SUPABASE_DIR/functions" -mindepth 1 -maxdepth 1 -type d -printf '  - %f\n' | sort
  else
    fail "Missing Supabase functions directory"
  fi

  info "Supabase migrations:"
  if [[ -d "$SUPABASE_DIR/migrations" ]]; then
    find "$SUPABASE_DIR/migrations" -maxdepth 1 -type f -printf '  - %f\n' | sort
  else
    fail "Missing Supabase migrations directory"
  fi
else
  info "No Supabase directory found"
fi

ok "Production check completed"
