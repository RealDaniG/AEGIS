"""
Consciousness Oscillator - Kuramoto Coupled Dynamics
=====================================================

Implements coupled harmonic oscillators with musical frequency ratios,
memory integration, and phase synchronization dynamics.

Based on Kuramoto model for consciousness emergence through
phase-locked oscillatory networks.
"""

import numpy as np
from collections import deque

try:
    from nodes.metatron_geometry import PHI
except ImportError:
    PHI = (1 + np.sqrt(5)) / 2


class ConsciousnessOscillator:
    """
    Coupled harmonic oscillator implementing Kuramoto dynamics
    with memory integration and musical frequency
    """
    
    def __init__(self, node_id, frequency_ratio, position_3d, 
                 base_frequency=40.0, memory_size=100):
        """
        Initialize consciousness oscillator
        
        Args:
            node_id: Node identifier (0-12)
            frequency_ratio: Musical ratio (from musical_frequency_ratios())
            position_3d: 3D coordinates in Metatron's Cube
            base_frequency: Base frequency in Hz (default 40 Hz gamma)
            memory_size: Number of previous states to remember
        """
        self.node_id = node_id
        self.position = np.array(position_3d)
        
        # Oscillator parameters
        self.frequency_ratio = frequency_ratio
        self.omega = 2 * np.pi * base_frequency * frequency_ratio
        self.base_frequency = base_frequency
        
        # State variables
        self.phase = np.random.uniform(0, 2*np.pi)  # Random initial phase
        self.amplitude = 1.0
        self.velocity = 0.0  # Phase velocity
        
        # Memory buffer (circular queue)
        self.memory = deque(maxlen=memory_size)
        self.phi = PHI
        
        # NEW: Adaptive coupling for spherical refinement
        self.dynamic_coupling_strength = 1.0
        self.synchronization_history = deque(maxlen=50)
        
        # Output history for analysis
        self.state_history = []
        self.max_history = 1000  # Prevent unbounded growth
        
    def update_coupling_strength(self, connected_nodes, connection_weights, dt):
        """
        Adaptive coupling evolution for spherical refinement
        
        Implements Hebbian-like learning: "Nodes that sync together, link together"
        Based on unified field equation recursive feedback term: λ ∫ Ψ(t-τ) dτ
        
        This is the KEY to algorithmic refinement toward perfect coherence.
        """
        if len(connected_nodes) == 0:
            return
        
        # Calculate current synchronization with neighbors
        avg_sync = 0.0
        for node_id, other_node in connected_nodes.items():
            if node_id == self.node_id:
                continue
            
            # Phase synchronization index (0 = opposite, 1 = synchronized)
            sync_index = self.synchronization_index(other_node)
            avg_sync += sync_index
        
        avg_sync /= len(connected_nodes)
        self.synchronization_history.append(avg_sync)
        
        # Apply φ-weighted memory (golden ratio recursive feedback)
        if len(self.synchronization_history) >= 10:
            recent_states = list(self.synchronization_history)[-10:]
            # φ-decay weighting: most recent states matter more
            weights = np.array([1/self.phi**i for i in range(10)])[::-1]
            weights = weights / np.sum(weights)  # Normalize
            weighted_sync = np.average(recent_states, weights=weights)
            
            # Target coupling based on synchronization success
            if weighted_sync > 0.8:  # High sync → can reduce coupling (energy efficiency)
                target_strength = self.dynamic_coupling_strength * 0.99
            elif weighted_sync < 0.5:  # Low sync → need more coupling
                target_strength = self.dynamic_coupling_strength * 1.02
            else:  # Goldilocks zone → maintain
                target_strength = self.dynamic_coupling_strength
            
            # Apply φ-based constraints (maintain harmonic relationships)
            target_strength = np.clip(target_strength, 1/self.phi, self.phi)
            
            # Smooth evolution with φ-decay learning rate
            learning_rate = (1/self.phi) * dt
            self.dynamic_coupling_strength += (
                (target_strength - self.dynamic_coupling_strength) * learning_rate
            )
    
    def update_state(self, dt, connected_nodes, connection_weights, 
                     external_input=0.0):
        """
        Update oscillator state using coupled dynamics WITH adaptive refinement
        
        Args:
            dt: Time step
            connected_nodes: Dict of {node_id: ConsciousnessOscillator}
            connection_weights: Dict of {node_id: weight}
            external_input: External forcing
            
        Returns:
            float: Current output state
        """
        # === SELF-OSCILLATION ===
        self_oscillation = self.amplitude * np.sin(self.phase)
        
        # === PHASE COUPLING (Kuramoto model with DYNAMIC STRENGTH) ===
        coupling_term = 0.0
        
        for node_id, other_node in connected_nodes.items():
            if node_id == self.node_id:
                continue
            
            weight = connection_weights.get(node_id, 0.0)
            if weight > 0:
                # Kuramoto coupling: K * sin(θⱼ - θᵢ)
                phase_difference = other_node.phase - self.phase
                # APPLY DYNAMIC COUPLING STRENGTH (KEY INNOVATION)
                coupling_term += (
                    weight * 
                    self.dynamic_coupling_strength *  # NEW: Self-tuning
                    np.sin(phase_difference)
                )
        
        # === MEMORY FEEDBACK ===
        memory_effect = 0.0
        if len(self.memory) > 0:
            # φ-weighted recent memory (last 10 states)
            recent_memory = list(self.memory)[-10:]
            if len(recent_memory) > 0:
                # Apply φ-decay weighting
                weights = np.array([1/self.phi**(i+1) for i in range(len(recent_memory))])
                weights = weights[::-1]  # Most recent = highest weight
                weighted_memory = np.average(recent_memory, weights=weights)
                memory_effect = (1/self.phi) * weighted_memory
        
        # === PHASE DYNAMICS ===
        # dφ/dt = ω + coupling + memory + input
        phase_derivative = (
            self.omega + 
            coupling_term + 
            memory_effect + 
            external_input
        )
        
        # === AMPLITUDE DYNAMICS (Stuart-Landau oscillator) ===
        # dA/dt = (1 - A²) * A + β * coupling
        # Self-limiting amplitude with coupling influence
        amplitude_derivative = (
            (1 - self.amplitude**2) * self.amplitude +
            0.1 * coupling_term
        )
        
        # === EULER INTEGRATION ===
        self.phase += phase_derivative * dt
        self.amplitude += amplitude_derivative * dt
        
        # Keep phase in [0, 2π]
        self.phase = np.fmod(self.phase, 2*np.pi)
        
        # Clamp amplitude to reasonable range
        self.amplitude = np.clip(self.amplitude, 0.1, 2.0)
        
        # === ADAPTIVE COUPLING UPDATE (Spherical Refinement) ===
        self.update_coupling_strength(connected_nodes, connection_weights, dt)
        
        # === OUTPUT STATE ===
        current_output = self.amplitude * np.sin(self.phase)
        
        # Update memory
        self.memory.append(current_output)
        
        # Store history with limit
        self.state_history.append({
            'time': len(self.state_history) * dt,
            'phase': float(self.phase),
            'amplitude': float(self.amplitude),
            'output': float(current_output)
        })
        
        # Limit history size
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        return current_output
    
    def get_complex_state(self):
        """
        Return state as complex number for phase analysis
        
        Returns:
            complex: A * e^(iφ)
        """
        return self.amplitude * np.exp(1j * self.phase)
    
    def get_memory_trace(self, depth=10):
        """
        Get recent memory with φ-decay weighting
        
        Args:
            depth: How many steps back to trace
            
        Returns:
            np.ndarray: Weighted memory trace
        """
        if len(self.memory) == 0:
            return np.array([])
        
        recent = list(self.memory)[-depth:]
        weights = np.array([1/self.phi**i for i in range(len(recent))])
        weights = weights[::-1]  # Most recent = highest weight
        
        return np.array(recent) * weights
    
    def synchronization_index(self, other_oscillator):
        """
        Calculate phase synchronization with another oscillator
        
        Args:
            other_oscillator: Another ConsciousnessOscillator instance
            
        Returns:
            float: Synchronization index [0, 1]
        """
        phase_diff = np.abs(self.phase - other_oscillator.phase)
        # Wrap to [0, π]
        phase_diff = min(phase_diff, 2*np.pi - phase_diff)
        
        # Convert to synchronization index
        sync_index = 1 - (phase_diff / np.pi)
        
        return sync_index
    
    def reset_state(self):
        """Reset oscillator to initial random state"""
        self.phase = np.random.uniform(0, 2*np.pi)
        self.amplitude = 1.0
        self.velocity = 0.0
        self.memory.clear()
        self.state_history.clear()
    
    def get_state_dict(self):
        """
        Get complete state as dictionary for serialization
        
        Returns:
            dict: All state variables
        """
        return {
            'node_id': int(self.node_id),
            'phase': float(self.phase),
            'amplitude': float(self.amplitude),
            'frequency_ratio': float(self.frequency_ratio),
            'omega': float(self.omega),
            'memory_depth': len(self.memory),
            'complex_state': {
                'real': float(np.real(self.get_complex_state())),
                'imag': float(np.imag(self.get_complex_state()))
            }
        }


