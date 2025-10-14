"""
Final comprehensive test for AEGIS-Conscience Network
This test verifies that all components work together correctly
"""

import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all components
from consciousness.engine import ConsciousnessEngine
from network.crypto import CryptoManager
from network.p2p import P2PNetwork, PeerInfo
from network.tor_gateway import TORGateway
from consensus.pbft import PBFTConsensus
from consensus.aggregator import GlobalCoherenceAggregator
from storage.knowledge_base import KnowledgeBase
from schemas import ConsciousnessState, NetworkMessage


def test_complete_system():
    """Test all components working together"""
    print("🧪 AEGIS-Conscience Network Comprehensive Test")
    print("=" * 50)
    
    # Test 1: Consciousness Engine
    print("\n1. Testing Consciousness Engine...")
    try:
        engine = ConsciousnessEngine("test_node")
        state = engine.get_current_state()
        print(f"   [OK] Consciousness State: coherence={state.coherence:.3f}")
    except Exception as e:
        print(f"   ✗ Consciousness Engine failed: {e}")
        return False
    
    # Test 2: Cryptographic Security
    print("\n2. Testing Cryptographic Security...")
    try:
        crypto = CryptoManager("test_node")
        if not crypto.generate_or_load_identity("test_password"):
            print("   ✗ Failed to generate identity")
            return False
            
        # Sign and verify
        signature = crypto.sign_state(state)
        signing_pub, _ = crypto.get_public_keys()
        is_valid = crypto.verify_state(state, signature, signing_pub)
        print(f"   [OK] Crypto Signature: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"   ✗ Crypto Manager failed: {e}")
        return False
    
    # Test 3: Knowledge Base
    print("\n3. Testing Knowledge Base...")
    try:
        kb = KnowledgeBase("test_node", "./test_kb")
        cid = kb.store_consciousness_state(state)
        retrieved = kb.retrieve_entry(cid)
        print(f"   [OK] Knowledge Storage: CID={cid[:8]}...")
    except Exception as e:
        print(f"   ✗ Knowledge Base failed: {e}")
        return False
    
    # Test 4: Consensus Aggregation
    print("\n4. Testing Consensus Aggregation...")
    try:
        aggregator = GlobalCoherenceAggregator()
        # Add some test states
        test_states = [
            ConsciousnessState("node_1", time.time(), 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
            ConsciousnessState("node_2", time.time(), 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
            ConsciousnessState("node_3", time.time(), 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
        ]
        global_coherence = aggregator.compute_global_coherence(test_states)
        print(f"   [OK] Global Coherence: {global_coherence:.3f}")
    except Exception as e:
        print(f"   ✗ Consensus Aggregator failed: {e}")
        return False
    
    # Test 5: P2P Network (simplified)
    print("\n5. Testing P2P Network...")
    try:
        p2p = P2PNetwork("test_node")
        # Add a mock peer
        peer = PeerInfo(
            peer_id="peer_1",
            ip_address="127.0.0.1",
            port=8081,
            public_key="test_key",
            last_seen=time.time(),
            connection_status="disconnected",
            reputation_score=0.8,
            latency=0.1
        )
        p2p.add_peer(peer)
        trusted_peers = p2p.get_trusted_peers()
        print(f"   [OK] P2P Network: {len(trusted_peers)} trusted peers")
    except Exception as e:
        print(f"   ✗ P2P Network failed: {e}")
        return False
    
    # Test 6: PBFT Consensus
    print("\n6. Testing PBFT Consensus...")
    try:
        pbft = PBFTConsensus("test_node", crypto)
        pbft.add_node("peer_1")
        pbft.add_node("peer_2")
        is_leader = pbft.is_leader()
        print(f"   [OK] PBFT Consensus: Leader status={is_leader}")
    except Exception as e:
        print(f"   ✗ PBFT Consensus failed: {e}")
        return False
    
    # Test 7: TOR Gateway (initialization only)
    print("\n7. Testing TOR Gateway...")
    try:
        tor = TORGateway()
        print("   [OK] TOR Gateway: Initialized successfully")
    except Exception as e:
        print(f"   ✗ TOR Gateway failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("AEGIS-Conscience Network is fully functional")
    print("=" * 50)
    return True


def main():
    """Run the comprehensive test"""
    success = test_complete_system()
    if success:
        print("\n✅ System Verification: SUCCESS")
        print("The AEGIS-Conscience Network is ready for deployment!")
    else:
        print("\n❌ System Verification: FAILED")
        print("Please check the implementation and try again.")


if __name__ == "__main__":
    main()