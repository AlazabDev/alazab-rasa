#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p reports
python scripts/backend_audit_fix.py --output reports/backend-audit-report.json
echo "Report written to reports/backend-audit-report.json"
