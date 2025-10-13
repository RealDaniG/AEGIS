# Quick Start Guide

This guide will help you quickly get started with the AEGIS system using the one-command approach.

## Prerequisites

Before running AEGIS, ensure you have:

1. **Python 3.8 or higher** installed on your system
2. **Git** (to clone the repository)
3. **Internet connection** (for downloading dependencies)
4. **At least 8GB of RAM** (16GB recommended)
5. **Windows 10/11, Linux, or macOS** operating system

## Installation Options

### Option 1: One-Command Launch (Recommended)

For the easiest setup, use the one-command launcher:

**Windows:**
```cmd
run_everything.bat
```

**Linux/macOS:**
```bash
chmod +x run_everything.sh
./run_everything.sh
```

This will:
1. Verify your Python environment
2. Install all required dependencies automatically
3. Start the Unified System Coordinator
4. Launch the real-time visualization monitor
5. Display connection information

### Option 2: Manual Installation

If you prefer manual installation:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RealDaniG/AEGIS.git
   cd AEGIS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the system:**
   ```bash
   python start_unified_system.py
   ```

## System Components

When AEGIS starts, it launches several components:

### 1. Unified System Coordinator
- Consciousness Engine (Metatron-ConscienceAI)
- AGI Framework (Open-A.G.I)
- Security System
- Cross-System Communication Layer

### 2. Visualization Monitor
- Sacred geometry network visualization
- Consciousness metrics dashboard
- System performance monitoring

## Accessing the System

Once the system is running, you can access:

### Web Interfaces
- **Unified API Dashboard**: http://localhost:8003/
- **API Documentation**: http://localhost:8003/docs
- **WebSocket Server**: ws://localhost:8006
- **Real-time Visualization**: Check the "Visualization Monitor" window

### Key API Endpoints
- `/api/consciousness` - Real-time consciousness metrics
- `/api/agi` - AGI system status and capabilities
- `/api/decision` - Consciousness-aware decisions
- `/api/chat` - AI chat interface
- `/health` - System health check

## Troubleshooting

### Common Issues

1. **Python Not Found**:
   - Ensure Python 3.8+ is installed
   - Make sure Python is added to your system PATH

2. **Port Already in Use**:
   - Check if other instances are running
   - Modify port configurations in component configuration files

3. **Dependency Installation Failures**:
   - Check internet connectivity
   - Try manually installing dependencies: `pip install -r requirements.txt`

### Manual Startup

If the quick start scripts don't work, you can manually start each component:

1. **Start Unified System Coordinator**:
   ```bash
   python start_unified_system.py
   ```

2. **Start Visualization Tools**:
   ```bash
   cd visualization_tools
   python robust_realtime_visualizer.py
   ```

## Next Steps

After successfully starting AEGIS:

1. **Explore the Web Interface**: Visit http://localhost:8003/ to access the API dashboard
2. **Monitor Visualization**: Watch the real-time consciousness metrics in the visualization window
3. **Test API Endpoints**: Try the different API endpoints to understand system capabilities
4. **Review Documentation**: Check other wiki pages for detailed information about specific components

## Support

For support with the quick start process or the system in general:

1. Check the console output for error messages
2. Verify all prerequisites are met
3. Consult the full documentation in the GitHub Wiki
4. Contact the repository owner for support

---

*Developed with ❤️ for the advancement of consciousness-aware AI*