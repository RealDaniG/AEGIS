# PowerShell script to start the complete Harmonic Orchestrator Monitoring System
# This script launches all required services in the correct order

Write-Host "=== Harmonic Orchestrator Monitoring System Startup ===" -ForegroundColor Cyan
Write-Host "Starting all required services..." -ForegroundColor Yellow

# Start the Unified API Server (port 8005)
Write-Host "1. Starting Unified API Server on port 8005..." -ForegroundColor Green
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "unified_api/server.py" -WorkingDirectory "d:\metatronV2\unified_api"

# Wait a moment for the API server to start
Start-Sleep -Seconds 3

# Start the Metatron Consciousness Engine Web Server (port 8003)
Write-Host "2. Starting Metatron Consciousness Engine Web Server on port 8003..." -ForegroundColor Green
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "scripts/metatron_web_server.py" -WorkingDirectory "d:\metatronV2\Metatron-ConscienceAI"

# Wait a moment for the web server to start
Start-Sleep -Seconds 3

# Start the Open-A.G.I System (port 8080)
Write-Host "3. Starting Open-A.G.I System on port 8080..." -ForegroundColor Green
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "main.py start-node" -WorkingDirectory "d:\metatronV2\Open-A.G.I"

Write-Host "=== All services started successfully ===" -ForegroundColor Cyan
Write-Host "Access the Harmonic Monitor at: http://localhost:8003" -ForegroundColor Yellow
Write-Host "Unified API available at: http://localhost:8005" -ForegroundColor Yellow
Write-Host "Open-A.G.I Dashboard available at: http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")