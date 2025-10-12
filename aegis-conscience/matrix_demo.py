"""
Matrix Connection Demo for AEGIS-Conscience Network
Demonstrates how to create a matrix connection between all nodes
"""

import asyncio
import time
import json
import os
import sys
from typing import List

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AEGISNode
from network.p2p import PeerInfo
from network.node_matrix import NodeInfo
from tools.matrix_visualizer import MatrixVisualizer


class MatrixDemo:
    """Demonstration of matrix connectivity between AEGIS nodes"""
    
    def __init__(self):
        self.nodes: List[AEGISNode] = []
        self.node_ports = [8080, 8081, 8082, 8083]
        self.node_ids = [f"node-{i+1}" for i in range(len(self.node_ports))]
    
    async def setup_nodes(self):
        """Set up multiple nodes for the demonstration"""
        print("🔧 Setting up AEGIS nodes for matrix demo...")
        
        # Create nodes
        for i, (node_id, port) in enumerate(zip(self.node_ids, self.node_ports)):
            print(f"Creating node {node_id} on port {port}")
            node = AEGISNode(node_id, port)
            self.nodes.append(node)
        
        # Connect nodes to each other (simulate discovery)
        print("🔗 Connecting nodes to form matrix...")
        for i, node in enumerate(self.nodes):
            # Add all other nodes as peers
            for j, (peer_id, peer_port) in enumerate(zip(self.node_ids, self.node_ports)):
                if i != j:  # Don't add self as peer
                    peer_info = PeerInfo(
                        peer_id=peer_id,
                        ip_address="127.0.0.1",
                        port=peer_port,
                        public_key=f"mock_key_{j}",
                        last_seen=time.time(),
                        connection_status="disconnected",
                        reputation_score=0.8,
                        latency=0.1
                    )
                    await node.add_peer(peer_info)
        
        print(f"✅ Set up {len(self.nodes)} nodes with mutual peer connections")
    
    async def start_nodes(self):
        """Start all nodes"""
        print("🚀 Starting nodes...")
        
        # Start each node in a separate task
        tasks = []
        for node in self.nodes:
            task = asyncio.create_task(self._run_node(node))
            tasks.append(task)
        
        # Let nodes run for a while to establish connections
        print("⏳ Nodes running, establishing matrix connections...")
        await asyncio.sleep(30)  # Run for 30 seconds to establish connections
        
        # Stop all nodes
        print("⏹️  Stopping nodes...")
        for node in self.nodes:
            await node.shutdown()
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _run_node(self, node: AEGISNode):
        """Run a single node"""
        try:
            await node.run()
        except Exception as e:
            print(f"Error running node {node.node_id}: {e}")
    
    def save_matrix_data(self):
        """Save matrix data for visualization"""
        print("💾 Saving matrix data for visualization...")
        
        # For demo purposes, we'll create example data
        # In a real implementation, this would come from the actual nodes
        matrix_data = {
            "total_nodes": len(self.nodes),
            "local_node_id": self.node_ids[0],
            "local_connections": len(self.node_ids) - 1,
            "connection_matrix": {},
            "known_nodes": {}
        }
        
        # Create full mesh connection matrix
        for node_id in self.node_ids:
            matrix_data["connection_matrix"][node_id] = [
                peer_id for peer_id in self.node_ids if peer_id != node_id
            ]
        
        # Create node information
        for i, (node_id, port) in enumerate(zip(self.node_ids, self.node_ports)):
            matrix_data["known_nodes"][node_id] = {
                "node_id": node_id,
                "ip_address": "127.0.0.1",
                "port": port,
                "public_key": f"mock_key_{i}",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": [peer_id for peer_id in self.node_ids if peer_id != node_id]
            }
        
        # Save to file
        with open("./matrix_data.json", "w") as f:
            json.dump(matrix_data, f, indent=2)
        
        print("✅ Matrix data saved to ./matrix_data.json")
        return matrix_data
    
    def visualize_matrix(self, matrix_data=None):
        """Visualize the connection matrix"""
        print("📊 Visualizing connection matrix...")
        
        visualizer = MatrixVisualizer()
        if matrix_data:
            visualizer.load_matrix_data(matrix_data)
        else:
            # Try to load from file
            try:
                visualizer.load_from_file("./matrix_data.json")
            except:
                print("❌ No matrix data available for visualization")
                return
        
        # Display visualization
        visualizer.visualize_matrix()
        visualizer.print_statistics()


async def main():
    """Main demo function"""
    print("=" * 80)
    print("AEGIS-CONSCIENCE NETWORK - MATRIX CONNECTION DEMO")
    print("=" * 80)
    
    demo = MatrixDemo()
    
    # Setup nodes
    await demo.setup_nodes()
    
    # Start nodes (this will run for 30 seconds)
    await demo.start_nodes()
    
    # Save and visualize matrix data
    matrix_data = demo.save_matrix_data()
    demo.visualize_matrix(matrix_data)
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())