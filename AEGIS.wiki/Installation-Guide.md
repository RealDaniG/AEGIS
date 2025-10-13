# Installation Guide

This guide provides detailed instructions for installing and setting up the AEGIS system on your local machine.

## System Requirements

### Hardware Requirements
- **CPU**: Modern multi-core processor (Intel i5/AMD Ryzen 5 or better recommended)
- **RAM**: Minimum 8GB (16GB recommended for optimal performance)
- **Storage**: At least 20GB of free disk space
- **GPU**: Optional but recommended for ML components (CUDA-compatible GPU)

### Software Requirements
- **Operating System**: 
  - Windows 10/11 (64-bit)
  - Linux (Ubuntu 20.04+, CentOS 8+, or equivalent)
  - macOS 10.15+ (Catalina or later)
- **Python**: Version 3.8 or higher
- **Git**: For cloning the repository
- **Docker**: For containerized deployments (optional but recommended)
- **Internet Connection**: For downloading dependencies

## Prerequisites Installation

### Windows

1. **Install Python**:
   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **Install Git**:
   - Download Git from [git-scm.com](https://git-scm.com/downloads)
   - Follow the installation wizard with default settings
   - Verify installation: `git --version`

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install Git
sudo apt install git

# Install Docker (optional)
sudo apt install docker.io
sudo usermod -aG docker $USER
```

### macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python and Git**:
   ```bash
   brew install python git
   ```

## Cloning the Repository

```bash
# Clone the AEGIS repository
git clone https://github.com/RealDaniG/AEGIS.git

# Navigate to the project directory
cd AEGIS
```

## Dependency Installation

### Automatic Installation (Recommended)

Use the provided installation scripts:

**Windows**:
```cmd
# Run the installation script
install.bat
```

**Linux/macOS**:
```bash
# Make the script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

### Manual Installation

If you prefer manual installation:

1. **Create a Virtual Environment** (recommended):
   ```bash
   # Create virtual environment
   python -m venv aegis-env
   
   # Activate virtual environment
   # Windows:
   aegis-env\Scripts\activate
   
   # Linux/macOS:
   source aegis-env/bin/activate
   ```

2. **Install Core Dependencies**:
   ```bash
   # Install main requirements
   pip install -r requirements.txt
   
   # Install Metatron-ConscienceAI requirements
   cd Metatron-ConscienceAI
   pip install -r requirements.txt
   cd ..
   
   # Install Open-A.G.I requirements
   cd Open-A.G.I
   pip install -r requirements.txt
   cd ..
   
   # Install aegis-conscience requirements
   cd aegis-conscience
   pip install -r requirements.txt
   cd ..
   
   # Install unified system requirements
   pip install -r unified_requirements.txt
   ```

3. **Install Visualization Dependencies**:
   ```bash
   # Install visualization tools dependencies
   pip install websockets requests plotly
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```env
# System Configuration
AEGIS_PORT=8005
AEGIS_WS_PORT=8006
AEGIS_DEBUG=false

# Database Configuration (if using)
DATABASE_URL=sqlite:///aegis.db

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# TOR Configuration (if using)
TOR_PROXY_HOST=127.0.0.1
TOR_PROXY_PORT=9050
```

### Node Configuration

For custom node configuration, create a `node_config.json` file:

```json
{
  "node_id": "aegis-node-001",
  "network": {
    "host": "0.0.0.0",
    "port": 8005,
    "ws_port": 8006
  },
  "security": {
    "enable_tls": false,
    "enable_tor": false
  },
  "modules": {
    "consciousness_engine": true,
    "agi_framework": true,
    "decision_engine": true
  }
}
```

## Running the System

### Option 1: One-Command Launch (Recommended)

**Windows**:
```cmd
run_everything.bat
```

**Linux/macOS**:
```bash
chmod +x run_everything.sh
./run_everything.sh
```

### Option 2: Manual Launch

1. **Start the Unified System Coordinator**:
   ```bash
   python start_unified_system.py
   ```

2. **Start Visualization Tools** (in a separate terminal):
   ```bash
   cd visualization_tools
   python robust_realtime_visualizer.py
   ```

## Verification

### Check System Health

Once the system is running, verify it's working correctly:

1. **Health Check Endpoint**:
   ```bash
   curl http://localhost:8003/health
   ```

2. **API Documentation**:
   Open your browser and navigate to: http://localhost:8003/docs

3. **Visualization Window**:
   Check that the visualization window opens and displays real-time metrics

### Test API Endpoints

1. **Consciousness Metrics**:
   ```bash
   curl http://localhost:8003/api/consciousness
   ```

2. **AGI Status**:
   ```bash
   curl http://localhost:8003/api/agi
   ```

3. **System State**:
   ```bash
   curl http://localhost:8003/state
   ```

## Troubleshooting

### Common Installation Issues

1. **Permission Denied Errors**:
   - On Linux/macOS, try using `sudo` for system-wide installations
   - Ensure you have write permissions to the installation directory

2. **Python Version Issues**:
   - Verify you're using Python 3.8 or higher: `python --version`
   - If multiple Python versions are installed, use `python3` instead of `python`

3. **Missing Dependencies**:
   - Ensure all requirements files are installed
   - Check internet connectivity for package downloads

### Common Runtime Issues

1. **Port Already in Use**:
   - Check if another instance is running: `netstat -an | grep 8005`
   - Kill the existing process or change the port configuration

2. **Connection Refused**:
   - Verify the system is running
   - Check firewall settings
   - Ensure localhost connections are allowed

3. **Module Import Errors**:
   - Verify all dependencies are installed
   - Check that you're in the correct virtual environment
   - Reinstall missing packages: `pip install package-name`

### Docker Deployment (Optional)

For containerized deployment:

1. **Build Docker Images**:
   ```bash
   docker-compose build
   ```

2. **Run Containers**:
   ```bash
   docker-compose up
   ```

## Performance Tuning

### Resource Allocation

1. **CPU Usage**:
   - Adjust the number of worker processes in configuration
   - Limit CPU usage with Docker resource constraints

2. **Memory Usage**:
   - Monitor memory consumption with system tools
   - Adjust batch sizes for ML components

3. **Network Optimization**:
   - Use local network for better performance
   - Enable compression for large data transfers

### Advanced Configuration

1. **Custom Logging**:
   Configure log levels and output destinations in the logging configuration file.

2. **Security Hardening**:
   - Enable TLS for secure communication
   - Configure firewall rules
   - Use strong authentication mechanisms

3. **Backup and Recovery**:
   - Regular database backups
   - Configuration file versioning
   - Disaster recovery procedures

## Updates and Maintenance

### Updating the System

1. **Pull Latest Changes**:
   ```bash
   git pull origin master
   ```

2. **Update Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Restart Services**:
   Stop and restart the system to apply updates.

### Monitoring

1. **System Logs**:
   Check log files in the `logs/` directory for system events.

2. **Performance Metrics**:
   Use the visualization tools to monitor system performance.

3. **Health Checks**:
   Regular health checks via the API endpoints.

## Support

If you encounter issues during installation:

1. Check the console output for error messages
2. Verify all prerequisites are met
3. Consult the full documentation in the GitHub Wiki
4. Contact the repository owner for support

---

*Developed with ❤️ for the advancement of consciousness-aware AI*