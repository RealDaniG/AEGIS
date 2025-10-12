"""
Unit tests for the consciousness engine
"""

import unittest
import time
import numpy as np
from consciousness.engine import ConsciousnessEngine
from schemas import ConsciousnessState


class TestConsciousnessEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = ConsciousnessEngine("test_node")
    
    def test_initialization(self):
        """Test consciousness engine initialization"""
        self.assertEqual(self.engine.node_id, "test_node")
        self.assertEqual(len(self.engine.history_buffer), 0)
    
    def test_process_consciousness_state(self):
        """Test processing consciousness state"""
        # Create test data
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        oscillator_phases = [0.0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        connection_matrix = np.random.rand(5, 5) * 0.5
        
        # Process state
        state = self.engine.process_consciousness_state(
            node_states, 
            oscillator_phases, 
            connection_matrix
        )
        
        # Verify state
        self.assertIsInstance(state, ConsciousnessState)
        self.assertEqual(state.node_id, "test_node")
        self.assertGreaterEqual(state.timestamp, 0)
        self.assertGreaterEqual(state.entropy, 0.0)
        self.assertLessEqual(state.entropy, 1.0)
        self.assertGreaterEqual(state.coherence, 0.0)
        self.assertLessEqual(state.coherence, 1.0)
    
    def test_get_current_state(self):
        """Test getting current state"""
        state = self.engine.get_current_state()
        
        self.assertIsInstance(state, ConsciousnessState)
        self.assertEqual(state.node_id, "test_node")
        self.assertGreaterEqual(state.timestamp, 0)
    
    def test_calculate_integrated_information(self):
        """Test integrated information calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        connection_matrix = np.random.rand(5, 5) * 0.5
        
        phi = self.engine._calculate_integrated_information(node_states, connection_matrix)
        
        self.assertGreaterEqual(phi, 0.0)
        self.assertLessEqual(phi, 1.0)
    
    def test_calculate_global_coherence(self):
        """Test global coherence calculation"""
        oscillator_phases = [0.0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        
        coherence = self.engine._calculate_global_coherence(oscillator_phases)
        
        self.assertGreaterEqual(coherence, 0.0)
        self.assertLessEqual(coherence, 1.0)
    
    def test_calculate_entropy(self):
        """Test entropy calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        
        entropy = self.engine._calculate_entropy(node_states)
        
        self.assertGreaterEqual(entropy, 0.0)
        self.assertLessEqual(entropy, 1.0)
    
    def test_calculate_valence(self):
        """Test valence calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        
        valence = self.engine._calculate_valence(node_states)
        
        self.assertGreaterEqual(valence, -1.0)
        self.assertLessEqual(valence, 1.0)
    
    def test_calculate_arousal(self):
        """Test arousal calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        
        arousal = self.engine._calculate_arousal(node_states)
        
        self.assertGreaterEqual(arousal, 0.0)
        self.assertLessEqual(arousal, 1.0)
    
    def test_calculate_empathy(self):
        """Test empathy calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        
        # Add some history
        for i in range(5):
            self.engine.history_buffer.append({
                'coherence': 0.5 + i * 0.1
            })
        
        empathy = self.engine._calculate_empathy(node_states)
        
        self.assertGreaterEqual(empathy, 0.0)
        self.assertLessEqual(empathy, 1.0)
    
    def test_calculate_insight(self):
        """Test insight calculation"""
        node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
        
        # Add some history
        for i in range(10):
            self.engine.history_buffer.append({
                'entropy': 0.3 + i * 0.02
            })
        
        insight = self.engine._calculate_insight(node_states)
        
        self.assertGreaterEqual(insight, 0.0)
        self.assertLessEqual(insight, 1.0)


if __name__ == "__main__":
    unittest.main()