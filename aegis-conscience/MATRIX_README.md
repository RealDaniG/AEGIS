# AEGIS-Conscience Network Matrix Connectivity

This module implements full mesh connectivity between all nodes in the AEGIS-Conscience Network, ensuring that every node maintains direct connections to all other nodes in the network.

## 🌐 Overview

The matrix connectivity system provides:
- **Full Mesh Topology**: Every node connects directly to every other node
- **Automatic Discovery**: Nodes automatically discover and connect to peers
- **Connection Management**: Continuous monitoring and maintenance of connections
- **Visualization**: Real-time visualization of network topology
- **Monitoring**: Tools for monitoring matrix connectivity status

## 📁 Directory Structure

```
aegis-conscience/
├── network/
│   └── node_matrix.py          # Node matrix manager implementation
├── tools/
│   └── matrix_visualizer.py    # Matrix visualization tool
├── matrix_demo.py              # Complete matrix demonstration
├── matrix_monitor.py           # Real-time matrix monitoring
├── matrix_status.py            # Simple matrix status checker
├── generate_matrix_example.py  # Example data generator
├── test_matrix_connectivity.py # Unit tests
├── MATRIX_CONNECTIVITY_GUIDE.md # Detailed usage guide
├── MATRIX_SUMMARY.md           # Implementation summary
└── MATRIX_README.md            # This file
```

## 🚀 Quick Start

### 1. Generate Example Data
```bash
python generate_matrix_example.py
```

### 2. Visualize the Matrix
```bash
python tools/matrix_visualizer.py
```

### 3. Check Matrix Status
```bash
python matrix_status.py
```

### 4. Run the Full Demo
```bash
python matrix_demo.py
```

## 🛠️ Core Components

### NodeMatrixManager
Located in `network/node_matrix.py`, this class manages the full mesh connectivity:
- Discovers nodes in the network
- Maintains connections between all nodes
- Updates and broadcasts matrix information
- Provides network topology data

### Integration with AEGISNode
The main node class in `main.py` integrates with NodeMatrixManager to automatically maintain matrix connectivity.

### Visualization Tools
The `tools/matrix_visualizer.py` provides comprehensive visualization of the connection matrix.

## 📊 Visualization Features

### Text-Based Matrix Diagram
```
Node           node-1         node-2         node-3
node-1         ●              ✓              ✓
node-2         ✓              ●              ✓
node-3         ✓              ✓              ●
```

### Connection Status Legend
- ● = Self (node connecting to itself)
- ✓ = Connected
- ✗ = Not Connected

### Network Statistics
- Total nodes count
- Connection counts per node
- Network connectivity percentage
- Most/least connected nodes

## 🧪 Testing

Run the unit tests:
```bash
python test_matrix_connectivity.py
```

## 🔍 Monitoring

### Real-Time Monitor
```bash
python matrix_monitor.py
```

### Status Checker
```bash
python matrix_status.py
```

## 📚 Documentation

- [MATRIX_CONNECTIVITY_GUIDE.md](MATRIX_CONNECTIVITY_GUIDE.md) - Detailed usage guide
- [MATRIX_SUMMARY.md](MATRIX_SUMMARY.md) - Implementation summary

## 🏗️ Docker Deployment

The matrix connectivity works with the existing Docker setup:
```bash
docker-compose up -d
```

## ⚙️ Configuration

The matrix system is automatically enabled when using the AEGISNode class. No additional configuration is required.

## 🔧 Troubleshooting

### Common Issues
1. **Nodes not connecting**: Check firewall settings and port availability
2. **Matrix not forming**: Verify node discovery is working correctly
3. **Visualization issues**: Ensure matrix data files are properly formatted

### Logs and Debugging
Enable debug logging to troubleshoot matrix connectivity issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

The full mesh topology is optimized for networks of 10-50 nodes. For larger networks, consider implementing partial mesh or hierarchical connectivity.

## 🔒 Security

- All connections use encrypted communication
- Timing-protected message sending prevents timing analysis
- Rate limiting prevents message flooding
- Node authentication ensures only trusted nodes connect

## 📤 API Reference

### NodeMatrixManager Methods
- `add_known_node(node_info)`: Add a known node to the matrix
- `remove_known_node(node_id)`: Remove a node from the matrix
- `start_matrix_management()`: Start maintaining matrix connectivity
- `stop_matrix_management()`: Stop matrix management
- `get_network_topology()`: Get current network topology information
- `broadcast_matrix_update()`: Broadcast matrix status to all nodes

## 🤝 Integration

The matrix system integrates seamlessly with:
- P2P network layer
- TOR onion services
- Dashboard and monitoring systems
- Consensus mechanisms
- Knowledge sharing protocols

## 📝 Example Use Cases

1. **Research Networks**: Full connectivity for collaborative research
2. **High Availability Systems**: Redundant connections for critical applications
3. **Real-time Collaboration**: Low-latency communication between all nodes
4. **Distributed Computing**: Efficient task distribution across all nodes

## 🆘 Support

For issues with the matrix connectivity system, please check:
1. The documentation in [MATRIX_CONNECTIVITY_GUIDE.md](MATRIX_CONNECTIVITY_GUIDE.md)
2. The implementation summary in [MATRIX_SUMMARY.md](MATRIX_SUMMARY.md)
3. The example scripts and tests for usage patterns

## 📄 License

This implementation is part of the AEGIS-Conscience Network and follows the same licensing terms as the main project.