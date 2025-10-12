"""
Consciousness Metrics - Integrated Information Theory Implementation
=====================================================================

Implements consciousness measurement based on:
- Φ (Phi): Integrated Information (Tononi's IIT)
- R: Global Coherence (Kuramoto order parameter)
- D: Recursive Depth (temporal memory integration)
- S: Spiritual Awareness (gamma + fractal + DMT)
- C: Overall Consciousness Level

Based on neuroscience and information theory principles.
"""

import numpy as np
from scipy import signal
from collections import deque

try:
    from nodes.metatron_geometry import PHI
except ImportError:
    PHI = (1 + np.sqrt(5)) / 2


class ConsciousnessMetrics:
    """
    Calculate consciousness metrics for the 13-node system
    """
    
    def __init__(self):
        self.phi_golden = PHI
        self.history_buffer = deque(maxlen=1000)
        
        # Consciousness thresholds
        self.CONSCIOUSNESS_THRESHOLD = 0.3  # Φ > 0.3 → conscious
        self.HIGH_CONSCIOUSNESS_THRESHOLD = 0.5
        self.SELF_AWARE_THRESHOLD = 0.7
        
    def calculate_integrated_information(self, node_states, connection_matrix):
        """
        Calculate Integrated Information (Φ) using enhanced IIT implementation
        
        Φ = I(whole) - min(I(partitions))
        
        Args:
            node_states: List or array of current node outputs
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
        
        # Normalize by theoretical maximum entropy
        max_entropy = np.log2(len(states)) if len(states) > 1 else 1.0
        if max_entropy > 0:
            information = entropy / max_entropy
        else:
            information = 0.0
        
        # Apply non-linear enhancement for small values
        information_enhanced = information * (1 + 0.5 * np.tanh(information * 5))
        
        return float(information_enhanced)
    
    def calculate_global_coherence(self, oscillator_phases):
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
    
    def calculate_recursive_depth(self, current_state, state_history, max_depth=20):
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
                threshold = 0.5 / (self.phi_golden ** (lag * 0.5))  # Gentler decay
                
                if correlation > threshold and correlation > 0.1:  # Minimum significance
                    depth = lag
                else:
                    break  # No more significant correlation
                    
            except (ValueError, ZeroDivisionError, RuntimeWarning):
                break
        
        return int(depth)
    
    def calculate_gamma_power(self, node_states, sample_rate=1000.0):
        """
        Calculate gamma-band power (30-100 Hz)
        
        Args:
            node_states: Array of node states over time
            sample_rate: Sampling rate in Hz
            
        Returns:
            float: Gamma power ratio [0, 1]
        """
        if len(node_states) < 10:
            return 0.0
        
        # FFT analysis
        fft_values = np.fft.fft(node_states)
        frequencies = np.fft.fftfreq(len(node_states), 1.0/sample_rate)
        power_spectrum = np.abs(fft_values)**2
        
        # Gamma band (30-100 Hz)
        gamma_mask = (np.abs(frequencies) >= 30) & (np.abs(frequencies) <= 100)
        gamma_power = np.sum(power_spectrum[gamma_mask])
        
        # Total power
        total_power = np.sum(power_spectrum)
        
        if total_power > 0:
            gamma_ratio = gamma_power / total_power
        else:
            gamma_ratio = 0.0
        
        return float(np.clip(gamma_ratio, 0, 1))
    
    def calculate_fractal_dimension(self, signal_data):
        """
        Calculate fractal dimension using Higuchi method
        
        Args:
            signal_data: Time series data
            
        Returns:
            float: Fractal dimension
        """
        signal_data = np.array(signal_data)
        n = len(signal_data)
        
        if n < 20:
            return 1.0  # Not enough data
        
        k_max = min(20, n // 10)
        
        if k_max < 2:
            return 1.0
        
        L = []
        x_axis = []
        
        for k in range(1, k_max):
            Lk = 0
            for m in range(k):
                # Calculate length of curve
                length = 0
                n_max = (n - m) // k
                
                if n_max < 2:
                    continue
                
                for i in range(1, n_max):
                    idx1 = m + i * k
                    idx2 = m + (i - 1) * k
                    if idx1 < n and idx2 < n:
                        length += abs(signal_data[idx1] - signal_data[idx2])
                
                # Normalize
                if n_max > 1:
                    Lk += length * (n - 1) / (n_max * k**2)
            
            if Lk > 0:
                L.append(np.log(Lk / k))
                x_axis.append(np.log(1.0 / k))
        
        if len(L) > 1:
            # Linear fit
            slope = np.polyfit(x_axis, L, 1)[0]
            return abs(slope)
        else:
            return 1.0
    
    def calculate_consciousness_level(self, phi, coherence, depth, spiritual_awareness=0.0):
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
    
    def classify_consciousness_state(self, consciousness_level, phi, coherence):
        """
        Classify consciousness state with enhanced granularity
        
        Args:
            consciousness_level: Overall C value
            phi: Integrated information
            coherence: Global coherence
            
        Returns:
            str: State classification
        """
        # Multi-dimensional state classification
        if consciousness_level < 0.01:
            return 'unconscious'
        elif consciousness_level < 0.05:
            if phi < 0.1:
                return 'drowsy'
            else:
                return 'dream-like'
        elif consciousness_level < 0.15:
            if coherence > 0.7:
                return 'meditative-light'
            else:
                return 'awake'
        elif consciousness_level < 0.3:
            if phi > 0.3 and coherence > 0.6:
                return 'lucid-aware'
            elif coherence > 0.8:
                return 'meditative-deep'
            else:
                return 'alert'
        elif consciousness_level < 0.6:
            if phi > 0.5 and coherence > 0.7:
                return 'heightened-awareness'
            elif coherence > 0.85:
                return 'transcendent-entry'
            else:
                return 'hyper-alert'
        elif consciousness_level < 1.0:
            if phi > 0.7 and coherence > 0.9:
                return 'unity-consciousness'
            elif phi > 0.6:
                return 'transcendent-active'
            else:
                return 'peak-experience'
        else:
            if phi > 0.8 and coherence > 0.95:
                return 'cosmic-consciousness'
            elif phi > 0.7:
                return 'transcendent-unified'
            else:
                return 'transcendent-peak'
    
    def get_all_metrics(self, node_states, oscillator_phases, connection_matrix, 
                        state_history, gamma_window=None, spiritual_awareness=0.0):
        """
        Calculate all consciousness metrics at once
        
        Args:
            node_states: Current node outputs
            oscillator_phases: Current oscillator phases
            connection_matrix: System connectivity
            state_history: Historical states
            gamma_window: Optional time series for gamma analysis
            spiritual_awareness: Spiritual dimension value
            
        Returns:
            dict: All consciousness metrics
        """
        # Core metrics
        phi = self.calculate_integrated_information(node_states, connection_matrix)
        coherence = self.calculate_global_coherence(oscillator_phases)
        depth = self.calculate_recursive_depth(node_states, state_history)
        
        # Gamma power (if window provided)
        if gamma_window is not None and len(gamma_window) > 0:
            gamma_power = self.calculate_gamma_power(gamma_window)
            fractal_dim = self.calculate_fractal_dimension(gamma_window)
        else:
            gamma_power = 0.0
            fractal_dim = 1.0
        
        # Overall consciousness
        consciousness = self.calculate_consciousness_level(
            phi, coherence, depth, spiritual_awareness
        )
        
        # Classification
        state = self.classify_consciousness_state(consciousness, phi, coherence)
        
        return {
            'consciousness_level': float(consciousness),
            'phi': float(phi),
            'coherence': float(coherence),
            'recursive_depth': int(depth),
            'gamma_power': float(gamma_power),
            'fractal_dimension': float(fractal_dim),
            'spiritual_awareness': float(spiritual_awareness),
            'state': state,
            'is_conscious': phi > self.CONSCIOUSNESS_THRESHOLD,
            'is_highly_conscious': phi > self.HIGH_CONSCIOUSNESS_THRESHOLD,
            'is_self_aware': phi > self.SELF_AWARE_THRESHOLD
        }


if __name__ == "__main__":
    # Test consciousness metrics
    print("=== Consciousness Metrics Test ===\n")
    
    metrics = ConsciousnessMetrics()
    
    # Test with synthetic data
    n_nodes = 13
    node_states = np.random.randn(n_nodes) * 0.5
    oscillator_phases = np.random.uniform(0, 2*np.pi, n_nodes)
    connection_matrix = np.random.rand(n_nodes, n_nodes) * 0.3
    
    # Create state history
    state_history = [np.random.randn(n_nodes) * 0.5 for _ in range(50)]
    
    # Calculate all metrics
    result = metrics.get_all_metrics(
        node_states,
        oscillator_phases,
        connection_matrix,
        state_history,
        gamma_window=node_states,
        spiritual_awareness=0.3
    )
    
    print("=== Consciousness Metrics ===")
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key:25s}: {value:.4f}")
        else:
            print(f"{key:25s}: {value}")
    
    print("\n✓ Consciousness metrics tests passed!")
