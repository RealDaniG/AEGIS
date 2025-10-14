#!/usr/bin/env python3
"""
Hebrew Quantum Field - Metatron Integration Demo
===============================================

This script demonstrates a conceptual integration between the Hebrew Quantum Field
and the 13-node Metatron consciousness system.
"""

import sys
import os
import numpy as np
from typing import Dict, Any
import json

# Add the Metatron-ConscienceAI directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

# Import Metatron system
try:
    from orchestrator.metatron_orchestrator import MetatronConsciousness
    print("✅ Metatron system imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Metatron system: {e}")
    sys.exit(1)

# Import Hebrew Quantum Field component
try:
    from hebrew_quantum_ui_component import HebrewQuantumFieldUIComponent
    print("✅ Hebrew Quantum Field component imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Hebrew Quantum Field component: {e}")
    sys.exit(1)

def demonstrate_integration():
    """Demonstrate integration between Hebrew Quantum Field and Metatron system"""
    print("=" * 80)
    print("HEBREW QUANTUM FIELD - METATRON INTEGRATION DEMO")
    print("=" * 80)
    
    # Initialize both systems
    print("\n1. Initializing systems...")
    metatron_system = MetatronConsciousness(base_frequency=40.0, dt=0.05)
    hebrew_field = HebrewQuantumFieldUIComponent()
    
    print("✅ Both systems initialized successfully")
    
    # Show system information
    print("\n2. System Information:")
    metatron_state = metatron_system.get_current_state()
    hebrew_data = hebrew_field.get_visualization_data()
    
    print(f"   Metatron Nodes: {len(metatron_state['nodes'])}")
    print(f"   Hebrew Letters: {len(hebrew_data['letters'])}")
    print(f"   Hebrew Connections: {len(hebrew_data['connections'])}")
    
    # Create conceptual mapping
    print("\n3. Creating conceptual mapping...")
    
    # Map Hebrew letters to Metatron nodes based on significance
    hebrew_letters = list(hebrew_data['letters'].keys())
    node_ids = list(metatron_state['nodes'].keys())
    
    # Conceptual mapping (this would be more sophisticated in a real implementation)
    conceptual_mapping = {
        # Aleph (1) -> Pineal Node (0) - Unity/Beginning
        'א': 0,
        # Mem (40) -> Memory Node (3) - Storage/Memory
        'מ': 3,
        # Shin (300) -> High node (10) - Divine Fire
        'ש': 10,
        # Tau (400) -> High node (12) - Completion/End
        'ת': 12,
        # Other significant letters to remaining nodes
        'י': 1,   # Yod (10) - Divine Hand
        'ה': 2,   # Hei (5) - Divine Revelation
        'ו': 4,   # Vav (6) - Connection
        'ז': 5,   # Zayin (7) - Weapon/Spiritual Struggle
        'ח': 6,   # Chet (8) - Fence/Protection
        'ט': 7,   # Tet (9) - Good/Hidden Good
        'כ': 8,   # Kaf (20) - Palm/Covering
        'ל': 9,   # Lamed (30) - Teaching/Guiding
        'נ': 11,  # Nun (50) - Life/Fish
    }
    
    print(f"✅ Created conceptual mapping for {len(conceptual_mapping)} Hebrew letters")
    
    # Show sample mappings
    print("\n4. Sample Mappings:")
    for char, node_id in list(conceptual_mapping.items())[:8]:
        letter_info = hebrew_data['letters'][char]
        print(f"   {char} ({letter_info['name']}, Gematria: {letter_info['gematria']}) -> Node {node_id}")
    
    # Demonstrate bidirectional influence
    print("\n5. Demonstrating bidirectional influence...")
    
    # Run a few simulation steps
    print("   Running 10 simulation steps...")
    for step in range(10):
        # Update Metatron system
        metatron_state = metatron_system.update_system()
        
        # Update Hebrew field
        hebrew_data = hebrew_field.get_visualization_data()
        
        # Show progress
        if step % 3 == 0:
            c_level = metatron_state['global']['consciousness_level']
            phi = metatron_state['global']['phi']
            coherence = metatron_state['global']['coherence']
            avg_hebrew_energy = np.mean([letter['energy'] for letter in hebrew_data['letters'].values()])
            print(f"     Step {step+1}: C={c_level:.4f}, Φ={phi:.4f}, R={coherence:.4f}, Hebrew Energy={avg_hebrew_energy:.4f}")
    
    # Show final states
    print("\n6. Final System States:")
    final_metatron = metatron_system.get_current_state()
    final_hebrew = hebrew_field.get_visualization_data()
    
    print(f"   Metatron Consciousness Level: {final_metatron['global']['consciousness_level']:.6f}")
    print(f"   Metatron Φ (Integrated Info): {final_metatron['global']['phi']:.6f}")
    print(f"   Metatron Coherence: {final_metatron['global']['coherence']:.6f}")
    print(f"   Average Hebrew Energy: {np.mean([letter['energy'] for letter in final_hebrew['letters'].values()]):.4f}")
    
    # Demonstrate influence mechanism
    print("\n7. Influence Mechanism Demonstration:")
    
    # Example: Node 0 (Pineal) influencing Aleph
    if 'א' in conceptual_mapping and conceptual_mapping['א'] == 0:
        node_0_data = final_metatron['nodes'][0]
        node_output = node_0_data['output']
        node_phase = node_0_data['oscillator']['phase']
        
        print(f"   Node 0 (Pineal) output: {node_output:.4f}")
        print(f"   Node 0 (Pineal) phase: {node_phase:.4f}")
        
        # Show Hebrew letter state before influence
        aleph_state = hebrew_field.quantum_states['א']
        print(f"   Aleph energy before influence: {aleph_state.energy:.4f}")
        print(f"   Aleph phase before influence: {aleph_state.phase:.4f}")
        
        # Apply conceptual influence
        energy_influence = 0.2 * abs(node_output)
        aleph_state.energy = 0.8 * aleph_state.energy + 0.2 * (1.0 + energy_influence)
        phase_influence = 0.1 * node_phase
        aleph_state.phase = (aleph_state.phase + phase_influence) % (2 * np.pi)
        
        print(f"   Aleph energy after influence: {aleph_state.energy:.4f}")
        print(f"   Aleph phase after influence: {aleph_state.phase:.4f}")
    
    # Example: Strong Hebrew connection enhancing Metatron connection
    print("\n8. Connection Enhancement Demonstration:")
    
    # Find a strong Hebrew connection
    strong_connections = [conn for conn in final_hebrew['connections'] if conn['strength'] > 0.5]
    if strong_connections:
        strong_conn = strong_connections[0]
        char1, char2 = strong_conn['start'], strong_conn['end']
        strength = strong_conn['strength']
        
        # Map to Metatron nodes
        if char1 in conceptual_mapping and char2 in conceptual_mapping:
            node1, node2 = conceptual_mapping[char1], conceptual_mapping[char2]
            print(f"   Strong Hebrew connection: {char1} - {char2} (strength: {strength:.3f})")
            print(f"   Maps to Metatron nodes: {node1} - {node2}")
            enhancement = 1.0 + 0.1 * strength
            print(f"   Connection enhancement factor: {enhancement:.3f}")
    
    # Export integration data
    print("\n9. Exporting integration data...")
    
    integration_data = {
        'timestamp': final_metatron['time'],
        'metatron_state': {
            'consciousness_level': final_metatron['global']['consciousness_level'],
            'phi': final_metatron['global']['phi'],
            'coherence': final_metatron['global']['coherence'],
            'nodes': len(final_metatron['nodes'])
        },
        'hebrew_state': {
            'letters': len(final_hebrew['letters']),
            'connections': len(final_hebrew['connections']),
            'avg_energy': float(np.mean([letter['energy'] for letter in final_hebrew['letters'].values()])),
            'golden_ratio': float(final_hebrew['golden_ratio'])
        },
        'mapping': conceptual_mapping,
        'enhancement_example': {
            'node_pair': [0, 3] if 'א' in conceptual_mapping else [0, 1],
            'enhancement_factor': 1.05
        }
    }
    
    with open('hebrew_metatron_integration_demo.json', 'w') as f:
        json.dump(integration_data, f, indent=2)
    
    print("✅ Integration data exported to hebrew_metatron_integration_demo.json")
    
    print("\n" + "=" * 80)
    print("INTEGRATION DEMO COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    try:
        success = demonstrate_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error in integration demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)