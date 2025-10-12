# WebSocket API Documentation

## Overview

The Open-A.G.I WebSocket API provides real-time, bidirectional communication between clients and the distributed intelligence network. It enables live updates, event notifications, and streaming data.

## Connection

### WebSocket URL
```
ws://localhost:8080/api/v1/ws
```

### Authentication
WebSocket connections require authentication with a JWT token obtained from the REST API.

```javascript
// Connect with authentication
const token = 'your_jwt_token';
const ws = new WebSocket(`ws://localhost:8080/api/v1/ws?token=${token}`);
```

## Connection Lifecycle

### Connection Establishment
```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws?token=your_token');

ws.onopen = function(event) {
    console.log('Connected to Open-A.G.I WebSocket API');
    
    // Subscribe to events after connection
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'network_events'
    }));
};
```

### Connection Closure
```javascript
ws.onclose = function(event) {
    console.log('WebSocket connection closed');
    console.log('Code:', event.code);
    console.log('Reason:', event.reason);
};
```

### Error Handling
```javascript
ws.onerror = function(event) {
    console.error('WebSocket error:', event);
};
```

## Message Format

All WebSocket messages use JSON format with a standard structure:

```json
{
  "type": "message_type",
  "data": {},
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Channels

### Network Events
Subscribe to network-wide events and updates.

```javascript
// Subscribe to network events
ws.send(JSON.stringify({
    "type": "subscribe",
    "channel": "network_events"
}));
```

**Events:**
- `node_joined`: New node joined the network
- `node_left`: Node left the network
- `network_partition`: Network partition detected
- `consensus_reached`: Consensus decision reached

### Consensus Events
Subscribe to consensus-related events.

```javascript
// Subscribe to consensus events
ws.send(JSON.stringify({
    "type": "subscribe",
    "channel": "consensus_events"
}));
```

**Events:**
- `proposal_submitted`: New proposal submitted
- `consensus_phase`: Consensus phase change
- `decision_executed`: Consensus decision executed
- `view_change`: Consensus view change

### Security Events
Subscribe to security-related events.

```javascript
// Subscribe to security events
ws.send(JSON.stringify({
    "type": "subscribe",
    "channel": "security_events"
}));
```

**Events:**
- `intrusion_detected`: Security intrusion detected
- `attack_blocked`: Attack blocked by security system
- `certificate_expired`: Node certificate expired
- `suspicious_activity`: Suspicious network activity

### Monitoring Events
Subscribe to system monitoring events.

```javascript
// Subscribe to monitoring events
ws.send(JSON.stringify({
    "type": "subscribe",
    "channel": "monitoring_events"
}));
```

**Events:**
- `metric_update`: System metric update
- `alert_raised`: Alert raised
- `performance_degradation`: Performance degradation detected
- `resource_exhausted`: System resource exhausted

## Message Types

### Control Messages

#### Subscribe
Subscribe to a channel for real-time updates.

```json
{
  "type": "subscribe",
  "channel": "network_events"
}
```

#### Unsubscribe
Unsubscribe from a channel.

```json
{
  "type": "unsubscribe",
  "channel": "network_events"
}
```

#### Ping
Send a ping to test connection.

```json
{
  "type": "ping"
}
```

#### Pong
Response to a ping message.

```json
{
  "type": "pong"
}
```

### Data Messages

#### Network Event
```json
{
  "type": "network_event",
  "event": "node_joined",
  "data": {
    "node_id": "node_123",
    "address": "node123.onion",
    "timestamp": "2023-01-01T00:00:00Z"
  },
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### Consensus Event
```json
{
  "type": "consensus_event",
  "event": "decision_executed",
  "data": {
    "proposal_id": "proposal_001",
    "decision": {
      "action": "update_parameter",
      "parameter": "learning_rate",
      "value": 0.01
    },
    "executed_at": "2023-01-01T00:05:00Z"
  },
  "timestamp": "2023-01-01T00:05:00Z"
}
```

#### Security Event
```json
{
  "type": "security_event",
  "event": "intrusion_detected",
  "data": {
    "attack_type": "ddos",
    "source_ip": "192.168.1.100",
    "blocked": true,
    "severity": "high"
  },
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### Monitoring Event
```json
{
  "type": "monitoring_event",
  "event": "metric_update",
  "data": {
    "metric": "cpu_usage",
    "value": 85.2,
    "threshold": 80.0,
    "status": "warning"
  },
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Client Examples

### JavaScript Client
```javascript
class OpenAGIWebSocketClient {
    constructor(url, token) {
        this.url = `${url}?token=${token}`;
        this.ws = null;
        this.listeners = {};
    }
    
    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = (event) => {
            console.log('Connected to Open-A.G.I WebSocket API');
            this.emit('connected', event);
        };
        
        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };
        
        this.ws.onclose = (event) => {
            console.log('WebSocket connection closed');
            this.emit('disconnected', event);
        };
        
        this.ws.onerror = (event) => {
            console.error('WebSocket error:', event);
            this.emit('error', event);
        };
    }
    
    handleMessage(message) {
        if (this.listeners[message.type]) {
            this.listeners[message.type].forEach(callback => {
                callback(message);
            });
        }
    }
    
    on(eventType, callback) {
        if (!this.listeners[eventType]) {
            this.listeners[eventType] = [];
        }
        this.listeners[eventType].push(callback);
    }
    
    emit(eventType, data) {
        if (this.listeners[eventType]) {
            this.listeners[eventType].forEach(callback => {
                callback(data);
            });
        }
    }
    
    subscribe(channel) {
        this.ws.send(JSON.stringify({
            type: 'subscribe',
            channel: channel
        }));
    }
    
    unsubscribe(channel) {
        this.ws.send(JSON.stringify({
            type: 'unsubscribe',
            channel: channel
        }));
    }
}

