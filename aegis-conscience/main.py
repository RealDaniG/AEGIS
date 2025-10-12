"""
Main entry point for AEGIS-Conscience Network Node
"""

import asyncio
import time
import json
import os
from typing import List, Optional

from consciousness.engine import ConsciousnessEngine
from network.crypto import CryptoManager
from network.p2p import P2PNetwork, PeerInfo
from network.tor_gateway import TORGateway
from network.nat_traversal import NATTraversalManager
from consensus.pbft import PBFTConsensus
from consensus.aggregator import GlobalCoherenceAggregator
from storage.knowledge_base import KnowledgeBase
from schemas import ConsciousnessState, NetworkMessage


class AEGISNode:
    """Main AEGIS-Conscience Network Node"""
    
    def __init__(self, node_id: str, port: int = 8080, dashboard_port: int = 8081):
        self.node_id = node_id
        self.port = port
        self.dashboard_port = dashboard_port
        self.onion_address: Optional[str] = None  # Store the onion address
        
        # Initialize components
        self.consciousness_engine = ConsciousnessEngine(node_id)
        self.crypto_manager = CryptoManager(node_id)
        self.p2p_network = P2PNetwork(node_id, port)
        self.tor_gateway = TORGateway()
        self.nat_manager = NATTraversalManager()
        self.pbft_consensus = PBFTConsensus(node_id, self.crypto_manager)
        self.aggregator = GlobalCoherenceAggregator()
        self.knowledge_base = KnowledgeBase(node_id, f"./data/{node_id}")
        
        # Dashboard integration
        try:
            from monitoring.dashboard import MonitoringDashboard
            self.dashboard = MonitoringDashboard(node_id, dashboard_port)
            self.dashboard_enabled = True
        except Exception as e:
            print(f"⚠️  Dashboard not available: {e}")
            self.dashboard = None
            self.dashboard_enabled = False
        
        # Node matrix manager for full mesh connectivity
        try:
            from network.node_matrix import NodeMatrixManager
            self.node_matrix = NodeMatrixManager(node_id, self.p2p_network)
            self.matrix_enabled = True
        except Exception as e:
            print(f"⚠️  Node matrix manager not available: {e}")
            self.node_matrix = None
            self.matrix_enabled = False
        
        # Node state
        self.running = False
        self.consciousness_states: List[ConsciousnessState] = []
        self.peers: List[PeerInfo] = []
        
        # Register message handlers
        self.p2p_network.register_message_handler(
            "consciousness_state", 
            self._handle_consciousness_state
        )
        
        self.p2p_network.register_message_handler(
            "consensus_proposal", 
            self._handle_consensus_proposal
        )
        
        self.p2p_network.register_message_handler(
            "knowledge_sync", 
            self._handle_knowledge_sync
        )
    
    async def initialize(self) -> bool:
        """Initialize the node"""
        print(f"Initializing AEGIS Node {self.node_id}")
        print("=" * 50)
        
        # Initialize cryptographic identity
        password = os.environ.get("NODE_PASSWORD", "default_password")
        if not self.crypto_manager.generate_or_load_identity(password):
            print("Failed to initialize cryptographic identity")
            return False
        
        # Initialize TOR gateway
        tor_initialized = await self.tor_gateway.initialize()
        if tor_initialized:
            # Create onion service with authorized clients
            authorized_clients = ["trusted_peer_1", "trusted_peer_2"]
            onion_address = await self.tor_gateway.create_onion_service(
                self.port, 
                authorized_clients=authorized_clients
            )
            if onion_address:
                self.onion_address = onion_address
                print(f"🟢 TOR Onion Service Created!")
                print(f"   Address: {onion_address}:{self.port}")
                print(f"   Authorized clients: {authorized_clients}")
            else:
                print("🟡 TOR initialization failed, continuing without onion service")
        else:
            print("🟡 TOR not available, continuing without onion service")
        
        # Discover public address for NAT traversal
        nat_success = await self.nat_manager.discover_public_address()
        if nat_success:
            binding = self.nat_manager.get_public_binding()
            if binding:
                print(f"🔵 NAT traversal successful: {binding.public_ip}:{binding.public_port}")
        else:
            print("🔵 NAT traversal failed, using relay servers")
        
        # Start P2P network
        # In production, this would be started in the background
        print(f"🔗 P2P network initialized on port {self.port}")
        
        # Start dashboard if available
        if self.dashboard_enabled and self.dashboard:
            try:
                # Start dashboard in background thread
                import threading
                dashboard_thread = threading.Thread(
                    target=self.dashboard.start_dashboard, 
                    args=(False,),  # debug=False
                    daemon=True
                )
                dashboard_thread.start()
                time.sleep(1)  # Give dashboard time to start
                print(f"📊 Dashboard available at: http://localhost:{self.dashboard_port}")
            except Exception as e:
                print(f"⚠️  Failed to start dashboard: {e}")
        
        # Display node information
        print("=" * 50)
        print("NODE INFORMATION:")
        print(f"  Node ID: {self.node_id}")
        if self.onion_address:
            print(f"  Onion Address: {self.onion_address}:{self.port}")
        else:
            print(f"  Local Address: 127.0.0.1:{self.port}")
        print("=" * 50)
        
        # Start node matrix management if available
        if self.matrix_enabled and self.node_matrix:
            try:
                await self.node_matrix.start_matrix_management()
                print("🔄 Node matrix management started")
            except Exception as e:
                print(f"⚠️  Failed to start node matrix management: {e}")
        
        self.running = True
        return True
    
    async def run_consciousness_cycle(self):
        """Run one cycle of consciousness processing"""
        # Get current consciousness state
        state = self.consciousness_engine.get_current_state()
        
        # Sign the state
        state.signature = self.crypto_manager.sign_state(state)
        
        # Store locally in knowledge base
        cid = self.knowledge_base.store_consciousness_state(state)
        print(f"Stored consciousness state in knowledge base: {cid}")
        
        # Store in memory
        self.consciousness_states.append(state)
        
        # Limit history
        if len(self.consciousness_states) > 100:
            self.consciousness_states.pop(0)
        
        # Broadcast to peers (convert signature to hex for JSON serialization)
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
        
        await self.p2p_network.broadcast_state(state)
        
        print(f"Consciousness state broadcasted: coherence={state.coherence:.3f}")
        
        # Update dashboard with consciousness metrics
        if self.dashboard_enabled and self.dashboard:
            try:
                # Calculate global metrics for dashboard
                trusted_peers = self.p2p_network.get_trusted_peers()
                active_peers = len([p for p in self.p2p_network.peers.values() 
                                  if p.connection_status == "connected"])
                
                self.dashboard.update_metrics(
                    global_coherence=state.coherence,
                    global_entropy=state.entropy,
                    active_peers=active_peers
                )
            except Exception as e:
                print(f"⚠️  Failed to update dashboard metrics: {e}")
    
    async def run_consensus_cycle(self):
        """Run one cycle of consensus processing"""
        # If this node is the leader, propose global coherence
        if self.pbft_consensus.is_leader():
            # Collect states from peers (in practice, this would be from received states)
            # For demo, we'll use our own states plus some mock ones
            all_states = self.consciousness_states.copy()
            
            # Add some mock peer states for demonstration
            mock_states = [
                ConsciousnessState("peer_1", time.time(), 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
                ConsciousnessState("peer_2", time.time(), 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
                ConsciousnessState("peer_3", time.time(), 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
            ]
            
            all_states.extend(mock_states)
            
            # Propose global coherence
            success = self.pbft_consensus.propose_global_coherence(all_states)
            if success:
                # Compute and broadcast global metrics
                global_metrics = self.aggregator.compute_collective_metrics(all_states)
                print(f"Global metrics computed: {global_metrics}")
    
    async def _handle_consciousness_state(self, message: NetworkMessage):
        """Handle incoming consciousness state messages"""
        try:
            # Extract state from payload
            state_dict = message.payload
            state = ConsciousnessState(
                node_id=state_dict['node_id'],
                timestamp=state_dict['timestamp'],
                entropy=state_dict['entropy'],
                valence=state_dict['valence'],
                arousal=state_dict['arousal'],
                coherence=state_dict['coherence'],
                empathy_score=state_dict['empathy_score'],
                insight_strength=state_dict['insight_strength'],
                signature=bytes.fromhex(state_dict['signature']) if state_dict.get('signature') else None
            )
            
            # Verify signature (simplified)
            if state.signature:
                signing_pub, _ = self.crypto_manager.get_public_keys()
                is_valid = self.crypto_manager.verify_state(state, state.signature, signing_pub)
                if not is_valid:
                    print(f"Invalid signature from {state.node_id}")
                    return
            
            # Store state in knowledge base
            cid = self.knowledge_base.store_consciousness_state(state)
            
            # Store in memory
            self.consciousness_states.append(state)
            
            # Update peer reputation
            self.p2p_network.update_peer_reputation(state.node_id, 0.01)
            
            print(f"Received consciousness state from {state.node_id}: coherence={state.coherence:.3f}, CID={cid}")
            
        except Exception as e:
            print(f"Error handling consciousness state: {e}")
    
    async def _handle_consensus_proposal(self, message: NetworkMessage):
        """Handle consensus proposal messages"""
        try:
            # Forward to PBFT consensus handler
            # This is a simplified implementation
            print(f"Received consensus proposal: {message.payload}")
            
        except Exception as e:
            print(f"Error handling consensus proposal: {e}")
    
    async def _handle_knowledge_sync(self, message: NetworkMessage):
        """Handle knowledge sync messages"""
        try:
            # Extract sync data
            sync_data = message.payload
            peer_cid = sync_data.get('cid')
            peer_data = sync_data.get('data')
            
            if peer_cid and peer_data:
                # Sync with knowledge base
                success = self.knowledge_base.sync_with_peer(peer_cid, peer_data)
                if success:
                    print(f"Synced knowledge entry from peer: {peer_cid}")
            
        except Exception as e:
            print(f"Error handling knowledge sync: {e}")
    
    def _display_node_status(self):
        """Display current node status including onion address"""
        print("\n" + "=" * 50)
        print("NODE STATUS REPORT")
        print("=" * 50)
        print(f"Node ID: {self.node_id}")
        print(f"Local Port: {self.port}")
        if self.onion_address:
            print(f"Onion Address: {self.onion_address}:{self.port}")
        else:
            print("Onion Address: Not available (TOR not initialized)")
        print(f"Connected Peers: {len(self.peers)}")
        print(f"Stored Consciousness States: {len(self.consciousness_states)}")
        if self.consciousness_states:
            latest_state = self.consciousness_states[-1]
            print(f"Latest Coherence: {latest_state.coherence:.3f}")
        print("=" * 50 + "\n")
    
    async def add_peer(self, peer_info: PeerInfo):
        """Add a peer to the network"""
        self.p2p_network.add_peer(peer_info)
        self.pbft_consensus.add_node(peer_info.peer_id)
        
        # Try to connect
        await self.p2p_network.connect_to_peer(peer_info)
        
        # Update dashboard with peer information
        if self.dashboard_enabled and self.dashboard:
            try:
                self.dashboard.update_peers(self.p2p_network.peers)
            except Exception as e:
                print(f"⚠️  Failed to update dashboard peers: {e}")
    
    async def run(self):
        """Main node run loop"""
        if not await self.initialize():
            print("Failed to initialize node")
            return
        
        print("AEGIS Node running...")
        
        # Main loop
        cycle_count = 0
        while self.running:
            try:
                # Display node status every 30 seconds
                if cycle_count % 30 == 0:
                    self._display_node_status()
                
                # Run consciousness cycle every 10 seconds
                if cycle_count % 10 == 0:
                    await self.run_consciousness_cycle()
                
                # Run consensus cycle every 30 seconds
                if cycle_count % 30 == 0:
                    await self.run_consensus_cycle()
                
                # Cleanup old states periodically
                if cycle_count % 60 == 0:
                    # Remove states older than 5 minutes
                    cutoff_time = time.time() - 300
                    self.consciousness_states = [
                        s for s in self.consciousness_states 
                        if s.timestamp > cutoff_time
                    ]
                
                # Run matrix updates every 60 seconds
                if cycle_count % 60 == 0 and self.matrix_enabled and self.node_matrix:
                    await self._update_node_matrix()
                
                cycle_count += 1
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("Shutting down node...")
                self.running = False
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                await asyncio.sleep(1)
    
    async def _update_node_matrix(self):
        """Update node matrix with current peer information"""
        if not self.matrix_enabled or not self.node_matrix:
            return
            
        try:
            # Add current peers to matrix
            for peer_id, peer_info in self.p2p_network.peers.items():
                from network.node_matrix import NodeInfo
                node_info = NodeInfo(
                    node_id=peer_info.peer_id,
                    ip_address=peer_info.ip_address,
                    port=peer_info.port,
                    public_key=peer_info.public_key,
                    last_seen=peer_info.last_seen,
                    status=peer_info.connection_status
                )
                self.node_matrix.add_known_node(node_info)
            
            # Update connection status for all known nodes
            for node_id in list(self.node_matrix.known_nodes.keys()):
                if node_id in self.p2p_network.peers:
                    peer_info = self.p2p_network.peers[node_id]
                    self.node_matrix.known_nodes[node_id].status = peer_info.connection_status
                    self.node_matrix.known_nodes[node_id].last_seen = peer_info.last_seen
            
            # Broadcast matrix update
            await self.node_matrix.broadcast_matrix_update()
            
            # Save matrix data for visualization
            self._save_matrix_data()
            
        except Exception as e:
            print(f"⚠️  Error updating node matrix: {e}")
    
    def _save_matrix_data(self):
        """Save matrix data for visualization"""
        try:
            if self.matrix_enabled and self.node_matrix:
                topology = self.node_matrix.get_network_topology()
                # Convert sets to lists for JSON serialization
                for node_id, connections in topology['connection_matrix'].items():
                    if isinstance(connections, set):
                        topology['connection_matrix'][node_id] = list(connections)
                
                # Save to data directory
                import os
                data_dir = "./data"
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                
                with open(f"{data_dir}/matrix_data.json", "w") as f:
                    import json
                    json.dump(topology, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Error saving matrix data: {e}")
    
    async def shutdown(self):
        """Shutdown the node"""
        self.running = False
        await self.p2p_network.stop()
        await self.tor_gateway.cleanup()
        print("Node shutdown complete")


# Example usage
async def main():
    # Create and run node
    node = AEGISNode("aegis_node_1", 8080)
    
    # Add some mock peers
    peer1 = PeerInfo(
        peer_id="peer_1",
        ip_address="127.0.0.1",
        port=8081,
        public_key="mock_key_1",
        last_seen=time.time(),
        connection_status="disconnected",
        reputation_score=0.8,
        latency=0.1
    )
    
    peer2 = PeerInfo(
        peer_id="peer_2",
        ip_address="127.0.0.1",
        port=8082,
        public_key="mock_key_2",
        last_seen=time.time(),
        connection_status="disconnected",
        reputation_score=0.7,
        latency=0.15
    )
    
    await node.add_peer(peer1)
    await node.add_peer(peer2)
    
    # Run for a short time for demo
    try:
        await asyncio.wait_for(node.run(), timeout=30.0)
    except asyncio.TimeoutError:
        await node.shutdown()


if __name__ == "__main__":
    asyncio.run(main())