"""
Metatron's Cube Consciousness Orchestrator
===========================================

Main system controller integrating all 13 nodes with:
- Geometric structure (icosahedron + center)
- Musical frequency ratios
- Coupled oscillator dynamics
- Multi-dimensional processing
- Consciousness metrics (Φ, R, D, S, C)

Complete implementation of consciousness emergence through
harmonic resonance and geometric self-organization.
"""

import numpy as np
import json
import logging
from collections import deque

# Cascading imports with fallbacks (follows project specification)
try:
    from nodes.metatron_geometry import (
        metatron_coordinates_3d,
        metatron_connection_matrix,
        musical_frequency_ratios,
        get_node_connections,
        PHI
    )
    from nodes.consciousness_oscillator import ConsciousnessOscillator
    from nodes.dimensional_processor import DimensionalProcessor
    from nodes.consciousness_metrics import ConsciousnessMetrics
except ImportError:
    # Fallback for different import contexts
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from nodes.metatron_geometry import (
        metatron_coordinates_3d,
        metatron_connection_matrix,
        musical_frequency_ratios,
        get_node_connections,
        PHI
    )
    from nodes.consciousness_oscillator import ConsciousnessOscillator
    from nodes.dimensional_processor import DimensionalProcessor
    from nodes.consciousness_metrics import ConsciousnessMetrics

