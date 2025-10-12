@echo off
chcp 65001 >nul 2>&1
REM ================================================================================
REM  AEGIS - Autonomous Governance and Intelligent Systems
REM  Complete System Launcher - Starts ALL components with a single command
REM  NOTE: For simplified launch, use START-AI.bat in the root directory
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
echo [Step 1/3] Verifying Python environment...
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
echo [Step 2/3] Checking and installing all dependencies...
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

REM Inform user about the new simplified launcher
echo.
echo NOTE: A new simplified launcher is now available!
echo       For easier system startup, you can now use:
echo.
echo       START-AI.bat - Single command to launch the complete system
echo.
echo       This will start all components with automatic dependency management
echo       and open the web interface automatically.
echo.

REM Start consolidated system
echo.
echo [Step 3/3] Starting Consolidated AEGIS System (1 Terminal)...
echo             - Consciousness Engine (Metatron-ConscienceAI)
echo             - AGI Framework (Open-A.G.I)
echo             - Consensus Protocol
echo             - P2P Networking Layer
echo             - Cross-System Communication
echo             - Integrated Web Interface
echo.
echo 🌐 Web UI will auto-open at: http://localhost:8003
echo.
echo Press Ctrl+C to stop all components
echo.

python start_consolidated_system.py

echo.
echo ========================================================================
echo.
echo AEGIS SYSTEM STOPPED
echo.
echo ========================================================================
echo.
echo To restart the system, run this launcher again.
echo.
echo For simplified startup, try the new START-AI.bat launcher!
echo.
echo For comprehensive documentation, visit:
echo    https://github.com/RealDaniG/AEGIS/wiki
echo.