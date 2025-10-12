# Open-A.G.I Installation Guide

## System Requirements

Before installing Open-A.G.I, ensure your system meets the following requirements:

### Hardware Requirements
- **CPU**: 2+ cores (4+ cores recommended)
- **RAM**: 4GB minimum (8GB+ recommended)
- **Storage**: 10GB free space
- **Network**: Stable internet connection

### Software Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+, CentOS 8+)
- **Python**: 3.9 or higher
- **TOR**: For anonymous communications
- **Git**: For cloning the repository

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/open-a-g-i.git
cd open-a-g-i
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install TOR

#### Windows
Download and install TOR Browser from the [official website](https://www.torproject.org/download/).

#### macOS
```bash
# Using Homebrew
brew install tor
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tor
```

#### CentOS/RHEL
```bash
sudo yum install tor
```

### 5. Configure TOR

Edit the TOR configuration file:

#### Ubuntu/Debian/CentOS
```bash
sudo nano /etc/tor/torrc
```

Add the following lines:
```
ControlPort 9051
CookieAuthentication 1
CookieAuthFileGroupReadable 1
```

Restart TOR:
```bash
sudo systemctl restart tor
```

## Quick Start

### 1. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cat > .env << EOF
# Network Configuration
TOR_CONTROL_PORT=9051
TOR_SOCKS_PORT=9050
P2P_PORT=8080

# Security Configuration
SECURITY_LEVEL=HIGH
MIN_COMPUTATION_SCORE=50.0
BYZANTINE_THRESHOLD_RATIO=0.33

# Consensus Configuration
POC_INTERVAL=300
PBFT_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=distributed_ai.log
EOF
```

### 2. Initialize a Node

```bash
python main.py start-node
```

### 3. Run Tests

To verify the installation, run the test suite:

```bash
python -m pytest tests/ -v
```

## Configuration Options

### Security Levels
- **STANDARD**: Basic security features
- **HIGH**: Enhanced security with additional checks
- **PARANOID**: Maximum security with strict validation

### Network Ports
- **TOR_SOCKS_PORT**: Port for TOR SOCKS proxy (default: 9050)
- **TOR_CONTROL_PORT**: Port for TOR control interface (default: 9051)
- **P2P_PORT**: Port for P2P communications (default: 8080)

## Troubleshooting

### Common Issues

#### TOR Connection Issues
If you encounter TOR connection issues:
1. Verify TOR is running: `systemctl status tor`
2. Check TOR configuration: `/etc/tor/torrc`
3. Ensure ports are not blocked by firewall

#### Python Dependency Issues
If you encounter Python dependency issues:
1. Update pip: `pip install --upgrade pip`
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

#### Permission Errors
If you encounter permission errors:
1. Ensure you're using a virtual environment
2. Run with appropriate user permissions
3. Check file permissions in the project directory

### Logs and Debugging

Check the log file for detailed error information:
```bash
tail -f distributed_ai.log
```

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## Docker Installation (Optional)

For containerized deployment, you can use Docker:

```bash
# Build the Docker image
docker build -t open-a-g-i .

# Run the container
docker run -p 8080:8080 open-a-g-i
```

## Next Steps

After successful installation, proceed to:
1. [Configuration Guide](configuration.md)
2. [API Reference](api/rest_api.md)
3. [Testing Guide](testing.md)