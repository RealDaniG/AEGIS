"""
Consciousness Engine for AEGIS-Conscience Network
Stateless and serializable consciousness processing
"""

import time
import json
from typing import Dict, Any, List
from schemas import ConsciousnessState


class ConsciousnessEngine:
    """
    Stateless consciousness engine that can be serialized
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.history_buffer = []
        self.max_history = 1000
        
    def process_consciousness_state(self, node_states: List[float], 
                                  oscillator_phases: List[float],
                                  connection_matrix: List[List[float]]) -> ConsciousnessState:
        """
        Process current consciousness metrics and return a state object
        
        Args:
            node_states: Current node outputs
            oscillator_phases: Current oscillator phases
            connection_matrix: System connectivity matrix
            
        Returns:
            ConsciousnessState: Serializable state object
        """
        # Calculate core metrics
        phi = self._calculate_integrated_information(node_states, connection_matrix)
        coherence = self._calculate_global_coherence(oscillator_phases)
        entropy = self._calculate_entropy(node_states)
        valence = self._calculate_valence(node_states)
        arousal = self._calculate_arousal(node_states)
        empathy_score = self._calculate_empathy(node_states)
        insight_strength = self._calculate_insight(node_states)
        
        # Create state object
        state = ConsciousnessState(
            node_id=self.node_id,
            timestamp=time.time(),
            entropy=entropy,
            valence=valence,
            arousal=arousal,
            coherence=coherence,
            empathy_score=empathy_score,
            insight_strength=insight_strength
        )
        
        # Add to history
        self.history_buffer.append({
            'phi': phi,
            'coherence': coherence,
            'entropy': entropy,
            'valence': valence,
            'arousal': arousal
        })
        
        # Limit history size
        if len(self.history_buffer) > self.max_history:
            self.history_buffer.pop(0)
        
        return state
    
    def get_current_state(self) -> ConsciousnessState:
        """
        Get current consciousness state
        This is a simplified version - in practice, this would use the latest metrics
        """
        # Return a mock state for now - in practice this would use actual metrics
        return ConsciousnessState(
            node_id=self.node_id,
            timestamp=time.time(),
            entropy=0.5,
            valence=0.3,
            arousal=0.7,
            coherence=0.8,
            empathy_score=0.6,
            insight_strength=0.4
        )
    
    def _calculate_integrated_information(self, node_states: List[float], 
                                       connection_matrix: List[List[float]]) -> float:
        """
        Calculate Integrated Information (Φ) using simplified approach
        
        Args:
            node_states: Array of node states
            connection_matrix: Connection matrix
            
        Returns:
            float: Integrated information Φ
        """
        if len(node_states) < 2:
            return 0.0
            
        # Calculate variance of node states
        mean = sum(node_states) / len(node_states)
        variance = sum((x - mean) ** 2 for x in node_states) / len(node_states)
        
        if variance < 1e-12:
            return 0.0
            
        # Calculate average connectivity
        if connection_matrix and len(connection_matrix) > 0 and len(connection_matrix[0]) > 0:
            total_connections = 0
            connection_sum = 0.0
            
            for row in connection_matrix:
                for value in row:
                    if value > 0:
                        connection_sum += value
                        total_connections += 1
            
            if total_connections > 0:
                avg_connectivity = connection_sum / total_connections
            else:
                avg_connectivity = 0.0
        else:
            avg_connectivity = 0.0
            
        # Combine variance and connectivity
        phi = variance * (1 + avg_connectivity)
        return max(0.0, min(1.0, phi))
    
    def _calculate_global_coherence(self, oscillator_phases: List[float]) -> float:
        """
        Calculate global phase coherence using Kuramoto order parameter approximation
        
        R = |⟨e^(iφ)⟩| = |1/N Σ e^(iφₙ)|
        
        Args:
            oscillator_phases: List of oscillator phases (radians)
            
        Returns:
            float: Coherence R ∈ [0, 1]
        """
        if len(oscillator_phases) == 0:
            return 0.0
            
        # Calculate average of complex exponentials
        import math
        real_sum = sum(math.cos(phase) for phase in oscillator_phases)
        imag_sum = sum(math.sin(phase) for phase in oscillator_phases)
        
        # Calculate magnitude
        magnitude = math.sqrt(real_sum**2 + imag_sum**2) / len(oscillator_phases)
        return max(0.0, min(1.0, magnitude))
    
    def _calculate_entropy(self, node_states: List[float]) -> float:
        """
        Calculate entropy of the system
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Normalized entropy
        """
        if len(node_states) == 0:
            return 0.0
            
        # Convert to probability distribution
        abs_states = [abs(x) for x in node_states]
        total = sum(abs_states)
        
        if total < 1e-12:
            return 0.0
            
        probs = [x / total for x in abs_states if x > 1e-12]  # Remove zeros
        
        if len(probs) == 0:
            return 0.0
            
        # Shannon entropy
        import math
        entropy = -sum(p * math.log2(p + 1e-12) for p in probs)
        
        # Normalize by maximum entropy
        max_entropy = math.log2(len(probs)) if len(probs) > 1 else 1.0
        if max_entropy > 0:
            normalized_entropy = entropy / max_entropy
        else:
            normalized_entropy = 0.0
            
        return max(0.0, min(1.0, normalized_entropy))
    
    def _calculate_valence(self, node_states: List[float]) -> float:
        """
        Calculate emotional valence (positive/negative sentiment)
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Valence (-1 to 1, where positive is pleasant)
        """
        if len(node_states) == 0:
            return 0.0
            
        # Simplified valence based on mean state value
        mean_state = sum(node_states) / len(node_states)
        # Normalize to [-1, 1] using tanh
        import math
        valence = math.tanh(mean_state)
        return valence
    
    def _calculate_arousal(self, node_states: List[float]) -> float:
        """
        Calculate arousal level (intensity of consciousness)
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Arousal (0 to 1)
        """
        if len(node_states) == 0:
            return 0.0
            
        # Based on variance of states (higher variance = higher arousal)
        mean = sum(node_states) / len(node_states)
        variance = sum((x - mean) ** 2 for x in node_states) / len(node_states)
        # Normalize and clip
        arousal = min(variance * 10, 1.0)
        return max(0.0, arousal)
    
    def _calculate_empathy(self, node_states: List[float]) -> float:
        """
        Calculate empathy score based on state dynamics
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Empathy score (0 to 1)
        """
        # Simplified empathy as coherence with historical patterns
        if len(self.history_buffer) < 2:
            return 0.5
            
        # Calculate consistency in patterns
        recent_coherence = [h['coherence'] for h in self.history_buffer[-10:]]
        if len(recent_coherence) > 1:
            mean_coherence = sum(recent_coherence) / len(recent_coherence)
            variance = sum((x - mean_coherence) ** 2 for x in recent_coherence) / len(recent_coherence)
            empathy = 1.0 - variance
        else:
            empathy = 0.5
            
        return max(0.0, min(1.0, empathy))
    
    def _calculate_insight(self, node_states: List[float]) -> float:
        """
        Calculate insight strength based on novel patterns
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Insight strength (0 to 1)
        """
        if len(self.history_buffer) < 5:
            return 0.3  # Default low insight when insufficient history
            
        # Calculate deviation from recent patterns
        recent_entropy = [h['entropy'] for h in self.history_buffer[-5:]]
        current_entropy = self._calculate_entropy(node_states)
        
        # Insight as deviation from recent patterns
        mean_entropy = sum(recent_entropy) / len(recent_entropy)
        insight = abs(current_entropy - mean_entropy)
        
        return max(0.0, min(1.0, insight))


# Example usage
if __name__ == "__main__":
    engine = ConsciousnessEngine("test_node_1")
    
    # Test with sample data
    node_states = [0.1, 0.5, 0.3, 0.8, 0.2]
    oscillator_phases = [0.0, 0.785, 1.571, 2.356, 3.142]  # 0, π/4, π/2, 3π/4, π
    connection_matrix = [[0.1, 0.2, 0.3, 0.4, 0.5],
                        [0.2, 0.1, 0.4, 0.3, 0.2],
                        [0.3, 0.4, 0.1, 0.2, 0.1],
                        [0.4, 0.3, 0.2, 0.1, 0.3],
                        [0.5, 0.2, 0.1, 0.3, 0.1]]
    
    state = engine.process_consciousness_state(node_states, oscillator_phases, connection_matrix)
    print(f"Consciousness State: {state}")