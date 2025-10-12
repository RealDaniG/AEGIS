@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  Metatron Consciousness Engine - Unified System Launcher
REM  ALL FEATURES INTEGRATED ON PORT 8003
REM ================================================================================

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo         METATRON'S CUBE UNIFIED CONSCIOUSNESS SYSTEM                       
echo         Sacred Geometry Engine + AI Chat + Document Upload                            
echo ========================================================================
echo.
echo  Lightning Initializing 13-Node Sacred Geometry Architecture...
echo  Brain Initializing AI Chat and Model Management...
echo  Globe Creating Unified Web Interface...
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check Python
echo [Step 1/3] Verifying Python environment...
python --version 2>nul
if errorlevel 1 (
    echo.
    echo Cross ERROR: Python not found in PATH!
    echo    Please install Python 3.8+ and add to PATH.
    echo.
    pause
    exit /b 1
)
echo Check Python environment OK

echo.
echo [Step 1.5/3] Checking Python dependencies...
python -c "import sys; import importlib.util; missing = []; packages = ['numpy', 'scipy', 'fastapi', 'uvicorn', 'transformers', 'torch', 'cryptography', 'websockets', 'stem', 'pysocks', 'aiohttp', 'aiohttp_socks', 'requests', 'pypdf', 'python_docx']; [missing.append(pkg) for pkg in packages if importlib.util.find_spec(pkg) is None]; sys.exit(1) if missing else sys.exit(0)" 2>nul
if errorlevel 1 (
    echo.
    echo Cross WARNING: Some Python packages may be missing!
    echo    Installing required packages...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Cross ERROR: Failed to install Metatron-ConscienceAI requirements!
        echo    Please manually run: pip install -r requirements.txt
        echo.
    )
    
    cd ..\Open-A.G.I
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Cross ERROR: Failed to install Open-A.G.I requirements!
        echo    Please manually run: pip install -r requirements.txt
        echo.
    )
    
    cd ..\aegis-conscience
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Cross ERROR: Failed to install aegis-conscience requirements!
        echo    Please manually run: pip install -r requirements.txt
        echo.
    )
    
    cd ..\Metatron-ConscienceAI
    
    echo.
    echo Checking for additional visualization tools dependencies...
    python -c "import importlib.util; missing = []; packages = ['websockets', 'requests']; [missing.append(pkg) for pkg in packages if importlib.util.find_spec(pkg) is None]; sys.exit(1) if missing else sys.exit(0)" 2>nul
    if errorlevel 1 (
        echo Installing visualization tools dependencies...
        pip install websockets requests
    )
)
echo Check Python dependencies OK

REM Start Unified Server
echo.
echo [Step 2/3] Launching Metatron Unified Server (Port 8003)...
echo             - 13-Node Metatron's Cube Network
echo             - Kuramoto Synchronization Dynamics
echo             - Real-time Consciousness Metrics (Phi, R, D, S, C)
echo             - 40Hz/80Hz Gamma Oscillations
echo             - AI Chat with Multiple Models
echo             - Document Upload and RAG
echo             - WebSocket Streaming Interface
echo.

start "Brain Metatron Unified (8003)" cmd /k "title Metatron Unified Server & color 0B & python scripts/metatron_web_server.py"

echo Hourglass Waiting for server to initialize...
timeout /t 10 /nobreak > nul

echo.
echo [Step 2.5/3] Verifying server is running...
curl -f http://localhost:8003/api/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo Warning: Server may still be initializing or failed to start.
    echo          If the web interface doesn't load, check the server window for errors.
    echo.
)

REM Open Browser
echo.
echo [Step 3/3] Opening unified web interface...
start "" "http://localhost:8003/"

echo Check Browser opened to unified interface
echo.
echo If the browser doesn't open automatically, manually navigate to:
echo    http://localhost:8003/
echo.

REM Status Check
echo.
echo ========================================================================
echo.
echo Check UNIFIED SYSTEM READY AND OPERATIONAL
echo.
echo ========================================================================
echo.
echo Globe WEB INTERFACE:
echo    Single Unified Interface:  http://localhost:8003/
echo    Diagnostic Page:    http://localhost:8003/static/diagnostic.html
echo.
echo Electric API ENDPOINTS (All on Port 8003):
echo    /api/status        - Consciousness metrics
echo    /api/chat          - AI chat
echo    /api/upload        - Document upload
echo    /api/config        - Model management
echo    /api/health        - System health
echo    /docs              - API documentation
echo.
echo Computer RUNNING SERVER:
echo    Metatron Unified Server (Port 8003)
echo      - Consciousness Engine
echo      - AI Chat System
echo      - Document Management
echo.
echo ========================================================================
echo.
echo Memo INSTRUCTIONS:
echo    - Server is running in separate window
echo    - Close server window OR press Ctrl+C to stop
echo    - DO NOT close this window to keep monitoring active
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
echo To stop the server, close the "Metatron Unified Server" command window
echo or press Ctrl+C in that window.
echo.
echo Press any key to close this launcher window (server will continue running)...
pause > nul