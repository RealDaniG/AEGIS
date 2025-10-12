<#
.run_auto_reprogram_scheduled.ps1
Run scheduled auto-reprogramming of ConscienceAI system

This script is called by the scheduled task to perform daily reprogramming.
#>

param(
    [string]$Workspace = ".",
    [string]$ServerUrl = "http://localhost:5180",
    [switch]$DryRun = $true
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
Write-Host " ConscienceAI Scheduled Auto-Reprogramming" -ForegroundColor Cyan
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

# Check if auto_reprogram.py exists
$autoReprogramScript = Join-Path $ScriptDir "scripts\auto_reprogram.py"
if (-not (Test-Path $autoReprogramScript)) {
    Write-Host "✗ Auto-reprogram script not found: $autoReprogramScript" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Auto-reprogram script found" -ForegroundColor Green
}

# Prepare arguments
$arguments = @($autoReprogramScript, "--workspace", $Workspace, "--server_url", $ServerUrl)
if ($DryRun) {
    $arguments += "--dry-run"
}

# Run auto-reprogramming
Write-Host "Starting auto-reprogramming..." -ForegroundColor Yellow
Write-Host "Workspace: $Workspace" -ForegroundColor Yellow
Write-Host "Server URL: $ServerUrl" -ForegroundColor Yellow
Write-Host "Dry Run: $DryRun" -ForegroundColor Yellow
Write-Host ""

try {
    $startTime = Get-Date
    & python $arguments
    $endTime = Get-Date
    
    $duration = ($endTime - $startTime).TotalSeconds
    Write-Host "Auto-reprogramming completed in $([math]::Round($duration, 2)) seconds" -ForegroundColor Green
    
} catch {
    Write-Host "✗ Auto-reprogramming failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Scheduled Auto-Reprogramming Completed" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Report saved to: ai_runs/auto_reprogram_report.json" -ForegroundColor Green
Write-Host ""