Param(
  [int]$ApiPort = 8005,
  [int]$WsPort = 8006,
  [string]$Host = "0.0.0.0"
)

# Set console encoding to UTF-8
chcp 65001 > $null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  UNIFIED METATRON-A.G.I SYSTEM STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
Write-Host "[1/3] Checking Python environment..." -ForegroundColor Yellow
python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and add to PATH." -ForegroundColor Red
    exit 1
}

# Check and install required packages
Write-Host "[2/3] Verifying Python dependencies..." -ForegroundColor Yellow
try {
    python -c "import sys; import importlib.util; missing = []; packages = ['numpy', 'aiohttp', 'fastapi', 'uvicorn', 'websockets', 'cryptography']; [missing.append(pkg) for pkg in packages if importlib.util.find_spec(pkg) is None]; sys.exit(1) if missing else sys.exit(0)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing required packages..." -ForegroundColor Yellow
        pip install -r unified_requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Warning: Failed to install some requirements" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Warning: Could not verify all dependencies" -ForegroundColor Yellow
}

# Start the unified system
Write-Host "[3/3] Starting Unified System..." -ForegroundColor Yellow
Write-Host "API Server: http://$Host:$ApiPort" -ForegroundColor Green
Write-Host "WebSocket Server: ws://$Host:$WsPort" -ForegroundColor Green
Write-Host ""

# Set environment variables
$env:UNIFIED_API_PORT = $ApiPort
$env:UNIFIED_WS_PORT = $WsPort

# Start the unified system
Write-Host "Starting Unified Metatron-A.G.I System..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the system" -ForegroundColor Yellow
Write-Host ""

python start_unified_system.py

Write-Host ""
Write-Host "Unified system stopped." -ForegroundColor Cyan