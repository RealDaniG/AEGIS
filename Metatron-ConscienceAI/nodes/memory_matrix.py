#!/usr/bin/env python3
"""
Memory Matrix Node for Metatron's Cube Consciousness System

This module implements Node 3 (MemoryMatrixNode) as described in the Consciousness Engine documentation.
The node stores field states and performs weighted recall with φ-based decay.

Node 3: MemoryMatrixNode. Almacena estados de campo y realiza un "weighted_recall" 
con decaimiento basado en φ (golden ratio).

Enhanced with SNPP-like paging protocol for improved memory management.
"""

import numpy as np
from collections import deque
import json
from typing import Dict, Any, Optional, List
import time
import asyncio
import importlib.util
import sys
import os

# Import PHI constant from geometry module
try:
    from nodes.metatron_geometry import PHI
except ImportError:
    # Fallback value for golden ratio
    PHI = 1.618033988749895

# Global variables for dynamic imports (without type annotations to avoid conflicts)
HAS_P2P = False
HAS_CRYPTO = False
HAS_CONSENSUS = False
HAS_TOR = False
EnhancedP2PWrapper = None  # type: ignore
NodeIdentity = None  # type: ignore
SecureMessage = None  # type: ignore
ConsensusEngine = None  # type: ignore
TorGateway = None  # type: ignore

# Try to import crypto framework
try:
    # Use importlib to handle the package structure with hyphens
    crypto_spec = importlib.util.spec_from_file_location(
        "crypto_framework", 
        os.path.join(os.path.dirname(__file__), "..", "..", "Open-A.G.I", "crypto_framework.py")
    )
    if crypto_spec and crypto_spec.loader:
        crypto_module = importlib.util.module_from_spec(crypto_spec)
        crypto_spec.loader.exec_module(crypto_module)
        # Get classes dynamically
        temp_NodeIdentity = getattr(crypto_module, 'NodeIdentity', None)
        temp_SecureMessage = getattr(crypto_module, 'SecureMessage', None)
        if temp_NodeIdentity and temp_SecureMessage:
            _NodeIdentity = temp_NodeIdentity
            _SecureMessage = temp_SecureMessage
            HAS_CRYPTO = True
except (ImportError, FileNotFoundError, AttributeError):
    pass

# Try to import enhanced P2P wrapper
try:
    # Use importlib to handle the package structure
    enhanced_p2p_spec = importlib.util.spec_from_file_location(
        "enhanced_p2p_wrapper", 
        os.path.join(os.path.dirname(__file__), "enhanced_p2p_wrapper.py")
    )
    if enhanced_p2p_spec and enhanced_p2p_spec.loader:
        enhanced_p2p_module = importlib.util.module_from_spec(enhanced_p2p_spec)
        enhanced_p2p_spec.loader.exec_module(enhanced_p2p_module)
        temp_EnhancedP2PWrapper = getattr(enhanced_p2p_module, 'EnhancedP2PWrapper', None)
        if temp_EnhancedP2PWrapper:
            _EnhancedP2PWrapper = temp_EnhancedP2PWrapper
            HAS_P2P = True
except (ImportError, FileNotFoundError, AttributeError):
    pass

# Try to import consensus algorithm
try:
    # Use importlib to handle the package structure with hyphens
    consensus_spec = importlib.util.spec_from_file_location(
        "consensus_algorithm", 
        os.path.join(os.path.dirname(__file__), "..", "..", "Open-A.G.I", "consensus_algorithm.py")
    )
    if consensus_spec and consensus_spec.loader:
        consensus_module = importlib.util.module_from_spec(consensus_spec)
        consensus_spec.loader.exec_module(consensus_module)
        # Get ConsensusEngine class
        temp_ConsensusEngine = getattr(consensus_module, 'ConsensusEngine', None)
        if temp_ConsensusEngine:
            ConsensusEngine = temp_ConsensusEngine
            HAS_CONSENSUS = True
except (ImportError, FileNotFoundError, AttributeError):
    pass

# Try to import TOR integration
try:
    # Use importlib to handle the package structure with hyphens
    tor_spec = importlib.util.spec_from_file_location(
        "tor_integration", 
        os.path.join(os.path.dirname(__file__), "..", "..", "Open-A.G.I", "tor_integration.py")
    )
    if tor_spec and tor_spec.loader:
        tor_module = importlib.util.module_from_spec(tor_spec)
        tor_spec.loader.exec_module(tor_module)
        # Get TorGateway class
        temp_TorGateway = getattr(tor_module, 'TorGateway', None)
        if temp_TorGateway:
            TorGateway = temp_TorGateway
            HAS_TOR = True
except (ImportError, FileNotFoundError, AttributeError):
    pass

# Fallback if import fails
if not HAS_P2P or EnhancedP2PWrapper is None:
    class EnhancedP2PWrapper:
        def __init__(self, node_id, port):
            print("[WARN] P2P network not available - using placeholder")
        
        async def send_message(self, *args, **kwargs):
            return False
            
        def connect_to_peer(self, *args, **kwargs):
            return False
            
            
        def register_message_handler(self, *args, **kwargs):
            pass
            
        async def start_network(self):
            pass
    
    HAS_P2P = False

