# AEGIS-Conscience Network Matrix Docker Demo
# This script demonstrates how to run the matrix connectivity with Docker on Windows

Write-Host "🐳 AEGIS-Conscience Network Matrix Docker Demo"
Write-Host "============================================="

# Check if Docker is available
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker is available: $dockerVersion"
} catch {
    Write-Host "❌ Docker is not installed or not in PATH"
    exit 1
}

# Check if docker-compose is available
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ docker-compose is available: $composeVersion"
} catch {
    Write-Host "❌ docker-compose is not installed or not in PATH"
    exit 1
}

# Build the images
Write-Host "🏗️  Building Docker images..."
docker-compose build

# Start the network
Write-Host "🚀 Starting AEGIS network with matrix connectivity..."
docker-compose up -d

# Wait a moment for services to start
Write-Host "⏳ Waiting for services to start..."
Start-Sleep -Seconds 10

# Check the status
Write-Host "🔍 Checking service status..."
docker-compose ps

# Show logs from one of the nodes
Write-Host "📋 Showing logs from aegis-node-1..."
docker-compose logs aegis-node-1

Write-Host ""
Write-Host "🌐 The AEGIS network is now running with matrix connectivity!"
Write-Host "   Node 1: http://localhost:8080"
Write-Host "   Node 2: http://localhost:8081"
Write-Host ""
Write-Host "📊 To visualize the matrix, generate example data and run the visualizer:"
Write-Host "   python generate_matrix_example.py"
Write-Host "   python tools/matrix_visualizer.py"
Write-Host ""
Write-Host "⏹️  To stop the network, run: docker-compose down"