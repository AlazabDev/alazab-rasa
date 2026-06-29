#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

log() { printf '[supabase-cloud-sync] %s\n' "$*"; }
fail() { printf '[supabase-cloud-sync][FAIL] %s\n' "$*" >&2; exit 1; }

SUPABASE_DIR="${SUPABASE_DIR:-}"
if [[ -z "$SUPABASE_DIR" ]]; then
  if [[ -d "supabase" ]]; then
    SUPABASE_DIR="supabase"
  elif [[ -d "azabot/supabase" ]]; then
    SUPABASE_DIR="azabot/supabase"
  else
    fail "No Supabase directory found"
  fi
fi

[[ -d "$SUPABASE_DIR" ]] || fail "Supabase directory not found: $SUPABASE_DIR"
[[ -f "$SUPABASE_DIR/.temp/project-ref" ]] || fail "Project is not linked; missing $SUPABASE_DIR/.temp/project-ref"
command -v supabase >/dev/null 2>&1 || fail "supabase CLI is not available on PATH"

PROJECT_REF="$(tr -d '[:space:]' < "$SUPABASE_DIR/.temp/project-ref")"
[[ -n "$PROJECT_REF" ]] || fail "Linked project ref is empty"
log "Linked project ref: $PROJECT_REF"

(
  cd "$SUPABASE_DIR"
  log "Listing migrations"
  supabase migration list

  log "Pushing migrations to Supabase Cloud"
  supabase db push

  if [[ -d "functions" ]]; then
    while IFS= read -r function_dir; do
      function_name="$(basename "$function_dir")"
      if [[ "$function_name" == "_shared" ]]; then
        log "Skipping shared support folder: $function_name"
        continue
      fi

      if supabase functions deploy "$function_name"; then
        log "Function deployed successfully: $function_name"
      else
        fail "Function deploy failed: $function_name"
      fi
    done < <(find functions -mindepth 1 -maxdepth 1 -type d | sort)
  else
    log "No functions directory found"
  fi
)

log "Supabase Cloud sync completed"
