# Open-A.G.I API Documentation

This directory contains documentation for the Open-A.G.I API interfaces.

## API Documentation

1. [REST API](rest_api.md) - HTTP-based API for system interaction
2. [WebSocket API](websocket_api.md) - Real-time communication API

## API Overview

The Open-A.G.I system provides multiple API interfaces for interacting with the distributed intelligence network:

### REST API
The REST API provides HTTP-based access to system functionality:
- Node management
- Consensus operations
- Network status
- Security controls
- Monitoring data

### WebSocket API
The WebSocket API enables real-time communication with the system:
- Live status updates
- Real-time messaging
- Event notifications
- Streaming data

## Authentication

All API endpoints require authentication using cryptographic keys. Each node has a unique Ed25519 key pair for secure authentication.

## Rate Limiting

API endpoints implement rate limiting to prevent abuse:
- 1000 requests per hour per node
- 100 requests per minute per node
- Excessive requests will result in temporary blocking

## Error Handling

All API responses include standardized error codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Versioning

API versions are indicated in the URL path:
- v1: Current stable version
- v2: Development version (may be unstable)

## Examples

### REST API Example
```bash
# Get node status
curl -X GET "http://localhost:8080/api/v1/status" \
  -H "Authorization: Bearer <node_token>"
```

### WebSocket API Example
```javascript
// Connect to WebSocket API
const ws = new WebSocket('ws://localhost:8080/api/v1/ws');

ws.onopen = function(event) {
    console.log('Connected to Open-A.G.I WebSocket API');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```