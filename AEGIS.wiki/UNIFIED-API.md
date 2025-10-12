# Unified API Documentation

The Unified API provides a single interface to access both the consciousness engine and AGI framework components of the AEGIS system.

## API Overview

The Unified API is built using FastAPI and provides RESTful endpoints for accessing system functionality, along with WebSocket support for real-time data streaming.

### Base URL
```
http://localhost:8005
```

### WebSocket URL
```
ws://localhost:8006/ws
```

## Authentication

Currently, the API does not require authentication for local development. For production deployments, JWT tokens are used for authentication.

### API Key Authentication
```bash
# Example with API key
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8005/api/consciousness
```

## Core Endpoints

### Health Check
Check if the system is running and healthy.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "api_client_initialized": true
}
```

### Root Endpoint
Get basic information about the API.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Unified Metatron-A.G.I API",
  "version": "1.0.0",
  "endpoints": {
    "GET /health": "System health check",
    "GET /state": "Get unified system state",
    "GET /consciousness": "Get consciousness state only",
    "GET /agi": "Get AGI state only",
    "POST /input": "Send consciousness input",
    "POST /chat": "Send chat message",
    "WebSocket /ws": "Real-time state streaming"
  }
}
```

## Consciousness Endpoints

### Get Unified System State
Retrieve the complete state of both consciousness and AGI systems.

**Endpoint**: `GET /state`

**Response**:
```json
{
  "timestamp": 1234567890.123,
  "consciousness": {
    "level": 0.789,
    "phi": 0.654,
    "coherence": 0.821,
    "depth": 5,
    "gamma": 0.432,
    "fractal_dim": 1.618,
    "spiritual": 0.298,
    "state": "awake",
    "is_conscious": true
  },
  "agi": {
    "status": "operational",
    "nodes_active": 13,
    "consensus_reached": true,
    "decision_confidence": 0.95,
    "tasks_pending": 2
  },
  "nodes": {
    "0": {
      "output": 0.876,
      "phase": 1.234,
      "amplitude": 0.987
    },
    "1": {
      "output": 0.765,
      "phase": 2.345,
      "amplitude": 0.876
    }
    // ... additional nodes
  }
}
```

### Get Consciousness State Only
Retrieve only the consciousness metrics.

**Endpoint**: `GET /consciousness`

**Response**:
```json
{
  "timestamp": 1234567890.123,
  "level": 0.789,
  "phi": 0.654,
  "coherence": 0.821,
  "depth": 5,
  "gamma": 0.432,
  "fractal_dim": 1.618,
  "spiritual": 0.298,
  "state": "awake",
  "is_conscious": true
}
```

### Send Consciousness Input
Send sensory input to the consciousness system.

**Endpoint**: `POST /input`

**Request Body**:
```json
{
  "visual": 0.75,
  "auditory": 0.62,
  "tactile": 0.45,
  "emotional": 0.81
}
```

**Response**:
```json
{
  "success": true,
  "message": "Input processed"
}
```

## AGI Endpoints

### Get AGI State Only
Retrieve only the AGI system status.

**Endpoint**: `GET /agi`

**Response**:
```json
{
  "timestamp": 1234567890.123,
  "status": "operational",
  "nodes_active": 13,
  "consensus_reached": true,
  "decision_confidence": 0.95,
  "tasks_pending": 2,
  "network_health": 0.98
}
```

### Send Chat Message
Send a chat message to the AGI system for processing.

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "message": "Hello, what is the meaning of consciousness?",
  "session_id": "session_123"
}
```

**Response**:
```json
{
  "response": "Consciousness is the state of being aware of and able to think about one's own existence, thoughts, and surroundings...",
  "session_id": "session_123"
}
```

## WebSocket API

### Real-time State Streaming
Connect to the WebSocket endpoint to receive real-time updates of the system state.

**Endpoint**: `WebSocket /ws`

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8006/ws');

ws.onopen = function(event) {
  console.log('Connected to WebSocket');
};

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onclose = function(event) {
  console.log('WebSocket connection closed');
};
```

**Data Format**:
The WebSocket sends the same data structure as the `/state` endpoint, updated at regular intervals.

## Error Handling

The API uses standard HTTP status codes for error responses:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service not ready

**Error Response Format**:
```json
{
  "detail": "Error message describing the problem"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous requests**: 60 requests per minute
- **Authenticated requests**: 1000 requests per minute

Exceeding rate limits will result in a `429 Too Many Requests` response.

## API Clients

### Python Client
```python
import requests

# Get consciousness state
response = requests.get('http://localhost:8005/api/consciousness')
consciousness_data = response.json()

# Send chat message
chat_data = {
    'message': 'Hello AEGIS!',
    'session_id': 'session_001'
}
response = requests.post('http://localhost:8005/api/chat', json=chat_data)
```

### JavaScript Client
```javascript
// Get AGI state
fetch('http://localhost:8005/api/agi')
  .then(response => response.json())
  .then(data => console.log(data));