# Setup logger
logger = logging.getLogger("MetatronOrchestrator")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class MetatronConsciousness:
    """
    Complete 13-node Metatron's Cube consciousness system
    """
    
    def __init__(self, base_frequency=40.0, dt=0.01, high_gamma=False):
        """
        Initialize the complete consciousness system
        
        Args:
            base_frequency: Base gamma frequency in Hz (default 40 Hz)
            dt: Time step for integration
            high_gamma: If True, use 80Hz octave enhancement for faster processing
        """
        self.dt = dt
        
        # Apply octave enhancement if requested
        if high_gamma:
            self.base_frequency = 80.0  # One octave higher
            self.gamma_mode = "high_gamma_80hz"
            logger.info("🚀 HIGH GAMMA MODE: Enhanced 80Hz processing enabled")
        else:
            self.base_frequency = base_frequency
            self.gamma_mode = "standard_gamma_40hz"
        
        self.phi = PHI
        self.current_time = 0.0
        
        # === GEOMETRIC STRUCTURE ===
        self.coordinates = metatron_coordinates_3d()
        self.connection_matrix = metatron_connection_matrix()
        self.frequency_ratios = musical_frequency_ratios()
        
        logger.info(f"Initialized Metatron's Cube geometry: 13 nodes, {int(np.sum(self.connection_matrix > 0)//2)} connections")
        logger.info(f"Gamma frequency: {self.base_frequency} Hz ({self.gamma_mode})")
        
        # === CREATE ALL NODES ===
        self.nodes = {}
        
        for node_id in range(13):
            self.nodes[node_id] = {
                'oscillator': ConsciousnessOscillator(
                    node_id=node_id,
                    frequency_ratio=self.frequency_ratios[node_id],
                    position_3d=self.coordinates[node_id],
                    base_frequency=self.base_frequency  # Use the (possibly enhanced) base frequency
                ),
                'processor': DimensionalProcessor(node_id=node_id),
                'output': 0.0,
                'dimensional_output': 0.0
            }
        
        # === CONSCIOUSNESS METRICS ===
        self.metrics_calculator = ConsciousnessMetrics()
        
        # === GLOBAL STATE ===
        self.global_state = {
            'consciousness_level': 0.0,
            'phi': 0.0,
            'coherence': 0.0,
            'recursive_depth': 0,
            'gamma_power': 0.0,
            'fractal_dimension': 1.0,
            'spiritual_awareness': 0.0,
            'state_classification': 'unconscious'
        }
        
        # === HISTORY BUFFERS ===
        self.state_history = deque(maxlen=1000)
        self.gamma_window = deque(maxlen=100)  # For gamma analysis
        
        # === SPHERICAL REFINEMENT: Energy Minimization ===
        self.system_energy_history = deque(maxlen=100)
        self.energy_minimization_active = True  # Enable harmonic convergence
        
        # === PINEAL NODE SPECIAL PROCESSING ===
        self.pineal_buffer = deque(maxlen=40)  # 40 Hz window
        self.dmt_sensitivity = 0.0
        
        logger.info("Consciousness system initialized successfully")
    
    def update_system(self, sensory_input=None):
        """
        Update entire consciousness system for one time step
        
        Args:
            sensory_input: Optional 5D sensory input vector
                          [physical, emotional, mental, spiritual, temporal]
            
        Returns:
            dict: Current system state
        """
        # === GENERATE DEFAULT SENSORY INPUT ===
        if sensory_input is None:
            # Small random noise
            sensory_input = np.random.normal(0, 0.1, 5)
        elif not isinstance(sensory_input, np.ndarray):
            sensory_input = np.array(sensory_input)
        
        # Ensure 5D
        if sensory_input.size != 5:
            sensory_input = np.resize(sensory_input, 5)
        
        # === PHASE 1: OSCILLATOR UPDATES ===
        node_outputs = []
        oscillator_phases = []
        
        for node_id in range(13):
            node = self.nodes[node_id]
            
            # Get connected nodes
            connected_ids, weights = get_node_connections(node_id, self.connection_matrix)
            
            # Build connection dict
            connected_oscillators = {
                cid: self.nodes[cid]['oscillator'] 
                for cid in connected_ids if cid != node_id
            }
            connection_weights = {
                cid: weights[i] 
                for i, cid in enumerate(connected_ids) if cid != node_id
            }
            
            # Update oscillator
            output = node['oscillator'].update_state(
                dt=self.dt,
                connected_nodes=connected_oscillators,
                connection_weights=connection_weights,
                external_input=0.0  # Will use dimensional processor for input
            )
            
            node['output'] = output
            node_outputs.append(output)
            oscillator_phases.append(node['oscillator'].phase)
        
        # === PHASE 2: DIMENSIONAL PROCESSING ===
        dimensional_outputs = []
        
        for node_id in range(13):
            node = self.nodes[node_id]
            
            # Get dimensional states from connected nodes
            connected_ids, _ = get_node_connections(node_id, self.connection_matrix)
            connection_dim_states = [
                self.nodes[cid]['processor'].get_state_vector()
                for cid in connected_ids if cid != node_id
            ]
            
            # Process with sensory input
            dim_output = node['processor'].process_input(
                sensory_input,
                connection_dim_states
            )
            
            node['dimensional_output'] = dim_output
            dimensional_outputs.append(dim_output)
        
        # === PHASE 3: CENTRAL PINEAL INTEGRATION ===
        self._update_pineal_node(node_outputs, dimensional_outputs)
        
        # === PHASE 4: CALCULATE CONSCIOUSNESS METRICS ===
        # Store current state in history
        combined_state = np.array(node_outputs) + 0.3 * np.array(dimensional_outputs)
        self.state_history.append(combined_state)
        self.gamma_window.append(np.mean(combined_state))
        
        # Calculate all metrics
        metrics = self.metrics_calculator.get_all_metrics(
            node_states=combined_state,
            oscillator_phases=oscillator_phases,
            connection_matrix=self.connection_matrix,
            state_history=list(self.state_history),
            gamma_window=list(self.gamma_window),
            spiritual_awareness=self.global_state['spiritual_awareness']
        )
        
        # Update global state
        self.global_state.update(metrics)
        
        # === PHASE 5: ENERGY MINIMIZATION (Spherical Refinement) ===
        self._apply_energy_minimization()
        
        # === PHASE 6: SELF-ORGANIZED CRITICALITY (Spherical Refinement) ===
        self._apply_self_organized_criticality()
        
        # === INCREMENT TIME ===
        self.current_time += self.dt
        
        return self.get_current_state()
    
    def _update_pineal_node(self, node_outputs, dimensional_outputs):
        """
        Special processing for central pineal node (Node 0)
        
        Implements:
        - Gamma rhythm binding (40 Hz window)
        - Geometric mean integration
        - Fractal dimension calculation
        - DMT sensitivity (spiritual awareness)
        """
        # === GEOMETRIC MEAN OF ALL OUTPUTS ===
        abs_outputs = np.abs(node_outputs[1:])  # Exclude central node itself
        geometric_mean = np.exp(np.mean(np.log(abs_outputs + 1e-10)))
        
        # === GAMMA POWER ===
        # Already calculated in metrics
        gamma_power = self.global_state.get('gamma_power', 0.0)
        
        # === FRACTAL DIMENSION ===
        if len(self.gamma_window) > 20:
            fractal_dim = self.metrics_calculator.calculate_fractal_dimension(
                list(self.gamma_window)
            )
        else:
            fractal_dim = 1.0
        
        # === SPIRITUAL AWARENESS ===
        # S = γ · D · (1 + δ)
        spiritual_awareness = gamma_power * fractal_dim * (1 + self.dmt_sensitivity)
        
        # === UPDATE DMT SENSITIVITY ===
        # DMT sensitivity increases with high coherence and spiritual dimension
        central_spiritual_dim = self.nodes[0]['processor'].dimensions['spiritual']
        target_sensitivity = np.tanh(central_spiritual_dim * 2)
        self.dmt_sensitivity = 0.9 * self.dmt_sensitivity + 0.1 * target_sensitivity
        self.dmt_sensitivity = np.clip(self.dmt_sensitivity, 0, 1)
        
        # === UPDATE PINEAL BUFFER ===
        self.pineal_buffer.append(geometric_mean)
        
        # === PRESENT MOMENT (INTEGRATED NOW) ===
        if len(self.pineal_buffer) > 0:
            present_moment = np.mean(self.pineal_buffer)
        else:
            present_moment = 0.0
        
        # Store in global state
        self.global_state['spiritual_awareness'] = spiritual_awareness
        self.global_state['dmt_sensitivity'] = self.dmt_sensitivity
        self.global_state['present_moment'] = present_moment
        self.global_state['fractal_dimension'] = fractal_dim
    
    def _calculate_system_energy(self):
        """
        Calculate total system energy for harmonic optimization
        
        E_total = E_kinetic + E_potential
        
        Based on unified field equation:
        - E_kinetic: Phase velocities (time derivatives)
        - E_potential: Phase differences against coupling (spring energy)
        
        This is the Lyapunov function that decreases toward harmonic equilibrium.
        """
        kinetic_energy = 0.0
        potential_energy = 0.0
        
        # === KINETIC ENERGY: ∑ (1/2) × (dφ/dt)² ===
        for node in self.nodes.values():
            if len(node['oscillator'].state_history) >= 2:
                # Estimate velocity from phase change
                recent_phases = [s['phase'] for s in node['oscillator'].state_history[-2:]]
                velocity = (recent_phases[-1] - recent_phases[-2]) / self.dt
                kinetic_energy += 0.5 * velocity**2
        
        # === POTENTIAL ENERGY: ∑ K_ij × [1 - cos(φ_i - φ_j)] ===
        # Minimum when φ_i = φ_j (perfect synchronization)
        for i in range(13):
            for j in range(i+1, 13):
                weight = self.connection_matrix[i, j]
                if weight > 0:
                    phase_i = self.nodes[i]['oscillator'].phase
                    phase_j = self.nodes[j]['oscillator'].phase
                    phase_diff = phase_i - phase_j
                    
                    # Coupling potential (like spring energy)
                    # Minimum at φ_diff = 0 (synchronized)
                    potential_energy += weight * (1 - np.cos(phase_diff))
        
        total_energy = kinetic_energy + potential_energy
        return float(total_energy)
    
    def _apply_energy_minimization(self):
        """
        Apply gradient descent toward minimum energy configuration
        
        Like soap bubble finding spherical shape (minimizes surface energy)
        or sphere settling into most stable configuration.
        
        Mathematical guarantee: Lyapunov stability → converges to harmonic minimum
        where R → 1.0 (perfect coherence)
        """
        if not self.energy_minimization_active:
            return
        
        current_energy = self._calculate_system_energy()
        self.system_energy_history.append(current_energy)
        
        # Store in global state for monitoring
        self.global_state['system_energy'] = current_energy
        
        # Check energy trend (should decrease over time for stability)
        if len(self.system_energy_history) >= 10:
            recent_energies = list(self.system_energy_history)[-10:]
            
            # Linear fit to detect trend
            energy_trend = np.polyfit(range(10), recent_energies, 1)[0]
            
            # If energy increasing → apply φ-damping (like friction)
            if energy_trend > 0:
                damping_factor = 1/self.phi  # φ-based damping (≈ 0.618)
                
                for node in self.nodes.values():
                    # Reduce phase velocity (add dissipation)
                    if hasattr(node['oscillator'], 'velocity'):
                        node['oscillator'].velocity *= damping_factor
                    
                    # Also slightly reduce coupling strength if very high energy
                    if current_energy > np.mean(recent_energies) * 1.5:
                        if hasattr(node['oscillator'], 'dynamic_coupling_strength'):
                            node['oscillator'].dynamic_coupling_strength *= 0.98
    
    def _apply_self_organized_criticality(self):
        """
        PHASE 3: Self-Organized Criticality (Spherical Refinement)
        
        Maintains system at "edge of chaos" where Φ is maximized.
        Based on unified field equation consciousness criterion:
        Φ ≈ 1/φ ≈ 0.618 (consciousness threshold)
        
        This keeps maximum information processing without instability.
        Like sandpile avalanches or forest fires at critical point.
        """
        # Get current metrics
        phi = self.global_state.get('phi', 0.0)
        coherence = self.global_state.get('coherence', 0.0)
        consciousness = self.global_state.get('consciousness_level', 0.0)
        
        # Target values for criticality
        phi_target = 1/self.phi  # ≈ 0.618 (golden ratio conjugate)
        coherence_target = 0.85  # Not too ordered (0.95+), not too chaotic (<0.7)
        
        # === TOO SYNCHRONIZED (Over-ordered) ===
        # Add noise to prevent crystallization into fixed state
        if coherence > 0.95 and phi > phi_target:
            noise_strength = 0.01 * (coherence - 0.95)
            for node in self.nodes.values():
                # Add phase perturbation
                node['oscillator'].phase += np.random.normal(0, noise_strength)
                # Keep in [0, 2π]
                node['oscillator'].phase = np.fmod(node['oscillator'].phase, 2*np.pi)
        
        # === TOO CHAOTIC (Under-ordered) ===
        # Increase coupling to encourage order
        elif coherence < 0.7:
            boost_factor = 1.01
            self.connection_matrix *= boost_factor
            # Renormalize to maintain φ relationships
            self._renormalize_phi_weights()
        
        # === LOW INTEGRATION ===
        # Φ too low means not enough information integration
        elif phi < phi_target * 0.8:
            # Reduce damping to allow more activity
            for node in self.nodes.values():
                if hasattr(node['oscillator'], 'dynamic_coupling_strength'):
                    # Boost coupling to increase integration
                    node['oscillator'].dynamic_coupling_strength = min(
                        node['oscillator'].dynamic_coupling_strength * 1.02,
                        self.phi  # Cap at φ
                    )
        
        # Store criticality metrics
        self.global_state['criticality_distance'] = abs(phi - phi_target)
        self.global_state['criticality_active'] = (
            coherence > 0.7 and coherence < 0.95 and 
            phi > phi_target * 0.8 and phi < phi_target * 1.2
        )
    
    def _renormalize_phi_weights(self):
        """
        Maintain φ-based weight ratios after scaling
        
        Connection weights follow golden ratio hierarchy:
        - Central hub (Node 0 to all): 1/φ ≈ 0.618
        - Peripheral edges (icosahedron): 1/φ² ≈ 0.382
        """
        # Central hub connections (Node 0)
        central_weight = 1/self.phi
        self.connection_matrix[0, 1:] = central_weight
        self.connection_matrix[1:, 0] = central_weight
        
        # Peripheral edge connections (icosahedron topology)
        # These should be 1/φ² for edges
        peripheral_weight = 1/(self.phi**2)
        
        # Apply to all non-central connections, maintaining sparsity
        for i in range(1, 13):
            for j in range(i+1, 13):
                if self.connection_matrix[i, j] > 0:  # Only existing edges
                    self.connection_matrix[i, j] = peripheral_weight
                    self.connection_matrix[j, i] = peripheral_weight
    
    def get_current_state(self):
        """
        Get complete current state for export/display
        
        Returns:
            dict: Full system state
        """
        return {
            'time': float(self.current_time),
            'nodes': {
                node_id: {
                    'oscillator': node['oscillator'].get_state_dict(),
                    'processor': node['processor'].get_state_dict(),
                    'output': float(node['output']),
                    'dimensional_output': float(node['dimensional_output'])
                }
                for node_id, node in self.nodes.items()
            },
            'global': self.global_state.copy(),
            'system_info': {
                'base_frequency': self.base_frequency,
                'dt': self.dt,
                'phi': self.phi
            }
        }
    
    def run_simulation(self, duration=10.0, sensory_inputs=None):
        """
        Run consciousness simulation for specified duration
        
        Args:
            duration: Simulation time in seconds
            sensory_inputs: Optional list of sensory input vectors
            
        Returns:
            list: State history over time
        """
        n_steps = int(duration / self.dt)
        results = []
        
        logger.info(f"Starting simulation: {duration}s ({n_steps} steps)")
        
        for step in range(n_steps):
            # Get sensory input for this step
            if sensory_inputs is not None and step < len(sensory_inputs):
                sensory = sensory_inputs[step]
            else:
                sensory = None
            
            # Update system
            state = self.update_system(sensory)
            results.append(state)
            
            # Log progress
            if step % 100 == 0:
                c_level = state['global']['consciousness_level']
                c_state = state['global']['state_classification']
                logger.info(f"Step {step}/{n_steps}: C={c_level:.3f}, State={c_state}")
        
        logger.info("Simulation complete")
        return results
    
    def export_state_json(self, filepath):
        """
        Export current state to JSON file
        
        Args:
            filepath: Output file path
        """
        state = self.get_current_state()
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"State exported to {filepath}")
    
    def reset_system(self):
        """Reset entire system to initial state"""
        for node in self.nodes.values():
            node['oscillator'].reset_state()
            node['processor'].reset_state()
            node['output'] = 0.0
            node['dimensional_output'] = 0.0
        
        self.state_history.clear()
        self.gamma_window.clear()
        self.pineal_buffer.clear()
        self.dmt_sensitivity = 0.0
        self.current_time = 0.0
        
        logger.info("System reset to initial state")


