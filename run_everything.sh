#!/bin/bash

# ================================================================================
#  AEGIS - Autonomous Governance and Intelligent Systems
#  Complete System Launcher - Starts ALL components with a single command
# ================================================================================

echo ""
echo "========================================================================"
echo "        AEGIS (Autonomous Governance and Intelligent Systems)"
echo "        Unified Consciousness-Aware Distributed AI System"
echo "========================================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check Python
echo "[Step 1/3] Verifying Python environment..."
if command -v python3 > /dev/null 2>&1; then
    python3 --version
elif command -v python > /dev/null 2>&1; then
    python --version
else
    echo ""
    echo "ERROR: Python not found in PATH!"
    echo "   Please install Python 3.8+ and add to PATH."
    echo ""
    exit 1
fi
echo "Check Python environment OK"

echo ""
echo "[Step 2/3] Checking and installing all dependencies..."
echo "Installing/updating core requirements..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --upgrade 2>/dev/null || echo "Warning: Some core requirements failed to install, continuing anyway..."
else
    echo "Warning: requirements.txt not found, skipping..."
fi

echo "Installing Metatron-ConscienceAI requirements..."
if [ -f "Metatron-ConscienceAI/requirements.txt" ]; then
    cd Metatron-ConscienceAI
    pip3 install -r requirements.txt --upgrade 2>/dev/null || echo "Warning: Some Metatron-ConscienceAI requirements failed to install, continuing anyway..."
    cd ..
else
    echo "Warning: Metatron-ConscienceAI/requirements.txt not found, skipping..."
fi

echo "Installing Open-A.G.I requirements..."
if [ -f "Open-A.G.I/requirements.txt" ]; then
    cd Open-A.G.I
    pip3 install -r requirements.txt --upgrade 2>/dev/null || echo "Warning: Some Open-A.G.I requirements failed to install, continuing anyway..."
    cd ..
else
    echo "Warning: Open-A.G.I/requirements.txt not found, skipping..."
fi

echo "Installing aegis-conscience requirements..."
if [ -f "aegis-conscience/requirements.txt" ]; then
    cd aegis-conscience
    pip3 install -r requirements.txt --upgrade 2>/dev/null || echo "Warning: Some aegis-conscience requirements failed to install, continuing anyway..."
    cd ..
else
    echo "Warning: aegis-conscience/requirements.txt not found, skipping..."
fi

echo "Installing unified system requirements..."
if [ -f "unified_requirements.txt" ]; then
    pip3 install -r unified_requirements.txt --upgrade 2>/dev/null || echo "Warning: Some unified system requirements failed to install, continuing anyway..."
else
    echo "Warning: unified_requirements.txt not found, skipping..."
fi

echo "Check All dependencies processed"

# Try to install some critical missing packages individually
echo ""
echo "Installing critical packages that might have failed..."
pip3 install torch transformers datasets peft safetensors 2>/dev/null
pip3 install fastapi uvicorn[standard] websockets 2>/dev/null
pip3 install cryptography pycryptodome pyotp fernet 2>/dev/null
pip3 install aiohttp aiohttp-socks stem asyncio-mqtt 2>/dev/null
pip3 install scikit-learn aiosqlite redis 2>/dev/null
pip3 install loguru prometheus-client psutil pandas 2>/dev/null
pip3 install flask zeroconf Flask-SocketIO netifaces 2>/dev/null
pip3 install pydantic click rich python-dotenv 2>/dev/null
pip3 install pypdf python-docx feedparser beautifulsoup4 lxml 2>/dev/null
pip3 install pytest-asyncio pytest-cov black flake8 mypy 2>/dev/null
pip3 install plotly python-socketio 2>/dev/null
pip3 install python-multipart 2>/dev/null

echo ""
echo "Dependency installation phase complete."

# Start consolidated system
echo ""
echo "[Step 3/3] Starting Consolidated AEGIS System (1 Terminal)..."
echo "            - Consciousness Engine (Metatron-ConscienceAI)"
echo "            - AGI Framework (Open-A.G.I)"
echo "            - Consensus Protocol"
echo "            - P2P Networking Layer"
echo "            - Cross-System Communication"
echo "            - Integrated Web Interface"
echo ""
echo "🌐 Web UI will auto-open at: http://localhost:8003"
echo ""
echo "Press Ctrl+C to stop all components"
echo ""

python3 start_consolidated_system.py

echo ""
echo "========================================================================"
echo ""
echo "AEGIS SYSTEM STOPPED"
echo ""
echo "========================================================================"
echo ""
echo "To restart the system, run this launcher again."
echo ""
echo "For comprehensive documentation, visit:"
echo "   https://github.com/RealDaniG/AEGIS/wiki"
echo ""

