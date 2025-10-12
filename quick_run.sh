#!/bin/bash
# quick_run.sh
# Quick start script for AEGIS system on Linux/macOS

echo "========================================"
echo "  AEGIS - Quick Start Script"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "run_everything.sh" ]; then
    echo "❌ Error: run_everything.sh not found!"
    echo "   Please run this script from the AEGIS root directory."
    exit 1
fi

echo "✅ Found AEGIS project files"
echo ""

# Check Python
echo "🔍 Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found!"
    echo "   Please install Python 3.8 or higher"
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
fi

# Make sure the script is executable
echo ""
echo "🔧 Setting permissions..."
chmod +x run_everything.sh

# Run the main launcher
echo ""
echo "🚀 Starting AEGIS system..."
echo "   This will launch the system and open the web interface"
echo ""

# Run the shell script
./run_everything.sh &

echo "✅ AEGIS system launch initiated!"
echo "   Check the new terminal window for system status"
echo "   Your web browser will open automatically with the visualization"
echo ""
echo "========================================"
echo "  AEGIS System Starting..."
echo "========================================"