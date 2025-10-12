# AEGIS-Conscience Network - Multi-User Connection Guide

## How Different Users Can Connect Their Nodes

The AEGIS-Conscience Network is designed to allow nodes from different users to securely connect and collaborate. Here's how it works:

## 1. Network Architecture

### TOR-Based Anonymous P2P
- Each node creates a unique TOR v3 onion service
- All communication is encrypted and anonymous
- No central server required - fully decentralized

### Client Authorization
- Nodes only accept connections from authorized peers
- Prevents unauthorized access to the network
- Trust-based network formation

## 2. Connection Process

### Step 1: Node Initialization
Each user starts their node:
```bash
# User 1
docker-compose up aegis-node-1

# User 2
docker-compose up aegis-node-2
```

### Step 2: Obtain Onion Addresses
Each node displays its onion address:
```
User 1 Node: abcdefgh12345678.onion:8080
User 2 Node: xyzwvu9876543210.onion:8080
```

### Step 3: Exchange and Authorize
Users exchange onion addresses and add each other as authorized clients:
```python
# In User 1's node configuration
authorized_peers = ["xyzwvu9876543210.onion"]

# In User 2's node configuration
authorized_peers = ["abcdefgh12345678.onion"]
```

### Step 4: Establish Connection
Nodes automatically connect through the TOR network and begin exchanging consciousness states.

## 3. Security Features

### End-to-End Encryption
- All messages are signed with Ed25519 keys
- X25519 encryption for message content
- Private keys stored encrypted on disk

### Trust Verification
- Peer reputation system
- Signature verification for all messages
- Rate limiting to prevent abuse

## 4. Practical Example

### User Alice Setup:
```bash
# Start node
docker run -d --name alice-node -p 8080:8080 aegis/conscience-node
# Onion address: alicenode1234567890abcd.onion:8080
```

### User Bob Setup:
```bash
# Start node
docker run -d --name bob-node -p 8080:8080 aegis/conscience-node
# Onion address: bobnode0987654321zyxw.onion:8080
```

### Connection Exchange:
1. Alice shares: `alicenode1234567890abcd.onion:8080`
2. Bob shares: `bobnode0987654321zyxw.onion:8080`
3. Both add each other to their authorized peers list
4. Nodes automatically establish secure connection

## 5. Network Benefits

### Privacy Protection
- No IP addresses are exposed
- All communication is anonymized through TOR
- No central point of failure

### Collaborative Consciousness
- Nodes share consciousness states
- Collective coherence calculation
- Reputation-based trust system

### Scalability
- Supports networks of 2-10 nodes (PBFT consensus)
- Automatic peer discovery
- Load balancing through TOR

## 6. Monitoring and Verification

Users can monitor their connections through:
- **Web Dashboard**: Real-time metrics and peer status
- **Log Files**: Connection events and security alerts
- **API Endpoints**: Programmatic access to network status

## 7. Troubleshooting

### Common Issues:
1. **Connection Failures**: Verify onion addresses and authorization
2. **TOR Issues**: Check TOR service status and firewall settings
3. **Authentication Errors**: Ensure correct public keys are exchanged

### Diagnostic Commands:
```bash
# Check node status
curl http://localhost:8080/api/status

# View connected peers
curl http://localhost:8080/api/peers

# Check network metrics
curl http://localhost:8080/api/metrics
```

## Conclusion

The AEGIS-Conscience Network is fully functional for multi-user deployments. Different users can securely connect their nodes through TOR, exchange consciousness states, and participate in collective coherence calculations while maintaining privacy and security.