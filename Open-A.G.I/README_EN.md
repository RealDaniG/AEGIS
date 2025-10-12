# 🤖 Open A.G.I - Advanced General Intelligence Framework

## ⚠️ LEGAL AND ETHICAL NOTICE

**This project is designed exclusively for academic research and ethical development of distributed artificial intelligence systems. The use of this code for malicious, illegal, or privacy-violating activities is strictly prohibited.**

### 🛡️ AEGIS Security Principles

- **Transparency**: All code is auditable and documented
- **Privacy**: Data protection through end-to-end encryption
- **Consensus**: Distributed decisions without single points of failure
- **Responsibility**: Traceability of all actions in the network

---

## 🏗️ System Architecture

### Main Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TOR Gateway   │◄──►│  P2P Network    │◄──►│ Knowledge Base  │
│                 │    │   Manager       │    │   Distributed   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Crypto Engine   │    │ Resource Pool   │    │ Consensus Core  │
│                 │    │   Manager       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Enhanced Module Structure (Version 3.0)

1. **[logging_system.py](file:///d:/metatronV2/Open-A.G.I/logging_system.py)** - Advanced logging with multi-level support, file rotation, JSON formatting, and security-aware logging
2. **[config_manager.py](file:///d:/metatronV2/Open-A.G.I/config_manager.py)** - Enhanced configuration management with dynamic loading, validation, encryption, and auto-reload
3. **[api_server.py](file:///d:/metatronV2/Open-A.G.I/api_server.py)** - Dedicated API server with RESTful endpoints, WebSocket support, authentication, and rate limiting
4. **[metrics_collector.py](file:///d:/metatronV2/Open-A.G.I/metrics_collector.py)** - Comprehensive metrics collection with Prometheus integration, custom metrics, and historical analysis
5. **[alert_system.py](file:///d:/metatronV2/Open-A.G.I/alert_system.py)** - Advanced alerting system with multiple notification channels, deduplication, and escalation policies
6. **[web_dashboard.py](file:///d:/metatronV2/Open-A.G.I/web_dashboard.py)** - Dedicated web dashboard with real-time visualization and responsive design
7. **[backup_system.py](file:///d:/metatronV2/Open-A.G.I/backup_system.py)** - Automated backup system with encryption, compression, and retention policies
8. **[test_framework.py](file:///d:/metatronV2/Open-A.G.I/test_framework.py)** - Enhanced testing framework with parallel execution and comprehensive reporting

### Security Features

- **🔐 End-to-End Encryption**: ChaCha20-Poly1305 + Double Ratchet
- **🌐 Anonymous Communications**: Full TOR network integration
- **🤝 Byzantine Consensus**: Fault tolerance with PBFT + Proof of Computation
- **🔑 Cryptographic Identities**: Ed25519 for digital signatures
- **🛡️ Attack Resistance**: Protection against Sybil, Eclipse, and poisoning

---

## 🚀 Installation and Setup

### Prerequisites

1. **Python 3.9+**
2. **TOR Browser or Daemon** (for anonymous communications)
3. **4GB+ RAM** (for ML operations)
4. **Stable Internet Connection**

### Installation

```bash
# Clone the repository
git clone https://github.com/KaseMaster/Open-A.G.I.git
cd Open-A.G.I

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install optional dependencies for enhanced features
pip install -r requirements-optional.txt

# Configure TOR (Ubuntu/Debian)
sudo apt-get install tor
sudo systemctl start tor
sudo systemctl enable tor
```

### TOR Configuration

```bash
# Edit TOR configuration
sudo nano /etc/tor/torrc

# Add the following lines:
ControlPort 9051
CookieAuthentication 1
CookieAuthFileGroupReadable 1
```

### Environment Variables

```bash
# Create .env file
cat > .env << EOF
# Network Configuration
TOR_CONTROL_PORT=9051
TOR_SOCKS_PORT=9050
P2P_PORT=8080

# Security Configuration
SECURITY_LEVEL=HIGH  # STANDARD, HIGH, PARANOID
MIN_COMPUTATION_SCORE=50.0
BYZANTINE_THRESHOLD_RATIO=0.33

# Consensus Configuration
POC_INTERVAL=300  # seconds between challenges
PBFT_TIMEOUT=30   # timeout for PBFT consensus

# Logging
LOG_LEVEL=INFO
LOG_FILE=aegis_system.log

# API Server
API_PORT=8000
API_HOST=0.0.0.0

# Web Dashboard
DASHBOARD_PORT=8080
DASHBOARD_HOST=0.0.0.0

# Backup System
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=30
EOF
```

---

## 🧠 Quick Start Guide

### Starting the System

```bash
# Start the main AEGIS node
python main.py start-node

# Start with custom configuration
python main.py start-node --config custom_config.json

# Dry run to validate modules
python main.py start-node --dry-run

# Check system health
python main.py health-check

# List available modules
python main.py list-modules
```

### Module Configuration

The system can be configured to enable/disable specific modules through the configuration file:

```json
{
  "app": {
    "log_level": "INFO",
    "enable": {
      "tor": true,
      "p2p": true,
      "crypto": true,
      "consensus": true,
      "monitoring": true,
      "resource_manager": true,
      "performance_optimizer": true,
      "logging_system": true,
      "config_manager": true,
      "api_server": true,
      "metrics_collector": true,
      "alert_system": true,
      "web_dashboard": true,
      "backup_system": true,
      "test_framework": true
    }
  }
}
```

### Using the API Server

```python
import requests

# Get system status
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get metrics
response = requests.get("http://localhost:8000/metrics")
print(response.json())

# Get configuration
response = requests.get("http://localhost:8000/config")
print(response.json())
```

### Web Dashboard Access

The web dashboard is available at `http://localhost:8080` by default and provides:

- Real-time system monitoring
- Performance metrics visualization
- Alert management
- Configuration interface
- System status overview

---

## 🔧 Advanced Usage

### Custom Alert Rules

```python
from alert_system import add_alert_rule, AlertRule, AlertLevel

# Add a custom alert rule
custom_rule = AlertRule(
    id="high_cpu_usage",
    name="High CPU Usage",
    description="Alert when CPU usage exceeds 80%",
    condition="cpu_usage > 80",
    level=AlertLevel.WARNING,
    notify_channels=["console", "email"]
)

add_alert_rule(custom_rule)
```

### Custom Metrics Collection

```python
from metrics_collector import register_metric, set_metric_value, MetricConfig, MetricType, MetricCategory

# Register a custom metric
custom_metric = MetricConfig(
    name="custom_processing_time",
    type=MetricType.HISTOGRAM,
    category=MetricCategory.PERFORMANCE,
    description="Processing time for custom operations"
)

register_metric(custom_metric)

# Set metric value
set_metric_value("custom_processing_time", 0.125)
```

### Backup Management

```python
from backup_system import get_backup_manager

# Create an immediate backup
manager = get_backup_manager()
backup_record = manager.create_backup()
print(f"Backup created: {backup_record}")
```

### Configuration Management

```python
from config_manager import get_config_value, set_metric_value

# Get a configuration value
log_level = get_config_value("app.log_level", "INFO")
print(f"Current log level: {log_level}")

# Configuration changes are automatically reloaded if auto-reload is enabled
```

---

## 🔒 Security Considerations

### Mitigated Threats

1. **Sybil Attacks**
   - Proof of Computation to validate identities
   - Reputation system based on contributions

2. **Eclipse Attacks**
   - Geographic diversification of TOR connections
   - Automatic circuit rotation

3. **Data Poisoning**
   - Byzantine consensus for validation
   - Cryptographic signatures on all contributions

4. **Traffic Analysis**
   - Communications exclusively through TOR
   - Temporal padding and synthetic noise

### Best Practices

- **Never** run as root user
- **Always** validate TOR certificates
- **Rotate** keys regularly (every 24h)
- **Monitor** security logs
- **Update** dependencies frequently

---

## 📊 Monitoring and Metrics

### System Metrics

```python
# Get network statistics
from metrics_collector import get_all_metrics
metrics = get_all_metrics()
print(f"CPU Usage: {metrics.get('cpu_usage_percent', {}).get('value', 0)}%")
print(f"Memory Usage: {metrics.get('memory_usage_bytes', {}).get('value', 0)} bytes")
```

### TOR Metrics

```python
# TOR network status (requires tor_integration module)
from tor_integration import get_network_status
tor_status = get_network_status()
print(f"Active circuits: {tor_status.get('active_circuits', 0)}")
print(f"Available nodes: {tor_status.get('available_nodes', 0)}")
```

### Security Logs

```bash
# Monitor logs in real-time
tail -f aegis_system.log | grep -E "(WARNING|ERROR|SECURITY)"

# Analyze attack patterns
grep "SECURITY" aegis_system.log | awk '{print $1, $2, $NF}' | sort | uniq -c
```

---

## 🧪 Testing and Validation

### Security Tests

```bash
# Run complete test suite
python -m pytest tests/ -v --cov=.

# Specific security tests
python -m pytest tests/test_security.py -v

# Consensus tests
python -m pytest tests/test_consensus.py -v

# TOR integration tests
python -m pytest tests/test_tor_integration.py -v
```

### Module Tests

```bash
# Test logging system
python -m pytest tests/test_logging_system.py -v

# Test configuration manager
python -m pytest tests/test_config_manager.py -v

# Test API server
python -m pytest tests/test_api_server.py -v

# Test metrics collector
python -m pytest tests/test_metrics_collector.py -v

# Test alert system
python -m pytest tests/test_alert_system.py -v

# Test web dashboard
python -m pytest tests/test_web_dashboard.py -v

# Test backup system
python -m pytest tests/test_backup_system.py -v

# Test framework
python -m pytest tests/test_test_framework.py -v
```

### Attack Simulation

```bash
# Simulate Sybil attack
python tests/simulate_sybil_attack.py --nodes 100 --malicious 30

# Simulate Eclipse attack
python tests/simulate_eclipse_attack.py --target node_123

# Byzantine resistance test
python tests/test_byzantine_resistance.py --byzantine_ratio 0.25
```

---

## 🤝 Contributions

### Code of Conduct

- **Ethical Use**: Only for legitimate research and development
- **Transparency**: Document all security changes
- **Responsibility**: Report vulnerabilities responsibly
- **Collaboration**: Respect diversity and inclusion

### Contribution Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-feature`)
3. **Implement** with security tests
4. **Document** changes and security considerations
5. **Submit** Pull Request with detailed description

### Vulnerability Reporting

**DO NOT** report vulnerabilities publicly. Use:
- Email: security@open-a-g-i.org
- PGP Key: [PGP Key for secure communication]

---

## 📚 Additional Documentation

- [Detailed Architecture Guide](docs/architecture.md)
- [Security Manual](docs/security_manual.md)
- [API Reference](docs/api_reference.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Module Documentation](docs/modules/)

---

## 📄 License

This project is licensed under the **MIT License with Ethical Use Clauses**.

### Additional Restrictions

- **Prohibited** use for illegal activities
- **Prohibited** use for unauthorized surveillance
- **Prohibited** use for information manipulation
- **Required** compliance with local privacy laws

---

## 🙏 Acknowledgments

- **TOR Project** for anonymity infrastructure
- **Cryptography.io** for cryptographic primitives
- **Security Community** for best practices
- **Distributed AI Researchers** for theoretical foundations

---

**⚠️ FINAL REMINDER: This software is a research tool. The user is fully responsible for its ethical and legal use. Developers are not responsible for misuse of this code.**

---

*Developed by AEGIS - Advanced General Intelligence System*  
*Version 3.0 - For ethical use only*