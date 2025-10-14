#!/usr/bin/env python3
"""
Test script to verify P2P integration in MemoryMatrixNode.
"""

import sys
import os
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nodes.memory_matrix import MemoryMatrixNode


def test_p2p_integration():
    """Test P2P integration features in MemoryMatrixNode."""
    print("=" * 60)
    print("TESTING P2P INTEGRATION IN MEMORY MATRIX NODE")
    print("=" * 60)
    
    # Create Memory Matrix Node
    print("Initializing MemoryMatrixNode...")
    memory_node = MemoryMatrixNode(node_id=3)
    
    # Test _establish_indirect_connection method
    print("\nTesting _establish_indirect_connection method...")
    result = memory_node._establish_indirect_connection("target_node_1", "relay_node_1")
    print(f"Connection result: {result}")
    assert result == True, "Indirect connection should succeed"
    print("✅ _establish_indirect_connection method works correctly")
    
    # Test that the node still functions normally
    print("\nTesting normal memory operations...")
    
    # Test storing field states
    test_field = np.random.randn(100)
    memory_node.store_field_state(test_field, {"test": "p2p_integration"})
    assert len(memory_node.memory_buffer) == 1, "Memory buffer should contain one entry"
    print("✅ Field state storage works correctly")
    
    # Test weighted recall
    recalled_field = memory_node.weighted_recall(test_field)
    assert recalled_field.shape == (100,), "Recalled field should have correct shape"
    print("✅ Weighted recall works correctly")
    
    # Test metrics
    metrics = memory_node.get_memory_metrics()
    assert "memory_buffer_size" in metrics, "Memory metrics should include buffer size"
    assert metrics["memory_buffer_size"] == 1, "Memory buffer size should be 1"
    print("✅ Memory metrics work correctly")
    
    print("\n" + "=" * 60)
    print("✅ ALL P2P INTEGRATION TESTS PASSED!")
    print("=" * 60)


def main():
    """Main test function."""
    try:
        test_p2p_integration()
        print("\n🎉 P2P integration test completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ P2P integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)