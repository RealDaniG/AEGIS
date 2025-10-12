"""
P2P Network Layer for AEGIS-Conscience Network
TCP over TOR v3 onion services with timing attack mitigation
"""

import asyncio
import json
import time
import socket
import random
from typing import Dict, List, Optional, Callable
from dataclasses import asdict

from schemas import ConsciousnessState, NetworkMessage, PeerInfo


class P2PNetwork:
    """P2P network layer using TCP over TOR with timing attack mitigation"""
    
    def __init__(self, node_id: str, port: int = 8080):
        self.node_id = node_id
        self.port = port
        self.peers: Dict[str, PeerInfo] = {}
        self.peer_connections: Dict[str, asyncio.StreamWriter] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.server = None
        self.running = False
        
        # Timing attack mitigation
        self.message_queue: List[Dict] = []
        self.last_message_time = time.time()
        self.message_interval = random.uniform(2.0, 5.0)  # Randomized interval
        self.dummy_traffic_enabled = True
        self.dummy_traffic_probability = 0.1  # 10% chance of dummy traffic
        
        # Rate limiting
        self.peer_message_counts: Dict[str, int] = {}
        self.peer_message_timestamps: Dict[str, float] = {}
        self.max_messages_per_minute = 5  # Limit to 5 messages per minute per peer
        
    async def start_server(self):
        """Start the P2P server"""
        try:
            self.server = await asyncio.start_server(
                self._handle_connection,
                '127.0.0.1',  # For local testing - will use TOR in production
                self.port
            )
            self.running = True
            
            # Start background tasks
            asyncio.create_task(self._message_sender())
            if self.dummy_traffic_enabled:
                asyncio.create_task(self._send_dummy_traffic())
            
            print(f"P2P server started on port {self.port}")
            
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            print(f"Error starting P2P server: {e}")
    
    async def _handle_connection(self, reader: asyncio.StreamReader, 
                               writer: asyncio.StreamWriter):
        """Handle incoming connections"""
        try:
            # Read message
            data = await reader.readline()
            if not data:
                return
                
            # Parse message
            message_dict = json.loads(data.decode().strip())
            message = self._dict_to_message(message_dict)
            
            # Handle message
            await self._handle_message(message, writer)
            
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def _handle_message(self, message: NetworkMessage, 
                            writer: asyncio.StreamWriter):
        """Handle incoming messages"""
        # Verify message is not expired
        if time.time() - message.timestamp > message.ttl:
            print(f"Message expired: {message.message_id}")
            return
        
        # Rate limiting check
        if not self._check_rate_limit(message.sender_id):
            print(f"Rate limit exceeded for peer {message.sender_id}")
            return
        
        # Validate message content
        if not self._validate_message(message):
            print(f"Invalid message from {message.sender_id}")
            return
        
        # Call appropriate handler
        if message.message_type in self.message_handlers:
            await self.message_handlers[message.message_type](message)
        else:
            print(f"Unhandled message type: {message.message_type}")
    
    def _check_rate_limit(self, peer_id: str) -> bool:
        """Check if peer has exceeded message rate limit"""
        current_time = time.time()
        
        # Reset count if more than a minute has passed
        if peer_id in self.peer_message_timestamps:
            if current_time - self.peer_message_timestamps[peer_id] > 60:
                self.peer_message_counts[peer_id] = 0
        
        # Update count
        self.peer_message_counts[peer_id] = self.peer_message_counts.get(peer_id, 0) + 1
        self.peer_message_timestamps[peer_id] = current_time
        
        # Check limit
        return self.peer_message_counts[peer_id] <= self.max_messages_per_minute
    
    def _validate_message(self, message: NetworkMessage) -> bool:
        """Validate message content"""
        # Check coherence range
        if 'coherence' in message.payload:
            coherence = message.payload['coherence']
            if not (0 <= coherence <= 1):
                return False
        
        # Check timestamp is not too old
        if time.time() - message.timestamp > 30:  # 30 seconds max age
            return False
            
        return True
    
    def register_message_handler(self, message_type: str, 
                               handler: Callable):
        """Register a handler for a message type"""
        self.message_handlers[message_type] = handler
    
    async def connect_to_peer(self, peer_info: PeerInfo) -> bool:
        """Connect to a peer"""
        try:
            # For now, connect directly - will use TOR in production
            reader, writer = await asyncio.open_connection(
                peer_info.ip_address,
                peer_info.port
            )
            
            self.peer_connections[peer_info.peer_id] = writer
            peer_info.connection_status = "connected"
            peer_info.last_seen = time.time()
            
            print(f"Connected to peer {peer_info.peer_id}")
            return True
        except Exception as e:
            print(f"Error connecting to peer {peer_info.peer_id}: {e}")
            peer_info.connection_status = "failed"
            return False
    
    async def send_state_to_peer(self, state: ConsciousnessState, 
                               peer_id: str) -> bool:
        """Send consciousness state to a peer (queued for timing protection)"""
        if peer_id not in self.peer_connections:
            print(f"Not connected to peer {peer_id}")
            return False
        
        # Convert state to dictionary, handling the signature properly
        state_dict = {
            'node_id': state.node_id,
            'timestamp': state.timestamp,
            'entropy': state.entropy,
            'valence': state.valence,
            'arousal': state.arousal,
            'coherence': state.coherence,
            'empathy_score': state.empathy_score,
            'insight_strength': state.insight_strength,
            'signature': state.signature.hex() if state.signature else None
        }
        
        # Create network message
        message = NetworkMessage(
            message_id=f"state_{int(time.time()*1000000)}",
            sender_id=self.node_id,
            recipient_id=peer_id,
            message_type="consciousness_state",
            payload=state_dict,
            timestamp=time.time()
        )
        
        # Queue message for sending with timing protection
        self.message_queue.append({
            'message': message,
            'peer_id': peer_id,
            'type': 'state'
        })
        
        return True
    
    async def broadcast_state(self, state: ConsciousnessState, 
                            exclude_peers: Optional[List[str]] = None) -> int:
        """Broadcast consciousness state to all peers (queued for timing protection)"""
        exclude_peers = exclude_peers or []
        sent_count = 0
        
        # Convert state to dictionary, handling the signature properly
        state_dict = {
            'node_id': state.node_id,
            'timestamp': state.timestamp,
            'entropy': state.entropy,
            'valence': state.valence,
            'arousal': state.arousal,
            'coherence': state.coherence,
            'empathy_score': state.empathy_score,
            'insight_strength': state.insight_strength,
            'signature': state.signature.hex() if state.signature else None
        }
        
        # Create network message
        message = NetworkMessage(
            message_id=f"state_{int(time.time()*1000000)}",
            sender_id=self.node_id,
            recipient_id="*",
            message_type="consciousness_state",
            payload=state_dict,
            timestamp=time.time()
        )
        
        for peer_id in list(self.peer_connections.keys()):
            if peer_id not in exclude_peers:
                # Queue message for sending with timing protection
                self.message_queue.append({
                    'message': message,
                    'peer_id': peer_id,
                    'type': 'state'
                })
                sent_count += 1
        
        return sent_count
    
    async def send_message(self, message: NetworkMessage, peer_id: str) -> bool:
        """Send a generic message to a peer (queued for timing protection)"""
        if peer_id not in self.peer_connections:
            print(f"Not connected to peer {peer_id}")
            return False
        
        # Queue message for sending with timing protection
        self.message_queue.append({
            'message': message,
            'peer_id': peer_id,
            'type': 'generic'
        })
        
        return True
    
    async def _message_sender(self):
        """Background task to send queued messages at randomized intervals"""
        while self.running:
            try:
                current_time = time.time()
                
                # Check if it's time to send messages
                if current_time - self.last_message_time >= self.message_interval and self.message_queue:
                    # Send a batch of messages
                    batch_size = min(3, len(self.message_queue))  # Send up to 3 messages at once
                    for _ in range(batch_size):
                        if self.message_queue:
                            item = self.message_queue.pop(0)
                            await self._send_message_now(item['message'], item['peer_id'])
                    
                    # Reset timer and randomize next interval
                    self.last_message_time = current_time
                    self.message_interval = random.uniform(2.0, 5.0)
                
                await asyncio.sleep(0.1)  # Check every 100ms
            except Exception as e:
                print(f"Error in message sender: {e}")
                await asyncio.sleep(1)
    
    async def _send_message_now(self, message: NetworkMessage, peer_id: str) -> bool:
        """Send a message immediately"""
        if peer_id not in self.peer_connections:
            return False
        
        try:
            writer = self.peer_connections[peer_id]
            # Convert message to dictionary, handling the signature properly
            message_dict = {
                'message_id': message.message_id,
                'sender_id': message.sender_id,
                'recipient_id': message.recipient_id,
                'message_type': message.message_type,
                'payload': message.payload,
                'timestamp': message.timestamp,
                'ttl': message.ttl,
                'signature': message.signature.hex() if message.signature else None,
                'route_path': message.route_path
            }
            message_data = json.dumps(message_dict).encode() + b'\n'
            writer.write(message_data)
            await writer.drain()
            
            return True
        except Exception as e:
            print(f"Error sending message to peer {peer_id}: {e}")
            return False
    
    async def _send_dummy_traffic(self):
        """Send dummy traffic to prevent timing analysis"""
        while self.running and self.dummy_traffic_enabled:
            try:
                # Random delay
                await asyncio.sleep(random.uniform(10, 60))  # 10-60 seconds
                
                # 10% chance to send dummy traffic
                if random.random() < self.dummy_traffic_probability and self.peer_connections:
                    # Select a random peer
                    peer_id = random.choice(list(self.peer_connections.keys()))
                    
                    # Create dummy message
                    dummy_message = NetworkMessage(
                        message_id=f"dummy_{int(time.time()*1000000)}",
                        sender_id=self.node_id,
                        recipient_id=peer_id,
                        message_type="dummy",
                        payload={"timestamp": time.time()},
                        timestamp=time.time()
                    )
                    
                    # Queue the dummy message
                    self.message_queue.append({
                        'message': dummy_message,
                        'peer_id': peer_id,
                        'type': 'dummy'
                    })
                    
            except Exception as e:
                print(f"Error sending dummy traffic: {e}")
    
    def add_peer(self, peer_info: PeerInfo):
        """Add a peer to the known peers list"""
        self.peers[peer_info.peer_id] = peer_info
    
    def update_peer_reputation(self, peer_id: str, score_delta: float):
        """Update a peer's reputation score"""
        if peer_id in self.peers:
            self.peers[peer_id].reputation_score = max(
                0.0, 
                min(1.0, self.peers[peer_id].reputation_score + score_delta)
            )
    
    def get_trusted_peers(self, min_reputation: float = 0.7) -> List[PeerInfo]:
        """Get peers with reputation above threshold"""
        return [
            peer for peer in self.peers.values() 
            if peer.reputation_score >= min_reputation
        ]
    
    def _dict_to_message(self, message_dict: Dict) -> NetworkMessage:
        """Convert dictionary to NetworkMessage"""
        # Handle optional fields
        signature = message_dict.get('signature')
        if signature is not None:
            signature = bytes.fromhex(signature) if isinstance(signature, str) else signature
            
        route_path = message_dict.get('route_path')
        if route_path is not None and isinstance(route_path, str):
            route_path = route_path.split(',') if route_path else []
            
        return NetworkMessage(
            message_id=message_dict['message_id'],
            sender_id=message_dict['sender_id'],
            recipient_id=message_dict['recipient_id'],
            message_type=message_dict['message_type'],
            payload=message_dict['payload'],
            timestamp=message_dict['timestamp'],
            ttl=message_dict.get('ttl', 60),
            signature=signature,
            route_path=route_path
        )
    
    async def stop(self):
        """Stop the P2P network"""
        self.running = False
        
        # Close all connections
        for writer in self.peer_connections.values():
            writer.close()
            await writer.wait_closed()
        
        # Close server
        if self.server:
            self.server.close()
            await self.server.wait_closed()


# Example usage
if __name__ == "__main__":
    # Create P2P network
    p2p = P2PNetwork("test_node_1", 8080)
    
    # Add a peer
    peer = PeerInfo(
        peer_id="peer_1",
        ip_address="127.0.0.1",
        port=8081,
        public_key="test_key",
        last_seen=time.time(),
        connection_status="disconnected",
        reputation_score=0.8,
        latency=0.1
    )
    p2p.add_peer(peer)
    
    print("P2P network initialized with timing attack mitigation")