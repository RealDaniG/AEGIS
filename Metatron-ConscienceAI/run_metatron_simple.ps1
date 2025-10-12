# run_metatron_web.ps1
# Simple launcher for Metatron's Cube Consciousness Web Interface

# Detect script directory
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

# Change to project root
Set-Location $ScriptDir

Write-Host ""
Write-Host "Starting Metatron Consciousness Server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server URL: http://localhost:8001" -ForegroundColor Yellow
Write-Host "WebSocket:  ws://localhost:8001/ws" -ForegroundColor Yellow
Write-Host "API Status: http://localhost:8001/api/status" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# Run the server directly
python scripts/metatron_web_server.py