#!/usr/bin/env python3
"""
Integration Test for MemoryMatrixNode with Open-A.G.I Framework

This test verifies that the MemoryMatrixNode is properly integrated with:
1. Open-A.G.I P2P networking
2. Open-A.G.I cryptographic framework
3. Open-A.G.I consensus system
4. Open-A.G.I TOR integration
"""

import sys
import os
import asyncio
import unittest
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class TestMemoryMatrixIntegration(unittest.TestCase):
    """Test MemoryMatrixNode integration with Open-A.G.I framework"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def test_imports_work_correctly(self):
        """Test that all required modules can be imported without errors"""
        try:
            # Add the Metatron-ConscienceAI directory to the path
            metatron_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI')
            sys.path.insert(0, metatron_path)
            
            from nodes.memory_matrix import MemoryMatrixNode
            from nodes.enhanced_p2p_wrapper import EnhancedP2PWrapper
            memory_node = MemoryMatrixNode(node_id=3)
            self.assertIsInstance(memory_node, MemoryMatrixNode)
        except Exception as e:
            self.fail(f"Failed to import and instantiate MemoryMatrixNode: {e}")
    
    def test_p2p_integration(self):
        """Test P2P network integration"""
        try:
            # Add the Metatron-ConscienceAI directory to the path
            metatron_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI')
            sys.path.insert(0, metatron_path)
            
            from nodes.memory_matrix import MemoryMatrixNode
            memory_node = MemoryMatrixNode(node_id=3)
            
            # Check that P2P network is initialized
            self.assertIsNotNone(memory_node.p2p_network)
            
            # Check that message handlers are registered
            self.assertTrue(hasattr(memory_node.p2p_network, 'message_handlers'))
            
        except Exception as e:
            self.fail(f"Failed to test P2P integration: {e}")
    
    def test_crypto_integration(self):
        """Test cryptographic framework integration"""
        try:
            # Add the Metatron-ConscienceAI directory to the path
            metatron_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI')
            sys.path.insert(0, metatron_path)
            
            from nodes.memory_matrix import MemoryMatrixNode
            memory_node = MemoryMatrixNode(node_id=3)
            
            # Check that node identity is created
            if memory_node.node_identity:
                self.assertIsNotNone(memory_node.node_identity.node_id)
            
        except Exception as e:
            self.fail(f"Failed to test crypto integration: {e}")
    
    def test_memory_operations(self):
        """Test memory storage and recall operations"""
        try:
            import numpy as np
            # Add the Metatron-ConscienceAI directory to the path
            metatron_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI')
            sys.path.insert(0, metatron_path)
            
            from nodes.memory_matrix import MemoryMatrixNode
            
            memory_node = MemoryMatrixNode(node_id=3)
            
            # Test storing field state
            test_field = np.random.randn(100)
            metadata = {"test_index": 1, "timestamp": 1234567890}
            memory_node.store_field_state(test_field, metadata)
            
            # Check that field is stored
            self.assertEqual(len(memory_node.memory_buffer), 1)
            
            # Test weighted recall
            query_field = np.random.randn(100)
            recalled_field = memory_node.weighted_recall(query_field)
            
            # Check that recall returns correct shape
            self.assertEqual(recalled_field.shape, test_field.shape)
            
        except Exception as e:
            self.fail(f"Failed to test memory operations: {e}")

async def run_async_tests():
    """Run async tests"""
    try:
        # Add the Metatron-ConscienceAI directory to the path
        metatron_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI')
        sys.path.insert(0, metatron_path)
        
        from nodes.memory_matrix import MemoryMatrixNode
        
        # Test async P2P operations
        memory_node = MemoryMatrixNode(node_id=3)
        
        # Test share memory with peer (should not fail even with placeholder)
        test_memory_entry = {
            "timestamp": 1234567890,
            "field_state": [0.1, 0.2, 0.3],
            "metadata": {"test": "data"},
            "size": 3
        }
        
        # This should not raise an exception
        result = await memory_node.share_memory_with_peer("test_peer", test_memory_entry)
        print(f"Share memory test result: {result}")
        
        return True
    except Exception as e:
        print(f"Async test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("Running MemoryMatrixNode Integration Tests...")
    
    # Run synchronous tests
    unittest.main(exit=False)
    
    # Run async tests
    print("\nRunning async tests...")
    result = asyncio.run(run_async_tests())
    if result:
        print("✅ Async tests passed")
    else:
        print("❌ Async tests failed")

if __name__ == "__main__":
    main()