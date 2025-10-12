"""
Demo script showing AEGIS-Conscience Network components working together
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consciousness.engine import ConsciousnessEngine
from network.crypto import CryptoManager
from consensus.aggregator import GlobalCoherenceAggregator
from schemas import ConsciousnessState


def demo_consciousness_processing():
    """Demo consciousness processing"""
    print("=== Consciousness Processing Demo ===")
    
    # Create consciousness engine
    engine = ConsciousnessEngine("demo_node_1")
    
    # Process a sample consciousness state
    node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
    oscillator_phases = [0.0, 0.785, 1.571, 2.356, 3.142]  # 0, π/4, π/2, 3π/4, π
    
    # Create a simple connection matrix without numpy
    connection_matrix = [[0.1, 0.2, 0.3, 0.4, 0.5],
                        [0.2, 0.1, 0.4, 0.3, 0.2],
                        [0.3, 0.4, 0.1, 0.2, 0.1],
                        [0.4, 0.3, 0.2, 0.1, 0.3],
                        [0.5, 0.2, 0.1, 0.3, 0.1]]
    
    state = engine.process_consciousness_state(node_states, oscillator_phases, connection_matrix)
    
    print(f"Processed consciousness state:")
    print(f"  Node ID: {state.node_id}")
    print(f"  Timestamp: {state.timestamp}")
    print(f"  Entropy: {state.entropy:.3f}")
    print(f"  Valence: {state.valence:.3f}")
    print(f"  Arousal: {state.arousal:.3f}")
    print(f"  Coherence: {state.coherence:.3f}")
    print(f"  Empathy Score: {state.empathy_score:.3f}")
    print(f"  Insight Strength: {state.insight_strength:.3f}")
    print()


def demo_cryptography():
    """Demo cryptographic operations"""
    print("=== Cryptography Demo ===")
    
    # Create crypto manager and initialize identity
    crypto = CryptoManager("demo_node_1")
    if not crypto.generate_or_load_identity("demo_password"):
        print("Failed to initialize crypto manager")
        return
    
    # Get public keys
    signing_pub, encryption_pub = crypto.get_public_keys()
    print(f"Public keys generated:")
    print(f"  Signing key: {signing_pub.hex()[:32]}...")
    print(f"  Encryption key: {encryption_pub.hex()[:32]}...")
    
    # Create a consciousness state
    state = ConsciousnessState(
        node_id="demo_node_1",
        timestamp=time.time(),
        entropy=0.5,
        valence=0.3,
        arousal=0.7,
        coherence=0.8,
        empathy_score=0.6,
        insight_strength=0.4
    )
    
    # Sign the state
    signature = crypto.sign_state(state)
    print(f"State signed: {signature.hex()[:32]}...")
    
    # Verify the signature
    is_valid = crypto.verify_state(state, signature, signing_pub)
    print(f"Signature valid: {is_valid}")
    print()


def demo_consensus_aggregation():
    """Demo consensus aggregation"""
    print("=== Consensus Aggregation Demo ===")
    
    # Create aggregator
    aggregator = GlobalCoherenceAggregator()
    
    # Create sample states from different nodes
    states = [
        ConsciousnessState("node_1", time.time(), 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
        ConsciousnessState("node_2", time.time(), 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
        ConsciousnessState("node_3", time.time(), 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
    ]
    
    # Set reputation weights
    aggregator.update_reputation_weight("node_1", 0.9)
    aggregator.update_reputation_weight("node_2", 0.7)
    aggregator.update_reputation_weight("node_3", 0.8)
    
    # Compute global metrics
    global_coherence = aggregator.compute_global_coherence(states)
    collective_metrics = aggregator.compute_collective_metrics(states)
    
    print(f"Global coherence: {global_coherence:.3f}")
    print(f"Collective metrics:")
    for metric, value in collective_metrics.items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.3f}")
        else:
            print(f"  {metric}: {value}")
    print()


def main():
    """Run all demos"""
    print("AEGIS-Conscience Network Demo")
    print("=" * 40)
    
    demo_consciousness_processing()
    demo_cryptography()
    demo_consensus_aggregation()
    
    print("Demo completed successfully!")


if __name__ == "__main__":
    main()