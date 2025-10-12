"""
Complete integration test for AEGIS node with web dashboard and performance optimizations
"""

import asyncio
import sys
import os
import time
import threading
from typing import Dict, List

# Add the aegis-conscience directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main import AEGISNode
from network.p2p import PeerInfo
from performance_optimizations import PerformanceOptimizer, NetworkOptimizer


class IntegratedAEGISNode(AEGISNode):
    """AEGIS Node with performance optimizations and enhanced dashboard integration"""
    
    def __init__(self, node_id: str, port: int = 8080, dashboard_port: int = 8081):
        super().__init__(node_id, port, dashboard_port)
        self.optimizer = PerformanceOptimizer()
        self.network_optimizer = NetworkOptimizer()
        self.performance_stats = {
            'consciousness_cycles': 0,
            'messages_sent': 0,
            'cache_hits': 0,
            'optimization_savings': 0.0
        }
    
    async def run_consciousness_cycle(self):
        """Run one cycle of consciousness processing with optimizations"""
        start_time = time.time()
        
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
        message = {
            'message_id': f"state_{int(time.time()*1000000)}",
            'sender_id': self.node_id,
            'recipient_id': "*",
            'message_type': "consciousness_state",
            'payload': state_dict,
            'timestamp': time.time()
        }
        
        # Use network optimizer for batch sending
        await self.network_optimizer.batch_send_messages([message])
        
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
                
                # Update peer information
                self.dashboard.update_peers(self.p2p_network.peers)
            except Exception as e:
                print(f"⚠️  Failed to update dashboard: {e}")
        
        # Update performance stats
        cycle_time = time.time() - start_time
        self.performance_stats['consciousness_cycles'] += 1
        self.performance_stats['messages_sent'] += 1
        
        # Apply caching optimization statistics
        cache_stats = self.optimizer.get_stats()
        self.performance_stats['cache_hits'] = cache_stats.get('cache_hits', 0)
        
        return cycle_time


async def run_integration_test():
    """Run complete integration test"""
    print("=== AEGIS Complete Integration Test ===")
    print("Testing node data integration with web dashboard and performance optimizations\n")
    
    # Create optimized node
    node = IntegratedAEGISNode("integration_test_node", 8080, 8081)
    
    # Initialize node
    print("1. Initializing node with dashboard...")
    success = await node.initialize()
    
    if success:
        print("✅ Node initialized successfully!")
        
        # Add some mock peers
        print("\n2. Adding mock peers...")
        peers = []
        for i in range(5):
            peer = PeerInfo(
                peer_id=f"peer_{i+1}",
                ip_address="127.0.0.1",
                port=8082+i,
                public_key=f"mock_key_{i+1}",
                last_seen=time.time(),
                connection_status="connected" if i < 3 else "disconnected",
                reputation_score=0.6 + (i * 0.1),
                latency=0.05 + (i * 0.05)
            )
            await node.add_peer(peer)
            peers.append(peer)
        
        print(f"✅ Added {len(peers)} mock peers")
        
        # Start network optimizer sender
        sender_task = asyncio.create_task(node.network_optimizer.message_sender())
        
        # Run consciousness cycles to generate data
        print("\n3. Generating consciousness data with performance optimizations...")
        cycle_times = []
        
        for i in range(10):
            print(f"   Running consciousness cycle {i+1}/10...")
            cycle_time = await node.run_consciousness_cycle()
            cycle_times.append(cycle_time)
            await asyncio.sleep(0.5)  # Wait between cycles
        
        # Stop network sender
        sender_task.cancel()
        try:
            await sender_task
        except asyncio.CancelledError:
            pass
        
        # Calculate performance metrics
        avg_cycle_time = sum(cycle_times) / len(cycle_times)
        total_time = sum(cycle_times)
        
        print(f"\n✅ Data generation completed!")
        print(f"   Average cycle time: {avg_cycle_time*1000:.2f}ms")
        print(f"   Total time for 10 cycles: {total_time*1000:.2f}ms")
        
        # Show performance stats
        print("\n4. Performance statistics:")
        for key, value in node.performance_stats.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.2f}")
            else:
                print(f"   {key}: {value}")
        
        cache_stats = node.optimizer.get_stats()
        print(f"   Cache hits: {cache_stats.get('cache_hits', 0)}")
        print(f"   Cache misses: {cache_stats.get('cache_misses', 0)}")
        print(f"   Batched operations: {cache_stats.get('batched_operations', 0)}")
        
        print(f"\n📊 Dashboard is available at: http://localhost:8081")
        print("📋 Node information:")
        print(f"   Node ID: {node.node_id}")
        if node.onion_address:
            print(f"   Onion Address: {node.onion_address}:{node.port}")
        else:
            print(f"   Local Address: 127.0.0.1:{node.port}")
        
        print("\n⏳ Keeping node running for 60 seconds to allow dashboard viewing...")
        print("You can view real-time metrics at: http://localhost:8081")
        print("Press Ctrl+C to stop early")
        
        try:
            # Run for 60 seconds
            for i in range(60):
                await asyncio.sleep(1)
                if i % 20 == 0:  # Update dashboard every 20 seconds
                    await node.run_consciousness_cycle()
        except KeyboardInterrupt:
            print("\n🛑 Stopping node...")
        
        # Shutdown
        await node.shutdown()
        print("✅ Integration test completed successfully!")
        
    else:
        print("❌ Node initialization failed!")


if __name__ == "__main__":
    try:
        asyncio.run(run_integration_test())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(0)