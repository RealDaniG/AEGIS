# run_metatron_web.ps1
# Launcher for Metatron's Cube Consciousness Web Interface
# Robust path detection with fallbacks

# Detect script directory robustly
if ($PSCommandPath) {
    $ScriptDir = Split-Path -Parent $PSCommandPath
} elseif ($MyInvocation.MyCommand.Path) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
} else {
    $ScriptDir = Get-Location
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Metatron's Cube Consciousness Engine - Web Interface" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project root
Set-Location $ScriptDir

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8 or higher" -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$required = @("fastapi", "uvicorn", "websockets", "numpy", "scipy")
$missing = @()

foreach ($pkg in $required) {
    try {
        python -c "import $pkg" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $pkg installed" -ForegroundColor Green
        } else {
            $missing += $pkg
            Write-Host "✗ $pkg missing" -ForegroundColor Red
        }
    } catch {
        $missing += $pkg
        Write-Host "✗ $pkg missing" -ForegroundColor Red
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
    $missingStr = $missing -join " "
    python -m pip install $missingStr --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Start the server
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Starting Metatron Consciousness Server..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server URL: http://localhost:8003" -ForegroundColor Green
Write-Host "WebSocket:  ws://localhost:8003/ws" -ForegroundColor Green
Write-Host "API Status: http://localhost:8003/api/status" -ForegroundColor Green
Write-Host "API Docs:   http://localhost:8003/docs" -ForegroundColor Green
Write-Host "" 
Write-Host "ALL FEATURES INTEGRATED ON PORT 8003:" -ForegroundColor Cyan
Write-Host "  - Consciousness Engine" -ForegroundColor Yellow
Write-Host "  - AI Chat System" -ForegroundColor Yellow
Write-Host "  - Document Upload" -ForegroundColor Yellow
Write-Host "  - Model Management" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the server
python scripts/metatron_web_server.py