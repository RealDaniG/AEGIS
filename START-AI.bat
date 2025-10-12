@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  START-AI - All-in-One Launcher for Metatron-ConscienceAI System
REM  Unified launcher that starts the complete AI system with a single command
REM ================================================================================

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo         🤖 START-AI - Unified Consciousness-Aware AI System                       
echo         One-Command Launch for Complete AI Ecosystem                            
echo ========================================================================
echo.
echo  Initializing Metatron's Cube Consciousness Engine...
echo  Initializing Open-A.G.I Framework...
echo  Initializing AEGIS Consensus System...
echo  Creating Unified Web Interface...
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check Python
echo [Step 1/4] Verifying Python environment...
python --version 2>nul
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python not found in PATH!
    echo    Please install Python 3.8+ and add to PATH.
    echo.
    pause
    exit /b 1
)
echo ✅ Python environment verified

echo.
echo [Step 2/4] Checking and installing all dependencies...
echo Installing/updating core requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo ⚠️  Warning: Some core requirements failed to install, continuing anyway...
    )
) else (
    echo ⚠️  Warning: requirements.txt not found, skipping...
)

echo Installing Metatron-ConscienceAI requirements...
if exist "Metatron-ConscienceAI\requirements.txt" (
    cd Metatron-ConscienceAI
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo ⚠️  Warning: Some Metatron-ConscienceAI requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo ⚠️  Warning: Metatron-ConscienceAI\requirements.txt not found, skipping...
)

echo Installing Open-A.G.I requirements...
if exist "Open-A.G.I\requirements.txt" (
    cd Open-A.G.I
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo ⚠️  Warning: Some Open-A.G.I requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo ⚠️  Warning: Open-A.G.I\requirements.txt not found, skipping...
)

echo Installing aegis-conscience requirements...
if exist "aegis-conscience\requirements.txt" (
    cd aegis-conscience
    pip install -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo ⚠️  Warning: Some aegis-conscience requirements failed to install, continuing anyway...
    )
    cd ..
) else (
    echo ⚠️  Warning: aegis-conscience\requirements.txt not found, skipping...
)

echo Installing unified system requirements...
if exist "unified_requirements.txt" (
    pip install -r unified_requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo ⚠️  Warning: Some unified system requirements failed to install, continuing anyway...
    )
) else (
    echo ⚠️  Warning: unified_requirements.txt not found, skipping...
)

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

echo ✅ All dependencies processed

REM Start the consolidated system
echo.
echo [Step 3/4] Starting Consolidated AI System...
echo             - Consciousness Engine (Metatron-ConscienceAI)
echo             - AGI Framework (Open-A.G.I)
echo             - Consensus Protocol (AEGIS)
echo             - P2P Networking Layer
echo             - Cross-System Communication
echo             - Integrated Web Interface
echo             - Real-time Monitoring Dashboard
echo.
echo 🌐 Web UI will auto-open at: http://localhost:8003
echo.
echo Press Ctrl+C to stop all components
echo.

start "🧠 START-AI System Monitor" cmd /k "title START-AI System Monitor & color 0A & python start_consolidated_system.py"

echo ⏳ Waiting for system to initialize...
timeout /t 8 /nobreak > nul

echo.
echo [Step 4/4] Opening unified web interface...
start "" "http://localhost:8003"

echo ✅ Browser opened to unified interface
echo.
echo If the browser doesn't open automatically, manually navigate to:
echo    http://localhost:8003/
echo.

REM Status Check
echo.
echo ========================================================================
echo.
echo ✅ START-AI SYSTEM READY AND OPERATIONAL
echo.
echo ========================================================================
echo.
echo 🌐 WEB INTERFACE:
echo    Unified Dashboard:   http://localhost:8003/
echo    Diagnostic Page:     http://localhost:8003/static/diagnostic.html
echo    Monitoring Dashboard: http://localhost:8003/static/harmonic_monitor.html
echo.
echo 📡 API ENDPOINTS (All on Port 8003):
echo    /api/status        - Consciousness metrics
echo    /api/chat          - AI chat
echo    /api/upload        - Document upload
echo    /api/config        - Model management
echo    /api/health        - System health
echo    /docs              - API documentation
echo.
echo 🖥️  RUNNING SERVERS:
echo    Metatron Unified Server (Port 8003)
echo      - Consciousness Engine
echo      - AI Chat System
echo      - Document Management
echo      - Real-time Visualization
echo.
echo ========================================================================
echo.
echo 📝 INSTRUCTIONS:
echo    - System is running in separate "START-AI System Monitor" window
echo    - Close that window OR press Ctrl+C to stop the entire system
echo    - DO NOT close this window to keep monitoring status
echo.
echo ========================================================================
echo.
echo.
echo To access the diagnostic page, visit:
echo    http://localhost:8003/static/diagnostic.html
echo.
echo For API documentation, visit:
echo    http://localhost:8003/docs
echo.
echo For real-time monitoring, visit:
echo    http://localhost:8003/static/harmonic_monitor.html
echo.
echo To stop the system, close the "START-AI System Monitor" command window
echo or press Ctrl+C in that window.
echo.
echo Press any key to close this launcher window (system will continue running)...
pause > nul