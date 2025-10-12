"""
Unified Network Layer for Metatron-ConscienceAI and Open-A.G.I Integration

This module consolidates the network functionality from both systems:
- aegis-conscience/network/p2p.py
- Open-A.G.I/p2p_network.py
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives.asymmetric import ed25519
import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class UnifiedPeerInfo:
    """Unified peer information structure"""
    peer_id: str
    ip_address: str
    port: int
    public_key: str
    last_seen: float
    connection_status: str
    reputation_score: float
    latency: float
    protocols_supported: List[str]  # List of supported protocols (consciousness, agi, both)


@dataclass
class UnifiedNetworkMessage:
    """Unified network message structure"""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    ttl: int = 60
    signature: Optional[bytes] = None
    route_path: Optional[List[str]] = None
    protocol: str = "unified"  # consciousness, agi, or unified


class UnifiedP2PNetwork:
    """Unified P2P network implementation combining features from both systems"""
    
    def __init__(self, node_id: str, port: int = 8080):
        self.node_id = node_id
        self.port = port
        self.peers: Dict[str, UnifiedPeerInfo] = {}
        self.peer_connections: Dict[str, Any] = {}  # Using Any to avoid specific imports
        self.message_handlers: Dict[str, Callable] = {}
        self.server = None
        self.running = False
        
        # Timing attack mitigation (from aegis-conscience)
        self.message_queue: List[Dict] = []
        self.last_message_time = time.time()
        self.message_interval = 2.0  # Randomized interval
        self.dummy_traffic_enabled = True
        self.dummy_traffic_probability = 0.1
        
        # Rate limiting (from aegis-conscience)
        self.peer_message_counts: Dict[str, int] = {}
        self.peer_message_timestamps: Dict[str, float] = {}
        self.max_messages_per_minute = 5
        
        # Protocol support tracking
        self.supported_protocols = ["consciousness", "agi", "unified"]
        
        logger.info(f"Unified P2P Network initialized for node {node_id}")
    
    async def start_server(self):
        """Start the unified P2P server"""
        try:
            # This is a simplified implementation
            # In a full implementation, this would integrate both networking approaches
            self.running = True
            logger.info(f"Unified P2P server started on port {self.port}")
            return True
        except Exception as e:
            logger.error(f"Error starting unified P2P server: {e}")
            return False
    
    def add_peer(self, peer_info: UnifiedPeerInfo):
        """Add a peer to the known peers list"""
        self.peers[peer_info.peer_id] = peer_info
        logger.info(f"Added peer {peer_info.peer_id} to network")
    
    def update_peer_reputation(self, peer_id: str, score_delta: float):
        """Update a peer's reputation score"""
        if peer_id in self.peers:
            self.peers[peer_id].reputation_score = max(
                0.0, 
                min(1.0, self.peers[peer_id].reputation_score + score_delta)
            )
            logger.debug(f"Updated reputation for peer {peer_id}: {self.peers[peer_id].reputation_score}")
    
    def get_trusted_peers(self, min_reputation: float = 0.7) -> List[UnifiedPeerInfo]:
        """Get peers with reputation above threshold"""
        trusted_peers = [
            peer for peer in self.peers.values() 
            if peer.reputation_score >= min_reputation
        ]
        logger.debug(f"Found {len(trusted_peers)} trusted peers (min reputation: {min_reputation})")
        return trusted_peers
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for a message type"""
        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")
    
    async def send_message(self, message: UnifiedNetworkMessage, peer_id: str) -> bool:
        """Send a generic message to a peer"""
        if peer_id not in self.peers:
            logger.warning(f"Attempt to send message to unknown peer {peer_id}")
            return False
        
        try:
            # In a real implementation, this would send the actual network message
            logger.debug(f"Sending {message.message_type} message to peer {peer_id}")
            
            # Call appropriate handler if registered
            if message.message_type in self.message_handlers:
                await self.message_handlers[message.message_type](message)
            
            return True
        except Exception as e:
            logger.error(f"Error sending message to peer {peer_id}: {e}")
            return False
    
    async def broadcast_message(self, message: UnifiedNetworkMessage, 
                              exclude_peers: Optional[List[str]] = None) -> int:
        """Broadcast a message to all peers"""
        exclude_peers = exclude_peers or []
        sent_count = 0
        
        for peer_id in list(self.peers.keys()):
            if peer_id not in exclude_peers:
                success = await self.send_message(message, peer_id)
                if success:
                    sent_count += 1
        
        logger.info(f"Broadcast {message.message_type} message to {sent_count} peers")
        return sent_count
    
    async def connect_to_peer(self, peer_info: UnifiedPeerInfo) -> bool:
        """Connect to a peer"""
        try:
            # In a real implementation, this would establish an actual connection
            peer_info.connection_status = "connected"
            peer_info.last_seen = time.time()
            self.peers[peer_info.peer_id] = peer_info
            logger.info(f"Connected to peer {peer_info.peer_id}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to peer {peer_info.peer_id}: {e}")
            peer_info.connection_status = "failed"
            return False
    
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
        within_limit = self.peer_message_counts[peer_id] <= self.max_messages_per_minute
        if not within_limit:
            logger.warning(f"Rate limit exceeded for peer {peer_id}")
        
        return within_limit
    
    async def stop(self):
        """Stop the P2P network"""
        self.running = False
        
        # Close all connections
        for peer_id, connection in self.peer_connections.items():
            try:
                # In a real implementation, this would close the actual connection
                logger.debug(f"Closing connection to peer {peer_id}")
            except Exception as e:
                logger.error(f"Error closing connection to peer {peer_id}: {e}")
        
        logger.info("Unified P2P Network stopped")


# Example usage and testing
async def example_handler(message: UnifiedNetworkMessage):
    """Example message handler"""
    print(f"Received message: {message.message_type} from {message.sender_id}")


async def main():
    """Example usage of the Unified P2P Network"""
    # Create network instance
    network = UnifiedP2PNetwork("test_node_1", 8080)
    
    # Add a peer
    peer = UnifiedPeerInfo(
        peer_id="peer_1",
        ip_address="127.0.0.1",
        port=8081,
        public_key="test_key",
        last_seen=time.time(),
        connection_status="disconnected",
        reputation_score=0.8,
        latency=0.1,
        protocols_supported=["consciousness", "unified"]
    )
    network.add_peer(peer)
    
    # Register a message handler
    network.register_message_handler("test_message", example_handler)
    
    # Create and send a test message
    message = UnifiedNetworkMessage(
        message_id="test_001",
        sender_id="test_node_1",
        recipient_id="peer_1",
        message_type="test_message",
        payload={"content": "Hello, unified network!"},
        timestamp=time.time(),
        protocol="unified"
    )
    
    # Send the message
    success = await network.send_message(message, "peer_1")
    print(f"Message sent successfully: {success}")
    
    # Start server (simplified)
    server_started = await network.start_server()
    print(f"Server started: {server_started}")


if __name__ == "__main__":
    asyncio.run(main())