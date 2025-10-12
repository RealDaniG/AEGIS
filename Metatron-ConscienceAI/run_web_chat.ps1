# run_web_chat.ps1
# Launcher for ConscienceAI Web Chat Server
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
Write-Host " ConscienceAI Web Chat Server" -ForegroundColor Cyan
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

$required = @("fastapi", "uvicorn", "websockets", "numpy", "transformers", "torch")
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
Write-Host " Starting ConscienceAI Web Chat Server..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server URL: http://localhost:5180" -ForegroundColor Green
Write-Host "WebSocket:  ws://localhost:5180/ws/chat" -ForegroundColor Green
Write-Host "API Status: http://localhost:5180/api/health" -ForegroundColor Green
Write-Host "API Docs:   http://localhost:5180/docs" -ForegroundColor Green
Write-Host "" 
Write-Host "ALL FEATURES INTEGRATED ON PORT 5180:" -ForegroundColor Cyan
Write-Host "  - AI Chat System" -ForegroundColor Yellow
Write-Host "  - Document Upload" -ForegroundColor Yellow
Write-Host "  - RAG Integration" -ForegroundColor Yellow
Write-Host "  - Session Management" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the server
python scripts/web_chat_server.py