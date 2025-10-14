"""
Node Matrix Manager for AEGIS-Conscience Network
Creates full mesh connectivity between all nodes in the network
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict, field

from network.p2p import PeerInfo
from schemas import NetworkMessage


@dataclass
class NodeInfo:
    """Information about a network node"""
    node_id: str
    ip_address: str
    port: int
    public_key: str
    onion_address: Optional[str] = None
    last_seen: float = 0.0
    status: str = "unknown"  # unknown, online, offline, connecting
    connections: Set[str] = field(default_factory=set)


class NodeMatrixManager:
    """Manages full mesh connectivity between all nodes in the network"""
    
    def __init__(self, local_node_id: str, p2p_network):
        self.local_node_id = local_node_id
        self.p2p_network = p2p_network
        self.known_nodes: Dict[str, NodeInfo] = {}
        self.connection_matrix: Dict[str, Set[str]] = {}  # node_id -> set of connected nodes
        self.running = False
        self.discovery_interval = 30  # seconds
        self.connection_check_interval = 10  # seconds
        
    def add_known_node(self, node_info: NodeInfo):
        """Add a known node to the matrix"""
        self.known_nodes[node_info.node_id] = node_info
        if node_info.node_id not in self.connection_matrix:
            self.connection_matrix[node_info.node_id] = set()
        print(f"📍 Added known node: {node_info.node_id}")
    
    def remove_known_node(self, node_id: str):
        """Remove a known node from the matrix"""
        if node_id in self.known_nodes:
            del self.known_nodes[node_id]
        if node_id in self.connection_matrix:
            del self.connection_matrix[node_id]
        print(f"🗑️  Removed known node: {node_id}")
    
    async def start_matrix_management(self):
        """Start the node matrix management"""
        self.running = True
        print("🔄 Starting node matrix management...")
        
        # Start background tasks
        asyncio.create_task(self._discovery_loop())
        asyncio.create_task(self._connection_management_loop())
        
    async def stop_matrix_management(self):
        """Stop the node matrix management"""
        self.running = False
        print("⏹️  Stopped node matrix management")
    
    async def _discovery_loop(self):
        """Periodically discover and update node information"""
        while self.running:
            try:
                await self._discover_nodes()
                await asyncio.sleep(self.discovery_interval)
            except Exception as e:
                print(f"⚠️  Error in discovery loop: {e}")
                await asyncio.sleep(5)
    
    async def _connection_management_loop(self):
        """Periodically manage connections to maintain full mesh"""
        while self.running:
            try:
                await self._maintain_full_mesh()
                await asyncio.sleep(self.connection_check_interval)
            except Exception as e:
                print(f"⚠️  Error in connection management loop: {e}")
                await asyncio.sleep(5)
    
    async def _discover_nodes(self):
        """Discover nodes in the network"""
        print("🔍 Discovering nodes...")
        
        # In a real implementation, this would use various discovery mechanisms:
        # 1. Bootstrap nodes
        # 2. Peer exchange protocols
        # 3. Registry services
        # 4. Broadcast discovery
        
        # For now, we'll simulate discovery by checking existing peers
        current_peers = self.p2p_network.peers
        for peer_id, peer_info in current_peers.items():
            if peer_id not in self.known_nodes:
                node_info = NodeInfo(
                    node_id=peer_info.peer_id,
                    ip_address=peer_info.ip_address,
                    port=peer_info.port,
                    public_key=peer_info.public_key,
                    last_seen=peer_info.last_seen,
                    status=peer_info.connection_status
                )
                self.add_known_node(node_info)
            else:
                # Update existing node info
                self.known_nodes[peer_id].last_seen = peer_info.last_seen
                self.known_nodes[peer_id].status = peer_info.connection_status
        
        print(f"   Found {len(self.known_nodes)} known nodes")
    
    async def _maintain_full_mesh(self):
        """Maintain full mesh connectivity between all nodes"""
        print("🔗 Maintaining full mesh connectivity...")
        
        # Ensure we're connected to all known nodes
        for node_id, node_info in self.known_nodes.items():
            if node_id == self.local_node_id:
                continue  # Skip self
            
            # Check if we're already connected
            if self._is_connected_to(node_id):
                print(f"   [OK] Already connected to {node_id}")
                continue
            
            # Try to connect
            print(f"   📡 Connecting to {node_id}...")
            await self._connect_to_node(node_info)
        
        # Update connection matrix
        self._update_connection_matrix()
        
        # Report matrix status
        await self._report_matrix_status()
    
    def _is_connected_to(self, node_id: str) -> bool:
        """Check if we're connected to a specific node"""
        return node_id in self.p2p_network.peer_connections
    
    async def _connect_to_node(self, node_info: NodeInfo):
        """Connect to a specific node"""
        try:
            # Create peer info for connection
            peer_info = PeerInfo(
                peer_id=node_info.node_id,
                ip_address=node_info.ip_address,
                port=node_info.port,
                public_key=node_info.public_key,
                last_seen=time.time(),
                connection_status="connecting",
                reputation_score=0.8,  # Default reputation
                latency=0.1  # Default latency
            )
            
            # Attempt connection
            success = await self.p2p_network.connect_to_peer(peer_info)
            if success:
                print(f"   ✅ Connected to {node_info.node_id}")
                node_info.status = "online"
                node_info.last_seen = time.time()
            else:
                print(f"   ❌ Failed to connect to {node_info.node_id}")
                node_info.status = "offline"
                
        except Exception as e:
            print(f"   ❌ Error connecting to {node_info.node_id}: {e}")
            node_info.status = "offline"
    
    def _update_connection_matrix(self):
        """Update the connection matrix with current connections"""
        # Clear current connections for this node
        self.connection_matrix[self.local_node_id] = set()
        
        # Add all current connections
        for peer_id in self.p2p_network.peer_connections.keys():
            self.connection_matrix[self.local_node_id].add(peer_id)
    
    async def _report_matrix_status(self):
        """Report the current status of the connection matrix"""
        total_nodes = len(self.known_nodes)
        if total_nodes == 0:
            return
            
        # Count connections for this node
        local_connections = len(self.connection_matrix.get(self.local_node_id, set()))
        
        # Calculate connectivity percentage
        connectivity = (local_connections / (total_nodes - 1)) * 100 if total_nodes > 1 else 100
        
        print(f"📊 Matrix Status: {local_connections}/{total_nodes-1} connections ({connectivity:.1f}% connectivity)")
        
        # Report detailed connections
        if self.connection_matrix.get(self.local_node_id):
            connected_nodes = ", ".join(self.connection_matrix[self.local_node_id])
            print(f"   Connected to: {connected_nodes}")
    
    def get_connection_matrix(self) -> Dict[str, Set[str]]:
        """Get the current connection matrix"""
        return self.connection_matrix.copy()
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get network topology information"""
        # Update connection status for all nodes
        for node_id, node_info in self.known_nodes.items():
            if node_id in self.p2p_network.peers:
                peer_info = self.p2p_network.peers[node_id]
                node_info.status = peer_info.connection_status
                node_info.last_seen = peer_info.last_seen
        
        # Convert sets to lists for JSON serialization
        connection_matrix = {}
        for k, v in self.connection_matrix.items():
            connection_matrix[k] = list(v) if isinstance(v, set) else v
        
        return {
            'total_nodes': len(self.known_nodes),
            'local_node_id': self.local_node_id,
            'local_connections': len(self.connection_matrix.get(self.local_node_id, set())),
            'connection_matrix': connection_matrix,
            'known_nodes': {k: asdict(v) for k, v in self.known_nodes.items()}
        }
    
    async def broadcast_matrix_update(self):
        """Broadcast matrix update to all connected nodes"""
        try:
            # Create matrix update message
            topology = self.get_network_topology()
            message = NetworkMessage(
                message_id=f"matrix_update_{int(time.time()*1000000)}",
                sender_id=self.local_node_id,
                recipient_id="*",
                message_type="matrix_update",
                payload=topology,
                timestamp=time.time()
            )
            
            # Broadcast to all connected peers
            for peer_id in self.p2p_network.peer_connections.keys():
                await self.p2p_network.send_message(message, peer_id)
                
        except Exception as e:
            print(f"⚠️  Error broadcasting matrix update: {e}")


# Example usage
if __name__ == "__main__":
    print("Node Matrix Manager - AEGIS-Conscience Network")
    print("This module manages full mesh connectivity between nodes")
    print("\nTo use this module:")
    print("1. Import NodeMatrixManager in your node implementation")
    print("2. Initialize with local node ID and P2P network reference")
    print("3. Add known nodes using add_known_node()")
    print("4. Start matrix management with start_matrix_management()")
    print("5. The manager will automatically maintain full mesh connectivity")