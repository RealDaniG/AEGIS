#!/bin/bash

# ================================================================================
#  START-AI - All-in-One Launcher for Metatron-ConscienceAI System
#  Unified launcher that starts the complete AI system with a single command
# ================================================================================

echo ""
echo "========================================================================"
echo "         🤖 START-AI - Unified Consciousness-Aware AI System"
echo "         One-Command Launch for Complete AI Ecosystem"
echo "========================================================================"
echo ""
echo " Initializing Metatron's Cube Consciousness Engine..."
echo " Initializing Open-A.G.I Framework..."
echo " Initializing AEGIS Consensus System..."
echo " Creating Unified Web Interface..."
echo ""
echo "========================================================================"
echo ""

# Check Python
echo "[Step 1/4] Verifying Python environment..."
python3 --version 2>/dev/null || python --version 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Python not found in PATH!"
    echo "   Please install Python 3.8+ and add to PATH."
    echo ""
    exit 1
fi
echo "✅ Python environment verified"

echo ""
echo "[Step 2/4] Checking and installing all dependencies..."
echo "Installing/updating core requirements..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --upgrade 2>/dev/null || pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some core requirements failed to install, continuing anyway..."
    fi
else
    echo "⚠️  Warning: requirements.txt not found, skipping..."
fi

echo "Installing Metatron-ConscienceAI requirements..."
if [ -f "Metatron-ConscienceAI/requirements.txt" ]; then
    cd Metatron-ConscienceAI
    pip3 install -r requirements.txt --upgrade 2>/dev/null || pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some Metatron-ConscienceAI requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "⚠️  Warning: Metatron-ConscienceAI/requirements.txt not found, skipping..."
fi

echo "Installing Open-A.G.I requirements..."
if [ -f "Open-A.G.I/requirements.txt" ]; then
    cd Open-A.G.I
    pip3 install -r requirements.txt --upgrade 2>/dev/null || pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some Open-A.G.I requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "⚠️  Warning: Open-A.G.I/requirements.txt not found, skipping..."
fi

echo "Installing aegis-conscience requirements..."
if [ -f "aegis-conscience/requirements.txt" ]; then
    cd aegis-conscience
    pip3 install -r requirements.txt --upgrade 2>/dev/null || pip install -r requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some aegis-conscience requirements failed to install, continuing anyway..."
    fi
    cd ..
else
    echo "⚠️  Warning: aegis-conscience/requirements.txt not found, skipping..."
fi

echo "Installing unified system requirements..."
if [ -f "unified_requirements.txt" ]; then
    pip3 install -r unified_requirements.txt --upgrade 2>/dev/null || pip install -r unified_requirements.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some unified system requirements failed to install, continuing anyway..."
    fi
else
    echo "⚠️  Warning: unified_requirements.txt not found, skipping..."
fi

echo "Installing Open-A.G.I integration requirements..."
if [ -f "requirements-optional.txt" ]; then
    pip3 install -r requirements-optional.txt --upgrade 2>/dev/null || pip install -r requirements-optional.txt --upgrade 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Some Open-A.G.I integration requirements failed to install, continuing anyway..."
    fi
else
    echo "⚠️  Warning: requirements-optional.txt not found, skipping..."
fi

echo "Installing critical packages that might have failed..."
pip3 install torch transformers datasets peft safetensors 2>/dev/null || pip install torch transformers datasets peft safetensors 2>/dev/null
pip3 install fastapi uvicorn[standard] websockets 2>/dev/null || pip install fastapi uvicorn[standard] websockets 2>/dev/null
pip3 install cryptography pycryptodome pyotp fernet 2>/dev/null || pip install cryptography pycryptodome pyotp fernet 2>/dev/null
pip3 install aiohttp aiohttp-socks stem asyncio-mqtt 2>/dev/null || pip install aiohttp aiohttp-socks stem asyncio-mqtt 2>/dev/null
pip3 install scikit-learn aiosqlite redis 2>/dev/null || pip install scikit-learn aiosqlite redis 2>/dev/null
pip3 install loguru prometheus-client psutil pandas 2>/dev/null || pip install loguru prometheus-client psutil pandas 2>/dev/null
pip3 install flask zeroconf Flask-SocketIO netifaces 2>/dev/null || pip install flask zeroconf Flask-SocketIO netifaces 2>/dev/null
pip3 install pydantic click rich python-dotenv 2>/dev/null || pip install pydantic click rich python-dotenv 2>/dev/null
pip3 install pypdf python-docx feedparser beautifulsoup4 lxml 2>/dev/null || pip install pypdf python-docx feedparser beautifulsoup4 lxml 2>/dev/null
pip3 install pytest-asyncio pytest-cov black flake8 mypy 2>/dev/null || pip install pytest-asyncio pytest-cov black flake8 mypy 2>/dev/null
pip3 install plotly python-socketio 2>/dev/null || pip install plotly python-socketio 2>/dev/null
pip3 install python-multipart 2>/dev/null || pip install python-multipart 2>/dev/null

