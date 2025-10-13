# Open-A.G.I Integration Guide

This guide explains how to integrate Open-A.G.I's infrastructure and deployment capabilities into the AEGIS system while preserving AEGIS's unique Metatron 13-node consciousness-aware architecture.

## Overview

The integration focuses on adopting Open-A.G.I's mature operational infrastructure while maintaining AEGIS's distinctive user experience and consciousness-aware AI engine. This includes:

1. CI/CD pipelines and multi-OS build automation
2. Multi-arch Docker containerization
3. SBOM generation and image signing
4. Deployment orchestration
5. Monitoring and metrics collection
6. P2P/TOR integration
7. Resource management and fault tolerance

## Architecture

The integration follows a modular adapter pattern:

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   AEGIS Core    │◄──►│  Adapter Layer   │◄──►│  Open-A.G.I Core   │
│ (Metatron 13-   │    │ (aegis-integration│    │ (Infrastructure &  │
│  node network)  │    │  /deploy, cross_  │    │  Deployment)       │
│                 │    │  system_comm,     │    │                 │
│                 │    │  visualization_   │    │                 │
│                 │    │  tools)           │    │                 │
└─────────────────┘    └──────────────────┘    └────────────────────┘
```

## Components

### 1. Deployment Adapter (`aegis-integration/deploy/deployment_adapter.py`)

The deployment adapter integrates Open-A.G.I's `deployment_orchestrator.py` with AEGIS's `unified_coordinator.py`.

#### Key Features:
- Node deployment and lifecycle management
- Multi-node network orchestration
- Status reporting and health checks

#### Usage:
```python
from aegis_integration.deploy.deployment_adapter import initialize_deployment_adapter, AEGISNodeConfig

# Initialize the adapter
adapter = initialize_deployment_adapter({
    "open_agi": {
        "orchestration_method": "docker",
        "default_image": "realdanig/aegis:latest"
    }
})

# Create node configurations
main_node = AEGISNodeConfig(
    node_id="metatron-main",
    node_type="main",
    host="localhost",
    p2p_port=8080,
    api_port=8003,
    web_port=8081,
    tor_enabled=True
)

# Deploy the network
result = await adapter.deploy_metatron_network([main_node, worker_node_1, worker_node_2])
```

### 2. TOR Adapter (`cross_system_comm/tor_adapter.py`)

The TOR adapter integrates Open-A.G.I's `tor_integration.py` with AEGIS's communication systems.

#### Key Features:
- Onion service creation and management
- TOR network status monitoring
- Security level configuration
- Circuit rotation

#### Usage:
```python
from cross_system_comm.tor_adapter import initialize_tor_adapter, AEGISTorConfig

# Initialize the adapter
config = AEGISTorConfig(
    control_port=9051,
    socks_port=9050,
    security_level="HIGH"
)

adapter = initialize_tor_adapter(config)

# Create onion services
api_onion = await adapter.create_onion_service(8003)  # API port
web_onion = await adapter.create_onion_service(8081)  # Web UI port
```

### 3. Metrics Bridge (`visualization_tools/metrics_bridge.py`)

The metrics bridge integrates Open-A.G.I's `monitoring_dashboard.py` and `metrics_collector.py` with AEGIS's visualization tools.

#### Key Features:
- System and network metrics collection
- Metatron consciousness metrics
- WebSocket broadcasting
- Prometheus export

#### Usage:
```python
from visualization_tools.metrics_bridge import initialize_metrics_bridge, AEGISMetricsConfig

# Initialize the bridge
config = AEGISMetricsConfig(
    collection_interval=10,
    enable_consciousness_metrics=True,
    websocket_broadcast=True
)

bridge = initialize_metrics_bridge(config)

# Start metrics collection
await bridge.start_collection()

# Register Metatron node metrics
bridge.register_metatron_metric("metatron-main", "consciousness_phi", 0.75)
```

## CI/CD Integration

### GitHub Actions Workflow (`.github/workflows/ci.yml`)

The workflow includes:
- Multi-OS testing matrix (Ubuntu, Windows, macOS)
- Multiple Python versions (3.9, 3.10, 3.11)
- Docker multi-arch builds (AMD64, ARM64)
- SBOM generation and vulnerability scanning
- Image signing with cosign
- Deployment validation

### Docker Configuration (`deploy/Dockerfile`)

The Dockerfile provides:
- Multi-stage build process
- Security hardening
- Environment variable standardization
- Health check endpoints
- Non-root user execution

### Development Environment (`deploy/docker-compose.dev.yml`)

The development compose file includes:
- Metatron main node
- Worker nodes (configurable)
- TOR proxy service
- Redis for caching
- Prometheus for metrics
- Grafana for visualization
- ELK stack for logging
- n8n for workflow automation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-optional.txt
```

