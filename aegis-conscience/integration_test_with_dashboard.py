"""
Integration test for AEGIS node with dashboard
"""

import asyncio
import sys
import os
import time

# Add the aegis-conscience directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main import AEGISNode
from network.p2p import PeerInfo


async def test_node_with_dashboard():
    """Test AEGIS node with dashboard integration"""
    print("=== AEGIS Node with Dashboard Integration Test ===\n")
    
    # Create node with dashboard on port 8081
    node = AEGISNode("integration_test_node", 8080, 8081)
    
    # Initialize node
    print("1. Initializing node...")
    success = await node.initialize()
    
    if success:
        print("✅ Node initialized successfully!")
        
        # Add some mock peers
        print("\n2. Adding mock peers...")
        peer1 = PeerInfo(
            peer_id="peer_1",
            ip_address="127.0.0.1",
            port=8082,
            public_key="mock_key_1",
            last_seen=time.time(),
            connection_status="connected",
            reputation_score=0.8,
            latency=0.1
        )
        
        peer2 = PeerInfo(
            peer_id="peer_2",
            ip_address="127.0.0.1",
            port=8083,
            public_key="mock_key_2",
            last_seen=time.time(),
            connection_status="disconnected",
            reputation_score=0.7,
            latency=0.15
        )
        
        await node.add_peer(peer1)
        await node.add_peer(peer2)
        print("✅ Mock peers added")
        
        # Run consciousness cycles to generate data
        print("\n3. Generating consciousness data...")
        for i in range(5):
            print(f"   Running consciousness cycle {i+1}/5...")
            await node.run_consciousness_cycle()
            await asyncio.sleep(1)  # Wait between cycles
        
        print("\n✅ Data generation completed!")
        print(f"\n📊 Dashboard is available at: http://localhost:8081")
        print("📋 Node information:")
        print(f"   Node ID: {node.node_id}")
        if node.onion_address:
            print(f"   Onion Address: {node.onion_address}:{node.port}")
        else:
            print(f"   Local Address: 127.0.0.1:{node.port}")
        
        print("\n⏳ Keeping node running for 30 seconds to allow dashboard viewing...")
        print("Press Ctrl+C to stop early")
        
        try:
            # Run for 30 seconds
            for i in range(30):
                await asyncio.sleep(1)
                if i % 10 == 0:  # Update dashboard every 10 seconds
                    await node.run_consciousness_cycle()
        except KeyboardInterrupt:
            print("\n🛑 Stopping node...")
        
        # Shutdown
        await node.shutdown()
        print("✅ Test completed successfully!")
        
    else:
        print("❌ Node initialization failed!")


if __name__ == "__main__":
    asyncio.run(test_node_with_dashboard())