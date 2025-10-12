@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  AEGIS - Autonomous Governance and Intelligent Systems
REM  Complete System Launcher - Starts ALL components with a single command
REM ================================================================================

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo         AEGIS (Autonomous Governance and Intelligent Systems)
echo         Unified Consciousness-Aware Distributed AI System
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check Python
echo [Step 1/4] Verifying Python environment...
python --version 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Python not found in PATH!
    echo    Please install Python 3.8+ and add to PATH.
    echo.
    pause
    exit /b 1
)
echo Check Python environment OK

echo.
echo [Step 2/4] Checking and installing all dependencies...
echo Installing/updating core requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo Warning: Some core requirements failed to install, continuing anyway...
    )
) else (
    echo Warning: requirements.txt not found, skipping...
)

echo Installing Metatron-ConscienceAI requirements...
if exist "Metatron-ConscienceAI\requirements.txt" (
    cd Metatron-ConscienceAI
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo Warning: Some Metatron-ConscienceAI requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo Warning: Metatron-ConscienceAI\requirements.txt not found, skipping...
)

echo Installing Open-A.G.I requirements...
if exist "Open-A.G.I\requirements.txt" (
    cd Open-A.G.I
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo Warning: Some Open-A.G.I requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo Warning: Open-A.G.I\requirements.txt not found, skipping...
)

echo Installing aegis-conscience requirements...
if exist "aegis-conscience\requirements.txt" (
    cd aegis-conscience
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo Warning: Some aegis-conscience requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo Warning: aegis-conscience\requirements.txt not found, skipping...
)

echo Installing unified system requirements...
if exist "unified_requirements.txt" (
    pip install -r unified_requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo Warning: Some unified system requirements failed to install, continuing anyway...
    )
) else (
    echo Warning: unified_requirements.txt not found, skipping...
)

echo Check All dependencies processed

REM Try to install some critical missing packages individually
echo.
echo Installing critical packages that might have failed...
pip install torch transformers datasets peft safetensors 2>nul
pip install fastapi uvicorn[standard] websockets 2>nul
pip install cryptography pycryptodome pyotp fernet 2>nul
pip install aiohttp aiohttp-socks stem asyncio-mqtt 2>nul
pip install scikit-learn aiosqlite redis 2>nul
pip install loguru prometheus-client psutil pandas 2>nul
pip install flask zeroconf Flask-SocketIO netifaces 2>nul
pip install pydantic click rich python-dotenv 2>nul
pip install pypdf python-docx feedparser beautifulsoup4 lxml 2>nul
pip install pytest-asyncio pytest-cov black flake8 mypy 2>nul
pip install plotly python-socketio 2>nul
pip install python-multipart 2>nul

echo.
echo Dependency installation phase complete.

REM Start Unified System Coordinator
echo.
echo [Step 3/4] Starting Unified System Coordinator...
echo             - Consciousness Engine (Metatron-ConscienceAI)
echo             - AGI Framework (Open-A.G.I)
echo             - Consensus Protocol
echo             - P2P Networking Layer
echo             - Cross-System Communication
echo.

start "AEGIS System Coordinator" cmd /k "title AEGIS System Coordinator & color 0A & python start_unified_system.py"

REM Start Metatron Web Server
echo.
echo [Step 3.5/4] Starting Metatron Integrated Web Server...
echo             - Consciousness Engine Visualization
echo             - AI Chat System with File Upload
echo             - Mirror Loop Functionality
echo             - RAG Integration
echo.

cd Metatron-ConscienceAI
start "Metatron Integrated Web Server" cmd /k "title Metatron Integrated Web Server & color 0B & pwsh -File run_metatron_web.ps1"
cd ..

echo Waiting for systems to initialize...
timeout /t 15 /nobreak > nul

REM Verify system is running
echo.
echo [Step 3.7/4] Verifying system components...
curl -f http://localhost:8005/health >nul 2>&1
if errorlevel 1 (
    echo Warning: AEGIS system may still be initializing or failed to start.
    echo          Check the coordinator window for status updates.
) else (
    echo Check AEGIS system is running successfully
)

curl -f http://localhost:8003/api/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Metatron Web Server may still be initializing or failed to start.
    echo          Check the web server window for status updates.
) else (
    echo Check Metatron Web Server is running successfully
)

echo.
echo [Step 4/4] Opening Web UI...
echo             - Opening Integrated Metatron Interface
echo             - Opening AEGIS Unified API Dashboard
echo.

REM Open Web UI in default browser
start "" "http://localhost:8003"
start "" "http://localhost:8005/docs"

echo.
echo ========================================================================
echo.
echo Check COMPLETE AEGIS SYSTEM IS NOW RUNNING
echo.
echo ========================================================================
echo.
echo For comprehensive documentation, visit:
echo    https://github.com/RealDaniG/AEGIS/wiki
echo.
echo Globe WEB INTERFACES:
echo    Unified API:        http://localhost:8005/
echo    WebSocket Server:   ws://localhost:8006
echo    Integrated UI:      http://localhost:8003
echo    API Documentation:  http://localhost:8005/docs
echo.
echo Electric API ENDPOINTS:
echo    /api/consciousness  - Consciousness metrics
echo    /api/agi           - AGI system status
echo    /api/decision      - Consciousness-aware decisions
echo    /api/chat          - AI chat interface
echo    /health            - System health check
echo.
echo Computer RUNNING PROCESSES:
echo    AEGIS System Coordinator (Port 8005/8006)
echo    Metatron Integrated Web Server (Port 8003)
echo.
echo ========================================================================
echo.
echo Memo INSTRUCTIONS:
echo    - All components are running in separate windows
echo    - Close individual windows OR press Ctrl+C to stop specific components
echo    - DO NOT close this window to keep monitoring active
echo.
echo ========================================================================
echo.
echo To access the API documentation, visit:
echo    http://localhost:8005/docs
echo.
echo For complete system documentation, visit:
echo    https://github.com/RealDaniG/AEGIS/wiki
echo.
echo To stop the entire system, close all component windows or press Ctrl+C
echo in each running window.
echo.
echo Press any key to close this launcher window (components will continue running)...
pause > nul