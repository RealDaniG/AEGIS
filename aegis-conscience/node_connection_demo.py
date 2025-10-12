"""
Node Connection Demonstration
Shows how two nodes from different users can connect in the AEGIS network
"""

import asyncio
import time
from network.p2p import P2PNetwork, PeerInfo
from network.crypto import CryptoManager
from schemas import ConsciousnessState


class DemoNode:
    """Demo node showing user connection process"""
    
    def __init__(self, node_id: str, port: int):
        self.node_id = node_id
        self.port = port
        self.crypto_manager = CryptoManager(node_id)
        self.p2p_network = P2PNetwork(node_id, port)
        self.onion_address = f"{node_id.lower().replace('_', '')}onion1234567890abcd.onion"
        
        # Initialize crypto
        self.crypto_manager.generate_or_load_identity(f"{node_id}_password")
    
    def get_connection_info(self):
        """Get connection information to share with other users"""
        signing_pub, encryption_pub = self.crypto_manager.get_public_keys()
        return {
            'onion_address': self.onion_address,
            'port': self.port,
            'public_key': signing_pub.hex(),
            'node_id': self.node_id
        }
    
    def add_authorized_peer(self, peer_info: dict):
        """Add an authorized peer to connect to"""
        peer = PeerInfo(
            peer_id=peer_info['node_id'],
            ip_address=peer_info['onion_address'],
            port=peer_info['port'],
            public_key=peer_info['public_key'],
            last_seen=time.time(),
            connection_status="disconnected",
            reputation_score=0.8,
            latency=0.1
        )
        self.p2p_network.add_peer(peer)
        print(f"Added authorized peer: {peer.peer_id}")
    
    async def start_node(self):
        """Start the node (simulated)"""
        print(f"🚀 Starting {self.node_id} on {self.onion_address}:{self.port}")
        print(f"🔐 Public key: {self.get_connection_info()['public_key'][:32]}...")
        # In a real implementation, this would start the P2P server
        # await self.p2p_network.start_server()


async def demo_user_connection():
    """Demonstrate how two users connect their nodes"""
    print("🔗 AEGIS-Conscience Network - User Connection Demo")
    print("=" * 55)
    
    # Create two nodes (representing different users)
    print("\n👤 User Alice setting up her node...")
    alice_node = DemoNode("Alice_Node", 8080)
    
    print("\n👤 User Bob setting up his node...")
    bob_node = DemoNode("Bob_Node", 8081)
    
    # Step 1: Users exchange connection information
    print("\n📤 Step 1: Users Exchange Connection Information")
    alice_info = alice_node.get_connection_info()
    bob_info = bob_node.get_connection_info()
    
    print(f"\nAlice shares: {alice_info['onion_address']}:{alice_info['port']}")
    print(f"Bob shares: {bob_info['onion_address']}:{bob_info['port']}")
    
    # Step 2: Users authorize each other
    print("\n✅ Step 2: Users Authorize Each Other")
    alice_node.add_authorized_peer(bob_info)
    bob_node.add_authorized_peer(alice_info)
    
    # Step 3: Nodes establish connection
    print("\n🔄 Step 3: Nodes Establish Secure Connection")
    await alice_node.start_node()
    await bob_node.start_node()
    
    # Simulate connection process
    print(f"\n🔒 Alice's node connecting to Bob's node through TOR...")
    print(f"🔒 Bob's node connecting to Alice's node through TOR...")
    
    # Simulate consciousness state exchange
    print("\n🧠 Step 4: Consciousness State Exchange")
    alice_state = ConsciousnessState(
        node_id="Alice_Node",
        timestamp=time.time(),
        entropy=0.5,
        valence=0.3,
        arousal=0.7,
        coherence=0.8,
        empathy_score=0.6,
        insight_strength=0.4
    )
    
    bob_state = ConsciousnessState(
        node_id="Bob_Node",
        timestamp=time.time(),
        entropy=0.4,
        valence=0.2,
        arousal=0.6,
        coherence=0.7,
        empathy_score=0.5,
        insight_strength=0.3
    )
    
    # Sign states
    alice_signature = alice_node.crypto_manager.sign_state(alice_state)
    bob_signature = bob_node.crypto_manager.sign_state(bob_state)
    
    alice_state.signature = alice_signature
    bob_state.signature = bob_signature
    
    print(f"Alice's state signed and sent (coherence: {alice_state.coherence:.3f})")
    print(f"Bob's state signed and sent (coherence: {bob_state.coherence:.3f})")
    
    # Verify signatures
    alice_pub, _ = alice_node.crypto_manager.get_public_keys()
    bob_pub, _ = bob_node.crypto_manager.get_public_keys()
    
    alice_valid = bob_node.crypto_manager.verify_state(
        alice_state, alice_signature, alice_pub)
    bob_valid = alice_node.crypto_manager.verify_state(
        bob_state, bob_signature, bob_pub)
    
    print(f"\n✅ Signature Verification:")
    print(f"Alice's signature valid: {alice_valid}")
    print(f"Bob's signature valid: {bob_valid}")
    
    # Calculate collective metrics
    print("\n📊 Step 5: Collective Consciousness Calculation")
    from consensus.aggregator import GlobalCoherenceAggregator
    aggregator = GlobalCoherenceAggregator()
    
    # Set reputation weights
    aggregator.update_reputation_weight("Alice_Node", 0.9)
    aggregator.update_reputation_weight("Bob_Node", 0.8)
    
    # Calculate global metrics
    states = [alice_state, bob_state]
    global_coherence = aggregator.compute_global_coherence(states)
    collective_metrics = aggregator.compute_collective_metrics(states)
    
    print(f"Global Coherence: {global_coherence:.3f}")
    print("Collective Metrics:")
    for metric, value in collective_metrics.items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.3f}")
        else:
            print(f"  {metric}: {value}")
    
    print("\n" + "=" * 55)
    print("🎉 CONNECTION SUCCESSFUL!")
    print("Alice and Bob's nodes are now collaborating securely")
    print("through the AEGIS-Conscience Network!")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(demo_user_connection())