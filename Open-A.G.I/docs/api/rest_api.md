# REST API Documentation

## Overview

The Open-A.G.I REST API provides HTTP-based access to system functionality. It enables external applications to interact with the distributed intelligence network.

## Base URL

```
http://localhost:8080/api/v1
```

## Authentication

All API endpoints require authentication using JWT tokens generated from node cryptographic keys.

```bash
# Generate authentication token
curl -X POST "http://localhost:8080/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "node_123",
    "public_key": "<base64_encoded_public_key>"
  }'
```

## API Endpoints

### Node Management

#### Get Node Status
```
GET /status
```
Retrieve the current status of the node.

**Response:**
```json
{
  "node_id": "node_123",
  "status": "running",
  "version": "1.0.0",
  "uptime": 3600,
  "peers": 5,
  "consensus_state": "active"
}
```

#### Get Node Information
```
GET /node/{node_id}
```
Retrieve detailed information about a specific node.

**Response:**
```json
{
  "node_id": "node_123",
  "public_key": "<base64_encoded_public_key>",
  "address": "node123.onion",
  "joined_at": "2023-01-01T00:00:00Z",
  "last_seen": "2023-01-01T01:00:00Z",
  "score": 85.5
}
```

### Network Operations

#### Get Network Statistics
```
GET /network/stats
```
Retrieve network-wide statistics.

**Response:**
```json
{
  "total_nodes": 25,
  "active_nodes": 23,
  "byzantine_threshold": 8,
  "average_score": 78.3,
  "total_messages": 12500,
  "network_health": 0.95
}
```

#### List Connected Peers
```
GET /network/peers
```
List all currently connected peers.

**Response:**
```json
{
  "peers": [
    {
      "node_id": "node_456",
      "address": "node456.onion",
      "connection_time": 1200,
      "last_message": "2023-01-01T00:59:00Z"
    }
  ]
}
```

### Consensus Operations

#### Submit Proposal
```
POST /consensus/proposal
```
Submit a proposal for consensus.

**Request:**
```json
{
  "proposal_id": "proposal_001",
  "data": {
    "action": "update_parameter",
    "parameter": "learning_rate",
    "value": 0.01
  },
  "timestamp": "2023-01-01T00:00:00Z"
}
```

**Response:**
```json
{
  "proposal_id": "proposal_001",
  "status": "submitted",
  "consensus_round": 15
}
```

#### Get Proposal Status
```
GET /consensus/proposal/{proposal_id}
```
Get the status of a specific proposal.

**Response:**
```json
{
  "proposal_id": "proposal_001",
  "status": "accepted",
  "consensus_round": 15,
  "votes": {
    "prepare": 20,
    "commit": 19
  },
  "executed_at": "2023-01-01T00:05:00Z"
}
```

### Security Operations

#### Get Security Status
```
GET /security/status
```
Retrieve current security status and metrics.

**Response:**
```json
{
  "intrusion_attempts": 5,
  "blocked_addresses": 3,
  "encryption_status": "active",
  "last_security_event": "2023-01-01T00:30:00Z"
}
```

#### Report Security Incident
```
POST /security/incident
```
Report a security incident.

**Request:**
```json
{
  "incident_type": "suspicious_activity",
  "description": "Unusual network traffic pattern",
  "evidence": "<base64_encoded_evidence>",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

**Response:**
```json
{
  "incident_id": "incident_001",
  "status": "reported",
  "investigation_status": "pending"
}
```

### Monitoring

#### Get System Metrics
```
GET /monitoring/metrics
```
Retrieve system performance metrics.

**Response:**
```json
{
  "cpu_usage": 45.2,
  "memory_usage": 65.8,
  "disk_usage": 32.1,
  "network_in": 1024000,
  "network_out": 512000,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### Get Recent Logs
```
GET /monitoring/logs?level=WARNING&limit=50
```
Retrieve recent system logs.

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2023-01-01T00:05:00Z",
      "level": "WARNING",
      "message": "High network latency detected",
      "component": "p2p_network"
    }
  ]
}
```

## Error Responses

All error responses follow a standard format:

```json
{
  "error": {
    "code": 404,
    "message": "Node not found",
    "details": "The specified node_id does not exist in the network"
  }
}
```

### Common Error Codes

- **400**: Bad Request - Invalid request parameters
- **401**: Unauthorized - Missing or invalid authentication
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource does not exist
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Unexpected server error
- **503**: Service Unavailable - System temporarily unavailable

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 1000 requests per hour per IP
- 100 requests per minute per IP
- Exceeding limits results in 429 Too Many Requests responses

## WebSocket Upgrade

Some endpoints support WebSocket upgrades for real-time updates:

```
GET /monitoring/stream
Connection: Upgrade
Upgrade: websocket
```

## Examples

### Python Example
```python
import requests
import json

# Get node status
response = requests.get('http://localhost:8080/api/v1/status')
if response.status_code == 200:
    status = response.json()
    print(f"Node status: {status['status']}")
```

### JavaScript Example
```javascript
// Get network statistics
fetch('http://localhost:8080/api/v1/network/stats')
  .then(response => response.json())
  .then(data => {
    console.log(`Total nodes: ${data.total_nodes}`);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```