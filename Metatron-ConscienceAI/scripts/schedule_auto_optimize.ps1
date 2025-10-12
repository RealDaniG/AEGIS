<#
.schedule_auto_optimize.ps1
Schedule daily auto-optimization of ConscienceAI chat parameters

This script registers a scheduled task that runs auto_optimize.py daily
to optimize chat parameters for better performance.
#>

param(
    [string]$StartTime = "08:00",
    [string]$Workspace = ".",
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

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Schedule ConscienceAI Auto-Optimization" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Validate parameters
Write-Host "Parameters:" -ForegroundColor Yellow
Write-Host "  Start Time: $StartTime" -ForegroundColor Yellow
Write-Host "  Workspace: $Workspace" -ForegroundColor Yellow
Write-Host "  Server URL: $ServerUrl" -ForegroundColor Yellow
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
$autoOptimizeScript = Join-Path $ScriptDir "auto_optimize.py"
if (-not (Test-Path $autoOptimizeScript)) {
    Write-Host "✗ Auto-optimize script not found: $autoOptimizeScript" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Auto-optimize script found" -ForegroundColor Green
}

# Create the scheduled task
$taskName = "ConscienceAI-AutoOptimize"
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$autoOptimizeScript`" --server_url `"$ServerUrl`"" -WorkingDirectory $repoRoot
$trigger = New-ScheduledTaskTrigger -Daily -At $StartTime
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId (Get-CimInstance Win32_ComputerSystem | Select-Object -ExpandProperty UserName) -LogonType Interactive

try {
    # Check if task already exists
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "⚠ Task already exists. Updating..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
    
    # Register the new task
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Daily auto-optimization of ConscienceAI chat parameters"
    
    Write-Host "✓ Scheduled task registered successfully" -ForegroundColor Green
    Write-Host "  Task Name: $taskName" -ForegroundColor Green
    Write-Host "  Schedule: Daily at $StartTime" -ForegroundColor Green
    Write-Host "  Script: $autoOptimizeScript" -ForegroundColor Green
    Write-Host ""
    
    # Show task details
    $task = Get-ScheduledTask -TaskName $taskName
    $taskInfo = $task | Get-ScheduledTaskInfo
    Write-Host "Task Status:" -ForegroundColor Yellow
    Write-Host "  State: $($task.State)" -ForegroundColor Yellow
    Write-Host "  Last Run: $($taskInfo.LastRunTime)" -ForegroundColor Yellow
    Write-Host "  Next Run: $($taskInfo.NextRunTime)" -ForegroundColor Yellow
    
} catch {
    Write-Host "✗ Failed to register scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Auto-Optimization Scheduled Successfully" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify the task:" -ForegroundColor Yellow
Write-Host "  schtasks /query /tn `"$taskName`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run manually:" -ForegroundColor Yellow
Write-Host "  python `"$autoOptimizeScript`" --server_url `"$ServerUrl`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "To remove the task:" -ForegroundColor Yellow
Write-Host "  schtasks /delete /tn `"$taskName`" /f" -ForegroundColor Yellow
Write-Host ""