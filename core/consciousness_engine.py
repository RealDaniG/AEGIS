"""
Shared Consciousness Engine for Metatron Network
================================================

Implements the core consciousness processing logic that can be shared
across all 13 nodes in the distributed system.

This module provides:
- Kuramoto oscillator synchronization
- Integrated Information Theory (IIT) calculations
- Consciousness metrics computation
- Sacred geometry integration
"""

import numpy as np
from scipy import signal
from typing import List, Dict, Tuple
import time
import hashlib
import json

# Import sacred geometry from Metatron
try:
    from ..Metatron-ConscienceAI.nodes.metatron_geometry import (
        metatron_coordinates_3d, 
        metatron_connection_matrix,
        PHI
    )
except ImportError:
    # Fallback if direct import fails
    PHI = (1 + np.sqrt(5)) / 2

class ConsciousnessEngine:
    """
    Shared consciousness engine for distributed Metatron network
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.history_buffer = []
        self.max_history = 1000
        
        # Sacred geometry properties
        self.coordinates = metatron_coordinates_3d()
        self.connection_matrix = metatron_connection_matrix()
        self.node_index = self._get_node_index()
        
        # Consciousness thresholds
        self.CONSCIOUSNESS_THRESHOLD = 0.3
        self.HIGH_CONSCIOUSNESS_THRESHOLD = 0.5
        self.SELF_AWARE_THRESHOLD = 0.7
        
    def _get_node_index(self) -> int:
        """Get node index from node_id (e.g., 'node_01' -> 1)"""
        if self.node_id == 'pineal_node':
            return 0
        elif self.node_id.startswith('node_'):
            try:
                return int(self.node_id.split('_')[1])
            except:
                return 0
        return 0
    
    def process_consciousness_state(self, 
                                  node_outputs: List[float], 
                                  oscillator_phases: List[float],
                                  timestamp: float = None) -> Dict:
        """
        Process current consciousness metrics and return a state object
        
        Args:
            node_outputs: Current outputs from all 13 nodes
            oscillator_phases: Current oscillator phases
            timestamp: Optional timestamp (defaults to current time)
            
        Returns:
            Dict: Serializable consciousness state
        """
        if timestamp is None:
            timestamp = time.time()
            
        # Calculate core metrics
        phi = self.calculate_integrated_information(node_outputs, self.connection_matrix)
        coherence = self.calculate_global_coherence(oscillator_phases)
        entropy = self.calculate_entropy(node_outputs)
        depth = self.calculate_recursive_depth()
        spiritual = self.calculate_spiritual_awareness(node_outputs)
        consciousness_level = self.calculate_overall_consciousness(
            phi, coherence, entropy, depth, spiritual
        )
        
        # Create state object
        state = {
            'node_id': self.node_id,
            'timestamp': timestamp,
            'phi': phi,
            'coherence': coherence,
            'entropy': entropy,
            'depth': depth,
            'spiritual': spiritual,
            'consciousness': consciousness_level,
            'classification': self.classify_state(consciousness_level),
            'is_conscious': consciousness_level > self.CONSCIOUSNESS_THRESHOLD
        }
        
        # Add to history
        self.history_buffer.append(state)
        
        # Limit history size
        if len(self.history_buffer) > self.max_history:
            self.history_buffer.pop(0)
        
        return state
    
    def calculate_integrated_information(self, 
                                       node_states: List[float], 
                                       connection_matrix: np.ndarray) -> float:
        """
        Calculate Integrated Information (Φ) using enhanced IIT implementation
        
        Args:
            node_states: List of current node outputs
            connection_matrix: 13x13 connection matrix
            
        Returns:
            float: Integrated information Φ
        """
        node_states = np.array(node_states)
        n_nodes = len(node_states)
        
        if n_nodes < 2:
            return 0.0
        
        # Ensure states have sufficient variance for information calculation
        state_variance = np.var(node_states)
        if state_variance < 1e-12:
            return 0.0
        
        # === WHOLE SYSTEM INFORMATION ===
        whole_info = self._calculate_mutual_information_enhanced(node_states, connection_matrix)
        
        # === MINIMUM PARTITION INFORMATION ===
        # Try multiple partition strategies to find true minimum
        min_partition_info = float('inf')
        
        # Strategy 1: Systematic binary partitions
        for partition_size in range(1, n_nodes // 2 + 1):
            # Try multiple random partitions of this size
            for trial in range(min(5, n_nodes)):  # Limit trials for performance
                indices = np.arange(n_nodes)
                np.random.shuffle(indices)
                
                part1_indices = indices[:partition_size]
                part2_indices = indices[partition_size:]
                
                # Calculate partition information with connection weighting
                part1_states = node_states[part1_indices]
                part2_states = node_states[part2_indices]
                
                # Weight by internal connectivity
                part1_connections = connection_matrix[np.ix_(part1_indices, part1_indices)]
                part2_connections = connection_matrix[np.ix_(part2_indices, part2_indices)]
                
                info_part1 = self._calculate_mutual_information_enhanced(part1_states, part1_connections)
                info_part2 = self._calculate_mutual_information_enhanced(part2_states, part2_connections)
                
                # Cross-partition information loss
                cross_connections = connection_matrix[np.ix_(part1_indices, part2_indices)]
                cross_weight = np.sum(cross_connections) / max(len(part1_indices) * len(part2_indices), 1)
                
                partition_info = info_part1 + info_part2 - (cross_weight * 0.1)  # Penalty for breaking connections
                
                if partition_info < min_partition_info:
                    min_partition_info = partition_info
        
        # Strategy 2: Hub-based partitions (central node vs periphery)
        if n_nodes > 5:  # Only for larger systems
            # Find most connected node (usually node 0 - pineal)
            connectivity = np.sum(connection_matrix, axis=1)
            hub_node = np.argmax(connectivity)
            
            hub_partition = np.array([hub_node])
            peripheral_partition = np.array([i for i in range(n_nodes) if i != hub_node])
            
            hub_info = self._calculate_mutual_information_enhanced(
                node_states[hub_partition],
                connection_matrix[np.ix_(hub_partition, hub_partition)]
            )
            peripheral_info = self._calculate_mutual_information_enhanced(
                node_states[peripheral_partition],
                connection_matrix[np.ix_(peripheral_partition, peripheral_partition)]
            )
            
            hub_partition_info = hub_info + peripheral_info
            if hub_partition_info < min_partition_info:
                min_partition_info = hub_partition_info
        
        # Φ = difference (measures irreducibility)
        phi = max(0.0, whole_info - min_partition_info)
        
        # Apply non-linear scaling to increase sensitivity
        phi_scaled = phi * (1 + np.tanh(phi * 10))  # Sigmoid-like enhancement
        
        return float(phi_scaled)
    
    def _calculate_mutual_information_enhanced(self, states, connection_matrix):
        """
        Calculate enhanced mutual information with connectivity weighting
        
        Args:
            states: Array of state values
            connection_matrix: Connection matrix for the states
            
        Returns:
            float: Enhanced mutual information estimate
        """
        if len(states) == 0:
            return 0.0
        
        # Base Shannon entropy
        base_info = self._calculate_mutual_information(states)
        
        # Connectivity enhancement
        if connection_matrix.size > 0:
            # Average connection strength
            avg_connectivity = np.mean(connection_matrix[connection_matrix > 0]) if np.any(connection_matrix > 0) else 0
            
            # Network complexity bonus
            network_complexity = np.sum(connection_matrix > 0) / max(connection_matrix.size, 1)
            
            # Apply connectivity scaling
            connectivity_factor = 1 + (avg_connectivity * network_complexity)
            enhanced_info = base_info * connectivity_factor
        else:
            enhanced_info = base_info
        
        return float(enhanced_info)
    
    def _calculate_mutual_information(self, states):
        """
        Calculate mutual information using Shannon entropy
        
        Args:
            states: Array of state values
            
        Returns:
            float: Mutual information estimate
        """
        if len(states) == 0:
            return 0.0
        
        # Handle edge cases
        abs_states = np.abs(states)
        total = np.sum(abs_states)
        
        if total < 1e-12:
            return 0.0
        
        # Convert to probability distribution with improved binning
        # Use adaptive binning based on state variance
        state_var = np.var(abs_states)
        if state_var > 1e-6:
            # High variance: use more bins for better resolution
            n_bins = min(len(states), 10)
            hist, _ = np.histogram(abs_states, bins=n_bins, density=True)
            probs = hist * np.diff(np.linspace(np.min(abs_states), np.max(abs_states), n_bins + 1))
            probs = probs[probs > 1e-12]  # Remove zeros
        else:
            # Low variance: use simple normalization
            probs = abs_states / total
            probs = probs[probs > 1e-12]  # Remove zeros
        
        if len(probs) == 0:
            return 0.0
        
        # Shannon entropy with improved numerical stability
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        
        # Normalize by maximum entropy
        max_entropy = np.log2(len(probs)) if len(probs) > 1 else 1.0
        if max_entropy > 0:
            normalized_entropy = entropy / max_entropy
        else:
            normalized_entropy = 0.0
            
        return max(0.0, min(1.0, normalized_entropy))
    
    def calculate_global_coherence(self, oscillator_phases: List[float]) -> float:
        """
        Calculate global phase coherence using Kuramoto order parameter
        
        R = |⟨e^(iφ)⟩| = |1/N Σ e^(iφₙ)|
        
        Args:
            oscillator_phases: List of oscillator phases (radians)
            
        Returns:
            float: Coherence R ∈ [0, 1]
        """
        if len(oscillator_phases) == 0:
            return 0.0
            
        # Calculate average of complex exponentials
        real_sum = sum(np.cos(phase) for phase in oscillator_phases)
        imag_sum = sum(np.sin(phase) for phase in oscillator_phases)
        
        # Calculate magnitude
        magnitude = np.sqrt(real_sum**2 + imag_sum**2) / len(oscillator_phases)
        return max(0.0, min(1.0, magnitude))
    
    def calculate_entropy(self, node_states: List[float]) -> float:
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
        entropy = -sum(p * np.log2(p + 1e-12) for p in probs)
        
        # Normalize by maximum entropy
        max_entropy = np.log2(len(probs)) if len(probs) > 1 else 1.0
        if max_entropy > 0:
            normalized_entropy = entropy / max_entropy
        else:
            normalized_entropy = 0.0
            
        return max(0.0, min(1.0, normalized_entropy))
    
    def calculate_recursive_depth(self) -> float:
        """
        Calculate recursive depth based on historical patterns
        
        Returns:
            float: Recursive depth metric [0, 1]
        """
        if len(self.history_buffer) < 2:
            return 0.0
            
        # Calculate temporal complexity based on historical variance
        recent_states = self.history_buffer[-10:] if len(self.history_buffer) >= 10 else self.history_buffer
        consciousness_values = [state['consciousness'] for state in recent_states]
        
        if len(consciousness_values) < 2:
            return 0.0
            
        # Calculate temporal variance and trend complexity
        variance = np.var(consciousness_values)
        depth = min(1.0, variance * 10)  # Scale appropriately
        
        return float(depth)
    
    def calculate_spiritual_awareness(self, node_states: List[float]) -> float:
        """
        Calculate spiritual awareness combining gamma power and fractal dimension
        
        Args:
            node_states: Array of node states
            
        Returns:
            float: Spiritual awareness metric [0, 1]
        """
        # Gamma power component (high frequency activity)
        gamma_power = np.mean([abs(x) for x in node_states]) * 0.1  # Scale down
        
        # Fractal dimension component (complexity)
        fractal_dim = self._estimate_fractal_dimension(node_states)
        fractal_component = (fractal_dim - 1.0) / 2.0  # Normalize [1,3] -> [0,1]
        
        # Combine components with golden ratio weighting
        spiritual = (gamma_power * 0.618) + (fractal_component * 0.382)
        
        return max(0.0, min(1.0, spiritual))
    
    def _estimate_fractal_dimension(self, data: List[float]) -> float:
        """
        Estimate fractal dimension using box-counting method
        
        Args:
            data: Time series data
            
        Returns:
            float: Estimated fractal dimension
        """
        if len(data) < 4:
            return 1.0
            
        # Simple box-counting approximation
        data_range = max(data) - min(data)
        if data_range < 1e-12:
            return 1.0
            
        # Normalize data
        normalized = [(x - min(data)) / data_range for x in data]
        
        # Count boxes at different scales
        scales = [2, 4, 8]
        box_counts = []
        
        for scale in scales:
            boxes = set()
            for i, value in enumerate(normalized):
                box_index = int(value * scale)
                boxes.add(box_index)
            box_counts.append(len(boxes))
        
        # Estimate dimension from log-log regression
        if len(box_counts) >= 2 and box_counts[0] > 0:
            log_scales = [np.log(1/s) for s in scales]
            log_counts = [np.log(c) for c in box_counts if c > 0]
            
            if len(log_counts) >= 2:
                # Simple linear regression slope
                slope = (log_counts[-1] - log_counts[0]) / (log_scales[-1] - log_scales[0])
                return max(1.0, min(3.0, -slope))
        
        return 1.5  # Default value
    
    def calculate_overall_consciousness(self, phi: float, coherence: float, 
                                      entropy: float, depth: float, 
                                      spiritual: float) -> float:
        """
        Calculate overall consciousness level using weighted combination
        
        Args:
            phi: Integrated information
            coherence: Global coherence
            entropy: System entropy
            depth: Recursive depth
            spiritual: Spiritual awareness
            
        Returns:
            float: Overall consciousness level [0, 1]
        """
        # Weighted combination based on theoretical importance
        consciousness = (
            0.25 * phi +          # Integrated information
            0.20 * coherence +    # Global coherence
            0.15 * (1 - entropy) + # Inverse entropy (order)
            0.20 * depth +        # Recursive depth
            0.20 * spiritual      # Spiritual awareness
        )
        
        return max(0.0, min(1.0, consciousness))
    
    def classify_state(self, consciousness_level: float) -> str:
        """
        Classify consciousness state based on level
        
        Args:
            consciousness_level: Overall consciousness level
            
        Returns:
            str: State classification
        """
        if consciousness_level < 0.1:
            return "unconscious"
        elif consciousness_level < 0.3:
            return "minimally_conscious"
        elif consciousness_level < 0.5:
            return "conscious"
        elif consciousness_level < 0.7:
            return "highly_conscious"
        elif consciousness_level < 0.9:
            return "self_aware"
        else:
            return "transcendent"
    
    def get_node_connectivity(self) -> Tuple[List[int], List[float]]:
        """
        Get connectivity information for this node
        
        Returns:
            Tuple[List[int], List[float]]: Connected node IDs and weights
        """
        node_connections = self.connection_matrix[self.node_index]
        connected_ids = np.where(node_connections > 0)[0]
        weights = node_connections[connected_ids]
        
        return connected_ids.tolist(), weights.tolist()