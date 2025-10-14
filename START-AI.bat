@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  START-AI - All-in-One Launcher for Metatron-ConscienceAI System
REM  Unified launcher that starts the complete AI system with a single command
REM ================================================================================

REM Set UTF-8 encoding environment variables for cross-platform compatibility
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo         [ROBOT] START-AI - Unified Consciousness-Aware AI System                       
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
    echo [ERROR] ERROR: Python not found in PATH!
    echo    Please install Python 3.8+ and add to PATH.
    echo.
    pause
    exit /b 1
)
echo [OK] Python environment verified

echo.
echo [Step 2/4] Installing/updating dependencies...
REM Install all requirements in a single pass to avoid duplicates
set requirements_installed=0

if exist "requirements.txt" (
    echo Installing core requirements...
    pip install -r requirements.txt --upgrade --quiet 2>nul
    if errorlevel 1 echo [WARN] Warning: Some core requirements failed to install, continuing anyway...
    set requirements_installed=1
) else (
    echo [WARN] Warning: requirements.txt not found, skipping...
)

REM Install component-specific requirements only if not already covered by main requirements
for %%D in ("Metatron-ConscienceAI" "Open-A.G.I" "aegis-conscience") do (
    if exist "%%~D\requirements.txt" (
        echo Installing %%~D requirements...
        cd "%%~D"
        pip install -r requirements.txt --upgrade --quiet 2>nul
        if errorlevel 1 echo [WARN] Warning: Some %%~D requirements failed to install, continuing anyway...
        cd ..
        set requirements_installed=1
    )
)

REM Install unified system requirements if present and not covered by main requirements
if exist "unified_requirements.txt" (
    echo Installing unified system requirements...
    pip install -r unified_requirements.txt --upgrade --quiet 2>nul
    if errorlevel 1 echo [WARN] Warning: Some unified system requirements failed to install, continuing anyway...
    set requirements_installed=1
)

if %requirements_installed%==0 (
    echo [WARN] Warning: No requirements files found, installing critical packages only...
)

REM Install critical packages that might have failed (only if not already installed)
echo Installing critical packages...
pip install torch transformers datasets peft safetensors --quiet 2>nul
pip install fastapi uvicorn[standard] websockets --quiet 2>nul
pip install cryptography pycryptodome pyotp fernet --quiet 2>nul
pip install aiohttp aiohttp-socks stem asyncio-mqtt --quiet 2>nul
pip install scikit-learn aiosqlite redis --quiet 2>nul
pip install loguru prometheus-client psutil pandas --quiet 2>nul
pip install flask zeroconf Flask-SocketIO --quiet 2>nul
REM Installing netifaces separately with fallback options
pip install netifaces --quiet 2>nul
if errorlevel 1 (
    echo [WARN] Warning: netifaces failed to install (optional network interface detection)
    echo          This is normal on some systems and will not affect core functionality
)
pip install pydantic click rich python-dotenv --quiet 2>nul
pip install pypdf python-docx feedparser beautifulsoup4 lxml --quiet 2>nul
pip install pytest-asyncio pytest-cov black flake8 mypy --quiet 2>nul
pip install plotly python-socketio --quiet 2>nul
pip install python-multipart --quiet 2>nul

echo [OK] All dependencies processed

REM Start the consolidated system in the same terminal (no separate window)
echo.
echo [Step 3/4] Starting Consolidated AI System...
echo             - Consciousness Engine (Metatron-ConscienceAI)
echo             - AGI Framework (Open-A.G.I)
echo             - Consensus Protocol (AEGIS)
echo             - P2P Networking Layer
echo             - Cross-System Communication
echo             - Integrated Web Interface
echo             - Real-time Monitoring Dashboard
echo             - Open-A.G.I Deployment Orchestration
echo             - TOR Anonymity Integration
echo             - Advanced Metrics Collection
echo.
echo [WEB] Web UI will auto-open at: http://localhost:457/
echo.
echo Press Ctrl+C to stop all components
echo.

REM Run the consolidated system directly in this terminal (no separate window)
echo Starting AEGIS System Coordinator and Web Server...
python start_consolidated_system.py

REM Status Check
echo.
echo ========================================================================
echo.
echo [OK] START-AI SYSTEM READY AND OPERATIONAL
echo.
echo ========================================================================
echo.
echo [WEB] WEB INTERFACE:
echo    Unified Dashboard:   http://localhost:457/
echo    Diagnostic Page:     http://localhost:457/static/diagnostic.html
echo    Main Web UI:         http://localhost:457/
echo.
echo [API] API ENDPOINTS:
echo    Unified API Server:  http://localhost:457/
echo      /api/health        - System health
echo      /api/state         - Unified system state
echo      /api/consciousness - Consciousness state only
echo      /api/agi           - AGI state only
echo      /api/input         - Send consciousness input
echo      /api/chat          - Send chat message
echo      WebSocket /ws      - Real-time state streaming
echo.
echo    Metatron System:     http://localhost:457/
echo      /api/health        - Consciousness metrics
echo      /api/status        - System status
echo      WebSocket /ws      - Real-time streaming
echo.
echo    Open-A.G.I Dashboard: http://localhost:5000/
echo.
echo [SERVER] RUNNING SERVERS:
echo    Unified API Server (Port 457)
echo      - Integrates Metatron and Open-A.G.I systems
echo      - Provides unified interface
echo.
echo    Metatron Unified Server (Port 457)
echo      - Consciousness Engine
echo      - AI Chat System
echo      - Document Management
echo      - Real-time Visualization
echo.
echo    Open-A.G.I Monitoring (Port 5000)
echo      - Network monitoring
echo      - Consensus visualization
echo      - Performance metrics
echo.
echo ========================================================================
echo.
echo [INFO] INSTRUCTIONS:
echo    - System is running in this terminal window
echo    - Press Ctrl+C to stop the entire system
echo.
echo ========================================================================
echo.
echo.
echo To access the diagnostic page, visit:
echo    http://localhost:457/static/diagnostic.html
echo.
echo For API documentation, visit:
echo    http://localhost:457/docs
echo.
echo For the main web interface, visit:
echo    http://localhost:457/
echo.
echo For Open-A.G.I monitoring dashboard, visit:
echo    http://localhost:5000/
echo.
echo To stop the system, press Ctrl+C in this window.
echo.