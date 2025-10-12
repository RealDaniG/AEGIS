"""
Test script to demonstrate AEGIS node with onion address display
"""

import asyncio
import sys
import os

# Add the aegis-conscience directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'aegis-conscience'))

from main import AEGISNode
from network.p2p import PeerInfo
import time


async def test_node_with_onion_display():
    """Test the AEGIS node with onion address display"""
    print("=== AEGIS Node Onion Address Display Test ===\n")
    
    # Create node
    node = AEGISNode("test_node_with_onion", 8085)
    
    # Initialize and show onion address
    print("1. Initializing node...")
    success = await node.initialize()
    
    if success:
        print("✅ Node initialized successfully!")
        
        # Show node information
        print(f"\nNode Information:")
        print(f"  - Node ID: {node.node_id}")
        print(f"  - Port: {node.port}")
        if hasattr(node, 'onion_address') and node.onion_address:
            print(f"  - Onion Address: {node.onion_address}:{node.port}")
        else:
            print(f"  - Onion Address: Not available (TOR not initialized)")
        
        # Show status
        node._display_node_status()
        
        print("\n2. Running node for 10 seconds...")
        # Run for a short time to show periodic status updates
        try:
            # Start a task to run the node
            node_task = asyncio.create_task(node.run())
            
            # Let it run for 10 seconds
            await asyncio.sleep(10)
            
            # Cancel the task
            node_task.cancel()
            try:
                await node_task
            except asyncio.CancelledError:
                pass
                
            # Shutdown
            await node.shutdown()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down node...")
            await node.shutdown()
        
        print("\n✅ Test completed successfully!")
    else:
        print("❌ Node initialization failed!")


if __name__ == "__main__":
    asyncio.run(test_node_with_onion_display())