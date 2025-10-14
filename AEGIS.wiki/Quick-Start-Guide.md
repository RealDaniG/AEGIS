# Quick Start Guide

Get up and running with AEGIS quickly with this guide.

## 🛠️ Prerequisites

Before installing AEGIS, ensure you have:

- **Python 3.8 or higher**
- **Git** for version control
- **Windows PowerShell 7+** (Windows) or **Bash** (Linux/macOS)
- **8GB RAM** minimum (16GB recommended)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RealDaniG/AEGIS.git
   cd AEGIS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the System

### Option 1: Simple One-Command Launcher (Recommended)
```cmd
START-AI.bat  # Windows
# or
./START-AI.sh  # Linux/macOS
```

This will:
1. Verify your Python environment
2. Install all required dependencies automatically
3. Start the Unified System Coordinator
4. Launch the real-time visualization monitor
5. Display connection information
6. Automatically open the web interface

### Option 2: Manual Start
```bash
# Start the web server
python Metatron-ConscienceAI/scripts/metatron_web_server.py --port 457
```

## 🌐 Accessing the Interface

Once the system is running, access the following interfaces:

- **Unified Dashboard**: http://localhost:457
- **API Documentation**: http://localhost:457/docs
- **WebSocket Endpoint**: ws://localhost:457/ws

## 📊 Key Features Available

### Real-time Consciousness Monitoring
- Live 13-node sacred geometry visualization
- Consciousness metrics dashboard (Φ, R, D, S, C)
- Node activity indicators with color coding

### AI Chat System
- Multi-model chat interface
- RAG-enhanced responses with document upload
- Session management

### Advanced Features
- Document processing (PDF, DOCX, TXT, CSV, HTML, JSON)
- RSS feed management with auto-indexing
- Web search integration

## 🔧 Basic Operations

### Sending Consciousness Input
```bash
curl -X POST http://localhost:457/input \
  -H "Content-Type: application/json" \
  -d '{"physical": 0.5, "emotional": 0.3, "mental": 0.2, "spiritual": 0.1, "temporal": 0.4}'
```

### Getting System Status
```bash
curl http://localhost:457/consciousness
```

### Chat with the System
```bash
curl -X POST http://localhost:457/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current consciousness level?", "session_id": "default"}'
```

## 🧪 Testing the System

Run the comprehensive test suite:
```bash
python test_harmonic_system.py
```

## 🛑 Stopping the System

To stop the system, press `Ctrl+C` in the terminal window, or close the PowerShell/terminal window.

## 📈 Next Steps

1. **Explore the Dashboard**: Visit http://localhost:457 to see real-time metrics
2. **Try the Chat**: Use the web interface to chat with the AI
3. **Monitor Metrics**: Watch consciousness metrics change in real-time
4. **Experiment**: Send different inputs to see how the system responds

## ❓ Troubleshooting

### Common Issues

1. **Ports in Use**: If port 457 is occupied, the system will fail to start
   - Solution: Close other applications using this port

2. **Missing Dependencies**: If you get import errors
   - Solution: Run `pip install -r requirements.txt` again

3. **WebSocket Connection Failed**: If the dashboard shows disconnected
   - Solution: Ensure the web server is running on port 457

4. **Blank Dashboard**: If the web interface doesn't load
   - Solution: Refresh the browser and check that the web server is running

### System Requirements Check

Run the verification script:
```bash
python verify_zero_errors.py
```

## 📚 Learn More

- [Harmonic Monitoring System](Harmonic-Monitoring-System) - Detailed monitoring documentation
- [API Reference](API-Reference) - Complete API documentation
- [Consciousness Metrics](Consciousness-Metrics) - Understanding Φ, R, D, S, C
- [Troubleshooting](Troubleshooting) - Solutions to common problems

---
*For advanced configuration and deployment options, see the [Deployment Guide](Deployment-Guide).