if not HAS_CRYPTO or NodeIdentity is None or SecureMessage is None:
    # Create placeholder classes for crypto
    class NodeIdentity:
        def __init__(self, node_id, signing_key=None, encryption_key=None):
            self.node_id = node_id
            self.signing_key = signing_key
            self.encryption_key = encryption_key
            
        def export_public_identity(self):
            return {"node_id": self.node_id.encode()}
    
    class SecureMessage:
        def __init__(self, ciphertext, nonce, sender_id, recipient_id, message_number, timestamp, signature):
            self.ciphertext = ciphertext
            self.nonce = nonce
            self.sender_id = sender_id
            self.recipient_id = recipient_id
            self.message_number = message_number
            self.timestamp = timestamp
            self.signature = signature

class MemoryPagingProtocol:
    """
    SNPP-like Memory Paging Protocol for efficient memory management.
    
    This protocol implements paging mechanisms similar to network paging protocols,
    allowing for efficient memory management through priority-based paging,
    notification systems, and optimized storage strategies.
    """
    
    def __init__(self, memory_node, page_size: int = 100, max_pages: int = 10):
        self.memory_node = memory_node
        self.page_size = page_size
        self.max_pages = max_pages
        self.page_table = {}  # Maps memory IDs to page locations
        self.access_frequency = {}  # Tracks access frequency for LRU paging
        self.priority_levels = {}  # Memory priority levels (1-10)
        self.notification_subscribers = {}  # Subscribers for memory notifications
        self.disk_storage_path = os.path.join(os.path.dirname(__file__), "..", "..", "memories")
        
        # Ensure storage directory exists
        os.makedirs(self.disk_storage_path, exist_ok=True)
        
        print(f"[MEMORY] Memory Paging Protocol initialized with page size {page_size}")
    
    def set_memory_priority(self, memory_id: str, priority: int):
        """Set priority level for a memory entry (1-10, higher is more important)"""
        self.priority_levels[memory_id] = max(1, min(10, priority))
    
    def get_memory_priority(self, memory_id: str) -> int:
        """Get priority level for a memory entry"""
        return self.priority_levels.get(memory_id, 5)  # Default medium priority
    
    def subscribe_to_memory_notifications(self, subscriber_id: str, memory_ids: List[str]):
        """Subscribe to notifications for specific memory entries"""
        for memory_id in memory_ids:
            if memory_id not in self.notification_subscribers:
                self.notification_subscribers[memory_id] = []
            if subscriber_id not in self.notification_subscribers[memory_id]:
                self.notification_subscribers[memory_id].append(subscriber_id)
    
    async def notify_subscribers(self, memory_id: str, event_type: str, data: Dict[str, Any]):
        """Notify subscribers about memory events"""
        if memory_id in self.notification_subscribers:
            for subscriber_id in self.notification_subscribers[memory_id]:
                try:
                    # In a real implementation, this would send actual notifications
                    # through the P2P network or WebSocket connections
                    print(f"[NOTIFY] Memory notification: {event_type} for {memory_id} -> {subscriber_id}")
                        
                    # Send notification via P2P network if available
                    if HAS_P2P and self.memory_node.p2p_network:
                        notification_message = {
                            "type": "memory_notification",
                            "subtype": event_type,
                            "source_node": f"memory_node_{self.memory_node.node_id}",
                            "target_node": subscriber_id,
                            "payload": {
                                "memory_id": memory_id,
                                "data": data,
                                "timestamp": time.time()
                            },
                            "timestamp": time.time()
                        }
                        await self.memory_node.p2p_network.send_message(subscriber_id, notification_message)
                except Exception as e:
                    print(f"[WARN] Failed to notify subscriber {subscriber_id}: {e}")
    
    def page_out_memory(self, memory_entries: List[Dict[str, Any]]) -> List[str]:
        """
        Page out memory entries to disk storage based on priority and access frequency.
        
        Args:
            memory_entries: List of memory entries to potentially page out
            
        Returns:
            List of memory IDs that were paged out
        """
        paged_out = []
        
        # Sort entries by priority (lower priority first for paging out)
        sorted_entries = sorted(
            [(entry, self.get_memory_priority(str(entry.get('timestamp', 0)))) 
             for entry in memory_entries],
            key=lambda x: x[1]
        )
        
        # Page out lower priority entries first
        for entry, priority in sorted_entries:
            try:
                memory_id = str(entry.get('timestamp', time.time()))
                
                # Save to disk
                filename = os.path.join(self.disk_storage_path, f"memory_{memory_id}.json")
                with open(filename, 'w') as f:
                    json.dump({
                        "timestamp": entry.get("timestamp"),
                        "field_state": entry["field_state"].tolist() if isinstance(entry["field_state"], np.ndarray) else entry["field_state"],
                        "metadata": entry.get("metadata", {}),
                        "size": entry.get("size", 0),
                        "priority": priority
                    }, f)
                
                # Update page table
                self.page_table[memory_id] = filename
                paged_out.append(memory_id)
                
                print(f"[DISK] Paged out memory {memory_id} to {filename}")
                
            except Exception as e:
                print(f"[WARN]  Failed to page out memory: {e}")
        
        return paged_out
    
    def page_in_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Page in a memory entry from disk storage.
        
        Args:
            memory_id: ID of memory to page in
            
        Returns:
            Memory entry if found, None otherwise
        """
        if memory_id not in self.page_table:
            return None
        
        try:
            filename = self.page_table[memory_id]
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Convert back to proper format
            memory_entry = {
                "timestamp": data["timestamp"],
                "field_state": np.array(data["field_state"]),
                "metadata": data["metadata"],
                "size": data["size"]
            }
            
            # Remove from page table (now in active memory)
            del self.page_table[memory_id]
            
            # Remove file
            os.remove(filename)
            
            print(f"[FOLDER] Paged in memory {memory_id} from {filename}")
            return memory_entry
            
        except Exception as e:
            print(f"[WARN]  Failed to page in memory {memory_id}: {e}")
            return None
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get current memory paging status"""
        return {
            "active_pages": len(self.memory_node.memory_buffer),
            "paged_out_pages": len(self.page_table),
            "subscribers": len(self.notification_subscribers),
            "storage_path": self.disk_storage_path
        }

