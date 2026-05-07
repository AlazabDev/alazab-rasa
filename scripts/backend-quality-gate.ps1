$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not (Test-Path ".\reports")) {
    New-Item -ItemType Directory -Path ".\reports" | Out-Null
}

Write-Host "Backend quality gate started..." -ForegroundColor Cyan

Write-Host "1/5 Static backend audit" -ForegroundColor Yellow
python scripts\backend_audit_fix.py --output reports\backend-audit-report.json
if ($LASTEXITCODE -ne 0) {
    throw "Static backend audit failed. Check reports\backend-audit-report.json"
}

Write-Host "2/5 Validate backend environment variables" -ForegroundColor Yellow
if (Test-Path "scripts\validate-backend-env.ps1") {
    & ".\scripts\validate-backend-env.ps1"
}
else {
    Write-Host "validate-backend-env.ps1 not found; skipped" -ForegroundColor DarkYellow
}

Write-Host "3/5 Compile backend Python files" -ForegroundColor Yellow
python -m compileall actions webhook
if ($LASTEXITCODE -ne 0) {
    throw "Compile step failed."
}

Write-Host "4/5 Smoke test maintenance flow" -ForegroundColor Yellow
python scripts\smoke-maintenance-core.py
if ($LASTEXITCODE -ne 0) {
    throw "Smoke test failed."
}

Write-Host "5/5 Project production checks" -ForegroundColor Yellow
if (Test-Path "scripts\production-readiness.mjs") {
    node scripts\production-readiness.mjs
    if ($LASTEXITCODE -ne 0) {
        throw "Production readiness checks failed."
    }
}
else {
    Write-Host "production-readiness.mjs not found; skipped" -ForegroundColor DarkYellow
}

Write-Host "Backend quality gate passed." -ForegroundColor Green
