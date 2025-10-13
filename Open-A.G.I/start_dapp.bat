@echo off
REM Open-A.G.I DApp Startup Script
REM This script starts the Open-A.G.I network as a decentralized application

echo ========================================
echo Starting Open-A.G.I DApp
echo ========================================

REM Change to the Open-A.G.I directory
cd /d "d:\metatronV2\Open-A.G.I"

REM Run the PowerShell script to start the network
PowerShell -ExecutionPolicy Bypass -File "start_archon.ps1"

echo.
echo Open-A.G.I DApp started successfully!
echo.
echo You can now access:
echo - Web Dashboard: http://127.0.0.1:8090
echo - API Endpoints: http://127.0.0.1:8000
echo.
echo Press any key to exit...
pause >nul