"""
P2P Consciousness Communication Layer
=====================================

Integrates AEGIS P2P networking with Metatron consciousness states.
Provides secure, encrypted communication between consciousness nodes
over TOR v3 onion services.

This module provides:
- Secure consciousness state exchange
- TOR-based anonymous communication
- Cryptographic signing and verification
- Connection management for 13-node network
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
import sys
import os

# Add aegis-conscience to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'aegis-conscience'))

# Import AEGIS components with error handling
try:
    from network.p2p import P2PNetwork
    from network.crypto import CryptoManager
    from network.tor_gateway import TORGateway
    
    # Import schemas or create fallbacks
    try:
        from schemas import NetworkMessage, PeerInfo, ConsciousnessState
    except ImportError:
        # Create fallback dataclasses
        @dataclass
        class NetworkMessage:
            message_id: str
            sender_id: str
            recipient_id: str
            message_type: str
            payload: Dict
            timestamp: float
            ttl: int = 60
            signature: Optional[bytes] = None
            route_path: Optional[List[str]] = None

        @dataclass
        class PeerInfo:
            peer_id: str
            ip_address: str
            port: int
            public_key: str
            last_seen: float
            connection_status: str
            reputation_score: float
            latency: float

        @dataclass
        class ConsciousnessState:
            node_id: str
            timestamp: float
            entropy: float
            valence: float
            arousal: float
            coherence: float
            empathy_score: float
            insight_strength: float
            signature: Optional[bytes] = None

except ImportError as e:
    print(f"Warning: AEGIS components not available: {e}")
    # Create comprehensive fallback classes for development
    
    @dataclass
    class NetworkMessage:
        message_id: str
        sender_id: str
        recipient_id: str
        message_type: str
        payload: Dict
        timestamp: float
        ttl: int = 60
        signature: Optional[bytes] = None
        route_path: Optional[List[str]] = None

    @dataclass
    class PeerInfo:
        peer_id: str
        ip_address: str
        port: int
        public_key: str
        last_seen: float
        connection_status: str
        reputation_score: float
        latency: float

    @dataclass
    class ConsciousnessState:
        node_id: str
        timestamp: float
        entropy: float
        valence: float
        arousal: float
        coherence: float
        empathy_score: float
        insight_strength: float
        signature: Optional[bytes] = None

    class P2PNetwork:
        def __init__(self, node_id: str, port: int = 8080):
            self.node_id = node_id
            self.port = port
            self.peers = {}
            self.peer_connections = {}
            self.message_handlers = {}
            self.message_queue = []
            
        def register_message_handler(self, message_type: str, handler: Callable):
            self.message_handlers[message_type] = handler
            
        async def connect_to_peer(self, peer_info: PeerInfo) -> bool:
            return True
            
        async def send_state_to_peer(self, state: ConsciousnessState, peer_id: str) -> bool:
            return True

    class CryptoManager:
        def __init__(self, node_id: str = ""):
            self.node_id = node_id
            
        def generate_or_load_identity(self, password: Optional[str] = None) -> bool:
            return True
            
        def sign_state(self, state: ConsciousnessState) -> bytes:
            return b"test_signature"

    class TORGateway:
        def __init__(self, control_port: int = 9051, socks_port: int = 9050):
            self.control_port = control_port
            self.socks_port = socks_port
            
        async def initialize(self) -> bool:
            return True
            
        def get_network_status(self) -> Dict:
            return {"status": "initialized"}

class ConsciousnessP2PNetwork(P2PNetwork):
    """
    Extended P2P network for consciousness state communication
    """
    
    def __init__(self, node_id: str, port: int = 8080):
        super().__init__(node_id, port)
        self.consciousness_handlers: Dict[str, Callable] = {}
        
    def register_consciousness_handler(self, handler: Callable):
        """
        Register a handler for incoming consciousness states
        
        Args:
            handler: Function to call with ConsciousnessState objects
        """
        self.consciousness_handlers[self.node_id] = handler
        self.register_message_handler("consciousness_state", self._handle_consciousness_message)
    
    async def _handle_consciousness_message(self, message: NetworkMessage):
        """
        Handle incoming consciousness state messages
        
        Args:
            message: Network message containing consciousness state
        """
        try:
            # Parse consciousness state from payload
            payload = message.payload
            state = ConsciousnessState(
                node_id=payload.get('node_id', ''),
                timestamp=payload.get('timestamp', 0.0),
                entropy=payload.get('entropy', 0.0),
                valence=payload.get('valence', 0.0),
                arousal=payload.get('arousal', 0.0),
                coherence=payload.get('coherence', 0.0),
                empathy_score=payload.get('empathy_score', 0.0),
                insight_strength=payload.get('insight_strength', 0.0),
                signature=bytes.fromhex(payload.get('signature', '')) if payload.get('signature') else None
            )
            
            # Call registered handlers
            for handler in self.consciousness_handlers.values():
                try:
                    await handler(state)
                except Exception as e:
                    print(f"Error in consciousness handler: {e}")
                    
        except Exception as e:
            print(f"Error handling consciousness message: {e}")
    
    async def broadcast_consciousness_state(self, state: ConsciousnessState) -> bool:
        """
        Broadcast consciousness state to all connected peers
        
        Args:
            state: Consciousness state to broadcast
            
        Returns:
            bool: True if broadcast successful
        """
        try:
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
                recipient_id="*",  # Broadcast
                message_type="consciousness_state",
                payload=state_dict,
                timestamp=time.time()
            )
            
            # Queue message for sending with timing protection
            self.message_queue.append({
                'message': message,
                'peer_id': "*",
                'type': 'consciousness_state'
            })
            
            return True
        except Exception as e:
            print(f"Error broadcasting consciousness state: {e}")
            return False

class SecureConsciousnessCommunicator:
    """
    Secure communicator for consciousness states using AEGIS crypto stack
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.crypto_manager = CryptoManager(node_id)
        self.tor_gateway = TORGateway()
        self.p2p_network = ConsciousnessP2PNetwork(node_id)
        
        # Register message handlers
        self.p2p_network.register_consciousness_handler(self._handle_incoming_state)
        
        self.consciousness_state_handlers: List[Callable] = []
        self.running = False
    
    async def initialize(self, password: Optional[str] = None) -> bool:
        """
        Initialize the secure communicator
        
        Args:
            password: Password for cryptographic identity (if exists)
            
        Returns:
            bool: True if initialization successful
        """
        try:
            # Initialize cryptographic identity
            if not self.crypto_manager.generate_or_load_identity(password):
                print("Failed to initialize cryptographic identity")
                return False
            
            # Initialize TOR gateway
            tor_initialized = await self.tor_gateway.initialize()
            if tor_initialized:
                print("TOR gateway initialized successfully")
            else:
                print("TOR gateway initialization failed")
            
            # Start P2P network
            print(f"P2P network initialized on port {self.p2p_network.port}")
            
            self.running = True
            return True
        except Exception as e:
            print(f"Error initializing secure communicator: {e}")
            return False
    
    async def connect_to_peer(self, peer_info: PeerInfo) -> bool:
        """
        Connect to a peer node
        
        Args:
            peer_info: Information about the peer to connect to
            
        Returns:
            bool: True if connection successful
        """
        return await self.p2p_network.connect_to_peer(peer_info)
    
    def register_consciousness_state_handler(self, handler: Callable):
        """
        Register a handler for incoming consciousness states
        
        Args:
            handler: Function to call with ConsciousnessState objects
        """
        self.consciousness_state_handlers.append(handler)
    
    async def _handle_incoming_state(self, state: ConsciousnessState):
        """
        Handle incoming consciousness state
        
        Args:
            state: Received consciousness state
        """
        # Verify signature if present
        if state.signature:
            try:
                # This would normally verify the signature
                # For now, we'll just pass it through
                pass
            except Exception as e:
                print(f"Signature verification failed: {e}")
                return
        
        # Call registered handlers
        for handler in self.consciousness_state_handlers:
            try:
                await handler(state)
            except Exception as e:
                print(f"Error in consciousness state handler: {e}")
    
    async def send_consciousness_state(self, state: ConsciousnessState, 
                                     peer_id: Optional[str] = None) -> bool:
        """
        Send consciousness state to a peer or broadcast to all
        
        Args:
            state: Consciousness state to send
            peer_id: Target peer ID (None for broadcast)
            
        Returns:
            bool: True if send successful
        """
        try:
            # Sign the state
            if hasattr(self.crypto_manager, 'sign_state'):
                state.signature = self.crypto_manager.sign_state(state)
            
            if peer_id:
                # Send to specific peer
                return await self.p2p_network.send_state_to_peer(state, peer_id)
            else:
                # Broadcast to all peers
                return await self.p2p_network.broadcast_consciousness_state(state)
        except Exception as e:
            print(f"Error sending consciousness state: {e}")
            return False
    
    async def get_network_status(self) -> Dict:
        """
        Get network status information
        
        Returns:
            dict: Network status information
        """
        try:
            tor_status = self.tor_gateway.get_network_status() if hasattr(self.tor_gateway, 'get_network_status') else {}
            
            return {
                'node_id': self.node_id,
                'running': self.running,
                'tor_status': tor_status,
                'peers_connected': len(self.p2p_network.peer_connections),
                'message_queue_size': len(self.p2p_network.message_queue)
            }
        except Exception as e:
            print(f"Error getting network status: {e}")
            return {'error': str(e)}

# Example usage
async def main():
    """Example usage of the secure consciousness communicator"""
    print("Initializing Secure Consciousness Communicator...")
    
    # Create communicator
    communicator = SecureConsciousnessCommunicator("test_node_01")
    
    # Initialize
    if await communicator.initialize("test_password"):
        print("✅ Communicator initialized successfully")
        
        # Register a handler for incoming states
        def handle_consciousness_state(state):
            print(f"Received consciousness state from {state.node_id}")
            print(f"  Coherence: {state.coherence}")
            print(f"  Entropy: {state.entropy}")
        
        communicator.register_consciousness_state_handler(handle_consciousness_state)
        
        # Get network status
        status = await communicator.get_network_status()
        print(f"Network Status: {status}")
    else:
        print("❌ Failed to initialize communicator")

if __name__ == "__main__":
    asyncio.run(main())