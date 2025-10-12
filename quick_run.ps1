# Quick Run Script for Metatron V2 + Open A.G.I.
# This script starts the complete system with all components

Write-Host "=== Metatron V2 + Open A.G.I. Quick Run Script ===" -ForegroundColor Green
Write-Host "Starting the consciousness-aware distributed AI system..." -ForegroundColor Yellow

# Check if we're in the right directory
if (-not (Test-Path "Metatron-ConscienceAI")) {
    Write-Host "Error: Metatron-ConscienceAI directory not found!" -ForegroundColor Red
    Write-Host "Please run this script from the root of the MetatronV2 repository." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "Open-A.G.I")) {
    Write-Host "Error: Open-A.G.I directory not found!" -ForegroundColor Red
    Write-Host "Please run this script from the root of the MetatronV2 repository." -ForegroundColor Red
    exit 1
}

# Install dependencies if not already installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
} else {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    .\venv\Scripts\Activate.ps1
}

# Start the Metatron Consciousness Engine
Write-Host "Starting Metatron Consciousness Engine..." -ForegroundColor Cyan
Start-Process -FilePath "Metatron-ConscienceAI\START_SYSTEM.bat" -WorkingDirectory "Metatron-ConscienceAI"

# Wait a few seconds for the consciousness engine to start
Write-Host "Waiting for consciousness engine to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Start the Open A.G.I. Framework
Write-Host "Starting Open A.G.I. Framework..." -ForegroundColor Cyan
Set-Location Open-A.G.I
Start-Process -FilePath "powershell.exe" -ArgumentList "-Command", "python main.py" -WorkingDirectory "."
Set-Location ..

# Start visualization tools
Write-Host "Starting Visualization Tools..." -ForegroundColor Cyan
Start-Process -FilePath "powershell.exe" -ArgumentList "-Command", "python visualization_tools/robust_realtime_visualizer.py" -WorkingDirectory "."

# Start consensus monitoring
Write-Host "Starting Consensus Monitoring..." -ForegroundColor Cyan
Start-Process -FilePath "powershell.exe" -ArgumentList "-Command", "python consensus_tools/improved_pbft_consensus.py --monitor" -WorkingDirectory "."

Write-Host "=== System Startup Complete ===" -ForegroundColor Green
Write-Host "The Metatron V2 + Open A.G.I. system is now running." -ForegroundColor Green
Write-Host "Access the web interface at http://localhost:8003" -ForegroundColor Green
Write-Host "Visualization dashboard is available through the visualization tools." -ForegroundColor Green