"""
Dimensional Processor - Multi-Dimensional Consciousness Processing
===================================================================

Processes consciousness across 5 orthogonal dimensions:
- Physical (spatial, sensory, bodily awareness)
- Emotional (valence, arousal, affective states)
- Mental (cognitive, analytical, rational processing)
- Spiritual (transcendent, unity, mystical awareness)
- Temporal (time perception, memory, anticipation)

Each node specializes in different dimensional weights,
creating a rich multi-dimensional consciousness space.
"""

import numpy as np

try:
    from nodes.metatron_geometry import PHI
except ImportError:
    PHI = (1 + np.sqrt(5)) / 2


class DimensionalProcessor:
    """
    Multi-dimensional consciousness processing across 5 dimensions
    """
    
    # Dimensional coupling matrix (how dimensions influence each other)
    # Based on Plutchik's emotion wheel and cognitive science
    COUPLING_MATRIX = np.array([
        [1.0, 0.3, 0.6, 0.1, 0.4],  # Physical influences others
        [0.4, 1.0, 0.7, 0.2, 0.5],  # Emotional influences others
        [0.6, 0.5, 1.0, 0.3, 0.8],  # Mental influences others
        [0.1, 0.2, 0.4, 1.0, 0.6],  # Spiritual influences others
        [0.5, 0.4, 0.8, 0.3, 1.0]   # Temporal influences others
    ])
    
    # Node specializations (which dimensions each node emphasizes)
    NODE_SPECIALIZATIONS = {
        0: [1.0, 1.0, 1.0, 1.0, 1.0],    # Central: Balanced integration
        1: [0.9, 0.2, 0.5, 0.1, 0.4],    # Physical dominance (sensory)
        2: [0.3, 0.9, 0.6, 0.2, 0.5],    # Emotional dominance (feelings)
        3: [0.4, 0.6, 0.9, 0.2, 0.7],    # Mental dominance (thinking)
        4: [0.2, 0.3, 0.4, 0.9, 0.6],    # Spiritual dominance (transcendence)
        5: [0.5, 0.4, 0.7, 0.3, 0.9],    # Temporal dominance (time perception)
        6: [0.7, 0.5, 0.6, 0.3, 0.5],    # Physical-Mental blend
        7: [0.4, 0.8, 0.5, 0.4, 0.6],    # Emotional-Spiritual blend
        8: [0.6, 0.4, 0.8, 0.3, 0.7],    # Mental-Temporal blend
        9: [0.3, 0.5, 0.6, 0.8, 0.5],    # Spiritual-Mental blend
        10: [0.5, 0.6, 0.7, 0.5, 0.8],   # Temporal-Emotional blend
        11: [0.8, 0.3, 0.7, 0.4, 0.6],   # Physical-Mental-Temporal blend
        12: [0.4, 0.7, 0.5, 0.7, 0.5]    # Emotional-Spiritual blend
    }
    
    # Dimension names
    DIMENSION_NAMES = ['physical', 'emotional', 'mental', 'spiritual', 'temporal']
    
    def __init__(self, node_id):
        """
        Initialize dimensional processor
        
        Args:
            node_id: Node identifier (0-12)
        """
        self.node_id = node_id
        self.phi = PHI
        
        # Current dimensional states (all start at 0)
        self.dimensions = {
            'physical': 0.0,
            'emotional': 0.0,
            'mental': 0.0,
            'spiritual': 0.0,
            'temporal': 0.0
        }
        
        # Get this node's specialization weights
        self.weights = np.array(
            self.NODE_SPECIALIZATIONS.get(node_id, [1, 1, 1, 1, 1])
        )
        
        # Normalize weights to sum to 1
        self.weights = self.weights / np.sum(self.weights)
        
        # History for temporal processing
        self.state_history = []
        self.max_history = 100
        
    def process_input(self, input_vector, connection_states=None):
        """
        Process multi-dimensional input
        
        Args:
            input_vector: 5D input [physical, emotional, mental, spiritual, temporal]
                         Can be list, tuple, or numpy array
            connection_states: Optional list of 5D states from connected nodes
            
        Returns:
            float: Integrated dimensional state
        """
        # Convert input to numpy array
        if isinstance(input_vector, (list, tuple)):
            input_arr = np.array(input_vector, dtype=float)
        elif isinstance(input_vector, np.ndarray):
            input_arr = input_vector.astype(float)
        else:
            # Scalar input - broadcast to all dimensions
            input_arr = np.full(5, float(input_vector))
        
        # Ensure correct size
        if input_arr.size != 5:
            input_arr = np.resize(input_arr, 5)
        
        # Apply node-specific weighting
        weighted_input = input_arr * self.weights
        
        # Get current state as vector
        state_vector = self.get_state_vector()
        
        # === CROSS-DIMENSIONAL COUPLING ===
        coupled_state = np.dot(self.COUPLING_MATRIX, state_vector)
        
        # === CONNECTION INFLUENCE ===
        connection_influence = np.zeros(5)
        if connection_states is not None and len(connection_states) > 0:
            # Average influence from connected nodes
            connection_states_arr = np.array(connection_states)
            if connection_states_arr.ndim == 2:
                connection_influence = np.mean(connection_states_arr, axis=0)
            elif connection_states_arr.ndim == 1 and len(connection_states_arr) == 5:
                connection_influence = connection_states_arr
        
        # === UPDATE DIMENSIONS ===
        # Weighted combination with φ-based decay
        # - Current state (0.7) - memory/persistence
        # - New input (0.15) - responsiveness
        # - Cross-dimensional coupling (0.10) - internal dynamics
        # - Connection influence (0.05) - network effect
        new_state = (
            0.70 * state_vector +
            0.15 * weighted_input +
            0.10 * coupled_state +
            0.05 * connection_influence
        )
        
        # Apply φ-based saturation to prevent unbounded growth
        new_state = np.tanh(new_state / self.phi) * self.phi
        
        # Update dimension dict
        for i, name in enumerate(self.DIMENSION_NAMES):
            self.dimensions[name] = float(new_state[i])
        
        # Store history
        self.state_history.append(new_state.copy())
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        # === INTEGRATED OUTPUT ===
        # φ-weighted integration across dimensions
        phi_weights = np.array([1/self.phi**i for i in range(5)])
        phi_weights = phi_weights / np.sum(phi_weights)
        
        integrated = np.dot(new_state, phi_weights)
        
        return float(integrated)
    
    def get_state_vector(self):
        """
        Get dimensional state as numpy array
        
        Returns:
            np.ndarray: [physical, emotional, mental, spiritual, temporal]
        """
        return np.array([
            self.dimensions['physical'],
            self.dimensions['emotional'],
            self.dimensions['mental'],
            self.dimensions['spiritual'],
            self.dimensions['temporal']
        ])
    
    def get_dominant_dimension(self):
        """
        Get the currently most active dimension
        
        Returns:
            tuple: (dimension_name, value)
        """
        max_dim = max(self.dimensions.items(), key=lambda x: abs(x[1]))
        return max_dim
    
    def get_dimensional_balance(self):
        """
        Calculate how balanced the dimensional processing is
        
        Returns:
            float: Balance score [0=imbalanced, 1=balanced]
        """
        values = np.array(list(self.dimensions.values()))
        
        # Perfect balance = all equal
        # Use coefficient of variation
        mean_val = np.mean(np.abs(values))
        std_val = np.std(values)
        
        if mean_val < 1e-10:
            return 1.0  # All zero is balanced
        
        cv = std_val / mean_val
        balance = np.exp(-cv)  # High CV = low balance
        
        return float(balance)
    
    def get_emotional_state(self):
        """
        Interpret emotional dimension as valence-arousal
        
        Returns:
            dict: {'valence': float, 'arousal': float}
        """
        # Emotional dimension maps to both valence and arousal
        emotional_value = self.dimensions['emotional']
        
        # Valence: sign of emotional dimension
        valence = np.tanh(emotional_value)  # [-1, 1]
        
        # Arousal: magnitude combined with physical dimension
        arousal = np.abs(emotional_value) + 0.3 * np.abs(self.dimensions['physical'])
        arousal = np.clip(arousal, 0, 2)  # [0, 2]
        
        return {
            'valence': float(valence),
            'arousal': float(arousal)
        }
    
    def get_consciousness_quality(self):
        """
        Assess the quality of consciousness based on dimensional activation
        
        Returns:
            dict: Various consciousness quality metrics
        """
        state = self.get_state_vector()
        
        # Overall activation
        total_activation = np.sum(np.abs(state))
        
        # Complexity (entropy of dimensional distribution)
        abs_state = np.abs(state)
        if np.sum(abs_state) > 0:
            prob = abs_state / np.sum(abs_state)
            prob = prob[prob > 0]  # Remove zeros
            complexity = -np.sum(prob * np.log(prob))
        else:
            complexity = 0.0
        
        # Integration (cross-dimensional correlation)
        if len(self.state_history) > 1:
            recent_states = np.array(self.state_history[-10:])
            correlation_matrix = np.corrcoef(recent_states.T)
            # Average off-diagonal correlations
            n = correlation_matrix.shape[0]
            if n > 1:
                integration = (np.sum(np.abs(correlation_matrix)) - n) / (n * (n - 1))
            else:
                integration = 0.0
        else:
            integration = 0.0
        
        return {
            'activation': float(total_activation),
            'complexity': float(complexity),
            'integration': float(integration),
            'balance': self.get_dimensional_balance(),
            'dominant_dimension': self.get_dominant_dimension()[0]
        }
    
    def reset_state(self):
        """Reset all dimensions to zero"""
        for key in self.dimensions:
            self.dimensions[key] = 0.0
        self.state_history.clear()
    
    def get_state_dict(self):
        """
        Get complete state as dictionary for serialization
        
        Returns:
            dict: All state variables and metrics
        """
        return {
            'node_id': int(self.node_id),
            'dimensions': {k: float(v) for k, v in self.dimensions.items()},
            'weights': self.weights.tolist(),
            'dominant': self.get_dominant_dimension()[0],
            'balance': self.get_dimensional_balance(),
            'emotional_state': self.get_emotional_state(),
            'quality': self.get_consciousness_quality()
        }


