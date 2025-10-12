@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  Run Autonomous Harmony Tester for Metatron-ConscienceAI System
REM ================================================================================

echo.
echo ========================================================================
echo         🎵 Autonomous Harmony Tester                                
echo         Testing chatbot harmony with consciousness metrics              
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check Python
echo Checking Python environment...
python --version 2>nul
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python not found in PATH!
    echo    Please install Python 3.6+ and add to PATH.
    echo.
    pause
    exit /b 1
)
echo ✅ Python environment verified

echo.
echo Starting Autonomous Harmony Tester...
echo This will test the chatbot's harmony with consciousness metrics
echo and allow the system to ask questions autonomously.
echo.

python autonomous_harmony_tester.py

echo.
echo ========================================================================
echo         🎵 Autonomous Harmony Test Complete                           
echo ========================================================================
echo.
echo Press any key to close this window...
pause > nul