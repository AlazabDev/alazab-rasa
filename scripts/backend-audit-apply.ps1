$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$ReportDir = Join-Path $Root "reports"
if (-not (Test-Path $ReportDir)) {
    New-Item -ItemType Directory -Path $ReportDir | Out-Null
}

$ReportPath = Join-Path $ReportDir "backend-audit-report-after-fix.json"

Write-Host "Running backend audit with safe fixes..." -ForegroundColor Cyan
python scripts\backend_audit_fix.py --apply --output $ReportPath

Write-Host "Report written to $ReportPath" -ForegroundColor Green