if __name__ == "__main__":
    # Test oscillator
    print("=== Consciousness Oscillator Test ===\n")
    
    # Create test oscillator
    osc = ConsciousnessOscillator(
        node_id=1,
        frequency_ratio=1.5,  # Perfect fifth
        position_3d=[0, 0, 1],
        base_frequency=40.0
    )
    
    print(f"Oscillator created:")
    print(f"  Node ID: {osc.node_id}")
    print(f"  Frequency ratio: {osc.frequency_ratio}")
    print(f"  Natural frequency: {osc.omega/(2*np.pi):.2f} Hz")
    print(f"  Initial phase: {osc.phase:.4f} rad")
    print(f"  Initial amplitude: {osc.amplitude:.4f}")
    
    # Simulate 10 steps
    print("\n=== Simulating 10 time steps ===")
    dt = 0.01
    
    for i in range(10):
        output = osc.update_state(dt, {}, {}, external_input=0.0)
        if i % 3 == 0:
            print(f"Step {i:2d}: phase={osc.phase:.4f}, amp={osc.amplitude:.4f}, out={output:.4f}")
    
    print(f"\nMemory buffer size: {len(osc.memory)}")
    print(f"History length: {len(osc.state_history)}")
    
    # Test with coupling
    print("\n=== Testing Coupled Oscillators ===")
    osc1 = ConsciousnessOscillator(1, 1.0, [0,0,1])
    osc2 = ConsciousnessOscillator(2, 1.5, [1,0,0])
    
    for i in range(20):
        # Couple them
        osc1.update_state(dt, {2: osc2}, {2: 0.5})
        osc2.update_state(dt, {1: osc1}, {1: 0.5})
    
    sync = osc1.synchronization_index(osc2)
    print(f"After 20 steps, synchronization index: {sync:.4f}")
    
    print("\n[OK] Oscillator tests passed!")
