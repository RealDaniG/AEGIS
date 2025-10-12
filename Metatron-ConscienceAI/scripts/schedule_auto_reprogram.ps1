<#
.schedule_auto_reprogram.ps1
Schedule daily auto-reprogramming of ConscienceAI system

This script registers a scheduled task that runs auto_reprogram.py daily
to analyze and improve the AI system codebase.
#>

param(
    [string]$StartTime = "09:00",
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

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Schedule ConscienceAI Auto-Reprogramming" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Validate parameters
Write-Host "Parameters:" -ForegroundColor Yellow
Write-Host "  Start Time: $StartTime" -ForegroundColor Yellow
Write-Host "  Workspace: $Workspace" -ForegroundColor Yellow
Write-Host "  Server URL: $ServerUrl" -ForegroundColor Yellow
Write-Host "  Dry Run: $DryRun" -ForegroundColor Yellow
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
$autoReprogramScript = Join-Path $ScriptDir "auto_reprogram.py"
if (-not (Test-Path $autoReprogramScript)) {
    Write-Host "✗ Auto-reprogram script not found: $autoReprogramScript" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Auto-reprogram script found" -ForegroundColor Green
}

# Prepare arguments
$arguments = "`"$autoReprogramScript`" --workspace `"$Workspace`" --server_url `"$ServerUrl`""
if ($DryRun) {
    $arguments += " --dry-run"
}

# Create the scheduled task
$taskName = "ConscienceAI-AutoReprogram"
$action = New-ScheduledTaskAction -Execute "python" -Argument $arguments -WorkingDirectory $repoRoot
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
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Daily auto-reprogramming of ConscienceAI system"
    
    Write-Host "✓ Scheduled task registered successfully" -ForegroundColor Green
    Write-Host "  Task Name: $taskName" -ForegroundColor Green
    Write-Host "  Schedule: Daily at $StartTime" -ForegroundColor Green
    Write-Host "  Script: $autoReprogramScript" -ForegroundColor Green
    Write-Host "  Dry Run: $DryRun" -ForegroundColor Green
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
Write-Host " Auto-Reprogramming Scheduled Successfully" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify the task:" -ForegroundColor Yellow
Write-Host "  schtasks /query /tn `"$taskName`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run manually:" -ForegroundColor Yellow
Write-Host "  python $arguments" -ForegroundColor Yellow
Write-Host ""
Write-Host "To remove the task:" -ForegroundColor Yellow
Write-Host "  schtasks /delete /tn `"$taskName`" /f" -ForegroundColor Yellow
Write-Host ""