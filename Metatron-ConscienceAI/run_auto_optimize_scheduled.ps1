<#
.run_auto_optimize_scheduled.ps1
Run scheduled auto-optimization of ConscienceAI chat parameters

This script is called by the scheduled task to perform daily optimization.
#>

param(
    [string]$ServerUrl = "http://localhost:5180"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Detect script directory robustly
if ($PSCommandPath) {
    $ScriptDir = Split-Path -Parent $PSCommandPath
} elseif ($MyInvocation.MyCommand.Path) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
} else {
    $ScriptDir = Get-Location
}

$repoRoot = Split-Path -Parent $ScriptDir
Set-Location $repoRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " ConscienceAI Scheduled Auto-Optimization" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8 or higher" -ForegroundColor Yellow
    exit 1
}

# Check if auto_optimize.py exists
$autoOptimizeScript = Join-Path $ScriptDir "scripts\auto_optimize.py"
if (-not (Test-Path $autoOptimizeScript)) {
    Write-Host "✗ Auto-optimize script not found: $autoOptimizeScript" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Auto-optimize script found" -ForegroundColor Green
}

# Run auto-optimization
Write-Host "Starting auto-optimization..." -ForegroundColor Yellow
Write-Host "Server URL: $ServerUrl" -ForegroundColor Yellow
Write-Host ""

try {
    $startTime = Get-Date
    & python $autoOptimizeScript --server_url $ServerUrl --iterations 5 --output "ai_runs/webchat_settings.json"
    $endTime = Get-Date
    
    $duration = ($endTime - $startTime).TotalSeconds
    Write-Host "Auto-optimization completed in $([math]::Round($duration, 2)) seconds" -ForegroundColor Green
    
} catch {
    Write-Host "✗ Auto-optimization failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Scheduled Auto-Optimization Completed" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Settings saved to: ai_runs/webchat_settings.json" -ForegroundColor Green
Write-Host ""