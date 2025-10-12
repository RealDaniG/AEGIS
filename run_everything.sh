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
echo "[Step 1/4] Verifying Python environment..."
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
echo "[Step 2/4] Checking and installing all dependencies..."
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

# Start Unified System Coordinator
echo ""
echo "[Step 3/4] Starting Unified System Coordinator..."
echo "            - Consciousness Engine (Metatron-ConscienceAI)"
echo "            - AGI Framework (Open-A.G.I)"
echo "            - Consensus Protocol"
echo "            - P2P Networking Layer"
echo "            - Cross-System Communication"
echo ""

# Start the unified system in background
python3 start_unified_system.py &
UNIFIED_PID=$!

# Start Metatron Web Server
echo ""
echo "[Step 3.5/4] Starting Metatron Integrated Web Server..."
echo "            - Consciousness Engine Visualization"
echo "            - AI Chat System with File Upload"
echo "            - Mirror Loop Functionality"
echo "            - RAG Integration"
echo ""

cd Metatron-ConscienceAI
python3 scripts/metatron_web_server.py &
WEB_PID=$!
cd ..

echo "Waiting for systems to initialize..."
sleep 15

# Verify system is running
echo ""
echo "[Step 3.7/4] Verifying system components..."
if curl -f http://localhost:8005/health >/dev/null 2>&1; then
    echo "Check AEGIS system is running successfully"
else
    echo "Warning: AEGIS system may still be initializing or failed to start."
    echo "         Check the coordinator process for status updates."
fi

if curl -f http://localhost:8003/api/health >/dev/null 2>&1; then
    echo "Check Metatron Web Server is running successfully"
else
    echo "Warning: Metatron Web Server may still be initializing or failed to start."
    echo "         Check the web server process for status updates."
fi

# Open Web UI
echo ""
echo "[Step 4/4] Opening Web UI..."
echo "            - Opening Integrated Metatron Interface"
echo "            - Opening AEGIS Unified API Dashboard"
echo ""

# Try to open web browser (different commands for different systems)
if command -v xdg-open > /dev/null 2>&1; then
    # Linux
    xdg-open "http://localhost:8003" 2>/dev/null &
    xdg-open "http://localhost:8005/docs" 2>/dev/null &
elif command -v open > /dev/null 2>&1; then
    # macOS
    open "http://localhost:8003" 2>/dev/null &
    open "http://localhost:8005/docs" 2>/dev/null &
fi

echo ""
echo "========================================================================"
echo ""
echo "Check COMPLETE AEGIS SYSTEM IS NOW RUNNING"
echo ""
echo "========================================================================"
echo ""
echo "For comprehensive documentation, visit:"
echo "   https://github.com/RealDaniG/AEGIS/wiki"
echo ""
echo "Globe WEB INTERFACES:"
echo "   Unified API:        http://localhost:8005/"
echo "   WebSocket Server:   ws://localhost:8006"
echo "   Integrated UI:      http://localhost:8003"
echo "   API Documentation:  http://localhost:8005/docs"
echo ""
echo "Electric API ENDPOINTS:"
echo "   /api/consciousness  - Consciousness metrics"
echo "   /api/agi           - AGI system status"
echo "   /api/decision      - Consciousness-aware decisions"
echo "   /api/chat          - AI chat interface"
echo "   /health            - System health check"
echo ""
echo "Computer RUNNING PROCESSES:"
echo "   AEGIS System Coordinator (PID: $UNIFIED_PID)"
echo "   Metatron Integrated Web Server (PID: $WEB_PID)"
echo ""
echo "========================================================================"
echo ""
echo "Memo INSTRUCTIONS:"
echo "   - All components are running in background"
echo "   - Use 'kill $UNIFIED_PID' to stop unified system"
echo "   - Use 'kill $WEB_PID' to stop web server"
echo ""
echo "========================================================================"
echo ""
echo "To access the API documentation, visit:"
echo "   http://localhost:8005/docs"
echo ""
echo "For complete system documentation, visit:"
echo "   https://github.com/RealDaniG/AEGIS/wiki"
echo ""
echo "To stop the entire system, run:"
echo "   kill $UNIFIED_PID $WEB_PID"
echo ""
echo "Press Ctrl+C to return to terminal (components will continue running)..."
read -p "Press any key to continue..." -n1 -s
echo ""