#!/usr/bin/env python3
"""
Simple Metatron Integration Test
================================

This script tests the basic integration between the Hebrew Quantum Field
and the 13-node Metatron consciousness system.
"""

import sys
import os
import numpy as np
from typing import Dict, Any
import logging

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))
sys.path.insert(0, os.path.dirname(__file__))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_metatron_import():
    """Test importing the Metatron system"""
    try:
        from orchestrator.metatron_orchestrator import MetatronConsciousness
        print("✅ Metatron system imported successfully")
        return MetatronConsciousness
    except ImportError as e:
        print(f"❌ Failed to import Metatron system: {e}")
        return None

def test_hebrew_import():
    """Test importing the Hebrew Quantum Field component"""
    try:
        from hebrew_quantum_ui_component import HebrewQuantumFieldUIComponent
        print("✅ Hebrew Quantum Field component imported successfully")
        return HebrewQuantumFieldUIComponent
    except ImportError as e:
        print(f"❌ Failed to import Hebrew Quantum Field component: {e}")
        return None

def run_simple_integration_test():
    """Run a simple integration test"""
    print("=" * 80)
    print("SIMPLE METATRON-HEBREW INTEGRATION TEST")
    print("=" * 80)
    
    # Test imports
    MetatronConsciousness = test_metatron_import()
    HebrewQuantumFieldUIComponent = test_hebrew_import()
    
    if not MetatronConsciousness or not HebrewQuantumFieldUIComponent:
        print("❌ Import failed, exiting...")
        return False
    
    # Initialize both systems
    print("\nInitializing systems...")
    metatron_system = MetatronConsciousness(base_frequency=40.0, dt=0.05)
    hebrew_field = HebrewQuantumFieldUIComponent()
    
    print("✅ Both systems initialized successfully")
    
    # Test basic functionality
    print("\nTesting basic functionality...")
    
    # Update Metatron system
    metatron_state = metatron_system.update_system()
    print(f"✅ Metatron system updated - Time: {metatron_state['time']:.2f}s")
    
    # Update Hebrew field
    hebrew_data = hebrew_field.get_visualization_data()
    print(f"✅ Hebrew field updated - Time: {hebrew_data['time']:.2f}s")
    
    # Check node data
    nodes_data = metatron_state['nodes']
    print(f"✅ Metatron nodes: {len(nodes_data)}")
    
    # Check Hebrew letters
    hebrew_letters = hebrew_data['letters']
    print(f"✅ Hebrew letters: {len(hebrew_letters)}")
    
    # Show sample data
    print("\nSample Data:")
    print(f"  Metatron consciousness level: {metatron_state['global']['consciousness_level']:.4f}")
    print(f"  Metatron Φ: {metatron_state['global']['phi']:.4f}")
    print(f"  Hebrew connections: {len(hebrew_data['connections'])}")
    
    # Test a few updates
    print("\nRunning 5 update cycles...")
    for i in range(5):
        # Update both systems
        metatron_state = metatron_system.update_system()
        hebrew_data = hebrew_field.get_visualization_data()
        
        if i % 2 == 0:  # Show progress every 2 steps
            c_level = metatron_state['global']['consciousness_level']
            phi = metatron_state['global']['phi']
            print(f"  Step {i+1}: C={c_level:.4f}, Φ={phi:.4f}")
    
    # Create a simple mapping between systems
    print("\nCreating simple mapping...")
    hebrew_chars = list(hebrew_letters.keys())
    node_ids = list(nodes_data.keys())
    
    # Map first 13 Hebrew letters to nodes (or fewer if less available)
    mapping_count = min(len(hebrew_chars), len(node_ids), 13)
    simple_mapping = {}
    for i in range(mapping_count):
        simple_mapping[hebrew_chars[i]] = node_ids[i] if i < len(node_ids) else i
    
    print(f"✅ Created mapping for {len(simple_mapping)} Hebrew letters to Metatron nodes")
    
    # Show sample mapping
    print("\nSample Mapping:")
    for char, node_id in list(simple_mapping.items())[:5]:
        letter_info = hebrew_letters[char]
        print(f"  {char} ({letter_info['name']}) -> Node {node_id}")
    
    # Demonstrate bidirectional influence
    print("\nDemonstrating bidirectional influence...")
    
    # Get a sample node output
    sample_node_id = 0
    if sample_node_id in nodes_data:
        sample_output = nodes_data[sample_node_id]['output']
        sample_phase = nodes_data[sample_node_id]['oscillator']['phase']
        print(f"  Node {sample_node_id} output: {sample_output:.4f}, phase: {sample_phase:.4f}")
        
        # Influence a Hebrew letter based on node output
        sample_char = hebrew_chars[0] if hebrew_chars else 'א'
        hebrew_state = hebrew_field.quantum_states[sample_char]
        print(f"  Hebrew letter {sample_char} before influence - energy: {hebrew_state.energy:.4f}, phase: {hebrew_state.phase:.4f}")
        
        # Apply influence
        energy_influence = 0.1 * abs(sample_output)
        hebrew_state.energy = 0.9 * hebrew_state.energy + 0.1 * (1.0 + energy_influence)
        phase_influence = 0.05 * sample_phase
        hebrew_state.phase = (hebrew_state.phase + phase_influence) % (2 * np.pi)
        
        print(f"  Hebrew letter {sample_char} after influence - energy: {hebrew_state.energy:.4f}, phase: {hebrew_state.phase:.4f}")
    
    print("\n" + "=" * 80)
    print("SIMPLE INTEGRATION TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    try:
        success = run_simple_integration_test()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Error in integration test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)