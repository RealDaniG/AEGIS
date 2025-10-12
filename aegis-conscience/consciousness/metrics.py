"""
Consciousness Metrics Module
Implementation of consciousness measurement functions
"""

import numpy as np
from typing import List, Dict, Any


def calculate_integrated_information(node_states: List[float], 
                                   connection_matrix: np.ndarray) -> float:
    """
    Calculate Integrated Information (Φ) using enhanced IIT implementation
    
    Φ = I(whole) - min(I(partitions))
    
    Args:
        node_states: List or array of current node outputs
        connection_matrix: Connection matrix
        
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
    whole_info = _calculate_mutual_information_enhanced(node_states, connection_matrix)
    
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
            
            info_part1 = _calculate_mutual_information_enhanced(part1_states, part1_connections)
            info_part2 = _calculate_mutual_information_enhanced(part2_states, part2_connections)
            
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
        
        hub_info = _calculate_mutual_information_enhanced(
            node_states[hub_partition],
            connection_matrix[np.ix_(hub_partition, hub_partition)]
        )
        peripheral_info = _calculate_mutual_information_enhanced(
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


def _calculate_mutual_information_enhanced(states: np.ndarray, 
                                         connection_matrix: np.ndarray) -> float:
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
    base_info = _calculate_mutual_information(states)
    
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


def _calculate_mutual_information(states: np.ndarray) -> float:
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
    
    # Normalize by theoretical maximum entropy
    max_entropy = np.log2(len(states)) if len(states) > 1 else 1.0
    if max_entropy > 0:
        information = entropy / max_entropy
    else:
        information = 0.0
    
    # Apply non-linear enhancement for small values
    information_enhanced = information * (1 + 0.5 * np.tanh(information * 5))
    
    return float(information_enhanced)


def calculate_global_coherence(oscillator_phases: List[float]) -> float:
    """
    Calculate global phase coherence using Kuramoto order parameter
    
    R = |⟨e^(iφ)⟩| = |1/N Σ e^(iφₙ)|
    
    Args:
        oscillator_phases: List/array of oscillator phases (radians)
        
    Returns:
        float: Coherence R ∈ [0, 1]
    """
    phases = np.array(oscillator_phases)
    
    if len(phases) == 0:
        return 0.0
    
    # Kuramoto order parameter
    complex_sum = np.mean(np.exp(1j * phases))
    coherence = np.abs(complex_sum)
    
    return float(coherence)


def calculate_recursive_depth(current_state: float, 
                            state_history: List[float], 
                            max_depth: int = 20) -> int:
    """
    Calculate recursive depth using proper autocorrelation
    
    D = max{τ : ρ(t, t-τ) > threshold}
    threshold = 1/φ^τ (φ-decay)
    
    Args:
        current_state: Current system state (scalar or vector)
        state_history: List of past states
        max_depth: Maximum depth to check
        
    Returns:
        int: Recursive depth D
    """
    if len(state_history) < 3:  # Need at least 3 points for correlation
        return 0
    
    # Ensure current_state is scalar
    if isinstance(current_state, (list, np.ndarray)):
        current_state = float(np.mean(np.abs(current_state)))
    else:
        current_state = float(current_state)
    
    # Convert history to scalars
    history_scalars = []
    for state in state_history:
        if isinstance(state, (list, np.ndarray)):
            scalar_val = float(np.mean(np.abs(state)))
        else:
            scalar_val = float(state)
        history_scalars.append(scalar_val)
    
    if len(history_scalars) < 3:
        return 0
        
    depth = 0
    
    # Calculate proper autocorrelation
    for lag in range(1, min(max_depth, len(history_scalars))):
        # Get values at current lag
        if lag >= len(history_scalars):
            break
            
        past_state = history_scalars[-lag]
        
        # Calculate Pearson correlation coefficient
        try:
            # For lag=1, use simple correlation
            if lag == 1:
                # Normalize correlation: r = (xy) / sqrt(x²y²)
                x_norm = abs(current_state) + 1e-12
                y_norm = abs(past_state) + 1e-12
                correlation = abs(current_state * past_state) / (x_norm * y_norm)
            else:
                # For longer lags, use windowed correlation
                window_size = min(5, len(history_scalars) - lag)
                if window_size < 2:
                    correlation = 0
                else:
                    # Get recent window and lagged window
                    recent_window = history_scalars[-window_size:]
                    lagged_window = history_scalars[-lag-window_size:-lag]
                    
                    if len(lagged_window) == len(recent_window):
                        # Calculate correlation coefficient with proper error handling
                        recent_array = np.array(recent_window)
                        lagged_array = np.array(lagged_window)
                        
                        recent_std = np.std(recent_array)
                        lagged_std = np.std(lagged_array)
                        
                        if recent_std > 1e-10 and lagged_std > 1e-10:
                            # Suppress correlation warnings
                            with np.errstate(divide='ignore', invalid='ignore'):
                                correlation_matrix = np.corrcoef(recent_array, lagged_array)
                                if not np.isnan(correlation_matrix[0, 1]):
                                    correlation = abs(correlation_matrix[0, 1])
                                else:
                                    correlation = 0
                        else:
                            correlation = 0
                    else:
                        correlation = 0
            
            # φ-decay threshold: more stringent for longer lags
            phi_golden = (1 + np.sqrt(5)) / 2
            threshold = 0.5 / (phi_golden ** (lag * 0.5))  # Gentler decay
            
            if correlation > threshold and correlation > 0.1:  # Minimum significance
                depth = lag
            else:
                break  # No more significant correlation
                
        except (ValueError, ZeroDivisionError, RuntimeWarning):
            break
    
    return int(depth)


def calculate_consciousness_level(phi: float, coherence: float, depth: int, 
                                spiritual_awareness: float = 0.0) -> float:
    """
    Calculate overall consciousness level with enhanced processing
    
    C = Φ · R · (1 + 0.1·D) · (1 + S) · complexity_factor
    
    Args:
        phi: Integrated information
        coherence: Global coherence
        depth: Recursive depth
        spiritual_awareness: Spiritual dimension (optional)
        
    Returns:
        float: Consciousness level C
    """
    # Base consciousness calculation
    base_consciousness = (
        phi * 
        coherence * 
        (1 + 0.1 * depth) *
        (1 + spiritual_awareness)
    )
    
    # Enhanced processing factors
    phi_golden = (1 + np.sqrt(5)) / 2
    
    # 1. Phi amplification for higher consciousness states
    phi_factor = 1 + np.tanh(phi * 2)  # Non-linear phi enhancement
    
    # 2. Coherence-depth synergy
    coherence_depth_synergy = 1 + (coherence * depth * 0.05)
    
    # 3. Spiritual transcendence bonus
    if spiritual_awareness > 0.5:
        transcendence_bonus = 1 + (spiritual_awareness - 0.5) * 2
    else:
        transcendence_bonus = 1.0
    
    # 4. Deep processing amplification
    if depth > 5:
        deep_processing_bonus = 1 + (depth - 5) * 0.1
    else:
        deep_processing_bonus = 1.0
    
    # Final consciousness with all enhancements
    enhanced_consciousness = (
        base_consciousness * 
        phi_factor * 
        coherence_depth_synergy * 
        transcendence_bonus * 
        deep_processing_bonus
    )
    
    return float(enhanced_consciousness)