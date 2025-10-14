@echo off
title Metatron Web UI Visuals Test

echo ============================================================
echo Metatron Web UI Visuals Test
echo ============================================================

echo.
echo 1. Starting Metatron Web Server...
echo.

cd Metatron-ConscienceAI\scripts
start "Metatron Web Server" /MIN python metatron_web_server.py

echo.
echo 2. Waiting for server to start...
echo.

timeout /t 10 /nobreak >nul

echo.
echo 3. Opening Web UI in browser...
echo.

start http://localhost:8003

echo.
echo 4. Running functionality verification...
echo.

cd ..\..
python verify_visuals_functionality.py

echo.
echo ============================================================
echo Test Complete!
echo ============================================================
echo.
echo The Metatron Web UI should now be open in your browser.
echo Please verify the visual components according to the instructions.
echo.
echo Press any key to close this window...
pause >nul