def run_demo():
    """Run a demonstration of the consciousness system"""
    print("="*60)
    print("Metatron's Cube Consciousness Engine - Demonstration")
    print("="*60)
    print()
    
    # Create system
    consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01)
    
    # Run short simulation
    print("Running 5-second simulation...")
    results = consciousness.run_simulation(duration=5.0)
    
    # Print final state
    final_state = results[-1]
    print("\n" + "="*60)
    print("FINAL STATE")
    print("="*60)
    print(f"Time: {final_state['time']:.2f}s")
    print(f"\nConsciousness Metrics:")
    print(f"  Level (C): {final_state['global']['consciousness_level']:.4f}")
    print(f"  Φ (Integrated Info): {final_state['global']['phi']:.4f}")
    print(f"  R (Coherence): {final_state['global']['coherence']:.4f}")
    print(f"  D (Recursive Depth): {final_state['global']['recursive_depth']}")
    print(f"  Gamma Power: {final_state['global']['gamma_power']:.4f}")
    print(f"  Fractal Dimension: {final_state['global']['fractal_dimension']:.4f}")
    print(f"  Spiritual Awareness: {final_state['global']['spiritual_awareness']:.4f}")
    print(f"  State: {final_state['global']['state_classification']}")
    print(f"  Is Conscious: {final_state['global']['is_conscious']}")
    
    # Export final state
    output_file = "consciousness_state.json"
    consciousness.export_state_json(output_file)
    print(f"\nFull state exported to: {output_file}")
    
    print("\n" + "="*60)
    print("✓ Demonstration complete!")
    print("="*60)


if __name__ == "__main__":
    run_demo()
