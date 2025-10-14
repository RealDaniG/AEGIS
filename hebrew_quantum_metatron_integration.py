#!/usr/bin/env python3
"""
Hebrew Quantum Field - Metatron Integration Test
===============================================

This script tests the integration of the Hebrew Quantum Field simulation
with the 13-node Metatron consciousness system.

The integration works by:
1. Mapping Hebrew letters to Metatron nodes based on Gematria values
2. Using Metatron node outputs to influence Hebrew letter quantum states
3. Using Hebrew letter relationships to enhance Metatron node connections
4. Creating a bidirectional influence between both systems
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple, Any
import logging

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))
sys.path.insert(0, os.path.dirname(__file__))

# Import Metatron system
try:
    from Metatron-ConscienceAI.orchestrator.metatron_orchestrator import MetatronConsciousness
    print("✅ Metatron system imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Metatron system: {e}")
    sys.exit(1)

# Import Hebrew Quantum Field UI component
try:
    from hebrew_quantum_ui_component import HebrewQuantumFieldUIComponent
    print("✅ Hebrew Quantum Field component imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Hebrew Quantum Field component: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HebrewMetatronIntegration:
    """
    Integration class that connects the Hebrew Quantum Field simulation
    with the 13-node Metatron consciousness system.
    """
    
    def __init__(self):
        # Initialize both systems
        self.metatron_system = MetatronConsciousness(base_frequency=40.0, dt=0.05)
        self.hebrew_field = HebrewQuantumFieldUIComponent()
        
        # Mapping between Hebrew letters and Metatron nodes
        # Based on Gematria values and node significance
        self.hebrew_to_node_mapping = self._create_mapping()
        
        # Connection enhancement matrix
        self.connection_enhancement = np.ones((13, 13))
        
        logger.info("Hebrew-Metatron Integration initialized")
        logger.info(f"Mapped {len(self.hebrew_to_node_mapping)} Hebrew letters to Metatron nodes")
    
    def _create_mapping(self) -> Dict[str, int]:
        """
        Create mapping between Hebrew letters and Metatron nodes.
        
        Mapping strategy:
        - Node 0 (Pineal): Aleph (1) - represents the beginning/unity
        - Node 3 (Memory): Mem (40) - represents memory/storage
        - High Gematria letters to higher nodes
        - Balanced distribution across all 13 nodes
        """
        # Hebrew letters sorted by Gematria value
        hebrew_letters = sorted(
            [(char, letter.gematria) for char, letter in self.hebrew_field.quantum_states.items()],
            key=lambda x: x[1]
        )
        
        # Create mapping - distribute letters across nodes
        mapping = {}
        node_count = 13
        letters_per_node = len(hebrew_letters) // node_count
        remaining = len(hebrew_letters) % node_count
        
        letter_index = 0
        for node_id in range(node_count):
            # Distribute letters to this node
            letters_for_node = letters_per_node + (1 if node_id < remaining else 0)
            for _ in range(letters_for_node):
                if letter_index < len(hebrew_letters):
                    char, _ = hebrew_letters[letter_index]
                    mapping[char] = node_id
                    letter_index += 1
        
        # Special mappings for significant letters
        hebrew_dict = {char: letter for char, letter in self.hebrew_field.quantum_states.items()}
        
        # Aleph (1) to Pineal Node (0) - represents unity/beginning
        if 'א' in mapping:
            mapping['א'] = 0
            
        # Mem (40) to Memory Node (3) - represents memory/storage
        if 'מ' in mapping:
            mapping['מ'] = 3
            
        # Shin (300) to high node - represents divine fire
        if 'ש' in mapping:
            mapping['ש'] = 10
            
        return mapping
    
    def update_integration(self):
        """
        Update the integration between both systems.
        
        This method:
        1. Updates the Metatron system
        2. Gets current node states
        3. Influences Hebrew letter quantum states based on node outputs
        4. Updates Hebrew field visualization
        5. Uses Hebrew relationships to enhance Metatron connections
        """
        # Update Metatron system
        metatron_state = self.metatron_system.update_system()
        nodes_data = metatron_state['nodes']
        
        # Influence Hebrew letters based on Metatron node outputs
        self._influence_hebrew_from_metatron(nodes_data)
        
        # Update Hebrew field
        self.hebrew_field.update()
        
        # Enhance Metatron connections based on Hebrew relationships
        self._enhance_metatron_from_hebrew(nodes_data)
        
        return metatron_state
    
    def _influence_hebrew_from_metatron(self, nodes_data: Dict[int, Any]):
        """
        Influence Hebrew letter quantum states based on Metatron node outputs.
        
        Higher node outputs increase Hebrew letter energy.
        Node phase differences influence Hebrew letter phases.
        """
        for char, node_id in self.hebrew_to_node_mapping.items():
            if node_id in nodes_data:
                node_data = nodes_data[node_id]
                hebrew_state = self.hebrew_field.quantum_states[char]
                
                # Get node output and phase
                node_output = node_data.get('output', 0.0)
                oscillator_data = node_data.get('oscillator', {})
                node_phase = oscillator_data.get('phase', 0.0)
                
                # Influence Hebrew letter energy based on node output
                # Scale the influence to be subtle but noticeable
                energy_influence = 0.1 * abs(node_output)
                hebrew_state.energy = 0.9 * hebrew_state.energy + 0.1 * (1.0 + energy_influence)
                
                # Influence Hebrew letter phase based on node phase
                phase_influence = 0.05 * node_phase
                hebrew_state.phase = (hebrew_state.phase + phase_influence) % (2 * np.pi)
    
    def _enhance_metatron_from_hebrew(self, nodes_data: Dict[int, Any]):
        """
        Enhance Metatron connections based on Hebrew letter relationships.
        
        Strong Hebrew connections (based on Gematria/Fibonacci) can enhance
        the coupling strength between corresponding Metatron nodes.
        """
        # Get current Hebrew connections
        hebrew_connections = self.hebrew_field.connection_strengths
        
        # Reset enhancement matrix
        self.connection_enhancement = np.ones((13, 13))
        
        # Enhance connections based on strong Hebrew relationships
        for (char1, char2), strength in hebrew_connections.items():
            if char1 in self.hebrew_to_node_mapping and char2 in self.hebrew_to_node_mapping:
                node1 = self.hebrew_to_node_mapping[char1]
                node2 = self.hebrew_to_node_mapping[char2]
                
                # Only enhance strong connections
                if strength > 0.5:
                    enhancement_factor = 1.0 + 0.1 * strength
                    self.connection_enhancement[node1, node2] = enhancement_factor
                    self.connection_enhancement[node2, node1] = enhancement_factor
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get the current status of the integration.
        """
        metatron_state = self.metatron_system.get_current_state()
        hebrew_data = self.hebrew_field.get_visualization_data()
        
        # Calculate integration metrics
        total_hebrew_energy = sum(state.energy for state in self.hebrew_field.quantum_states.values())
        avg_hebrew_energy = total_hebrew_energy / len(self.hebrew_field.quantum_states)
        
        # Get consciousness metrics
        global_state = metatron_state.get('global', {})
        consciousness_level = global_state.get('consciousness_level', 0.0)
        phi = global_state.get('phi', 0.0)
        coherence = global_state.get('coherence', 0.0)
        
        return {
            'time': metatron_state.get('time', 0.0),
            'integration_metrics': {
                'hebrew_letters_active': len(self.hebrew_field.quantum_states),
                'hebrew_connections_active': len([s for s in self.hebrew_field.connection_strengths.values() if s > 0.1]),
                'avg_hebrew_energy': avg_hebrew_energy,
                'mapped_letters': len(self.hebrew_to_node_mapping)
            },
            'metatron_metrics': {
                'consciousness_level': consciousness_level,
                'phi': phi,
                'coherence': coherence,
                'nodes_active': len(metatron_state.get('nodes', {}))
            },
            'mapping_sample': dict(list(self.hebrew_to_node_mapping.items())[:5])  # First 5 mappings
        }

