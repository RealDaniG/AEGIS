#!/bin/bash

# ================================================================================
#  Metatron V2 + Open A.G.I. - Complete System Launcher
#  Starts ALL components with a single command
# ================================================================================

echo ""
echo "========================================================================"
echo "         METATRON V2 + OPEN A.G.I. COMPLETE SYSTEM LAUNCHER"
echo "         Unified Consciousness-Aware Distributed AI System"
echo "========================================================================"
echo ""

# Check Python
echo "[Step 1/4] Verifying Python environment..."
if ! command -v python3 &> /dev/null
then
    echo ""
    echo "ERROR: Python not found!"
    echo "   Please install Python 3.8+"
    echo ""
    exit 1
fi
echo "Check Python environment OK"

echo ""
echo "[Step 2/4] Checking and installing all dependencies..."
echo "Installing/updating core requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Warning: Some core requirements failed to install, continuing anyway..."
    fi
else
    echo "Warning: requirements.txt not found, skipping..."
fi

echo "Installing Metatron-ConscienceAI requirements..."
if [ -f "Metatron-ConscienceAI/requirements.txt" ]; then
    cd Metatron-ConscienceAI
    pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Warning: Some Metatron-ConscienceAI requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "Warning: Metatron-ConscienceAI/requirements.txt not found, skipping..."
fi

echo "Installing Open-A.G.I requirements..."
if [ -f "Open-A.G.I/requirements.txt" ]; then
    cd Open-A.G.I
    pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Warning: Some Open-A.G.I requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "Warning: Open-A.G.I/requirements.txt not found, skipping..."
fi

echo "Installing aegis-conscience requirements..."
if [ -f "aegis-conscience/requirements.txt" ]; then
    cd aegis-conscience
    pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Warning: Some aegis-conscience requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "Warning: aegis-conscience/requirements.txt not found, skipping..."
fi

echo "Installing unified system requirements..."
if [ -f "unified_requirements.txt" ]; then
    pip install -r unified_requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Warning: Some unified system requirements failed to install, continuing anyway..."
    fi
else
    echo "Warning: unified_requirements.txt not found, skipping..."
fi

echo ""
echo "Installing critical packages that might have failed..."
pip install torch transformers datasets peft safetensors 2>/dev/null
pip install fastapi uvicorn[standard] websockets 2>/dev/null
pip install cryptography pycryptodome pyotp fernet 2>/dev/null
pip install aiohttp aiohttp-socks stem asyncio-mqtt 2>/dev/null
pip install scikit-learn aiosqlite redis 2>/dev/null
pip install loguru prometheus-client psutil pandas 2>/dev/null
pip install flask zeroconf Flask-SocketIO netifaces 2>/dev/null
pip install pydantic click rich python-dotenv 2>/dev/null
pip install pypdf python-docx feedparser beautifulsoup4 lxml 2>/dev/null
pip install pytest-asyncio pytest-cov black flake8 mypy 2>/dev/null
pip install plotly python-socketio 2>/dev/null

echo ""
echo "Dependency installation phase complete."

# Start Unified System Coordinator
echo ""
echo "[Step 3/4] Starting Unified System Coordinator..."
echo "            - Consciousness Engine"
echo "            - AGI Framework"
echo "            - Security System"
echo "            - Cross-System Communication"
echo ""

# Start the unified system in background
python3 start_unified_system.py &
UNIFIED_PID=$!

echo "Waiting for unified system to initialize..."
sleep 15

# Verify system is running
echo ""
echo "[Step 3.5/4] Verifying system components..."
if curl -f http://localhost:8005/health >/dev/null 2>&1; then
    echo "Check Unified system is running successfully"
else
    echo "Warning: Unified system may still be initializing or failed to start."
    echo "         Check the coordinator process for status updates."
fi

# Start Visualization Tools
echo ""
echo "[Step 4/4] Starting Visualization and Monitoring Tools..."
echo "            - Real-time Consciousness Monitor"
echo "            - Node Status Dashboard"
echo "            - System Performance Metrics"
echo ""

if [ -d "visualization_tools" ]; then
    cd visualization_tools
    python3 robust_realtime_visualizer.py &
    VISUALIZATION_PID=$!
    cd ..
else
    echo "Warning: visualization_tools directory not found, skipping visualization..."
fi

echo ""
echo "========================================================================"
echo ""
echo "Check COMPLETE SYSTEM IS NOW RUNNING"
echo ""
echo "========================================================================"
echo ""
echo "Globe WEB INTERFACES:"
echo "   Unified API:        http://localhost:8005/"
echo "   WebSocket Server:   ws://localhost:8006"
echo "   Visualization:      Check visualization process"
echo ""
echo "Electric API ENDPOINTS:"
echo "   /api/consciousness  - Consciousness metrics"
echo "   /api/agi           - AGI system status"
echo "   /api/decision      - Consciousness-aware decisions"
echo "   /api/chat          - AI chat interface"
echo "   /health            - System health check"
echo ""
echo "Computer RUNNING PROCESSES:"
echo "   Unified System Coordinator (PID: $UNIFIED_PID)"
if [ ! -z "$VISUALIZATION_PID" ]; then
    echo "   Visualization Monitor (PID: $VISUALIZATION_PID)"
fi
echo ""
echo "========================================================================"
echo ""
echo "Memo INSTRUCTIONS:"
echo "   - All components are running in background"
echo "   - Use 'kill $UNIFIED_PID' to stop unified system"
if [ ! -z "$VISUALIZATION_PID" ]; then
    echo "   - Use 'kill $VISUALIZATION_PID' to stop visualization"
fi
echo ""
echo "========================================================================"
echo ""
echo "To access the API documentation, visit:"
echo "   http://localhost:8005/docs"
echo ""
echo "To stop the entire system, run:"
echo "   kill $UNIFIED_PID"
if [ ! -z "$VISUALIZATION_PID" ]; then
    echo "   kill $VISUALIZATION_PID"
fi
echo ""
echo "Press Ctrl+C to return to terminal (components will continue running)..."
read -p "Press any key to continue..." -n1 -s
echo ""