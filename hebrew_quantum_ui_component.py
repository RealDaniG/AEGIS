#!/usr/bin/env python3
"""
Hebrew Quantum Field UI Component
=================================

A UI component for visualizing the Hebrew Quantum Field that can be integrated
below the quick actions panel in the Metatron UI.

This component provides:
- Real-time visualization of Hebrew letters in quantum harmony
- Dynamic connections showing Gematria relationships
- Energy and phase visualization
- Fibonacci sequence and golden ratio integration
"""

import numpy as np
from typing import Dict, List, Tuple, Any
import logging
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

@dataclass
class HebrewLetter:
    """Represents a Hebrew letter with its properties"""
    char: str
    name: str
    gematria: int
    sound: str
    frequency: float

# Hebrew letters with their properties
HEBREW_LETTERS = {
    'א': HebrewLetter('א', 'Aleph', 1, 'silent', 1.0),
    'ב': HebrewLetter('ב', 'Bet', 2, 'b/v', 1.1225),
    'ג': HebrewLetter('ג', 'Gimel', 3, 'g', 1.2599),
    'ד': HebrewLetter('ד', 'Dalet', 4, 'd', 1.4142),
    'ה': HebrewLetter('ה', 'Hei', 5, 'h', 1.4983),
    'ו': HebrewLetter('ו', 'Vav', 6, 'v', 1.5874),
    'ז': HebrewLetter('ז', 'Zayin', 7, 'z', 1.6818),
    'ח': HebrewLetter('ח', 'Chet', 8, 'ch', 1.7818),
    'ט': HebrewLetter('ט', 'Tet', 9, 't', 1.8877),
    'י': HebrewLetter('י', 'Yod', 10, 'y', 2.0),
    'כ': HebrewLetter('כ', 'Kaf', 20, 'k', 2.2449),
    'ל': HebrewLetter('ל', 'Lamed', 30, 'l', 2.3784),
    'מ': HebrewLetter('מ', 'Mem', 40, 'm', 2.5198),
    'נ': HebrewLetter('נ', 'Nun', 50, 'n', 2.6697),
    'ס': HebrewLetter('ס', 'Samech', 60, 's', 2.8284),
    'ע': HebrewLetter('ע', 'Ayin', 70, 'silent', 2.9966),
    'פ': HebrewLetter('פ', 'Pei', 80, 'p/f', 3.1748),
    'צ': HebrewLetter('צ', 'Tzadi', 90, 'tz', 3.3636),
    'ק': HebrewLetter('ק', 'Kuf', 100, 'k', 3.5636),
    'ר': HebrewLetter('ר', 'Reish', 200, 'r', 3.7755),
    'ש': HebrewLetter('ש', 'Shin', 300, 'sh/s', 4.0),
    'ת': HebrewLetter('ת', 'Tav', 400, 't', 4.2379)
}

class SimulationState(Enum):
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class QuantumState:
    """Represents the quantum state of a Hebrew letter"""
    letter: HebrewLetter
    amplitude: complex = 1.0 + 0j
    phase: float = 0.0
    energy: float = 1.0

