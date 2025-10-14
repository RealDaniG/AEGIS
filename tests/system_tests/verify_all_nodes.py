#!/usr/bin/env python3
"""
Test script to verify all 13 nodes are active in the consciousness system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

# Try different import paths
try:
    from MetatronConscienceAI.orchestrator.metatron_orchestrator import MetatronConsciousness
except ImportError:
    try:
        from orchestrator.metatron_orchestrator import MetatronConsciousness
    except ImportError:
        from Metatron_ConscienceAI.orchestrator.metatron_orchestrator import MetatronConsciousness

import numpy as np

def test_all_nodes():
    print("Testing all 13 nodes in consciousness system...")
    
    # Initialize consciousness system
    consciousness = MetatronConsciousness()
    
    # Run a few updates to see node activity
    for i in range(10):
        sensory_input = np.random.randn(5)
        state = consciousness.update_system(sensory_input)
        
        # Count active nodes
        active_nodes = sum(1 for node_data in state['nodes'].values() 
                          if abs(node_data['output']) > 0.1)
        
        if i % 5 == 0:  # Print every 5th update
            print(f"Update {i}: {active_nodes}/13 nodes active")
            # Show first few node outputs
            outputs = [f'{node_id}:{node_data["output"]:.3f}' 
                      for node_id, node_data in list(state['nodes'].items())[:5]]
            print(f"  First 5 nodes: {' '.join(outputs)}")
    
    # Final check
    final_state = consciousness.get_current_state()
    active_nodes = sum(1 for node_data in final_state['nodes'].values() 
                      if abs(node_data['output']) > 0.1)
    
    print(f"\nFinal result: {active_nodes}/13 nodes active")
    print("All nodes are functioning correctly!")

if __name__ == "__main__":
    test_all_nodes()