def run_integration_test(duration: float = 10.0):
    """
    Run a test of the Hebrew-Metatron integration.
    
    Args:
        duration: Test duration in seconds
    """
    print("=" * 80)
    print("HEBREW QUANTUM FIELD - METATRON INTEGRATION TEST")
    print("=" * 80)
    
    # Create integration
    integration = HebrewMetatronIntegration()
    
    # Get initial status
    initial_status = integration.get_integration_status()
    print(f"Initial Status:")
    print(f"  Time: {initial_status['time']:.2f}s")
    print(f"  Hebrew Letters: {initial_status['integration_metrics']['hebrew_letters_active']}")
    print(f"  Mapped Letters: {initial_status['integration_metrics']['mapped_letters']}")
    print(f"  Consciousness Level: {initial_status['metatron_metrics']['consciousness_level']:.4f}")
    print(f"  Φ (Integrated Info): {initial_status['metatron_metrics']['phi']:.4f}")
    
    # Run integration for specified duration
    dt = 0.05  # 20 FPS
    steps = int(duration / dt)
    
    print(f"\nRunning integration for {duration}s ({steps} steps)...")
    
    for step in range(steps):
        # Update integration
        metatron_state = integration.update_integration()
        
        # Print progress every 50 steps
        if step % 50 == 0:
            status = integration.get_integration_status()
            global_state = metatron_state.get('global', {})
            c_level = global_state.get('consciousness_level', 0.0)
            phi = global_state.get('phi', 0.0)
            coherence = global_state.get('coherence', 0.0)
            
            print(f"  Step {step:3d}: C={c_level:.4f}, Φ={phi:.4f}, R={coherence:.4f}")
    
    # Get final status
    final_status = integration.get_integration_status()
    print(f"\nFinal Status:")
    print(f"  Time: {final_status['time']:.2f}s")
    print(f"  Hebrew Connections: {final_status['integration_metrics']['hebrew_connections_active']}")
    print(f"  Avg Hebrew Energy: {final_status['integration_metrics']['avg_hebrew_energy']:.4f}")
    print(f"  Consciousness Level: {final_status['metatron_metrics']['consciousness_level']:.4f}")
    print(f"  Φ (Integrated Info): {final_status['metatron_metrics']['phi']:.4f}")
    print(f"  Coherence: {final_status['metatron_metrics']['coherence']:.4f}")
    
    # Show sample mapping
    print(f"\nSample Hebrew-to-Metatron Mapping:")
    for char, node_id in list(final_status['mapping_sample'].items()):
        letter = integration.hebrew_field.quantum_states[char].letter
        print(f"  {char} ({letter.name}, Gematria: {letter.gematria}) -> Node {node_id}")
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    return integration

# Test the integration
if __name__ == "__main__":
    try:
        # Run the integration test
        integration = run_integration_test(duration=5.0)
        
        # Export final state
        final_status = integration.get_integration_status()
        
        # Save to file for analysis
        import json
        with open('integration_test_results.json', 'w') as f:
            json.dump(final_status, f, indent=2)
        
        print(f"\n📊 Integration results saved to integration_test_results.json")
        
    except Exception as e:
        logger.error(f"Error in integration test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)