#!/usr/bin/env pwsh
# quick_run.ps1
# Quick start script for AEGIS system on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AEGIS - Quick Start Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "run_everything.bat")) {
    Write-Host "❌ Error: run_everything.bat not found!" -ForegroundColor Red
    Write-Host "   Please run this script from the AEGIS root directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found AEGIS project files" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "🔍 Checking Python environment..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "   Please install Python 3.8 or higher" -ForegroundColor Yellow
    exit 1
}

# Run the main launcher
Write-Host ""
Write-Host "🚀 Starting AEGIS system..." -ForegroundColor Cyan
Write-Host "   This will launch the system and open the web interface" -ForegroundColor Yellow
Write-Host ""

# Run the batch file
Start-Process -FilePath ".\run_everything.bat" -NoNewWindow

Write-Host "✅ AEGIS system launch initiated!" -ForegroundColor Green
Write-Host "   Check the new command window for system status" -ForegroundColor Yellow
Write-Host "   Your web browser will open automatically with the visualization" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AEGIS System Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan