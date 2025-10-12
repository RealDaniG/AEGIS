#!/bin/bash

# Quick Run Script for Metatron V2 + Open A.G.I.
# This script starts the complete system with all components

echo "=== Metatron V2 + Open A.G.I. Quick Run Script ==="
echo "Starting the consciousness-aware distributed AI system..."

# Check if we're in the right directory
if [ ! -d "Metatron-ConscienceAI" ]; then
    echo "Error: Metatron-ConscienceAI directory not found!"
    echo "Please run this script from the root of the MetatronV2 repository."
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "Open-A.G.I" ]; then
    echo "Error: Open-A.G.I directory not found!"
    echo "Please run this script from the root of the MetatronV2 repository."
    exit 1
fi

# Install dependencies if not already installed
echo "Checking dependencies..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the Metatron Consciousness Engine
echo "Starting Metatron Consciousness Engine..."
cd Metatron-ConscienceAI
./START_SYSTEM.sh &
cd ..

# Wait a few seconds for the consciousness engine to start
echo "Waiting for consciousness engine to initialize..."
sleep 10

# Start the Open A.G.I. Framework
echo "Starting Open A.G.I. Framework..."
cd Open-A.G.I
python main.py &
cd ..

# Start visualization tools
echo "Starting Visualization Tools..."
python visualization_tools/robust_realtime_visualizer.py &

# Start consensus monitoring
echo "Starting Consensus Monitoring..."
python consensus_tools/improved_pbft_consensus.py --monitor &

echo "=== System Startup Complete ==="
echo "The Metatron V2 + Open A.G.I. system is now running."
echo "Access the web interface at http://localhost:8003"
echo "Visualization dashboard is available through the visualization tools."