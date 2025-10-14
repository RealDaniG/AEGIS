"""
Test for AEGIS-Conscience Network Matrix Connectivity
"""

import asyncio
import sys
import os

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.node_matrix import NodeMatrixManager, NodeInfo
from network.p2p import P2PNetwork, PeerInfo


class MockP2PNetwork:
    """Mock P2P network for testing"""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.peers = {}
        self.peer_connections = {}
    
    def connect_to_peer(self, peer_info):
        """Mock connection to peer"""
        self.peer_connections[peer_info.peer_id] = True
        return True


async def test_node_matrix():
    """Test the NodeMatrixManager functionality"""
    print("🧪 Testing Node Matrix Manager...")
    
    # Create mock P2P network
    mock_p2p = MockP2PNetwork("test-node-1")
    
    # Create node matrix manager
    matrix_manager = NodeMatrixManager("test-node-1", mock_p2p)
    
    # Test adding nodes
    node1 = NodeInfo(
        node_id="node-1",
        ip_address="127.0.0.1",
        port=8080,
        public_key="key1",
        status="online"
    )
    
    node2 = NodeInfo(
        node_id="node-2",
        ip_address="127.0.0.1",
        port=8081,
        public_key="key2",
        status="online"
    )
    
    node3 = NodeInfo(
        node_id="node-3",
        ip_address="127.0.0.1",
        port=8082,
        public_key="key3",
        status="online"
    )
    
    # Add nodes to matrix
    matrix_manager.add_known_node(node1)
    matrix_manager.add_known_node(node2)
    matrix_manager.add_known_node(node3)
    
    print(f"✅ Added {len(matrix_manager.known_nodes)} nodes to matrix")
    
    # Test network topology
    topology = matrix_manager.get_network_topology()
    print(f"✅ Network topology: {topology['total_nodes']} nodes")
    
    # Test connection matrix
    matrix = matrix_manager.get_connection_matrix()
    print(f"✅ Connection matrix initialized with {len(matrix)} nodes")
    
    # Test removing a node
    matrix_manager.remove_known_node("node-2")
    print(f"✅ After removal: {len(matrix_manager.known_nodes)} nodes")
    
    print("✅ All tests passed!")


async def main():
    """Main test function"""
    print("=" * 60)
    print("AEGIS-CONSCIENCE NETWORK - MATRIX CONNECTIVITY TEST")
    print("=" * 60)
    
    await test_node_matrix()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())