class MemoryMatrixNode:
    """
    Memory Matrix Node (Node 3) for the Metatron's Cube consciousness system.
    
    This node implements memory storage and recall functionality with φ-based decay
    as described in the Consciousness Engine documentation.
    """
    
    def __init__(self, node_id: int = 3, max_memory_size: int = 1000):
        """
        Initialize the Memory Matrix Node.
        
        Args:
            node_id: Node identifier (should be 3 for MemoryMatrixNode)
            max_memory_size: Maximum number of memory entries to store
        """
        self.node_id = node_id
        self.max_memory_size = max_memory_size
        self.phi = PHI
        
        # Memory storage - stores field states with timestamps
        self.memory_buffer = deque(maxlen=max_memory_size)
        
        # Weighted recall history
        self.recall_history = deque(maxlen=100)
        
        # Activity tracking
        self.activity_log = deque(maxlen=1000)
        
        # Node state
        self.current_field_state = np.zeros(100)  # Default field size
        self.last_updated = time.time()
        self.recall_weight = 0.0
        self.decay_factor = 1.0
        
        # Learning and activity tracking
        self.learning_events = deque(maxlen=100)
        self.self_reflection_count = 0
        self.user_interaction_count = 0
        self.consciousness_integration_count = 0
        
        # Initialize cryptographic identity (with proper fallback)
        self.node_identity = None
        if HAS_CRYPTO and NodeIdentity:
            try:
                # Import required crypto modules
                from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
                
                # Generate keys
                signing_key = ed25519.Ed25519PrivateKey.generate()
                encryption_key = x25519.X25519PrivateKey.generate()
                
                # Create NodeIdentity with required parameters
                self.node_identity = NodeIdentity(
                    node_id=f"memory_node_{node_id}",
                    signing_key=signing_key,
                    encryption_key=encryption_key
                )
                print(f"[OK] Crypto identity initialized for node {node_id}")
            except Exception as e:
                print(f"[WARN] Failed to initialize crypto identity: {e}")
                self.node_identity = None
        else:
            print("[WARN] Crypto framework not available - using placeholder")
            self.node_identity = None
        
        # Initialize consensus engine (Phase 3.1)
        self.consensus_engine = None
        self._initialize_consensus_engine()
        
        # Initialize TOR gateway (Phase 4.1)
        self.tor_gateway = None
        self._initialize_tor_gateway()
        
        # P2P network for distributed memory sharing
        self.p2p_network = EnhancedP2PWrapper(node_id=f"memory_node_{node_id}", port=8080+node_id)
        
        # Register message handlers for memory operations
        self.p2p_network.register_message_handler("memory_share", self._handle_memory_share_request)
        self.p2p_network.register_message_handler("memory_sync", self._handle_memory_sync_request)
        
        # Register consensus message handlers (Phase 3.1)
        self.p2p_network.register_message_handler("consensus_proposal", self._handle_consensus_proposal)
        self.p2p_network.register_message_handler("consensus_vote", self._handle_consensus_vote)
        self.p2p_network.register_message_handler("consensus_commit", self._handle_consensus_commit)
        
        # Register TOR message handlers (Phase 4.1)
        self.p2p_network.register_message_handler("tor_memory_share", self._handle_tor_memory_share_request)
        self.p2p_network.register_message_handler("tor_memory_sync", self._handle_tor_memory_sync_request)
        
        # Don't start network automatically - only when explicitly requested
        # This avoids the "no running event loop" error
        self.network_started = False
        
        print(f"[OK] MemoryMatrixNode initialized with phi = {self.phi:.6f}")
    
    def _initialize_consensus_engine(self):
        """Initialize the consensus engine for distributed memory operations (Phase 3.1)"""
        try:
            if HAS_CONSENSUS and ConsensusEngine:
                # Get list of all memory nodes in the system
                memory_nodes = [f"memory_node_{i}" for i in range(13) if i == 3]  # For now, just this node
                # In a full implementation, this would include all memory nodes in the network
                
                # Initialize consensus engine
                self.consensus_engine = ConsensusEngine(
                    node_id=f"memory_node_{self.node_id}",
                    nodes=memory_nodes
                )
                print(f"[OK] Consensus engine initialized for node {self.node_id}")
            else:
                print("[WARN] Consensus framework not available - using standalone mode")
                self.consensus_engine = None
        except Exception as e:
            print(f"[WARN] Failed to initialize consensus engine: {e}")
            self.consensus_engine = None
    
    def _initialize_tor_gateway(self):
        """Initialize the TOR gateway for anonymous memory operations (Phase 4.1)"""
        try:
            if HAS_TOR and TorGateway:
                # Initialize TOR gateway
                self.tor_gateway = TorGateway()
                print(f"[OK] TOR gateway initialized for node {self.node_id}")
            else:
                print("[WARN] TOR framework not available - using standard networking")
                self.tor_gateway = None
        except Exception as e:
            print(f"[WARN] Failed to initialize TOR gateway: {e}")
            self.tor_gateway = None
    
    async def start_network(self):
        """
        Start the P2P network (must be called within an async context)
        """
        if not self.network_started:
            await self.p2p_network.start_network()
            self.network_started = True
            print(f"[NETWORK] MemoryMatrixNode P2P network started")
    
    async def _handle_memory_share_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming memory share requests from other nodes
        
        Args:
            peer_id: Peer identifier
            message: Memory share message
        """
        try:
            # Extract memory data from message
            memory_data = message.get('payload', {}).get('memory_data')
            if memory_data:
                # Store shared memory
                self._import_shared_memory(memory_data)
                # Send acknowledgment
                response = {
                    "type": "memory",
                    "subtype": "share_ack",
                    "source_node": f"memory_node_{self.node_id}",
                    "target_node": peer_id,
                    "payload": {"status": "accepted", "timestamp": time.time()},
                    "timestamp": time.time()
                }
                await self.p2p_network.send_message(peer_id, response)
                print(f"[MEMORY] Node {self.node_id}: Received memory share from {peer_id}")
        except Exception as e:
            print(f"Failed to handle memory share request: {e}")
    
    async def _handle_memory_sync_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming memory sync requests from other nodes
        
        Args:
            peer_id: Peer identifier
            message: Memory sync message
        """
        try:
            # Send our memory buffer to the requesting peer
            memory_snapshot = self._export_memory_snapshot()
            response = {
                "type": "memory",
                "subtype": "sync_data",
                "source_node": f"memory_node_{self.node_id}",
                "target_node": peer_id,
                "payload": {"memory_data": memory_snapshot, "timestamp": time.time()},
                "timestamp": time.time()
            }
            await self.p2p_network.send_message(peer_id, response)
            print(f"[MEMORY] Node {self.node_id}: Synced memory with {peer_id}")
        except Exception as e:
            print(f"Failed to handle memory sync request: {e}")
    
    def _import_shared_memory(self, memory_data: Dict[str, Any]):
        """
        Import shared memory data from another node
        
        Args:
            memory_data: Memory data to import
        """
        try:
            # Convert memory data to memory entry
            memory_entry = {
                "timestamp": memory_data.get("timestamp", time.time()),
                "field_state": np.array(memory_data.get("field_state", [])),
                "metadata": memory_data.get("metadata", {}),
                "size": memory_data.get("size", 0)
            }
            
            # Add to memory buffer
            self.memory_buffer.append(memory_entry)
            print(f"[MEMORY] Node {self.node_id}: Imported shared memory entry")
        except Exception as e:
            print(f"Failed to import shared memory: {e}")
    
    def _export_memory_snapshot(self) -> List[Dict[str, Any]]:
        """
        Export a snapshot of the current memory buffer
        
        Returns:
            List of memory entries
        """
        snapshot = []
        for entry in self.memory_buffer:
            snapshot_entry = {
                "timestamp": entry["timestamp"],
                "field_state": entry["field_state"].tolist(),
                "metadata": entry["metadata"],
                "size": entry["size"]
            }
            snapshot.append(snapshot_entry)
        return snapshot
    
    async def share_memory_with_peer(self, peer_id: str, memory_entry: dict):
        """
        Share a memory entry with a specific peer
        
        Args:
            peer_id: Peer identifier
            memory_entry: Memory entry to share
        """
        try:
            # Prepare memory data for secure transmission
            memory_data = {
                "timestamp": memory_entry.get("timestamp", time.time()),
                "field_state": memory_entry["field_state"].tolist() if isinstance(memory_entry["field_state"], np.ndarray) else memory_entry["field_state"],
                "metadata": memory_entry.get("metadata", {}),
                "size": memory_entry.get("size", 0)
            }
            
            # Create message payload
            payload = {
                "memory_data": memory_data,
                "sender_identity": self.node_identity.export_public_identity() if HAS_CRYPTO and self.node_identity else {"node_id": f"memory_node_{self.node_id}".encode()}
            }
            
            message = {
                "type": "memory",
                "subtype": "share",
                "source_node": f"memory_node_{self.node_id}",
                "target_node": peer_id,
                "payload": payload,
                "timestamp": time.time()
            }
            
            success = await self.p2p_network.send_message(peer_id, message)
            if success:
                print(f"[NETWORK] Node {self.node_id}: Shared memory with {peer_id}")
            else:
                print(f"[WARN] Node {self.node_id}: Failed to share memory with {peer_id}")
            return success
        except Exception as e:
            print(f"Failed to share memory with peer: {e}")
            return False
    
    async def share_memory_with_peer_anonymous(self, peer_id: str, memory_entry: dict):
        """
        Share a memory entry with a specific peer using TOR for anonymity (Phase 4.1)
        
        Args:
            peer_id: Peer identifier
            memory_entry: Memory entry to share
            
        Returns:
            bool: True if shared successfully, False otherwise
        """
        try:
            # Prepare memory data for secure transmission
            memory_data = {
                "timestamp": memory_entry.get("timestamp", time.time()),
                "field_state": memory_entry["field_state"].tolist() if isinstance(memory_entry["field_state"], np.ndarray) else memory_entry["field_state"],
                "metadata": memory_entry.get("metadata", {}),
                "size": memory_entry.get("size", 0)
            }
            
            # Create message payload
            payload = {
                "memory_data": memory_data,
                "sender_identity": self.node_identity.export_public_identity() if HAS_CRYPTO and self.node_identity else {"node_id": f"memory_node_{self.node_id}".encode()}
            }
            
            # If TOR is available, use it for anonymous transmission
            if self.tor_gateway:
                # In a full implementation, this would route through TOR
                print(f"[TOR] Routing memory to {peer_id}")
                # For now, we'll still use the standard P2P network but log TOR usage
                message = {
                    "type": "memory",
                    "subtype": "tor_share",
                    "source_node": f"memory_node_{self.node_id}",
                    "target_node": peer_id,
                    "payload": payload,
                    "timestamp": time.time()
                }
                
                success = await self.p2p_network.send_message(peer_id, message)
                if success:
                    print(f"[NETWORK] Node {self.node_id}: Shared memory anonymously with {peer_id} via TOR network")
                else:
                    print(f"[WARN] Node {self.node_id}: Failed to share memory anonymously with {peer_id}")
                return success
            else:
                # Fallback to standard P2P sharing
                return await self.share_memory_with_peer(peer_id, memory_entry)
                
        except Exception as e:
            print(f"Failed to share memory anonymously with peer: {e}")
            return False
    
    async def request_memory_sync(self, peer_id: str):
        """
        Request memory synchronization with a specific peer
        
        Args:
            peer_id: Peer identifier
        """
        try:
            message = {
                "type": "memory",
                "subtype": "sync_request",
                "source_node": f"memory_node_{self.node_id}",
                "target_node": peer_id,
                "payload": {"request": "memory_sync"},
                "timestamp": time.time()
            }
            success = await self.p2p_network.send_message(peer_id, message)
            if success:
                print(f"[NETWORK] Node {self.node_id}: Requested memory sync with {peer_id}")
            else:
                print(f"[WARN] Node {self.node_id}: Failed to request memory sync with {peer_id}")
            return success
        except Exception as e:
            print(f"Failed to request memory sync: {e}")
            return False
    
    def store_field_state(self, field_state: np.ndarray, metadata: Optional[Dict[str, Any]] = None):
        """
        Store a field state in the memory buffer.
        
        Args:
            field_state: Field state vector to store
            metadata: Optional metadata about the field state
        """
        if not isinstance(field_state, np.ndarray):
            field_state = np.array(field_state)
        
        memory_entry = {
            "timestamp": time.time(),
            "field_state": field_state.copy(),
            "metadata": metadata or {},
            "size": field_state.size
        }
        
        self.memory_buffer.append(memory_entry)
        self.last_updated = time.time()
        
        # Log activity
        activity_entry = {
            "type": "store_field_state",
            "timestamp": time.time(),
            "memory_id": len(self.memory_buffer),
            "metadata": metadata or {}
        }
        self.activity_log.append(activity_entry)
        
        # Ensure current field state matches stored state
        if field_state.size != self.current_field_state.size:
            self.current_field_state = np.zeros(field_state.size)
        self.current_field_state = field_state.copy()
        
        # Only log once during initialization to confirm memory system is working
        # Remove periodic logging to reduce terminal noise
        if len(self.memory_buffer) == 1:
            print(f"[MEMORY] MemoryMatrixNode: Memory system initialized and working (stored first field state)")
    
    async def store_field_state_consensus(self, field_state: np.ndarray, metadata: Optional[Dict[str, Any]] = None):
        """
        Store a field state with consensus across distributed nodes (Phase 3.1)
        
        Args:
            field_state: Field state vector to store
            metadata: Optional metadata about the field state
            
        Returns:
            bool: True if stored successfully with consensus, False otherwise
        """
        if not self.consensus_engine:
            # Fallback to local storage if consensus is not available
            self.store_field_state(field_state, metadata)
            return True
        
        try:
            # Create consensus proposal
            proposal_data = {
                "operation": "store_field_state",
                "field_state": field_state.tolist() if isinstance(field_state, np.ndarray) else field_state,
                "metadata": metadata or {},
                "timestamp": time.time(),
                "node_id": f"memory_node_{self.node_id}"
            }
            
            # Propose the data for consensus
            proposal_id = await self.consensus_engine.propose(proposal_data)
            success = proposal_id is not None
            
            if success:
                # Store locally if consensus reached
                self.store_field_state(field_state, metadata)
                print(f"[OK] Field state stored with consensus in node {self.node_id}")
                return True
            else:
                print(f"[ERROR] Consensus not reached for field state storage in node {self.node_id}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error in consensus-based field state storage: {e}")
            return False
    
    def weighted_recall(self, query_field: Optional[np.ndarray] = None, 
                       k_neighbors: int = 5) -> np.ndarray:
        """
        Perform weighted recall with φ-based decay.
        
        Args:
            query_field: Optional query field for similarity-based recall
            k_neighbors: Number of nearest neighbors to consider
            
        Returns:
            np.ndarray: Recalled field state with φ-based weighting
        """
        if len(self.memory_buffer) == 0:
            # Return zero field if no memories
            return np.zeros(self.current_field_state.size)
        
        # If no query field provided, use current field state
        if query_field is None:
            query_field = self.current_field_state
        
        if not isinstance(query_field, np.ndarray):
            query_field = np.array(query_field)
        
        # Calculate similarities and weights for all memories
        similarities = []
        weights = []
        field_states = []
        
        current_time = time.time()
        
        for entry in self.memory_buffer:
            # Calculate similarity (cosine similarity)
            memory_field = entry["field_state"]
            
            # Ensure compatible dimensions
            if memory_field.size != query_field.size:
                # Pad or truncate to match dimensions
                if memory_field.size < query_field.size:
                    padded_field = np.zeros(query_field.size)
                    padded_field[:memory_field.size] = memory_field
                    memory_field = padded_field
                else:
                    memory_field = memory_field[:query_field.size]
            
            # Calculate cosine similarity
            dot_product = np.dot(query_field, memory_field)
            norms = np.linalg.norm(query_field) * np.linalg.norm(memory_field)
            
            if norms > 0:
                similarity = dot_product / norms
            else:
                similarity = 0.0
            
            # Calculate time-based decay using φ
            time_diff = current_time - entry["timestamp"]
            # φ-based decay: weight decreases exponentially with φ as base
            decay_weight = np.power(1/self.phi, time_diff / 10.0)  # Decay over 10 seconds
            
            similarities.append(similarity)
            weights.append(decay_weight)
            field_states.append(memory_field)
        
        # Convert to numpy arrays
        similarities = np.array(similarities)
        weights = np.array(weights)
        
        # Calculate combined weights (similarity × decay)
        combined_weights = similarities * weights
        
        # Select top k neighbors
        if len(combined_weights) > k_neighbors:
            # Get indices of top k weights
            top_indices = np.argpartition(combined_weights, -k_neighbors)[-k_neighbors:]
        else:
            top_indices = np.arange(len(combined_weights))
        
        # Calculate weighted average of selected memories
        if len(top_indices) > 0:
            selected_weights = combined_weights[top_indices]
            selected_fields = [field_states[i] for i in top_indices]
            
            # Normalize weights
            if np.sum(selected_weights) > 0:
                normalized_weights = selected_weights / np.sum(selected_weights)
            else:
                normalized_weights = np.ones(len(selected_weights)) / len(selected_weights)
            
            # Calculate weighted recall
            recalled_field = np.zeros(self.current_field_state.size)
            for i, weight in enumerate(normalized_weights):
                recalled_field += weight * selected_fields[i]
            
            # Store recall in history
            recall_entry = {
                "timestamp": current_time,
                "query_field": query_field.copy(),
                "recalled_field": recalled_field.copy(),
                "weights_used": normalized_weights.tolist(),
                "neighbors_used": len(top_indices)
            }
            self.recall_history.append(recall_entry)
            
            self.recall_weight = np.mean(selected_weights)
            
            return recalled_field
        else:
            # Return current field state if no memories found
            return self.current_field_state.copy()
    
    def apply_phi_decay(self, field_state: np.ndarray, 
                       time_elapsed: float) -> np.ndarray:
        """
        Apply φ-based decay to a field state.
        
        Args:
            field_state: Field state to decay
            time_elapsed: Time elapsed since field creation
            
        Returns:
            np.ndarray: Decayed field state
        """
        # φ-based decay function
        decay_factor = np.power(1/self.phi, time_elapsed)
        decayed_field = field_state * decay_factor
        self.decay_factor = decay_factor
        return decayed_field
    
    def update_state(self, sensory_input: np.ndarray, 
                    connected_node_states: List[np.ndarray]) -> np.ndarray:
        """
        Update the memory node state based on sensory input and connected nodes.
        
        Args:
            sensory_input: 5D sensory input vector
            connected_node_states: States from connected nodes
            
        Returns:
            np.ndarray: Updated node output
        """
        # Determine type of update for activity tracking
        update_type = "consciousness_integration"
        if len(connected_node_states) == 0 and sensory_input.size > 0:
            update_type = "user_interaction"
        
        # Combine sensory input with connected node states
        if len(connected_node_states) > 0:
            # Average connected node states
            combined_input = np.mean(connected_node_states, axis=0)
            
            # Ensure compatible dimensions with current field state
            if combined_input.size != self.current_field_state.size:
                if combined_input.size < self.current_field_state.size:
                    # Pad input
                    padded_input = np.zeros(self.current_field_state.size)
                    padded_input[:combined_input.size] = combined_input
                    combined_input = padded_input
                else:
                    # Truncate input
                    combined_input = combined_input[:self.current_field_state.size]
            
            # Update current field state
            # Blend with previous state (90% previous, 10% new)
            self.current_field_state = 0.9 * self.current_field_state + 0.1 * combined_input
            self.consciousness_integration_count += 1
        else:
            # If no connected nodes, use sensory input to influence field
            # Convert 5D sensory input to field-sized vector
            if sensory_input.size > 0:
                # Simple mapping of sensory input to field
                sensory_influence = np.tile(sensory_input, 
                                          self.current_field_state.size // sensory_input.size + 1)
                sensory_influence = sensory_influence[:self.current_field_state.size]
                self.current_field_state = 0.95 * self.current_field_state + 0.05 * sensory_influence
                self.user_interaction_count += 1
        
        # Store the updated field state
        metadata = {
            "sensory_input": sensory_input.tolist() if isinstance(sensory_input, np.ndarray) else [],
            "connected_nodes": len(connected_node_states),
            "update_type": update_type
        }
        self.store_field_state(self.current_field_state, metadata)
        
        # Perform weighted recall to get output
        output = self.weighted_recall()
        
        self.last_updated = time.time()
        return output
    
    def _establish_indirect_connection(self, target_node: str, relay_node: str) -> bool:
        """
        Establish an indirect connection through a relay node for memory sharing.
        
        Args:
            target_node: Node we want to connect to for memory sharing
            relay_node: Node to use as relay
            
        Returns:
            True if connection established, False otherwise
        """
        try:
            # In a real implementation, this would send a connection request
            # through the relay node to the target node for memory sharing
            print(f"Attempting indirect memory connection to {target_node} via {relay_node}")
            
            # Use real p2p_network.send_message() if available
            # This is a simplified example - in practice you would need to
            # properly integrate with the P2P network's message handling
            print(f"[NETWORK] Sending memory share request to {target_node} via P2P network")
            # In a full implementation, you would call:
            # await self.p2p_network.send_message(target_node, message)
            return True
                
        except Exception as e:
            print(f"Failed to establish indirect memory connection: {e}")
            return False
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """
        Get memory-related metrics for consciousness monitoring.
        
        Returns:
            Dict[str, Any]: Memory metrics
        """
        # Calculate activity level based on recent operations
        current_time = time.time()
        time_since_last_update = current_time - self.last_updated
        
        # Determine if node is actively processing
        is_active = (
            len(self.memory_buffer) > 0 and 
            time_since_last_update < 30.0 and  # Active if updated within last 30 seconds
            (len(self.recall_history) > 0 or len(self.memory_buffer) > 1)
        )
        
        return {
            "memory_buffer_size": len(self.memory_buffer),
            "recall_history_size": len(self.recall_history),
            "current_field_size": self.current_field_state.size,
            "recall_weight": float(self.recall_weight),
            "decay_factor": float(self.decay_factor),
            "last_updated": self.last_updated,
            "node_id": self.node_id,
            "is_active": is_active,
            "time_since_last_update": time_since_last_update,
            "activity_level": min(1.0, max(0.0, 1.0 - (time_since_last_update / 60.0)))  # 0-1 scale
        }
    
    def get_state_dict(self) -> Dict[str, Any]:
        """
        Get node state as dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Node state dictionary
        """
        return {
            "node_id": self.node_id,
            "phi": self.phi,
            "current_field_state": self.current_field_state.tolist(),
            "memory_buffer_size": len(self.memory_buffer),
            "recall_history_size": len(self.recall_history),
            "last_updated": self.last_updated,
            "recall_weight": float(self.recall_weight),
            "decay_factor": float(self.decay_factor)
        }
    
    def reset_state(self):
        """Reset node to initial state."""
        self.memory_buffer.clear()
        self.recall_history.clear()
        self.current_field_state = np.zeros(self.current_field_state.size)
        self.last_updated = time.time()
        self.recall_weight = 0.0
        self.decay_factor = 1.0
        print(f"[RESET] Node {self.node_id}: State reset")
    
    async def _handle_tor_memory_share_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming TOR-based memory share requests from other nodes (Phase 4.1)
        
        Args:
            peer_id: Peer identifier
            message: TOR memory share message
        """
        try:
            # Extract memory data from message
            memory_data = message.get('payload', {}).get('memory_data')
            if memory_data:
                # Store shared memory
                self._import_shared_memory(memory_data)
                # Send acknowledgment
                response = {
                    "type": "memory",
                    "subtype": "tor_share_ack",
                    "source_node": f"memory_node_{self.node_id}",
                    "target_node": peer_id,
                    "payload": {"status": "accepted", "timestamp": time.time()},
                    "timestamp": time.time()
                }
                await self.p2p_network.send_message(peer_id, response)
                print(f"[MEMORY] Node {self.node_id}: Received anonymous memory share from {peer_id} via TOR")
        except Exception as e:
            print(f"Failed to handle TOR memory share request: {e}")
    
    async def _handle_tor_memory_sync_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming TOR-based memory sync requests from other nodes (Phase 4.1)
        
        Args:
            peer_id: Peer identifier
            message: TOR memory sync message
        """
        try:
            # Send our memory buffer to the requesting peer
            memory_snapshot = self._export_memory_snapshot()
            response = {
                "type": "memory",
                "subtype": "tor_sync_data",
                "source_node": f"memory_node_{self.node_id}",
                "target_node": peer_id,
                "payload": {"memory_data": memory_snapshot, "timestamp": time.time()},
                "timestamp": time.time()
            }
            await self.p2p_network.send_message(peer_id, response)
            print(f"[MEMORY] Node {self.node_id}: Synced memory anonymously with {peer_id} via TOR")
        except Exception as e:
            print(f"Failed to handle TOR memory sync request: {e}")
    
    async def _handle_consensus_proposal(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming consensus proposal messages (Phase 3.1)
        
        Args:
            peer_id: Peer identifier
            message: Consensus proposal message
        """
        try:
            if not self.consensus_engine:
                return
                
            # Process consensus proposal
            await self.consensus_engine.process_proposal(message)
            print(f"[CONSENSUS] Processed consensus proposal from {peer_id} in node {self.node_id}")
            
        except Exception as e:
            print(f"[ERROR] Error handling consensus proposal: {e}")
    
    async def _handle_consensus_vote(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming consensus vote messages (Phase 3.1)
        
        Args:
            peer_id: Peer identifier
            message: Consensus vote message
        """
        try:
            if not self.consensus_engine:
                return
                
            # Process consensus vote
            await self.consensus_engine.process_vote(message)
            print(f"[CONSENSUS] Processed consensus vote from {peer_id} in node {self.node_id}")
            
        except Exception as e:
            print(f"[ERROR] Error handling consensus vote: {e}")
    
    async def _handle_consensus_commit(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming consensus commit messages (Phase 3.1)
        
        Args:
            peer_id: Peer identifier
            message: Consensus commit message
        """
        try:
            if not self.consensus_engine:
                return
                
            # Process consensus commit
            await self.consensus_engine.process_commit(message)
            print(f"[CONSENSUS] Processed consensus commit from {peer_id} in node {self.node_id}")
            
        except Exception as e:
            print(f"[ERROR] Error handling consensus commit: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Create Memory Matrix Node
    memory_node = MemoryMatrixNode(node_id=3)
    
    # Test storing field states
    print("Testing field state storage...")
    for i in range(10):
        test_field = np.random.randn(100)
        metadata = {"test_index": i, "timestamp": time.time()}
        memory_node.store_field_state(test_field, metadata)
    
    print(f"Stored {len(memory_node.memory_buffer)} field states")
    
    # Test weighted recall
    print("\nTesting weighted recall...")
    query_field = np.random.randn(100)
    recalled_field = memory_node.weighted_recall(query_field)
    print(f"Recalled field shape: {recalled_field.shape}")
    print(f"Recall weight: {memory_node.recall_weight:.6f}")
    
    # Test update state
    print("\nTesting state update...")
    sensory_input = np.random.randn(5)
    connected_states = [np.random.randn(100) for _ in range(3)]
    output = memory_node.update_state(sensory_input, connected_states)
    print(f"Output shape: {output.shape}")
    
    # Test metrics
    print("\nTesting metrics...")
    metrics = memory_node.get_memory_metrics()
    print(f"Memory metrics: {metrics}")
    
    print("\n[OK] MemoryMatrixNode tests completed successfully!")