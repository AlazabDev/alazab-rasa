$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$DbUrl = [Environment]::GetEnvironmentVariable("UBERFIX_DB_URL")
if (-not $DbUrl) {
    throw "Missing UBERFIX_DB_URL"
}

$ApiKey = [Environment]::GetEnvironmentVariable("UBERFIX_API_KEY")
if (-not $ApiKey) {
    throw "Missing UBERFIX_API_KEY"
}

$SqlFile = [Environment]::GetEnvironmentVariable("UBERFIX_DB_SQL_FILE")
if (-not $SqlFile) {
    $SqlFile = "deploy\production\sql\uberfix.sql"
}

if (-not (Test-Path $SqlFile)) {
    throw "SQL file not found: $SqlFile"
}

if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    throw "psql is required but not installed."
}

Write-Host "Applying UberFix schema from: $SqlFile" -ForegroundColor Cyan
& psql $DbUrl -v ON_ERROR_STOP=1 -f $SqlFile

Write-Host "Schema applied." -ForegroundColor Green
Write-Host "Reminder: keep UBERFIX_API_KEY in environment only; never hardcode in scripts." -ForegroundColor Yellow
