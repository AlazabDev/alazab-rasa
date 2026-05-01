param(
    [string]$HostAddress = "127.0.0.1",
    [int]$RasaPort = 5005,
    [int]$ActionPort = 5055,
    [int]$WebhookPort = 8000
)

$ErrorActionPreference = "Stop"

function Require-File {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        throw "Required file is missing: $Path"
    }
}

function Require-EnvAny {
    param(
        [string]$Name,
        [string[]]$Alternatives = @()
    )

    $names = @($Name) + $Alternatives
    foreach ($item in $names) {
        if ([Environment]::GetEnvironmentVariable($item)) {
            return
        }
    }

    throw "Missing required environment variable. Set one of: $($names -join ', ')"
}

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

Require-File "domain.yml"
Require-File "config.yml"
Require-File "credentials.yml"
Require-File "actions\__init__.py"
Require-File "webhook\server.py"
Require-File "endpoints.yml"

$EndpointsFile = "endpoints.yml"

if (-not [Environment]::GetEnvironmentVariable("ALLOWED_ORIGINS")) {
    $env:ALLOWED_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
}

Require-EnvAny -Name "ADMIN_PASSWORD"
Require-EnvAny -Name "ADMIN_SESSION_SECRET"
Require-EnvAny -Name "MAINTENANCE_GATEWAY_URL" -Alternatives @("UBERFIX_API_URL", "UBERFIX_BOT_GATEWAY_URL")
Require-EnvAny -Name "MAINTENANCE_API_KEY" -Alternatives @("UBERFIX_API_KEY")

$CommonEnv = @{
    PYTHONUTF8 = "1"
    PYTHONUNBUFFERED = "1"
}

foreach ($key in $CommonEnv.Keys) {
    [Environment]::SetEnvironmentVariable($key, $CommonEnv[$key], "Process")
}

Write-Host "Starting backend without Docker..." -ForegroundColor Cyan
Write-Host "Rasa endpoint file: $EndpointsFile"
Write-Host "Allowed origins: $env:ALLOWED_ORIGINS"

$ActionArgs = @(
    "-m", "rasa_sdk.endpoint",
    "--actions", "actions",
    "--port", $ActionPort
)

$RasaArgs = @(
    "run",
    "--enable-api",
    "--host", $HostAddress,
    "--port", $RasaPort,
    "--credentials", "credentials.yml",
    "--endpoints", $EndpointsFile,
    "--cors", $env:ALLOWED_ORIGINS
)

$WebhookArgs = @(
    "-m", "uvicorn",
    "webhook.server:app",
    "--host", $HostAddress,
    "--port", $WebhookPort
)

$Processes = @()

try {
    $Processes += Start-Process -FilePath "python" -ArgumentList $ActionArgs -WorkingDirectory $Root -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    $Processes += Start-Process -FilePath "rasa" -ArgumentList $RasaArgs -WorkingDirectory $Root -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    $Processes += Start-Process -FilePath "python" -ArgumentList $WebhookArgs -WorkingDirectory $Root -PassThru -WindowStyle Hidden

    Write-Host "Action server: http://$HostAddress`:$ActionPort" -ForegroundColor Green
    Write-Host "Rasa server:   http://$HostAddress`:$RasaPort" -ForegroundColor Green
    Write-Host "Webhook API:   http://$HostAddress`:$WebhookPort" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

    while ($true) {
        foreach ($process in $Processes) {
            if ($process.HasExited) {
                throw "Process exited unexpectedly: PID $($process.Id)"
            }
        }
        Start-Sleep -Seconds 3
    }
}
finally {
    foreach ($process in $Processes) {
        if ($process -and -not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }
}
