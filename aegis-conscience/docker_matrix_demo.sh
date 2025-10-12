#!/bin/bash

# AEGIS-Conscience Network Matrix Docker Demo
# This script demonstrates how to run the matrix connectivity with Docker

echo "🐳 AEGIS-Conscience Network Matrix Docker Demo"
echo "============================================="

# Check if Docker is available
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null
then
    echo "❌ docker-compose is not installed or not in PATH"
    exit 1
fi

echo "✅ Docker and docker-compose are available"

# Build the images
echo "🏗️  Building Docker images..."
docker-compose build

# Start the network
echo "🚀 Starting AEGIS network with matrix connectivity..."
docker-compose up -d

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check the status
echo "🔍 Checking service status..."
docker-compose ps

# Show logs from one of the nodes
echo "📋 Showing logs from aegis-node-1..."
docker-compose logs aegis-node-1

echo ""
echo "🌐 The AEGIS network is now running with matrix connectivity!"
echo "   Node 1: http://localhost:8080"
echo "   Node 2: http://localhost:8081"
echo ""
echo "📊 To visualize the matrix, generate example data and run the visualizer:"
echo "   python generate_matrix_example.py"
echo "   python tools/matrix_visualizer.py"
echo ""
echo "⏹️  To stop the network, run: docker-compose down"