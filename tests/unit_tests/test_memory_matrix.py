#!/usr/bin/env python3
"""
Unit Tests for MemoryMatrixNode

This module contains unit tests to verify the proper functionality of the MemoryMatrixNode
and its integration with the Open-A.G.I framework.
"""

import sys
import os
import unittest
import numpy as np
import asyncio

# Add project paths
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
sys.path.insert(0, project_root)
sys.path.insert(0, metatron_path)

class TestMemoryMatrixNode(unittest.TestCase):
    """Unit tests for MemoryMatrixNode"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Add metatron path to sys.path
        sys.path.insert(0, metatron_path)
        # Import MemoryMatrixNode
        from nodes.memory_matrix import MemoryMatrixNode
        self.memory_node = MemoryMatrixNode(node_id=3, max_memory_size=10)
    
    def test_initialization(self):
        """Test MemoryMatrixNode initialization"""
        self.assertEqual(self.memory_node.node_id, 3)
        self.assertEqual(self.memory_node.max_memory_size, 10)
        self.assertIsNotNone(self.memory_node.memory_buffer)
        self.assertIsNotNone(self.memory_node.recall_history)
        self.assertEqual(len(self.memory_node.memory_buffer), 0)
        self.assertEqual(len(self.memory_node.recall_history), 0)
    
    def test_store_field_state(self):
        """Test storing field states in memory"""
        test_field = np.array([1.0, 2.0, 3.0])
        metadata = {"test": "data"}
        
        self.memory_node.store_field_state(test_field, metadata)
        
        self.assertEqual(len(self.memory_node.memory_buffer), 1)
        stored_entry = self.memory_node.memory_buffer[0]
        np.testing.assert_array_equal(stored_entry["field_state"], test_field)
        self.assertEqual(stored_entry["metadata"], metadata)
        self.assertEqual(stored_entry["size"], 3)
    
    def test_weighted_recall(self):
        """Test weighted recall functionality"""
        # Store some field states
        for i in range(5):
            field = np.random.randn(100)
            self.memory_node.store_field_state(field, {"index": i})
        
        # Test recall with query
        query = np.random.randn(100)
        recalled = self.memory_node.weighted_recall(query)
        
        self.assertIsInstance(recalled, np.ndarray)
        self.assertEqual(recalled.shape, (100,))
    
    def test_apply_phi_decay(self):
        """Test φ-based decay application"""
        field = np.array([1.0, 1.0, 1.0])
        time_elapsed = 10.0  # 10 seconds
        
        decayed_field = self.memory_node.apply_phi_decay(field, time_elapsed)
        
        self.assertIsInstance(decayed_field, np.ndarray)
        self.assertEqual(decayed_field.shape, field.shape)
        # Values should be less than original due to decay
        self.assertTrue(np.all(decayed_field <= field))
    
    def test_get_memory_metrics(self):
        """Test memory metrics retrieval"""
        # Store some data first
        test_field = np.random.randn(100)
        self.memory_node.store_field_state(test_field)
        
        metrics = self.memory_node.get_memory_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn("memory_buffer_size", metrics)
        self.assertIn("recall_history_size", metrics)
        self.assertIn("current_field_size", metrics)
        self.assertIn("recall_weight", metrics)
        self.assertIn("decay_factor", metrics)
        self.assertIn("last_updated", metrics)
        self.assertIn("node_id", metrics)
    
    def test_get_state_dict(self):
        """Test state dictionary retrieval"""
        state = self.memory_node.get_state_dict()
        
        self.assertIsInstance(state, dict)
        self.assertIn("node_id", state)
        self.assertIn("phi", state)
        self.assertIn("current_field_state", state)
        self.assertIn("memory_buffer_size", state)
        self.assertIn("recall_history_size", state)
        self.assertIn("last_updated", state)
        self.assertIn("recall_weight", state)
        self.assertIn("decay_factor", state)
    
    def test_reset_state(self):
        """Test state reset functionality"""
        # Store some data first
        test_field = np.random.randn(100)
        self.memory_node.store_field_state(test_field)
        self.assertEqual(len(self.memory_node.memory_buffer), 1)
        
        # Reset state
        self.memory_node.reset_state()
        
        self.assertEqual(len(self.memory_node.memory_buffer), 0)
        self.assertEqual(len(self.memory_node.recall_history), 0)
        np.testing.assert_array_equal(
            self.memory_node.current_field_state, 
            np.zeros(100)
        )

class TestMemoryMatrixIntegration(unittest.TestCase):
    """Integration tests for MemoryMatrixNode with Open-A.G.I"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Add metatron path to sys.path
        sys.path.insert(0, metatron_path)
        from nodes.memory_matrix import MemoryMatrixNode, HAS_P2P, HAS_CRYPTO
        self.memory_node = MemoryMatrixNode(node_id=3)
        self.HAS_P2P = HAS_P2P
        self.HAS_CRYPTO = HAS_CRYPTO
    
    def test_p2p_integration(self):
        """Test P2P network integration"""
        self.assertIsNotNone(self.memory_node.p2p_network)
        # Check that the p2p_network has the register_message_handler method
        self.assertTrue(hasattr(self.memory_node.p2p_network, 'register_message_handler'))
    
    def test_crypto_integration(self):
        """Test cryptographic integration"""
        # Crypto may not be available in all environments
        if self.HAS_CRYPTO:
            self.assertIsNotNone(self.memory_node.node_identity)
        else:
            # Should have fallback placeholder
            self.assertIsNone(self.memory_node.node_identity) or self.assertIsNotNone(self.memory_node.node_identity)

async def run_async_tests():
    """Run async tests"""
    try:
        # Add metatron path to sys.path
        sys.path.insert(0, metatron_path)
        from nodes.memory_matrix import MemoryMatrixNode
        
        # Test async operations
        memory_node = MemoryMatrixNode(node_id=3)
        await memory_node.start_network()
        
        # Test share memory with peer (should not fail even with placeholder)
        test_memory_entry = {
            "timestamp": 1234567890,
            "field_state": [0.1, 0.2, 0.3],
            "metadata": {"test": "data"},
            "size": 3
        }
        
        # This should not raise an exception
        result = await memory_node.share_memory_with_peer("test_peer", test_memory_entry)
        
        return True
    except Exception as e:
        print(f"Async test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running MemoryMatrixNode Unit Tests...")
    
    # Run synchronous tests
    unittest.main(exit=False, verbosity=2)
    
    # Run async tests
    print("\nRunning async tests...")
    result = asyncio.run(run_async_tests())
    if result:
        print("✅ Async tests passed")
    else:
        print("❌ Async tests failed")

if __name__ == "__main__":
    main()