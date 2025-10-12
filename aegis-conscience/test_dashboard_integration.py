"""
Test script to verify dashboard integration with real AEGIS node data
"""

import sys
import os
import time
import threading
from typing import Dict, List

# Add the aegis-conscience directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from monitoring.dashboard import MonitoringDashboard
from network.p2p import PeerInfo
from schemas import ConsciousnessState


class MockAEGISNode:
    """Mock AEGIS node for testing dashboard integration"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.dashboard = MonitoringDashboard(node_id, 8081)
        self.running = False
        self.consciousness_states: List[ConsciousnessState] = []
        self.peers: Dict[str, PeerInfo] = {}
        
    def start_dashboard(self):
        """Start the dashboard in a separate thread"""
        def run_dashboard():
            try:
                self.dashboard.start_dashboard(debug=False)
            except KeyboardInterrupt:
                self.dashboard.stop_dashboard()
        
        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        time.sleep(1)  # Give dashboard time to start
        return dashboard_thread.is_alive()
    
    def update_metrics(self, global_coherence: float, global_entropy: float, active_peers: int):
        """Update dashboard metrics"""
        self.dashboard.update_metrics(global_coherence, global_entropy, active_peers)
    
    def update_peers(self, peers: Dict[str, PeerInfo]):
        """Update dashboard peers"""
        self.dashboard.update_peers(peers)
    
    def add_mock_peers(self):
        """Add some mock peers for testing"""
        peers = {}
        for i in range(5):
            peer_id = f"peer_{i+1}"
            peers[peer_id] = PeerInfo(
                peer_id=peer_id,
                ip_address=f"192.168.1.{100+i}",
                port=8080+i,
                public_key=f"key_{i}",
                last_seen=time.time(),
                connection_status="connected" if i < 3 else "disconnected",
                reputation_score=0.6 + (i * 0.1),
                latency=0.05 + (i * 0.05)
            )
        self.peers = peers
        return peers


def test_dashboard_integration():
    """Test the dashboard integration"""
    print("=== AEGIS Dashboard Integration Test ===\n")
    
    # Create mock node
    node = MockAEGISNode("test_node_1")
    
    # Start dashboard
    print("1. Starting dashboard...")
    dashboard_started = node.start_dashboard()
    if dashboard_started:
        print("✅ Dashboard started successfully on http://localhost:8081")
    else:
        print("❌ Failed to start dashboard")
        return
    
    # Add mock peers
    print("\n2. Adding mock peers...")
    peers = node.add_mock_peers()
    node.update_peers(peers)
    print(f"✅ Added {len(peers)} mock peers")
    
    # Simulate metrics updates
    print("\n3. Simulating metrics updates...")
    for i in range(10):
        coherence = 0.5 + (i * 0.05)  # Increasing coherence
        entropy = 0.3 - (i * 0.02)    # Decreasing entropy
        active_peers = 3 + (i % 3)    # Varying peer count
        
        node.update_metrics(coherence, entropy, active_peers)
        print(f"   Update {i+1}: Coherence={coherence:.2f}, Entropy={entropy:.2f}, Peers={active_peers}")
        time.sleep(0.5)
    
    print("\n✅ Dashboard integration test completed!")
    print("\nYou can view the dashboard at: http://localhost:8081")
    print("Press Ctrl+C to stop the test")


if __name__ == "__main__":
    try:
        test_dashboard_integration()
        # Keep the script running to allow dashboard access
        print("\nDashboard is running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping dashboard...")
        sys.exit(0)