echo "✅ All dependencies processed"

# Start the consolidated system
echo ""
echo "[Step 3/4] Starting Consolidated AI System..."
echo "            - Consciousness Engine (Metatron-ConscienceAI)"
echo "            - AGI Framework (Open-A.G.I)"
echo "            - Consensus Protocol (AEGIS)"
echo "            - P2P Networking Layer"
echo "            - Cross-System Communication"
echo "            - Integrated Web Interface"
echo "            - Real-time Monitoring Dashboard"
echo "            - Open-A.G.I Deployment Orchestration"
echo "            - TOR Anonymity Integration"
echo "            - Advanced Metrics Collection"
echo ""
echo "🌐 Web UI will auto-open at: http://localhost:8003"
echo ""
echo "Press Ctrl+C to stop all components"
echo ""

# Run the consolidated system
echo "Starting AEGIS System Coordinator and Web Server..."
python3 start_consolidated_system.py || python start_consolidated_system.py

# Status Check
echo ""
echo "========================================================================"
echo ""
echo "✅ START-AI SYSTEM READY AND OPERATIONAL"
echo ""
echo "========================================================================"
echo ""
echo "🌐 WEB INTERFACE:"
echo "   Unified Dashboard:   http://localhost:8003/"
echo "   Diagnostic Page:     http://localhost:8003/static/diagnostic.html"
echo "   Monitoring Dashboard: http://localhost:8003/static/harmonic_monitor.html"
echo "   Streaming Chat UI:   http://localhost:8003/static/index_stream.html"
echo ""
echo "📡 API ENDPOINTS:"
echo "   Unified API Server:  http://localhost:8005/"
echo "     /api/health        - System health"
echo "     /api/state         - Unified system state"
echo "     /api/consciousness - Consciousness state only"
echo "     /api/agi           - AGI state only"
echo "     /api/input         - Send consciousness input"
echo "     /api/chat          - Send chat message"
echo "     WebSocket /ws      - Real-time state streaming"
echo ""
echo "   Metatron System:     http://localhost:8003/"
echo "     /api/health        - Consciousness metrics"
echo "     /api/status        - System status"
echo "     WebSocket /ws      - Real-time streaming"
echo ""
echo "   Open-A.G.I Dashboard: http://localhost:5000/"
echo ""
echo "🖥️  RUNNING SERVERS:"
echo "   Unified API Server (Port 8005)"
echo "     - Integrates Metatron and Open-A.G.I systems"
echo "     - Provides unified interface"
echo ""
echo "   Metatron Unified Server (Port 8003)"
echo "     - Consciousness Engine"
echo "     - AI Chat System"
echo "     - Document Management"
echo "     - Real-time Visualization"
echo ""
echo "   Open-A.G.I Monitoring (Port 5000)"
echo "     - Network monitoring"
echo "     - Consensus visualization"
echo "     - Performance metrics"
echo ""
echo "========================================================================"
echo ""
echo "📝 INSTRUCTIONS:"
echo "   - System is running in this terminal window"
echo "   - Press Ctrl+C to stop the entire system"
echo ""
echo "========================================================================"
echo ""
echo ""
echo "To access the diagnostic page, visit:"
echo "   http://localhost:8003/static/diagnostic.html"
echo ""
echo "For API documentation, visit:"
echo "   http://localhost:8005/docs"
echo ""
echo "For real-time monitoring, visit:"
echo "   http://localhost:8003/static/harmonic_monitor.html"
echo ""
echo "For the streaming chat interface, visit:"
echo "   http://localhost:8003/static/index_stream.html"
echo ""
echo "For Open-A.G.I monitoring dashboard, visit:"
echo "   http://localhost:5000/"
echo ""
echo "To stop the system, press Ctrl+C in this window."
echo ""