$ErrorActionPreference = "Stop"

function Test-AnyEnv {
    param([string[]]$Names)

    foreach ($name in $Names) {
        if ([Environment]::GetEnvironmentVariable($name)) {
            return $true
        }
    }

    return $false
}

$Checks = @(
    @{
        Name = "Admin password"
        Vars = @("ADMIN_PASSWORD")
    },
    @{
        Name = "Admin session secret"
        Vars = @("ADMIN_SESSION_SECRET")
    },
    @{
        Name = "Maintenance gateway URL"
        Vars = @("MAINTENANCE_GATEWAY_URL", "UBERFIX_API_URL", "UBERFIX_BOT_GATEWAY_URL")
    },
    @{
        Name = "Maintenance API key"
        Vars = @("MAINTENANCE_API_KEY", "UBERFIX_API_KEY")
    },
    @{
        Name = "Allowed CORS origins"
        Vars = @("ALLOWED_ORIGINS")
    }
)

$Failed = @()

foreach ($check in $Checks) {
    if (Test-AnyEnv -Names $check.Vars) {
        Write-Host "[ok] $($check.Name)" -ForegroundColor Green
    }
    else {
        $Failed += "$($check.Name): $($check.Vars -join ' or ')"
        Write-Host "[missing] $($check.Name): $($check.Vars -join ' or ')" -ForegroundColor Red
    }
}

if ($Failed.Count -gt 0) {
    throw "Backend environment is incomplete."
}

Write-Host "Backend environment is ready." -ForegroundColor Cyan