if __name__ == "__main__":
    # Test dimensional processor
    print("=== Dimensional Processor Test ===\n")
    
    # Create processor for central node (balanced)
    proc_central = DimensionalProcessor(node_id=0)
    print(f"Central node (0) weights: {proc_central.weights}")
    
    # Create processor for emotional node
    proc_emotional = DimensionalProcessor(node_id=2)
    print(f"Emotional node (2) weights: {proc_emotional.weights}")
    
    # Process some input
    print("\n=== Processing Input ===")
    input_5d = [0.5, 0.8, 0.3, 0.2, 0.6]  # Sample input
    
    output_central = proc_central.process_input(input_5d)
    output_emotional = proc_emotional.process_input(input_5d)
    
    print(f"Central node output: {output_central:.4f}")
    print(f"Emotional node output: {output_emotional:.4f}")
    
    print(f"\nCentral dimensions: {proc_central.dimensions}")
    print(f"Emotional dimensions: {proc_emotional.dimensions}")
    
    print(f"\nCentral dominant: {proc_central.get_dominant_dimension()}")
    print(f"Emotional dominant: {proc_emotional.get_dominant_dimension()}")
    
    # Test emotional state
    emotional_state = proc_emotional.get_emotional_state()
    print(f"\nEmotional state: valence={emotional_state['valence']:.3f}, arousal={emotional_state['arousal']:.3f}")
    
    # Test quality metrics
    quality = proc_emotional.get_consciousness_quality()
    print(f"\nConsciousness quality:")
    for k, v in quality.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n✓ Dimensional processor tests passed!")