### 2. Run Development Environment

```bash
cd deploy
docker-compose -f docker-compose.dev.yml up
```

### 3. Initialize Adapters

```python
# Initialize deployment adapter
from aegis_integration.deploy.deployment_adapter import initialize_deployment_adapter
deployment_adapter = initialize_deployment_adapter()

# Initialize TOR adapter
from cross_system_comm.tor_adapter import initialize_tor_adapter
tor_adapter = initialize_tor_adapter()

# Initialize metrics bridge
from visualization_tools.metrics_bridge import initialize_metrics_bridge
metrics_bridge = initialize_metrics_bridge()
```

### 4. Deploy Metatron Network

```python
# Create node configurations
node_configs = [
    AEGISNodeConfig(node_id="metatron-main", node_type="main", ...),
    AEGISNodeConfig(node_id="metatron-worker-1", node_type="worker", ...),
    # ... more nodes
]

# Deploy network
result = await deployment_adapter.deploy_metatron_network(node_configs)
```

## Configuration

### Environment Variables

The system uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `TOR_ENABLED` | Enable TOR integration | `true` |
| `NODE_TYPE` | Node type (main/worker) | `worker` |
| `P2P_PORT` | P2P communication port | `8080` |
| `API_PORT` | API server port | `8003` |
| `WEB_PORT` | Web UI port | `8081` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Configuration Files

1. **TOR Configuration** (`deploy/torrc`): TOR network settings
2. **Docker Configuration** (`deploy/Dockerfile`): Container build instructions
3. **Development Environment** (`deploy/docker-compose.dev.yml`): Local development setup
4. **Metrics Configuration** (`visualization_tools/metrics_bridge.py`): Metrics collection settings

## Security Considerations

### 1. Image Signing
All Docker images are signed using cosign for supply chain security.

### 2. SBOM Generation
Software Bill of Materials is generated for each build to track dependencies.

### 3. TOR Anonymity
TOR controls are exposed through the UI with role-based access to protect anonymity.

### 4. Secret Management
CI secrets are managed through GitHub's secret store. Never commit private keys.

## Troubleshooting

### Common Issues

1. **Docker Build Failures**
   - Ensure all dependencies are listed in requirements files
   - Check Dockerfile for correct paths and commands

2. **TOR Connection Issues**
   - Verify TOR is running and accessible
   - Check firewall settings for TOR ports (9050, 9051)

3. **Metrics Collection Failures**
   - Ensure required system libraries are installed
   - Check permissions for system monitoring

### Logs and Monitoring

- Application logs: `/logs/` directory
- TOR logs: `/var/log/tor/` in container
- Docker logs: `docker logs <container_name>`
- Prometheus metrics: `http://localhost:9090`
- Grafana dashboard: `http://localhost:3000`

## Future Enhancements

### Planned Features

1. **Kubernetes Deployment**: Add Helm charts for Kubernetes deployment
2. **Advanced Monitoring**: Integrate with Grafana dashboards for Metatron metrics
3. **Auto-scaling**: Implement automatic node scaling based on load
4. **Enhanced Security**: Add more sophisticated TOR controls and privacy features
5. **Performance Optimization**: Integrate Open-A.G.I's performance optimizer

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add tests
5. Submit a pull request

## API Reference

### DeploymentAdapter

#### Methods
- `deploy_node(node_config: AEGISNodeConfig) -> bool`
- `stop_node(node_id: str) -> bool`
- `get_node_status(node_id: str) -> Dict[str, Any]`
- `update_node(node_id: str, config_updates: Dict[str, Any]) -> bool`
- `deploy_metatron_network(node_configs: List[AEGISNodeConfig]) -> Dict[str, Any]`
- `get_network_status() -> Dict[str, Any]`

### TorAdapter

#### Methods
- `initialize() -> bool`
- `create_onion_service(port: int, target_port: int = None) -> Optional[str]`
- `get_network_status() -> Dict[str, Any]`
- `get_onion_address(port: int) -> Optional[str]`
- `rotate_circuit() -> bool`
- `set_security_level(security_level: str) -> bool`
- `disconnect() -> bool`

### MetricsBridge

#### Methods
- `set_metric_value(name: str, value: Any, labels: Dict[str, str] = None)`
- `get_metric_value(name: str) -> Any`
- `get_all_metrics() -> Dict[str, Any]`
- `get_metatron_network_metrics() -> Dict[str, Any]`
- `start_collection()`
- `stop_collection()`
- `export_metrics_prometheus() -> str`

## License

This integration is part of the AEGIS project and follows the same licensing terms.