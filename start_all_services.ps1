# start_all_services.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  METATRONV2 UNIFIED SYSTEM LAUNCHER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "Metatron-ConscienceAI\START_SYSTEM.bat")) {
    Write-Host "❌ Error: Cannot find Metatron-ConscienceAI directory" -ForegroundColor Red
    Write-Host "Please run this script from the METATRONV2 root directory" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "Open-A.G.I\start_archon.ps1")) {
    Write-Host "❌ Error: Cannot find Open-A.G.I directory" -ForegroundColor Red
    Write-Host "Please run this script from the METATRONV2 root directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[1/3] Starting Metatron-ConsciousnessAI on port 8003..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/c", "cd Metatron-ConscienceAI && START_SYSTEM.bat" -WindowStyle Minimized
Write-Host "✅ Metatron-ConsciousnessAI started" -ForegroundColor Green

Write-Host "`nWaiting for Metatron to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "`n[2/3] Starting Open-A.G.I on port 8090..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-File", "Open-A.G.I\start_archon.ps1" -WindowStyle Minimized
Write-Host "✅ Open-A.G.I started" -ForegroundColor Green

Write-Host "`nWaiting for Open-A.G.I to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "`n[3/3] Starting Unified API System on port 8005..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "start_unified_system.py"
Write-Host "✅ Unified API System started" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  ALL SERVICES STARTED SUCCESSFULLY!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`n🔧 ACCESS THE UNIFIED SYSTEM:" -ForegroundColor Yellow
Write-Host "   Web Interface: http://localhost:8003/" -ForegroundColor White
Write-Host "   Unified API: http://localhost:8005/" -ForegroundColor White
Write-Host "   API Documentation: http://localhost:8005/docs" -ForegroundColor White
Write-Host "   WebSocket: ws://localhost:8005/ws" -ForegroundColor White

Write-Host "`n📊 SERVICE PORTS:" -ForegroundColor Yellow
Write-Host "   Metatron-ConsciousnessAI: 8003" -ForegroundColor White
Write-Host "   Open-A.G.I: 8090" -ForegroundColor White
Write-Host "   Unified API: 8005" -ForegroundColor White
Write-Host "   WebSocket Server: 8006" -ForegroundColor White

Write-Host "`n⚠️  IMPORTANT NOTES:" -ForegroundColor Yellow
Write-Host "   - Services are running in separate windows" -ForegroundColor White
Write-Host "   - Close individual service windows to stop them" -ForegroundColor White
Write-Host "   - Run 'python verify_services.py' to check service status" -ForegroundColor White

Write-Host "`n🚀 System is ready for Unified State Retrieval!" -ForegroundColor Green