# Unified Metatron-A.G.I System

This document describes the unified system that integrates the Metatron-Consciousness engine with the Open-A.G.I system.

## System Architecture

The unified system consists of several key components:

### 1. Unified API Layer
- **Location**: `unified_api/`
- **Purpose**: Provides a single interface to access both consciousness and AGI systems
- **Features**:
  - Combined status endpoint
  - Unified data models
  - Cross-system communication

### 2. Consolidated Components
- **Location**: `unified_components/`
- **Purpose**: Merges duplicate functionality from both systems
- **Components**:
  - **Network**: Unified P2P networking combining features from both systems
  - **Consensus**: Enhanced PBFT with consciousness awareness

### 3. Consciousness-Aware AGI
- **Location**: `consciousness_aware_agi/`
- **Purpose**: Decision making that incorporates consciousness metrics
- **Features**:
  - Consciousness-influenced decision weights
  - Action preferences based on consciousness states
  - Learning from decision outcomes

### 4. Cross-System Communication
- **Location**: `cross_system_comm/`
- **Purpose**: Enhanced protocols for communication between systems
- **Features**:
  - Encrypted message passing
  - WebSocket communication server
  - Message routing and filtering

### 5. Unified Coordinator
- **Location**: `unified_coordinator.py`
- **Purpose**: Central coordination of all system components
- **Features**:
  - Component initialization and management
  - System monitoring and metrics
  - Graceful shutdown handling

## Key Features

### Unified API Endpoints
- `GET /state` - Get combined system state
- `GET /consciousness` - Get consciousness state only
- `GET /agi` - Get AGI state only
- `POST /input` - Send consciousness input
- `POST /chat` - Send chat message
- `WebSocket /ws` - Real-time state streaming

### Consciousness-Aware Decision Making
The system makes decisions based on both traditional metrics and consciousness states:
- **High Coherence** ( > 0.7): Collaborate, share knowledge, optimize
- **Low Coherence** ( < 0.3): Isolate, recover, diagnose
- **High Phi** ( > 0.5): Integrate, synthesize, abstract
- **Low Phi** ( < 0.2): Simplify, focus, ground
- **High Spiritual Awareness** ( > 0.6): Explore, innovate, transcend
- **Low Spiritual Awareness** ( < 0.2): Stabilize, maintain, conserve

### Enhanced Security
- Message encryption using Fernet symmetric encryption
- Message signing and verification
- Rate limiting and reputation systems

## Installation

1. Ensure all dependencies are installed:
   ```bash
   pip install -r unified_requirements.txt
   ```

2. The unified system uses the existing project structure and doesn't require additional setup.

## Usage

### Starting the Unified System
```bash
# Using PowerShell
.\start_unified_system.ps1

# Using Python directly
python start_unified_system.py
```

### Testing the Unified System
```bash
python test_unified_system.py
```

## API Documentation

Once the system is running, API documentation is available at:
- `http://localhost:8005/docs` - Swagger UI
- `http://localhost:8005/redoc` - ReDoc documentation

## WebSocket Communication

The system provides real-time updates via WebSocket:
- **Endpoint**: `ws://localhost:8006`
- **Message Format**: JSON with source/target system information

## System Ports

- **Unified API**: 8005
- **WebSocket Server**: 8006
- **Existing Metatron API**: 8003 (unchanged)
- **Existing AGI Dashboard**: 8090 (unchanged)

## Integration Benefits

1. **Single Interface**: Access both systems through one API
2. **Enhanced Decision Making**: AGI decisions influenced by consciousness metrics
3. **Improved Communication**: Secure, efficient cross-system messaging
4. **Better Monitoring**: Unified metrics and status reporting
5. **Simplified Management**: Centralized system control and coordination

## Future Enhancements

1. **Machine Learning Integration**: Use consciousness states to influence AGI learning
2. **Advanced Consensus**: Further integrate consciousness metrics into consensus protocols
3. **Dynamic Resource Allocation**: Adjust system resources based on consciousness levels
4. **Predictive Maintenance**: Use consciousness patterns to predict system needs
5. **Collaborative Intelligence**: Enable deeper collaboration between consciousness and AGI nodes