// Usage
const client = new OpenAGIWebSocketClient('ws://localhost:8080/api/v1/ws', 'your_token');
client.connect();

client.on('connected', () => {
    client.subscribe('network_events');
});

client.on('network_event', (message) => {
    console.log('Network event:', message);
});
```

### Python Client
```python
import websocket
import json
import threading

class OpenAGIWebSocketClient:
    def __init__(self, url, token):
        self.url = f"{url}?token={token}"
        self.ws = None
        self.listeners = {}
        self.running = False
        
    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # Run in separate thread
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()
        
    def on_open(self, ws):
        print("Connected to Open-A.G.I WebSocket API")
        self.emit('connected')
        
    def on_message(self, ws, message):
        data = json.loads(message)
        self.handle_message(data)
        
    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")
        self.emit('error', error)
        
    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")
        self.running = False
        self.emit('disconnected')
        
    def handle_message(self, message):
        message_type = message.get('type')
        if message_type in self.listeners:
            for callback in self.listeners[message_type]:
                callback(message)
                
    def on(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        
    def emit(self, event_type, data=None):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)
                
    def subscribe(self, channel):
        message = {
            "type": "subscribe",
            "channel": channel
        }
        self.ws.send(json.dumps(message))
        
    def unsubscribe(self, channel):
        message = {
            "type": "unsubscribe",
            "channel": channel
        }
        self.ws.send(json.dumps(message))

# Usage
client = OpenAGIWebSocketClient('ws://localhost:8080/api/v1/ws', 'your_token')
client.connect()

def on_connected():
    client.subscribe('network_events')
    
def on_network_event(message):
    print(f"Network event: {message}")

client.on('connected', on_connected)
client.on('network_event', on_network_event)
```

## Best Practices

### Connection Management
1. Implement reconnection logic for dropped connections
2. Handle authentication token expiration
3. Use ping/pong to detect connection health
4. Implement proper error handling

### Message Handling
1. Validate all incoming messages
2. Handle message rate limiting
3. Implement message queuing for high-volume channels
4. Use appropriate data structures for message storage

### Security
1. Always use secure WebSocket connections (wss://) in production
2. Validate authentication tokens
3. Implement message signing for critical operations
4. Monitor for suspicious activity

### Performance
1. Subscribe only to necessary channels
2. Implement message filtering on the client side
3. Use compression for large messages
4. Batch multiple small messages when possible