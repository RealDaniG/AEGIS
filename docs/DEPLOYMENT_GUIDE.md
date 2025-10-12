# AEGIS Deployment Guide

## Overview

This guide provides instructions for deploying the AEGIS (Autonomous Governance and Intelligent Systems) platform in various environments, from development to production.

## Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU**: 4 cores (Intel/AMD)
- **RAM**: 8 GB
- **Storage**: 50 GB available disk space
- **OS**: Ubuntu 20.04+, CentOS 8+, Windows 10/11, macOS 11+
- **Network**: 100 Mbps internet connection

#### Recommended Requirements
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **Network**: 1 Gbps connection

### Software Dependencies

#### Required Software
- **Python**: 3.8-3.11
- **Docker**: 20.10+ (optional, for containerized deployment)
- **Git**: 2.25+
- **Node.js**: 14+ (for web interface)

#### Python Packages
Install required packages:
```bash
pip install -r requirements.txt
pip install -r unified_requirements.txt
```

## Deployment Options

### 1. Development Deployment

For local development and testing:

```bash
# Clone the repository
git clone https://github.com/RealDaniG/AEGIS.git
cd AEGIS

# Install dependencies
pip install -r requirements.txt
pip install -r unified_requirements.txt

# Start the system
./run_everything.sh  # Linux/macOS
# or
run_everything.bat   # Windows
```

### 2. Docker Deployment

For containerized deployment:

```bash
# Build Docker images
docker-compose build

# Start the system
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Kubernetes Deployment

For production Kubernetes deployment:

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods
kubectl get services
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# System Configuration
AEGIS_ENV=production
AEGIS_LOG_LEVEL=INFO
AEGIS_DATA_DIR=/var/lib/aegis

# Network Configuration
AEGIS_API_PORT=8005
AEGIS_WEBSOCKET_PORT=8006
AEGIS_P2P_PORT=8080

# Security Configuration
AEGIS_JWT_SECRET=your_jwt_secret_here
AEGIS_ENCRYPTION_KEY=your_encryption_key_here

# Database Configuration
AEGIS_DB_HOST=localhost
AEGIS_DB_PORT=5432
AEGIS_DB_NAME=aegis
AEGIS_DB_USER=aegis
AEGIS_DB_PASSWORD=your_password_here
```

### Configuration Files

#### Main Configuration
`config/aegis.yaml`:
```yaml
system:
  name: "AEGIS"
  version: "2.3"
  environment: "production"

network:
  api_port: 8005
  websocket_port: 8006
  p2p_port: 8080
  external_address: "your.domain.com"

security:
  jwt_secret: "your_jwt_secret"
  encryption_key: "your_encryption_key"
  enable_tls: true

database:
  host: "localhost"
  port: 5432
  name: "aegis"
  user: "aegis"
  password: "your_password"
```

## Security Setup

### TLS Configuration

For production deployments, configure TLS:

```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/aegis.key \
  -out /etc/ssl/certs/aegis.crt
```

### Authentication Setup

Configure JWT authentication:

```bash
# Generate JWT secret
openssl rand -base64 32 > /etc/aegis/jwt_secret

# Set permissions
chmod 600 /etc/aegis/jwt_secret
```

## Monitoring and Logging

### Log Configuration

Configure logging in `config/logging.yaml`:
```yaml
version: 1
formatters:
  standard:
    format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
handlers:
  file:
    class: logging.FileHandler
    filename: /var/log/aegis/system.log
    formatter: standard
loggers:
  aegis:
    level: INFO
    handlers: [file]
    propagate: false
```

### Monitoring Setup

For production monitoring, set up Prometheus and Grafana:

```bash
# Start monitoring stack
docker-compose -f monitoring/docker-compose.yml up -d

# Access Grafana
# http://localhost:3000
```

## Backup and Recovery

### Data Backup

Regular backup procedure:
```bash
# Backup database
pg_dump -h localhost -U aegis aegis > backup/aegis_$(date +%Y%m%d).sql

# Backup configuration
tar -czf backup/config_$(date +%Y%m%d).tar.gz /etc/aegis/

# Backup logs
tar -czf backup/logs_$(date +%Y%m%d).tar.gz /var/log/aegis/
```

### Disaster Recovery

Recovery procedure:
```bash
# Restore database
psql -h localhost -U aegis aegis < backup/aegis_20230101.sql

# Restore configuration
tar -xzf backup/config_20230101.tar.gz -C /

# Restart services
systemctl restart aegis
```

## Performance Tuning

### System Optimization

For optimal performance:

1. **Database Tuning**:
   ```bash
   # PostgreSQL configuration
   shared_buffers = 256MB
   effective_cache_size = 1GB
   maintenance_work_mem = 64MB
   ```

2. **Network Optimization**:
   ```bash
   # System limits
   ulimit -n 65536
   sysctl -w net.core.somaxconn=65535
   ```

3. **Memory Management**:
   ```bash
   # JVM settings (if using Java components)
   export JAVA_OPTS="-Xmx4g -Xms2g"
   ```

## Troubleshooting

### Common Issues

#### Startup Problems
```bash
# Check system logs
tail -f /var/log/aegis/system.log

# Verify dependencies
pip check

# Check port availability
netstat -tuln | grep -E "(8005|8006|8080)"
```

#### Network Issues
```bash
# Test connectivity
ping your.domain.com
curl -v http://localhost:8005/health

# Check firewall
iptables -L
```

#### Performance Issues
```bash
# Monitor system resources
htop
iotop
nethogs

# Check application metrics
curl http://localhost:8005/metrics
```

### Health Checks

Verify system health:
```bash
# API health check
curl -f http://localhost:8005/health

# WebSocket connectivity
websocat ws://localhost:8006/ws

# Database connectivity
psql -h localhost -U aegis aegis -c "SELECT 1;"
```

## Maintenance

### Regular Maintenance Tasks

1. **Daily**:
   - Check system logs
   - Verify backup completion
   - Monitor resource usage

2. **Weekly**:
   - Update dependencies
   - Rotate logs
   - Performance review

3. **Monthly**:
   - Security audit
   - Database maintenance
   - System optimization

### Update Procedure

For system updates:
```bash
# Stop services
systemctl stop aegis

# Backup current version
tar -czf backup/aegis_$(date +%Y%m%d).tar.gz /opt/aegis

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Start services
systemctl start aegis
```

## Production Checklist

Before going to production, ensure:

- [ ] TLS certificates configured
- [ ] Firewall rules set
- [ ] Backup procedures tested
- [ ] Monitoring configured
- [ ] Security audit completed
- [ ] Performance tuning applied
- [ ] Documentation updated
- [ ] Disaster recovery plan tested

This deployment guide provides a comprehensive approach to deploying AEGIS in various environments while maintaining security, performance, and reliability.