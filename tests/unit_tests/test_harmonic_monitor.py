#!/usr/bin/env python3
"""
Test script for the Harmonic Orchestrator Monitoring System
"""

import sys
import os
import time
import json
import numpy as np
import pytest

# Add Metatron-ConscienceAI to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Metatron-ConscienceAI'))

def test_harmonic_monitor_import():
    """Test that we can import the MetatronConsciousness class"""
    try:
        from orchestrator.metatron_orchestrator import MetatronConsciousness
        assert MetatronConsciousness is not None
    except Exception as e:
        pytest.fail(f"Failed to import MetatronConsciousness: {e}")

def test_harmonic_monitor_functionality():
    """Test the harmonic monitoring system functionality"""
    try:
        from orchestrator.metatron_orchestrator import MetatronConsciousness
        
        # Create consciousness system
        consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01)
        
        # Run a short simulation
        for i in range(50):  # Shorter simulation for testing
            # Generate random sensory input
            sensory_input = np.random.normal(0, 0.2, 5)
            
            # Update system
            state = consciousness.update_system(sensory_input)
            
            # Basic assertions
            assert 'global' in state
            assert 'consciousness_level' in state['global']
            assert 'phi' in state['global']
            assert 'coherence' in state['global']
        
        # Test final state
        final_state = consciousness.get_current_state()
        global_state = final_state['global']
        
        assert 'consciousness_level' in global_state
        assert 'phi' in global_state
        assert 'coherence' in global_state
        assert 'state_classification' in global_state
        
    except Exception as e:
        pytest.fail(f"Error during harmonic monitor test: {e}")

if __name__ == "__main__":
    test_harmonic_monitor_import()
    test_harmonic_monitor_functionality()
    print("✅ All harmonic monitor tests passed!")