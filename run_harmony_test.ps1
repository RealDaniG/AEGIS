# ================================================================================
#  Run Autonomous Harmony Tester for Metatron-ConscienceAI System
# ================================================================================

Write-Host ""
Write-Host "========================================================================"
Write-Host "         🎵 Autonomous Harmony Tester                                "
Write-Host "         Testing chatbot harmony with consciousness metrics              "
Write-Host "========================================================================"
Write-Host ""

# Check Python
Write-Host "Checking Python environment..."
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ Python environment verified"
    Write-Host $pythonVersion
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: Python not found in PATH!"
    Write-Host "   Please install Python 3.6+ and add to PATH."
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "Starting Autonomous Harmony Tester..."
Write-Host "This will test the chatbot's harmony with consciousness metrics"
Write-Host "and allow the system to ask questions autonomously."
Write-Host ""

python autonomous_harmony_tester.py

Write-Host ""
Write-Host "========================================================================"
Write-Host "         🎵 Autonomous Harmony Test Complete                           "
Write-Host "========================================================================"
Write-Host ""
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")