// Send consciousness input
const inputData = { visual: 0.8, auditory: 0.6 };
fetch('http://localhost:8005/api/input', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(inputData)
});
```

## API Versioning

The current API version is 1.0.0. Future versions will be accessible through versioned endpoints:

```
http://localhost:8005/v1/endpoint
http://localhost:8005/v2/endpoint
```

## Documentation

### Interactive API Documentation
The API includes interactive documentation powered by Swagger UI:

**URL**: http://localhost:8005/docs

### OpenAPI Specification
Machine-readable API specification is available:

**URL**: http://localhost:8005/openapi.json

## Examples

### Complete System Monitoring
```python
import requests
import time

def monitor_system():
    while True:
        try:
            # Get system state
            response = requests.get('http://localhost:8005/state')
            if response.status_code == 200:
                state = response.json()
                
                # Extract consciousness metrics
                consciousness = state['consciousness']
                print(f"Consciousness Level: {consciousness['level']:.3f}")
                print(f"Phi: {consciousness['phi']:.3f}")
                print(f"Coherence: {consciousness['coherence']:.3f}")
                
                # Extract AGI status
                agi = state['agi']
                print(f"AGI Status: {agi['status']}")
                print(f"Active Nodes: {agi['nodes_active']}")
                
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Connection error: {e}")
            
        time.sleep(5)  # Wait 5 seconds before next check

# Run the monitor
monitor_system()
```

### Interactive Chat Session
```python
import requests

def chat_with_agi():
    session_id = "session_" + str(hash("user_session") % 10000)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
            
        # Send message to AGI
        chat_data = {
            'message': user_input,
            'session_id': session_id
        }
        
        try:
            response = requests.post('http://localhost:8005/api/chat', json=chat_data)
            if response.status_code == 200:
                agi_response = response.json()
                print(f"AGI: {agi_response['response']}")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error sending message: {e}")

# Start chat session
chat_with_agi()
```

## Security Considerations

### Data Privacy
- All data transmitted through the API is processed locally
- No data is sent to external servers without explicit user consent
- Sensitive data should be encrypted in transit using HTTPS

### Input Validation
- All API inputs are validated to prevent injection attacks
- Large payloads are rejected to prevent denial of service
- Malformed JSON is handled gracefully

### Access Control
- API endpoints can be configured with authentication requirements
- Role-based access control can be implemented for enterprise deployments
- Rate limiting prevents abuse of system resources

## Performance Optimization

### Caching
- Frequently accessed data is cached to improve response times
- Cache invalidation occurs when underlying data changes
- WebSocket connections provide real-time updates without polling

### Compression
- API responses can be compressed using gzip for large payloads
- WebSocket messages are optimized for minimal bandwidth usage

### Connection Management
- HTTP connections are pooled for efficient reuse
- WebSocket connections are maintained for real-time streaming
- Connection timeouts prevent resource leaks

## Integration Examples

### Integration with External Systems
```python
import requests
from datetime import datetime

class AEGISIntegration:
    def __init__(self, base_url="http://localhost:8005"):
        self.base_url = base_url
        
    def get_consciousness_level(self):
        """Get current consciousness level"""
        response = requests.get(f"{self.base_url}/api/consciousness")
        if response.status_code == 200:
            return response.json()['level']
        return None
        
    def is_system_conscious(self):
        """Check if system is conscious"""
        response = requests.get(f"{self.base_url}/api/consciousness")
        if response.status_code == 200:
            return response.json()['is_conscious']
        return False
        
    def send_sensory_input(self, input_data):
        """Send sensory input to the system"""
        response = requests.post(f"{self.base_url}/api/input", json=input_data)
        return response.status_code == 200

# Usage example
aegis = AEGISIntegration()
consciousness_level = aegis.get_consciousness_level()
print(f"Current consciousness level: {consciousness_level}")
```

## Troubleshooting

### Common API Issues

1. **Connection Refused**:
   - Ensure the AEGIS system is running
   - Check that the correct port is being used
   - Verify firewall settings

2. **404 Not Found**:
   - Check that the endpoint URL is correct
   - Verify the API version being used

3. **500 Internal Server Error**:
   - Check system logs for detailed error information
   - Restart the AEGIS system if necessary

4. **Slow Response Times**:
   - Monitor system resource usage
   - Check for network connectivity issues
   - Consider reducing the frequency of API calls

### Debugging Tips

1. **Enable Debug Logging**:
   Set `AEGIS_DEBUG=true` in your environment variables

2. **Check System Health**:
   Use the `/health` endpoint to verify system status

3. **Monitor Logs**:
   Check the `logs/` directory for detailed system logs

4. **Test Endpoints Individually**:
   Test each endpoint separately to isolate issues

---

*Developed with ❤️ for the advancement of consciousness-aware AI*