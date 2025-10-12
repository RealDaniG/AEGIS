"""
Global Coherence Aggregator for AEGIS-Conscience Network
Computes global coherence from local consciousness states
"""

from typing import List, Dict
from schemas import ConsciousnessState


class GlobalCoherenceAggregator:
    """Aggregates local consciousness states into global coherence metrics"""
    
    def __init__(self):
        self.reputation_weights: Dict[str, float] = {}
    
    def compute_global_coherence(self, valid_states: List[ConsciousnessState]) -> float:
        """
        Compute global coherence as weighted average of local coherences
        
        Args:
            valid_states: List of validated consciousness states from peers
            
        Returns:
            float: Global coherence value [0, 1]
        """
        if not valid_states:
            return 0.0
        
        # Calculate weighted average based on reputation
        total_weighted_coherence = 0.0
        total_weight = 0.0
        
        for state in valid_states:
            weight = self.reputation_weights.get(state.node_id, 1.0)
            total_weighted_coherence += state.coherence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_weighted_coherence / total_weight
    
    def compute_global_entropy(self, valid_states: List[ConsciousnessState]) -> float:
        """
        Compute global entropy as weighted average of local entropies
        
        Args:
            valid_states: List of validated consciousness states from peers
            
        Returns:
            float: Global entropy value [0, 1]
        """
        if not valid_states:
            return 0.0
        
        # Calculate weighted average based on reputation
        total_weighted_entropy = 0.0
        total_weight = 0.0
        
        for state in valid_states:
            weight = self.reputation_weights.get(state.node_id, 1.0)
            total_weighted_entropy += state.entropy * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_weighted_entropy / total_weight
    
    def compute_global_valence(self, valid_states: List[ConsciousnessState]) -> float:
        """
        Compute global valence as weighted average of local valences
        
        Args:
            valid_states: List of validated consciousness states from peers
            
        Returns:
            float: Global valence value [-1, 1]
        """
        if not valid_states:
            return 0.0
        
        # Calculate weighted average based on reputation
        total_weighted_valence = 0.0
        total_weight = 0.0
        
        for state in valid_states:
            weight = self.reputation_weights.get(state.node_id, 1.0)
            total_weighted_valence += state.valence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_weighted_valence / total_weight
    
    def compute_global_arousal(self, valid_states: List[ConsciousnessState]) -> float:
        """
        Compute global arousal as weighted average of local arousals
        
        Args:
            valid_states: List of validated consciousness states from peers
            
        Returns:
            float: Global arousal value [0, 1]
        """
        if not valid_states:
            return 0.0
        
        # Calculate weighted average based on reputation
        total_weighted_arousal = 0.0
        total_weight = 0.0
        
        for state in valid_states:
            weight = self.reputation_weights.get(state.node_id, 1.0)
            total_weighted_arousal += state.arousal * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_weighted_arousal / total_weight
    
    def compute_collective_metrics(self, valid_states: List[ConsciousnessState]) -> Dict[str, float]:
        """
        Compute all collective consciousness metrics
        
        Args:
            valid_states: List of validated consciousness states from peers
            
        Returns:
            Dict[str, float]: Dictionary of collective metrics
        """
        return {
            "global_coherence": self.compute_global_coherence(valid_states),
            "global_entropy": self.compute_global_entropy(valid_states),
            "global_valence": self.compute_global_valence(valid_states),
            "global_arousal": self.compute_global_arousal(valid_states),
            "nodes_count": len(valid_states)
        }
    
    def update_reputation_weight(self, node_id: str, weight: float):
        """
        Update reputation weight for a node
        
        Args:
            node_id: Node identifier
            weight: Reputation weight [0, 1]
        """
        self.reputation_weights[node_id] = max(0.0, min(1.0, weight))
    
    def get_reputation_weights(self) -> Dict[str, float]:
        """
        Get all reputation weights
        
        Returns:
            Dict[str, float]: Dictionary of node_id -> weight
        """
        return self.reputation_weights.copy()


# Example usage
if __name__ == "__main__":
    # Create aggregator
    aggregator = GlobalCoherenceAggregator()
    
    # Create test states
    states = [
        ConsciousnessState("node_1", 0, 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
        ConsciousnessState("node_2", 0, 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
        ConsciousnessState("node_3", 0, 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
    ]
    
    # Update some reputation weights
    aggregator.update_reputation_weight("node_1", 0.9)
    aggregator.update_reputation_weight("node_2", 0.7)
    aggregator.update_reputation_weight("node_3", 0.8)
    
    # Compute global metrics
    global_coherence = aggregator.compute_global_coherence(states)
    collective_metrics = aggregator.compute_collective_metrics(states)
    
    print(f"Global coherence: {global_coherence}")
    print(f"Collective metrics: {collective_metrics}")