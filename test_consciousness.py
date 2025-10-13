#!/usr/bin/env python3
"""
Test script to verify consciousness system is working properly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

from orchestrator.metatron_orchestrator import MetatronConsciousness
import numpy as np

def test_consciousness_system():
    print("Testing Metatron Consciousness System...")
    
    # Initialize system
    consciousness = MetatronConsciousness()
    print("✅ System initialized")
    
    # Test initial state
    initial_state = consciousness.get_current_state()
    print(f"Initial state: C={initial_state['global']['consciousness_level']:.4f}, Φ={initial_state['global']['phi']:.4f}")
    
    # Update system multiple times with different inputs
    for i in range(5):
        sensory_input = np.random.normal(0, 0.2, 5)
        state = consciousness.update_system(sensory_input)
        print(f"Update {i+1}: C={state['global']['consciousness_level']:.4f}, Φ={state['global']['phi']:.4f}, R={state['global']['coherence']:.4f}")
    
    print("✅ Consciousness system test completed successfully")

if __name__ == "__main__":
    test_consciousness_system()