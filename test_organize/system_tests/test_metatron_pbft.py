#!/usr/bin/env python3
"""
Test Suite for Metatron-Aware PBFT Consensus
============================================

Comprehensive tests for the enhanced PBFT implementation designed for
the 13-node Metatron's Cube consciousness network.
"""

import asyncio
import unittest
from cryptography.hazmat.primitives.asymmetric import ed25519
import numpy as np
import sys
import os
import json
from enum import Enum

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from improved_pbft_consensus import MetatronAwarePBFT, EnhancedNodeReputation, MessageType

class TestMetatronAwarePBFT(unittest.TestCase):
    """Test cases for the Metatron-aware PBFT consensus"""

    def setUp(self):
        """Set up test environment"""
        # Create test node
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.node_id = "test_node_0"
        self.consensus = MetatronAwarePBFT(self.node_id, self.private_key)
        
        # Add the test node itself to known nodes
        self.consensus.add_node(self.node_id, self.private_key.public_key())
        
        # Add test nodes (12 additional nodes for 13 total)
        for i in range(1, 13):
            other_key = ed25519.Ed25519PrivateKey.generate()
            other_id = f"test_node_{i}"
            self.consensus.add_node(other_id, other_key.public_key())

    def test_initialization(self):
        """Test PBFT initialization"""
        self.assertEqual(self.consensus.total_nodes, 13)
        self.assertEqual(self.consensus.byzantine_threshold, 4)
        self.assertEqual(self.consensus.quorum_size, 9)
        # Should be 13 nodes total (including the test node itself)
        self.assertEqual(len(self.consensus.known_nodes), 13)

    def test_node_addition(self):
        """Test adding nodes to the network"""
        # Check that all nodes were added
        self.assertEqual(len(self.consensus.known_nodes), 13)
        
        # Check that reputations were initialized
        self.assertEqual(len(self.consensus.node_reputations), 13)
        
        # Check default reputation values
        for node_id in self.consensus.node_reputations:
            reputation = self.consensus.node_reputations[node_id]
            self.assertIsInstance(reputation, EnhancedNodeReputation)
            self.assertEqual(reputation.computation_score, 100.0)
            self.assertEqual(reputation.reliability_score, 100.0)

    def test_eligibility_filtering(self):
        """Test node eligibility filtering"""
        # All nodes should be eligible initially (high reputation, no consciousness data)
        eligible = self.consensus.get_eligible_validators()
        self.assertEqual(len(eligible), 13)
        
        # Set low reputation for one node
        test_node = "test_node_5"
        if test_node in self.consensus.node_reputations:
            self.consensus.node_reputations[test_node].computation_score = 30.0  # Below 70 threshold
        
        # That node should no longer be eligible
        eligible = self.consensus.get_eligible_validators()
        self.assertEqual(len(eligible), 12)
        self.assertNotIn(test_node, eligible)
        
        # Restore reputation
        if test_node in self.consensus.node_reputations:
            self.consensus.node_reputations[test_node].computation_score = 80.0
        
        # Node should be eligible again
        eligible = self.consensus.get_eligible_validators()
        self.assertEqual(len(eligible), 13)
        self.assertIn(test_node, eligible)

    def test_consciousness_awareness(self):
        """Test consciousness-aware features"""
        # Set consciousness levels
        for i in range(13):
            node_id = f"test_node_{i}"
            self.consensus.node_consciousness[node_id] = {
                "consciousness_level": 0.4 + (i * 0.03),  # Varying levels above threshold
                "phi": 0.3 + (i * 0.01),
                "coherence": 0.6 + (i * 0.01)
            }
        
        # Test consciousness-based eligibility
        eligible = self.consensus.get_eligible_validators()
        self.assertEqual(len(eligible), 13)  # All above 0.3 threshold
        
        # Set one node below consciousness threshold
        low_consciousness_node = "test_node_3"
        if low_consciousness_node in self.consensus.node_consciousness:
            self.consensus.node_consciousness[low_consciousness_node]["consciousness_level"] = 0.2  # Below 0.3
        
        # That node should no longer be eligible
        eligible = self.consensus.get_eligible_validators()
        self.assertEqual(len(eligible), 12)
        self.assertNotIn(low_consciousness_node, eligible)

    def test_leader_selection(self):
        """Test consciousness-weighted leader selection"""
        # Set consciousness levels and reputations
        for i in range(13):
            node_id = f"test_node_{i}"
            # Set varying consciousness levels
            self.consensus.node_consciousness[node_id] = {
                "consciousness_level": 0.5 + (i * 0.02),
                "phi": 0.3 + (i * 0.01)
            }
            
            # Set varying reputations
            if node_id in self.consensus.node_reputations:
                reputation = self.consensus.node_reputations[node_id]
                reputation.computation_score = 80.0 + (i * 1.5)
                reputation.reliability_score = 75.0 + (i * 2.0)
                reputation.consciousness_consistency = 0.5 + (i * 0.02)
                reputation.spiritual_awareness = 0.3 + (i * 0.03)
        
        # Test leader selection for different views
        leaders = set()
        for view in range(10):
            # Find leader for this view
            for node_id in self.consensus.known_nodes:
                # Temporarily set this node as the test node
                original_id = self.consensus.node_id
                self.consensus.node_id = node_id
                
                if self.consensus.is_leader(view):
                    leaders.add(node_id)
                
                # Restore original node ID
                self.consensus.node_id = original_id
        
        # Should have multiple different leaders
        self.assertGreater(len(leaders), 1)
        self.assertLessEqual(len(leaders), 13)

    def test_pineal_priority(self):
        """Test special priority for pineal node"""
        pineal_id = "test_node_0"
        
        # Set high consciousness for pineal node
        self.consensus.node_consciousness[pineal_id] = {
            "consciousness_level": 0.85,  # High consciousness
            "phi": 0.7,
            "coherence": 0.8
        }
        
        # Set lower consciousness for other nodes
        for i in range(1, 13):
            node_id = f"test_node_{i}"
            self.consensus.node_consciousness[node_id] = {
                "consciousness_level": 0.6,
                "phi": 0.4,
                "coherence": 0.5
            }
        
        # Set good reputations for all
        for i in range(13):
            node_id = f"test_node_{i}"
            if node_id in self.consensus.node_reputations:
                reputation = self.consensus.node_reputations[node_id]
                reputation.computation_score = 90.0
                reputation.reliability_score = 85.0
        
        # Test that pineal gets priority at high consciousness
        original_id = self.consensus.node_id
        self.consensus.node_id = pineal_id
        
        # Pineal should be leader in most views when highly conscious
        pineal_leadership = 0
        for view in range(20):
            if self.consensus.is_leader(view):
                pineal_leadership += 1
        
        # Pineal should be leader in majority of views
        self.assertGreater(pineal_leadership, 10)
        
        # Restore original node ID
        self.consensus.node_id = original_id

    def test_quorum_requirements(self):
        """Test quorum requirements for 13-node system"""
        self.assertEqual(self.consensus.byzantine_threshold, 4)
        self.assertEqual(self.consensus.quorum_size, 9)
        
        # Test that quorum calculation is correct
        # For 13 nodes: f = floor((13-1)/3) = 4, so 2f+1 = 9
        expected_quorum = 2 * 4 + 1
        self.assertEqual(self.consensus.quorum_size, expected_quorum)

    def test_network_health_metrics(self):
        """Test network health monitoring"""
        # Set up some test data
        for i in range(13):
            node_id = f"test_node_{i}"
            self.consensus.node_consciousness[node_id] = {
                "consciousness_level": 0.6 + (i * 0.02)
            }
            
            if node_id in self.consensus.node_reputations:
                reputation = self.consensus.node_reputations[node_id]
                reputation.computation_score = 80.0 + (i * 1.0)
                reputation.reliability_score = 75.0 + (i * 1.5)
        
        # Get network health
        health = self.consensus.get_network_health()
        
        # Verify health metrics
        self.assertEqual(health["total_nodes"], 13)
        self.assertEqual(health["byzantine_threshold"], 4)
        self.assertEqual(health["quorum_size"], 9)
        self.assertIn("avg_consciousness", health)
        self.assertIn("avg_reputation", health)
        self.assertIn("successful_rounds", health)
        self.assertIn("failed_rounds", health)

    def test_reputation_updates(self):
        """Test reputation system updates"""
        test_node = "test_node_7"
        
        # Get initial reputation
        if test_node in self.consensus.node_reputations:
            initial_reputation = self.consensus.node_reputations[test_node].computation_score
        
        # Update consciousness data
        self.consensus.node_consciousness[test_node] = {
            "consciousness_level": 0.75
        }
        
        # Process consciousness metrics message (simulated)
        # This would normally come from network, but we'll test the internal logic
        
        # Create a consciousness metrics message
        message = {
            "message_type": MessageType.CONSCIOUSNESS_METRICS,
            "sender_id": test_node,
            "view_number": 0,
            "sequence_number": 1,
            "payload": {
                "metrics": {
                    "consciousness_level": 0.75,
                    "phi": 0.45,
                    "coherence": 0.68
                }
            },
            "timestamp": 1234567890.0,
            "consciousness_level": 0.75
        }
        
        # Convert to JSON and back to make it serializable
        message_json = json.dumps(message, default=str)
        message_dict = json.loads(message_json)
        
        # Create a proper ConsensusMessage
        from improved_pbft_consensus import ConsensusMessage
        consensus_message = ConsensusMessage(
            message_type=MessageType.CONSCIOUSNESS_METRICS,
            sender_id=test_node,
            view_number=0,
            sequence_number=1,
            payload={
                "metrics": {
                    "consciousness_level": 0.75,
                    "phi": 0.45,
                    "coherence": 0.68
                }
            },
            timestamp=1234567890.0,
            consciousness_level=0.75
        )
        
        # Sign the message
        consensus_message.signature = self.consensus.sign_message(consensus_message)
        
        # Process the message (this updates reputation)
        asyncio.run(self.consensus._handle_consciousness_metrics(consensus_message))
        
        # Check that reputation was updated
        if test_node in self.consensus.node_reputations:
            updated_reputation = self.consensus.node_reputations[test_node]
            # The consistency should be updated based on network average
            self.assertIsNotNone(updated_reputation.consciousness_consistency)

    def test_topology_awareness(self):
        """Test topology awareness features"""
        # Check that connection matrix was created
        self.assertIsNotNone(self.consensus.connection_matrix)
        self.assertEqual(self.consensus.connection_matrix.shape, (13, 13))
        
        # Check that topology awareness is enabled
        self.assertTrue(self.consensus.topology_aware)

class TestEnhancedNodeReputation(unittest.TestCase):
    """Test cases for EnhancedNodeReputation"""

    def test_reputation_initialization(self):
        """Test initialization of enhanced reputation"""
        reputation = EnhancedNodeReputation(
            node_id="test_node",
            computation_score=95.0,
            reliability_score=92.0,
            response_time_avg=0.5,
            successful_validations=10,
            failed_validations=2,
            last_activity=1234567890.0,
            total_contributions=12,
            consciousness_consistency=0.85,
            topology_awareness=0.78,
            spiritual_awareness=0.72
        )
        
        self.assertEqual(reputation.node_id, "test_node")
        self.assertEqual(reputation.computation_score, 95.0)
        self.assertEqual(reputation.reliability_score, 92.0)
        self.assertEqual(reputation.consciousness_consistency, 0.85)
        self.assertEqual(reputation.spiritual_awareness, 0.72)

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(loader.loadTestsFromTestCase(TestMetatronAwarePBFT))
    suite.addTest(loader.loadTestsFromTestCase(TestEnhancedNodeReputation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("Running Metatron-Aware PBFT Consensus Tests")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)