#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p reports

echo "Backend quality gate started..."

echo "1/5 Static backend audit"
python scripts/backend_audit_fix.py --output reports/backend-audit-report.json

echo "2/5 Validate backend environment variables"
if [[ -f "scripts/validate-backend-env.sh" ]]; then
  bash scripts/validate-backend-env.sh
else
  echo "validate-backend-env.sh not found; skipped"
fi

echo "3/5 Compile backend Python files"
python -m compileall actions webhook

echo "4/5 Smoke test maintenance flow"
python scripts/smoke-maintenance-core.py

echo "5/5 Project production checks"
if [[ -f "scripts/production-readiness.mjs" ]]; then
  node scripts/production-readiness.mjs
else
  echo "production-readiness.mjs not found; skipped"
fi

echo "Backend quality gate passed."
