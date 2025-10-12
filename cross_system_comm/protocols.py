"""
Enhanced Cross-System Communication Protocols

This module implements advanced communication protocols between 
Metatron-Consciousness and Open-A.G.I systems.
"""

import asyncio
import json
import logging
import time
import base64
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
import aiohttp
import websockets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from unified_components.network import UnifiedP2PNetwork, UnifiedNetworkMessage
from unified_api.models import UnifiedSystemState

logger = logging.getLogger(__name__)


@dataclass
class CrossSystemMessage:
    """Message structure for cross-system communication"""
    message_id: str
    source_system: str  # "metatron" or "agi"
    target_system: str  # "metatron" or "agi"
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    priority: int = 1  # 1-10, higher is more urgent
    ttl: int = 300  # Time to live in seconds
    encrypted: bool = False
    signature: Optional[str] = None


class CrossSystemCommunicator:
    """Enhanced communication layer between consciousness and AGI systems"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.p2p_network = UnifiedP2PNetwork(node_id)
        self.message_handlers: Dict[str, Callable] = {}
        self.running = False
        self.websocket_connections: Dict[str, Any] = {}
        self.message_queue: List[CrossSystemMessage] = []
        self.processed_messages: set = set()
        
        # Security settings
        self.encryption_enabled = True
        self.encryption_key = None
        self._generate_encryption_key()
        
        # Performance metrics
        self.metrics = {
            "messages_sent": 0,
            "messages_received": 0,
            "messages_dropped": 0,
            "encryption_used": 0,
            "errors": 0
        }
        
        logger.info(f"Cross-System Communicator initialized for node {node_id}")
    
    def _generate_encryption_key(self):
        """Generate encryption key for secure communication"""
        try:
            # Generate a proper Fernet key
            self.encryption_key = Fernet.generate_key()
            self.cipher_suite = Fernet(self.encryption_key)
            logger.info("Encryption key generated successfully")
        except Exception as e:
            logger.error(f"Failed to generate encryption key: {e}")
            self.encryption_enabled = False
    
    async def initialize(self) -> bool:
        """Initialize the cross-system communicator"""
        try:
            # Initialize P2P network
            await self.p2p_network.start_server()
            
            # Register internal message handlers
            self.p2p_network.register_message_handler("cross_system", self._handle_p2p_message)
            
            self.running = True
            logger.info("Cross-System Communicator initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Cross-System Communicator: {e}")
            return False
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for cross-system messages"""
        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")
    
    async def send_message(self, message: CrossSystemMessage, 
                          use_websocket: bool = False) -> bool:
        """Send a cross-system message"""
        try:
            # Check if message has expired
            if time.time() - message.timestamp > message.ttl:
                logger.warning(f"Message {message.message_id} expired")
                self.metrics["messages_dropped"] += 1
                return False
            
            # Encrypt message if enabled
            if self.encryption_enabled and not message.encrypted:
                message = self._encrypt_message(message)
            
            # Add to processed set to prevent duplicates
            self.processed_messages.add(message.message_id)
            
            if use_websocket:
                # Send via WebSocket
                success = await self._send_via_websocket(message)
            else:
                # Send via P2P network
                success = await self._send_via_p2p(message)
            
            if success:
                self.metrics["messages_sent"] += 1
                logger.debug(f"Message {message.message_id} sent successfully")
            else:
                self.metrics["messages_dropped"] += 1
                logger.warning(f"Failed to send message {message.message_id}")
            
            return success
        except Exception as e:
            logger.error(f"Error sending message {message.message_id}: {e}")
            self.metrics["errors"] += 1
            return False
    
    def _encrypt_message(self, message: CrossSystemMessage) -> CrossSystemMessage:
        """Encrypt message payload"""
        try:
            if not self.encryption_key:
                return message
            
            # Convert payload to JSON and encrypt
            payload_json = json.dumps(message.payload)
            encrypted_payload = self.cipher_suite.encrypt(payload_json.encode())
            
            # Create encrypted message
            encrypted_message = CrossSystemMessage(
                message_id=message.message_id,
                source_system=message.source_system,
                target_system=message.target_system,
                message_type=message.message_type,
                payload={"encrypted_data": base64.b64encode(encrypted_payload).decode()},
                timestamp=message.timestamp,
                priority=message.priority,
                ttl=message.ttl,
                encrypted=True
            )
            
            self.metrics["encryption_used"] += 1
            return encrypted_message
        except Exception as e:
            logger.error(f"Error encrypting message: {e}")
            return message
    
    def _decrypt_message(self, message: CrossSystemMessage) -> CrossSystemMessage:
        """Decrypt message payload"""
        try:
            if not self.encryption_key or not message.encrypted:
                return message
            
            # Decrypt payload
            encrypted_data = base64.b64decode(message.payload["encrypted_data"])
            decrypted_payload = self.cipher_suite.decrypt(encrypted_data)
            payload = json.loads(decrypted_payload.decode())
            
            # Create decrypted message
            decrypted_message = CrossSystemMessage(
                message_id=message.message_id,
                source_system=message.source_system,
                target_system=message.target_system,
                message_type=message.message_type,
                payload=payload,
                timestamp=message.timestamp,
                priority=message.priority,
                ttl=message.ttl,
                encrypted=False
            )
            
            return decrypted_message
        except Exception as e:
            logger.error(f"Error decrypting message: {e}")
            return message
    
    async def _send_via_p2p(self, message: CrossSystemMessage) -> bool:
        """Send message via P2P network"""
        try:
            # Convert to unified network message
            unified_message = UnifiedNetworkMessage(
                message_id=message.message_id,
                sender_id=self.node_id,
                recipient_id=message.target_system,
                message_type=f"cross_system_{message.message_type}",
                payload=asdict(message),
                timestamp=message.timestamp,
                protocol="unified"
            )
            
            # Send via P2P network
            success = await self.p2p_network.send_message(unified_message, message.target_system)
            return success
        except Exception as e:
            logger.error(f"Error sending via P2P: {e}")
            return False
    
    async def _send_via_websocket(self, message: CrossSystemMessage) -> bool:
        """Send message via WebSocket"""
        try:
            # This is a simplified implementation
            # In a real system, this would connect to the appropriate WebSocket endpoint
            logger.debug(f"Would send message via WebSocket: {message.message_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending via WebSocket: {e}")
            return False
    
    async def _handle_p2p_message(self, unified_message: UnifiedNetworkMessage):
        """Handle incoming P2P messages"""
        try:
            # Convert unified message to cross-system message
            message_dict = unified_message.payload
            message = CrossSystemMessage(
                message_id=message_dict["message_id"],
                source_system=message_dict["source_system"],
                target_system=message_dict["target_system"],
                message_type=message_dict["message_type"].replace("cross_system_", ""),
                payload=message_dict["payload"],
                timestamp=message_dict["timestamp"],
                priority=message_dict.get("priority", 1),
                ttl=message_dict.get("ttl", 300),
                encrypted=message_dict.get("encrypted", False)
            )
            
            # Check for duplicates
            if message.message_id in self.processed_messages:
                logger.debug(f"Duplicate message ignored: {message.message_id}")
                return
            
            # Decrypt if necessary
            if message.encrypted:
                message = self._decrypt_message(message)
            
            # Add to processed set
            self.processed_messages.add(message.message_id)
            self.metrics["messages_received"] += 1
            
            # Handle based on message type
            await self._route_message(message)
            
        except Exception as e:
            logger.error(f"Error handling P2P message: {e}")
            self.metrics["errors"] += 1
    
    async def _route_message(self, message: CrossSystemMessage):
        """Route message to appropriate handler"""
        try:
            # Call registered handler if exists
            if message.message_type in self.message_handlers:
                await self.message_handlers[message.message_type](message)
                return
            
            # Default handling based on target system
            if message.target_system == "metatron":
                await self._handle_metatron_message(message)
            elif message.target_system == "agi":
                await self._handle_agi_message(message)
            else:
                logger.warning(f"Unknown target system: {message.target_system}")
        except Exception as e:
            logger.error(f"Error routing message {message.message_id}: {e}")
    
    async def _handle_metatron_message(self, message: CrossSystemMessage):
        """Handle messages destined for Metatron system"""
        logger.debug(f"Handling Metatron message: {message.message_type}")
        # In a real implementation, this would forward to Metatron system
        pass
    
    async def _handle_agi_message(self, message: CrossSystemMessage):
        """Handle messages destined for AGI system"""
        logger.debug(f"Handling AGI message: {message.message_type}")
        # In a real implementation, this would forward to AGI system
        pass
    
    async def broadcast_system_state(self, state: UnifiedSystemState) -> bool:
        """Broadcast system state to all connected systems"""
        try:
            message = CrossSystemMessage(
                message_id=f"state_{int(time.time() * 1000000)}",
                source_system="unified_coordinator",
                target_system="all",
                message_type="system_state_update",
                payload={
                    "consciousness": asdict(state.consciousness) if state.consciousness else None,
                    "agi": asdict(state.agi) if state.agi else None,
                    "timestamp": state.timestamp,
                    "status": state.system_status if isinstance(state.system_status, str) else state.system_status.value
                },
                timestamp=time.time(),
                priority=5
            )
            
            success = await self.send_message(message)
            return success
        except Exception as e:
            logger.error(f"Error broadcasting system state: {e}")
            return False
    
    async def request_consciousness_sync(self, target_node: str) -> Optional[Dict[str, Any]]:
        """Request consciousness state synchronization from a target node"""
        try:
            message = CrossSystemMessage(
                message_id=f"sync_request_{int(time.time() * 1000000)}",
                source_system=self.node_id,
                target_system=target_node,
                message_type="consciousness_sync_request",
                payload={
                    "request_type": "full_sync",
                    "timestamp": time.time()
                },
                timestamp=time.time(),
                priority=3
            )
            
            # Send message and wait for response (simplified)
            await self.send_message(message)
            logger.info(f"Consciousness sync request sent to {target_node}")
            return {"status": "requested", "target": target_node}
        except Exception as e:
            logger.error(f"Error requesting consciousness sync: {e}")
            return None
    
    def get_communication_metrics(self) -> Dict[str, Any]:
        """Get communication performance metrics"""
        return self.metrics.copy()
    
    async def start_message_processing(self):
        """Start background message processing"""
        while self.running:
            try:
                # Process message queue
                if self.message_queue:
                    message = self.message_queue.pop(0)
                    await self._process_queued_message(message)
                
                # Clean up old processed messages
                self._cleanup_processed_messages()
                
                await asyncio.sleep(0.1)  # Prevent busy waiting
            except Exception as e:
                logger.error(f"Error in message processing loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_queued_message(self, message: CrossSystemMessage):
        """Process a queued message"""
        try:
            await self._route_message(message)
        except Exception as e:
            logger.error(f"Error processing queued message {message.message_id}: {e}")
    
    def _cleanup_processed_messages(self):
        """Clean up old processed message IDs to prevent memory growth"""
        try:
            # Keep only recent message IDs (last 10000)
            if len(self.processed_messages) > 10000:
                # Convert to list, sort by timestamp (if we stored timestamps), and remove oldest
                # For simplicity, we'll just clear and rebuild with recent messages
                # In a real implementation, we'd store timestamps with message IDs
                recent_messages = set(list(self.processed_messages)[-5000:])
                self.processed_messages = recent_messages
        except Exception as e:
            logger.error(f"Error cleaning up processed messages: {e}")
    
    async def stop(self):
        """Stop the communicator"""
        self.running = False
        await self.p2p_network.stop()
        logger.info("Cross-System Communicator stopped")


# WebSocket server for real-time communication
class WebSocketCommunicationServer:
    """WebSocket server for real-time cross-system communication"""
    
    def __init__(self, host: str = "localhost", port: int = 8006):
        self.host = host
        self.port = port
        self.communicator = CrossSystemCommunicator("websocket_server")
        self.clients: Dict[str, Any] = {}
        self.running = False
    
    async def start(self):
        """Start the WebSocket server"""
        try:
            await self.communicator.initialize()
            self.running = True
            
            # Start WebSocket server
            server = await websockets.serve(
                self._handle_client, 
                self.host, 
                self.port
            )
            
            logger.info(f"WebSocket Communication Server started on {self.host}:{self.port}")
            
            # Start message processing
            await self.communicator.start_message_processing()
            
            # Keep server running
            await server.wait_closed()
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
    
    async def _handle_client(self, websocket):
        """Handle WebSocket client connections"""
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        self.clients[client_id] = websocket
        logger.info(f"New WebSocket client connected: {client_id}")
        
        try:
            async for message in websocket:
                await self._handle_websocket_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket client disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Error handling WebSocket client {client_id}: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
    
    async def _handle_websocket_message(self, websocket, message: str):
        """Handle incoming WebSocket messages"""
        try:
            # Parse message
            message_data = json.loads(message)
            
            # Convert to CrossSystemMessage
            cross_message = CrossSystemMessage(
                message_id=message_data.get("message_id", f"ws_{int(time.time() * 1000000)}"),
                source_system=message_data.get("source_system", "websocket_client"),
                target_system=message_data.get("target_system", "all"),
                message_type=message_data.get("message_type", "unknown"),
                payload=message_data.get("payload", {}),
                timestamp=message_data.get("timestamp", time.time()),
                priority=message_data.get("priority", 1),
                ttl=message_data.get("ttl", 300)
            )
            
            # Route message
            await self.communicator._route_message(cross_message)
            
            # Broadcast to other clients if needed
            if cross_message.target_system == "all":
                await self._broadcast_to_clients(message, exclude=websocket)
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message received via WebSocket")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
    
    async def _broadcast_to_clients(self, message: str, exclude=None):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
            
        disconnected_clients = []
        for client_id, websocket in self.clients.items():
            if websocket != exclude:
                try:
                    await websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client_id)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {e}")
        
        # Remove disconnected clients
        for client_id in disconnected_clients:
            if client_id in self.clients:
                del self.clients[client_id]
    
    async def stop(self):
        """Stop the WebSocket server"""
        self.running = False
        await self.communicator.stop()
        logger.info("WebSocket Communication Server stopped")


# Example usage
async def example_message_handler(message: CrossSystemMessage):
    """Example message handler"""
    print(f"Received cross-system message: {message.message_type} from {message.source_system}")


async def main():
    """Example usage of the Cross-System Communicator"""
    # Create communicator
    communicator = CrossSystemCommunicator("test_node_1")
    
    try:
        # Initialize
        await communicator.initialize()
        
        # Register message handler
        communicator.register_message_handler("test_message", example_message_handler)
        
        # Create and send a test message
        message = CrossSystemMessage(
            message_id="test_001",
            source_system="metatron",
            target_system="agi",
            message_type="test_message",
            payload={"content": "Hello from Metatron to AGI!"},
            timestamp=time.time(),
            priority=5
        )
        
        # Send message
        success = await communicator.send_message(message)
        print(f"Message sent: {success}")
        
        # Get metrics
        metrics = communicator.get_communication_metrics()
        print(f"Communication metrics: {metrics}")
        
        # Wait a bit to process messages
        await asyncio.sleep(1)
        
    finally:
        await communicator.stop()


if __name__ == "__main__":
    asyncio.run(main())