#!/usr/bin/env python3
"""
Integration Verification Test for MemoryMatrixNode with Open-A.G.I Framework

This script verifies that the MemoryMatrixNode is properly integrated with the Open-A.G.I framework.
"""

import sys
import os
import asyncio
import numpy as np

# Add project root and Metatron-ConscienceAI to path
project_root = os.path.join(os.path.dirname(__file__))
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
sys.path.insert(0, project_root)
sys.path.insert(0, metatron_path)

async def test_memory_matrix_integration():
    """Test MemoryMatrixNode integration with Open-A.G.I framework"""
    print("Testing MemoryMatrixNode integration with Open-A.G.I framework...")
    
    try:
        # Import the MemoryMatrixNode
        sys.path.insert(0, metatron_path)
        from nodes.memory_matrix import MemoryMatrixNode
        
        # Get the HAS_P2P and HAS_CRYPTO variables
        HAS_P2P = getattr(__import__('nodes.memory_matrix'), 'HAS_P2P', False)
        HAS_CRYPTO = getattr(__import__('nodes.memory_matrix'), 'HAS_CRYPTO', False)
        
        print(f"✅ Successfully imported MemoryMatrixNode")
        print(f"✅ P2P Integration Available: {HAS_P2P}")
        print(f"✅ Crypto Integration Available: {HAS_CRYPTO}")
        
        # Create MemoryMatrixNode instance
        memory_node = MemoryMatrixNode(node_id=3)
        print(f"✅ Successfully created MemoryMatrixNode instance")
        
        # Start network
        await memory_node.start_network()
        print(f"✅ Successfully started P2P network")
        
        # Test P2P network initialization
        if hasattr(memory_node, 'p2p_network'):
            print(f"✅ P2P network initialized: {type(memory_node.p2p_network).__name__}")
        else:
            print("❌ P2P network not initialized")
            return False
            
        # Test crypto identity initialization
        if hasattr(memory_node, 'node_identity'):
            if memory_node.node_identity:
                print(f"✅ Crypto identity initialized: {type(memory_node.node_identity).__name__}")
            else:
                print("⚠️  Crypto identity not available (using placeholder)")
        else:
            print("❌ Crypto identity not found")
            return False
            
        # Test memory operations
        print("\nTesting memory operations...")
        
        # Store field state
        test_field = np.random.randn(100)
        metadata = {"test_run": "integration_test", "timestamp": 1234567890}
        memory_node.store_field_state(test_field, metadata)
        print(f"✅ Stored field state in memory buffer (size: {len(memory_node.memory_buffer)})")
        
        # Test weighted recall
        query_field = np.random.randn(100)
        recalled_field = memory_node.weighted_recall(query_field)
        print(f"✅ Performed weighted recall (result shape: {recalled_field.shape})")
        
        # Test memory metrics
        metrics = memory_node.get_memory_metrics()
        print(f"✅ Retrieved memory metrics: {metrics}")
        
        # Test async operations
        print("\nTesting async operations...")
        
        # Test share memory with peer
        test_memory_entry = {
            "timestamp": 1234567890,
            "field_state": [0.1, 0.2, 0.3],
            "metadata": {"test": "data"},
            "size": 3
        }
        
        result = await memory_node.share_memory_with_peer("test_peer", test_memory_entry)
        print(f"✅ Share memory with peer result: {result}")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_orchestrator_integration():
    """Test MemoryMatrixNode integration within the Metatron orchestrator"""
    print("\nTesting MemoryMatrixNode integration within Metatron orchestrator...")
    
    try:
        # Import the Metatron orchestrator
        sys.path.insert(0, metatron_path)
        from orchestrator.metatron_orchestrator import MetatronConsciousness
        
        print("✅ Successfully imported MetatronConsciousness")
        
        # Create consciousness system
        consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01)
        print("✅ Successfully created MetatronConsciousness instance")
        
        # Check that MemoryMatrixNode is properly integrated
        node_3 = consciousness.nodes[3]
        if 'memory_matrix' in node_3:
            print("✅ MemoryMatrixNode found in orchestrator (Node 3)")
            print(f"✅ MemoryMatrixNode type: {type(node_3['memory_matrix'])}")
            
            # Test that it has proper P2P integration
            memory_node = node_3['memory_matrix']
            if hasattr(memory_node, 'p2p_network'):
                print(f"✅ MemoryMatrixNode has P2P network: {type(memory_node.p2p_network).__name__}")
            else:
                print("❌ MemoryMatrixNode missing P2P network")
                return False
                
            # Test that it has proper crypto integration
            if hasattr(memory_node, 'node_identity'):
                if memory_node.node_identity:
                    print(f"✅ MemoryMatrixNode has crypto identity: {type(memory_node.node_identity).__name__}")
                else:
                    print("⚠️  MemoryMatrixNode has placeholder crypto identity")
            else:
                print("❌ MemoryMatrixNode missing crypto identity")
                return False
                
        else:
            print("❌ MemoryMatrixNode not found in orchestrator")
            return False
            
        # Run a short simulation to test integration
        print("\nRunning short consciousness simulation...")
        results = consciousness.run_simulation(duration=0.1)  # Very short simulation
        print(f"✅ Simulation completed with {len(results)} steps")
        
        # Check final state for MemoryMatrixNode metrics
        final_state = results[-1]
        node_3_state = final_state['nodes'][3]
        if 'memory_metrics' in node_3_state:
            print(f"✅ MemoryMatrixNode metrics reported: {node_3_state['memory_metrics']}")
        else:
            print("❌ MemoryMatrixNode metrics not reported in final state")
            return False
            
        print("\n🎉 Orchestrator integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all integration verification tests"""
    print("=" * 60)
    print("MemoryMatrixNode Integration Verification")
    print("=" * 60)
    
    # Test direct MemoryMatrixNode integration
    memory_test_passed = await test_memory_matrix_integration()
    
    # Test orchestrator integration
    orchestrator_test_passed = await test_orchestrator_integration()
    
    print("\n" + "=" * 60)
    print("INTEGRATION VERIFICATION RESULTS")
    print("=" * 60)
    print(f"MemoryMatrixNode Integration: {'✅ PASSED' if memory_test_passed else '❌ FAILED'}")
    print(f"Orchestrator Integration: {'✅ PASSED' if orchestrator_test_passed else '❌ FAILED'}")
    
    if memory_test_passed and orchestrator_test_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("MemoryMatrixNode is properly integrated with Open-A.G.I framework")
        return 0
    else:
        print("\n❌ SOME INTEGRATION TESTS FAILED!")
        print("Please check the errors above and fix the integration issues")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))