param(
    [string]$PythonVersion = "3.11"
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

Write-Host "--- Alazab Group Chatbot: Windows Setup ---" -ForegroundColor Cyan

# 1. Check Python
Write-Host "1. Checking Python..." -ForegroundColor Yellow
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    Write-Host "   Using Python Launcher (py)"
    $pythonCmd = "py -$PythonVersion"
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $ver = python --version
    Write-Host "   Using python ($ver)"
    $pythonCmd = "python"
} else {
    Write-Error "Python not found. Please install Python $PythonVersion from python.org"
}

# 2. Create Virtual Environment
Write-Host "2. Creating Virtual Environment (.venv)..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    & $pythonCmd -m venv .venv
    Write-Host "   Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "   .venv already exists."
}

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$VenvPip = Join-Path $Root ".venv\Scripts\pip.exe"

# 3. Upgrade Pip and Install Dependencies
Write-Host "3. Installing dependencies..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -e ".[dev]"

# 4. Check .env
Write-Host "4. Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "   Created .env from .env.example. PLEASE FILL IT WITH REAL KEYS." -ForegroundColor Green
    } else {
        Write-Host "   .env is missing and no .env.example found. Please create .env manually." -ForegroundColor Red
    }
} else {
    Write-Host "   .env exists."
}

# 5. Create necessary directories
Write-Host "5. Creating local directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "models", "logs", ".runtime", "ssl" -Force | Out-Null

Write-Host "`nSetup Complete!" -ForegroundColor Green
Write-Host "To start the bot locally (No Docker), run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\run-nodocker.ps1"
Write-Host ""
Write-Host "To run with Docker Compose, ensure Docker Desktop is running and run:"
Write-Host "  make up"
