#!/usr/bin/env python3
"""
Test script to verify MemoryMatrixNode integration with the Metatron consciousness system.
"""

import sys
import os
import json
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from orchestrator.metatron_orchestrator import MetatronConsciousness
    print("✅ Successfully imported MetatronConsciousness")
except ImportError as e:
    print(f"❌ Failed to import MetatronConsciousness: {e}")
    raise SystemExit(1)

def test_memory_node_integration():
    """Test that MemoryMatrixNode is properly integrated into the consciousness system."""
    print("=" * 60)
    print("TESTING MEMORY MATRIX NODE INTEGRATION")
    print("=" * 60)
    
    # Initialize consciousness system
    print("Initializing consciousness system...")
    consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01)
    
    # Check that all 13 nodes are created
    print(f"Total nodes created: {len(consciousness.nodes)}")
    assert len(consciousness.nodes) == 13, f"Expected 13 nodes, got {len(consciousness.nodes)}"
    
    # Check that Node 3 is a MemoryMatrixNode
    node_3 = consciousness.nodes[3]
    assert 'memory_matrix' in node_3, "Node 3 should have a MemoryMatrix component"
    print("✅ Node 3 correctly initialized as MemoryMatrixNode")
    
    # Run a few simulation steps to test memory integration
    print("\nRunning simulation steps...")
    for step in range(5):
        # Generate random sensory input
        sensory_input = np.random.normal(0, 0.1, 5)
        
        # Update system
        state = consciousness.update_system(sensory_input)
        
        # Check that Node 3 has memory metrics
        node_3_state = state['nodes'][3]
        if 'memory_metrics' in node_3_state:
            memory_metrics = node_3_state['memory_metrics']
            print(f"Step {step + 1}: Node 3 memory buffer size: {memory_metrics['memory_buffer_size']}")
        
        # Print consciousness level
        c_level = state['global']['consciousness_level']
        print(f"Step {step + 1}: Consciousness level: {c_level:.4f}")
    
    # Get final state and verify MemoryMatrixNode metrics
    final_state = consciousness.get_current_state()
    node_3_final = final_state['nodes'][3]
    
    assert 'memory_metrics' in node_3_final, "Node 3 should have memory metrics in final state"
    
    memory_metrics = node_3_final['memory_metrics']
    print(f"\nFinal Node 3 Memory Metrics:")
    print(f"  Memory buffer size: {memory_metrics['memory_buffer_size']}")
    print(f"  Recall history size: {memory_metrics['recall_history_size']}")
    print(f"  Current field size: {memory_metrics['current_field_size']}")
    print(f"  Recall weight: {memory_metrics['recall_weight']:.6f}")
    print(f"  Decay factor: {memory_metrics['decay_factor']:.6f}")
    
    # Verify memory buffer is being populated
    assert memory_metrics['memory_buffer_size'] > 0, "Memory buffer should contain entries"
    print("✅ Memory buffer is being populated")
    
    # Test reset functionality
    print("\nTesting reset functionality...")
    consciousness.reset_system()
    
    # Check that Node 3 is reset
    reset_state = consciousness.get_current_state()
    reset_node_3 = reset_state['nodes'][3]
    reset_memory_metrics = reset_node_3['memory_metrics']
    
    assert reset_memory_metrics['memory_buffer_size'] == 0, "Memory buffer should be empty after reset"
    print("✅ MemoryMatrixNode reset successfully")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - MemoryMatrixNode is properly integrated!")
    print("=" * 60)
    
    return True

def main():
    """Main test function."""
    try:
        test_memory_node_integration()
        print("\n🎉 Memory Matrix Node integration test completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Memory Matrix Node integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)