class HebrewQuantumFieldUIComponent:
    """
    UI Component for Hebrew Quantum Field Visualization
    
    This component can be integrated below the quick actions panel in the Metatron UI.
    It provides a real-time visualization of the Hebrew Quantum Field with the following features:
    
    1. Circular arrangement of the 22 Hebrew letters
    2. Dynamic connections showing quantum relationships
    3. Color-coded energy levels for each letter
    4. Real-time phase visualization
    5. Fibonacci sequence and golden ratio indicators
    6. Connection strength visualization
    """
    
    def __init__(self, parent_container=None):
        self.parent_container = parent_container
        self.state = SimulationState.INITIALIZING
        self.time = 0.0
        self.dt = 0.05
        self.quantum_states: Dict[str, QuantumState] = {}
        self.connection_strengths: Dict[Tuple[str, str], float] = {}
        self.is_running = False
        
        # Visualization data that will be sent to the UI
        self.visualization_data = {
            'time': 0.0,
            'letters': {},
            'connections': [],
            'fibonacci_info': {
                'sequence': [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987],
                'golden_ratio_approx': PHI
            },
            'golden_ratio': PHI
        }
        
        # Initialize the component
        self._initialize_component()
        
    def _initialize_component(self):
        """Initialize the UI component"""
        logger.info("Initializing Hebrew Quantum Field UI Component")
        
        # Initialize quantum states for each Hebrew letter
        for char, letter in HEBREW_LETTERS.items():
            self.quantum_states[char] = QuantumState(letter)
        
        # Initialize connections between letters
        self._initialize_connections()
        
        self.state = SimulationState.RUNNING
        self.is_running = True
        self._update_visualization_data()
        
    def _initialize_connections(self):
        """Initialize connections between letters based on Gematria"""
        letters = list(HEBREW_LETTERS.keys())
        fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        
        for i, char1 in enumerate(letters):
            for char2 in letters[i+1:]:
                val1 = HEBREW_LETTERS[char1].gematria
                val2 = HEBREW_LETTERS[char2].gematria
                
                # Calculate connection strength based on Fibonacci relationships
                diff = abs(val1 - val2)
                if diff in fibonacci_numbers:
                    strength = 1.0 / (diff + 1)
                elif (val1 + val2) in fibonacci_numbers:
                    strength = 0.7 / (val1 + val2) ** 0.5
                else:
                    strength = 0.1 / (diff + 1)
                
                self.connection_strengths[(char1, char2)] = strength
                self.connection_strengths[(char2, char1)] = strength
    
    def update(self):
        """Update the quantum field state for visualization"""
        if self.state != SimulationState.RUNNING:
            return
        
        self.time += self.dt
        
        # Update each quantum state
        for state in self.quantum_states.values():
            # Update phase based on energy and frequency
            state.phase = (state.phase + 2 * np.pi * state.letter.frequency * self.dt) % (2 * np.pi)
            
            # Update amplitude based on phase
            state.amplitude = np.sqrt(state.energy) * (np.cos(state.phase) + 1j * np.sin(state.phase))
            
            # Update energy with some variation
            state.energy = 0.95 * state.energy + 0.05 * (1.0 + 0.5 * np.sin(self.time * state.letter.frequency))
        
        # Update connection strengths based on phase coherence
        self._update_connections()
        
        # Update visualization data
        self._update_visualization_data()
    
    def _update_connections(self):
        """Update connection strengths based on phase coherence"""
        for (char1, char2), strength in list(self.connection_strengths.items()):
            state1 = self.quantum_states[char1]
            state2 = self.quantum_states[char2]
            
            # Calculate phase coherence
            phase_diff = (state1.phase - state2.phase) % (2 * np.pi)
            coherence = np.cos(phase_diff)
            
            # Update strength based on coherence
            new_strength = 0.9 * strength + 0.1 * (0.5 + 0.5 * coherence)
            self.connection_strengths[(char1, char2)] = max(0.01, min(1.0, new_strength))
    
    def _update_visualization_data(self):
        """Update the visualization data for the UI"""
        # Update time
        self.visualization_data['time'] = self.time
        
        # Update letter positions and states
        positions = {}
        max_energy = max(s.energy for s in self.quantum_states.values()) or 1.0
        
        for char, state in self.quantum_states.items():
            # Calculate position in circular arrangement
            angle = 2 * np.pi * state.letter.gematria / 22  # 22 letters in Hebrew alphabet
            radius = 0.5 + 0.2 * np.sin(self.time * 0.5)  # Pulsing effect
            x = np.cos(angle + self.time * 0.2) * radius
            y = np.sin(angle + self.time * 0.2) * radius
            positions[char] = (x, y)
            
            # Calculate color based on energy
            energy_ratio = state.energy / max_energy
            r = min(1.0, energy_ratio * 2)
            g = min(1.0, (1 - energy_ratio) * 2)
            b = 0.5 + 0.5 * np.sin(state.phase)
            
            self.visualization_data['letters'][char] = {
                'position': (x, y),
                'energy': state.energy,
                'phase': state.phase,
                'color': (r, g, b),
                'name': state.letter.name,
                'gematria': state.letter.gematria
            }
        
        # Update connections (only show strong connections)
        self.visualization_data['connections'] = []
        sorted_connections = sorted(self.connection_strengths.items(), 
                                   key=lambda x: x[1], reverse=True)
        
        for (char1, char2), strength in sorted_connections[:30]:  # Top 30 connections
            if strength > 0.1:  # Only show significant connections
                if char1 in positions and char2 in positions:
                    x1, y1 = positions[char1]
                    x2, y2 = positions[char2]
                    
                    # Calculate phase difference for color
                    phase_diff = (self.quantum_states[char1].phase - 
                                 self.quantum_states[char2].phase) % (2 * np.pi)
                    hue = phase_diff / (2 * np.pi)
                    
                    self.visualization_data['connections'].append({
                        'start': char1,
                        'end': char2,
                        'start_pos': (x1, y1),
                        'end_pos': (x2, y2),
                        'strength': strength,
                        'phase_diff': phase_diff,
                        'color_hue': hue
                    })
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get the current visualization data for the UI"""
        if self.is_running:
            self.update()
        return self.visualization_data
    
    def toggle_simulation(self) -> bool:
        """Toggle the simulation on/off"""
        if self.is_running:
            self.state = SimulationState.PAUSED
            self.is_running = False
        else:
            self.state = SimulationState.RUNNING
            self.is_running = True
        return self.is_running
    
    def reset_simulation(self):
        """Reset the simulation"""
        self.state = SimulationState.STOPPED
        self.time = 0.0
        
        # Reset quantum states
        for state in self.quantum_states.values():
            state.phase = 0.0
            state.energy = 1.0
            state.amplitude = 1.0 + 0j
        
        self.state = SimulationState.RUNNING
        self._update_visualization_data()
    
    def get_component_info(self) -> Dict[str, Any]:
        """Get information about this UI component"""
        return {
            'name': 'Hebrew Quantum Field Visualizer',
            'description': 'Real-time visualization of Hebrew letters in quantum harmony',
            'version': '1.0.0',
            'author': 'Metatron System',
            'features': [
                '22 Hebrew letters in circular arrangement',
                'Quantum connections based on Gematria',
                'Real-time energy and phase visualization',
                'Fibonacci sequence integration',
                'Golden ratio approximation display'
            ]
        }

# Test the component
if __name__ == "__main__":
    # Create and test the UI component
    component = HebrewQuantumFieldUIComponent()
    
    # Get initial data
    data = component.get_visualization_data()
    print("Hebrew Quantum Field UI Component Test")
    print(f"Time: {data['time']:.2f}")
    print(f"Letters: {len(data['letters'])}")
    print(f"Connections: {len(data['connections'])}")
    print(f"Golden Ratio: {data['golden_ratio']:.6f}")
    
    # Test toggle
    is_running = component.toggle_simulation()
    print(f"Simulation toggled, now running: {is_running}")
    
    # Get component info
    info = component.get_component_info()
    print(f"\nComponent Info:")
    print(f"Name: {info['name']}")
    print(f"Description: {info['description']}")
    print(f"Features: {', '.join(info['features'])}")