"""
Integration test for AEGIS-Conscience Network
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consciousness.engine import ConsciousnessEngine
from network.crypto import CryptoManager
from consensus.aggregator import GlobalCoherenceAggregator
from storage.knowledge_base import KnowledgeBase
from schemas import ConsciousnessState


def test_consciousness_engine():
    """Test consciousness engine"""
    print("Testing Consciousness Engine...")
    try:
        engine = ConsciousnessEngine("test_node")
        state = engine.get_current_state()
        print(f"  [OK] Consciousness Engine: {state.coherence:.3f} coherence")
        return True
    except Exception as e:
        print(f"  ✗ Consciousness Engine failed: {e}")
        return False


def test_crypto_manager():
    """Test crypto manager"""
    print("Testing Crypto Manager...")
    try:
        crypto = CryptoManager("test_node")
        # Generate identity with password
        if not crypto.generate_or_load_identity("test_password"):
            print(f"  ✗ Crypto Manager failed: Could not generate identity")
            return False
            
        # Test key generation
        signing_pub, encryption_pub = crypto.get_public_keys()
        print(f"  [OK] Crypto Manager: Keys generated")
        
        # Test signing
        state = ConsciousnessState(
            node_id="test_node",
            timestamp=time.time(),
            entropy=0.5,
            valence=0.3,
            arousal=0.7,
            coherence=0.8,
            empathy_score=0.6,
            insight_strength=0.4
        )
        signature = crypto.sign_state(state)
        is_valid = crypto.verify_state(state, signature, signing_pub)
        print(f"  [OK] Crypto Manager: Signing {'valid' if is_valid else 'invalid'}")
        return is_valid
    except Exception as e:
        print(f"  ✗ Crypto Manager failed: {e}")
        return False


def test_consensus_aggregator():
    """Test consensus aggregator"""
    print("Testing Consensus Aggregator...")
    try:
        aggregator = GlobalCoherenceAggregator()
        states = [
            ConsciousnessState("node_1", time.time(), 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
            ConsciousnessState("node_2", time.time(), 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
            ConsciousnessState("node_3", time.time(), 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
        ]
        global_coherence = aggregator.compute_global_coherence(states)
        print(f"  [OK] Consensus Aggregator: {global_coherence:.3f} global coherence")
        return True
    except Exception as e:
        print(f"  ✗ Consensus Aggregator failed: {e}")
        return False


def test_knowledge_base():
    """Test knowledge base"""
    print("Testing Knowledge Base...")
    try:
        kb = KnowledgeBase("test_node", "./test_knowledge")
        state = ConsciousnessState(
            node_id="test_node",
            timestamp=time.time(),
            entropy=0.5,
            valence=0.3,
            arousal=0.7,
            coherence=0.8,
            empathy_score=0.6,
            insight_strength=0.4
        )
        cid = kb.store_consciousness_state(state)
        retrieved = kb.retrieve_entry(cid)
        if retrieved:
            print(f"  [OK] Knowledge Base: Stored and retrieved entry {cid[:8]}...")
            return True
        else:
            print(f"  ✗ Knowledge Base: Failed to retrieve entry")
            return False
    except Exception as e:
        print(f"  ✗ Knowledge Base failed: {e}")
        return False


def main():
    """Run all tests"""
    print("AEGIS-Conscience Network Integration Test")
    print("=" * 45)
    
    tests = [
        test_consciousness_engine,
        test_crypto_manager,
        test_consensus_aggregator,
        test_knowledge_base
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All tests passed! AEGIS-Conscience Network is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")


if __name__ == "__main__":
    main()