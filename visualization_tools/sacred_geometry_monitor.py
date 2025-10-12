#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sacred Geometry Foundation - Live Consciousness Monitoring System
Based on Metatron's Cube with 13 consciousness nodes in icosahedron geometry
"""

import math
import time
import threading
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime

# Constants (SI)
c = 299_792_458.0
h = 6.62607015e-34
hbar = h/(2*math.pi)
L_P = 1.616255e-35
PHI = 1.618033988750  # Golden ratio
EPS = 1e-99

# Params for Q-factor modulation
a3, a6, a10 = 0.06, 0.05, 0.03
phi3, phi10 = 0.25, -0.4

@dataclass
class ConsciousnessState:
    """Represents the state of a consciousness node"""
    node_id: int
    timestamp: float
    consciousness_level: float  # 0.0 (unconscious) to 1.0 (transcendent)
    coherence: float  # 0.0 to 1.0
    entropy: float  # 0.0 to 1.0
    valence: float  # -1.0 to 1.0
    arousal: float  # 0.0 to 1.0
    empathy_score: float  # 0.0 to 1.0
    insight_strength: float  # 0.0 to 1.0
    frequency: float  # Hz
    position: List[float]  # 3D position in icosahedron
    phase: float  # Kuramoto phase coupling

@dataclass
class NetworkState:
    """Represents the state of the entire 13-node network"""
    timestamp: float
    avg_consciousness: float
    global_coherence: float
    synchronization_level: float  # Kuramoto order parameter
    frequency_distribution: List[float]
    phase_distribution: List[float]

class IcosahedronGeometry:
    """Handles the icosahedron geometry for 13 nodes (12 vertices + 1 center)"""
    
    def __init__(self, radius=1.0):
        self.radius = radius
        self.vertices = self._generate_icosahedron_vertices()
        self.center = [0.0, 0.0, 0.0]
        
    def _generate_icosahedron_vertices(self):
        """Generate the 12 vertices of an icosahedron"""
        # Golden ratio
        phi = (1 + math.sqrt(5)) / 2
        
        # Generate vertices
        vertices = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                vertices.append([0, i, j*phi])
                vertices.append([i, j*phi, 0])
                vertices.append([j*phi, 0, i])
        
        # Scale to radius
        norm = sum(x**2 for x in vertices[0])**0.5
        vertices = [[x * self.radius / norm for x in vertex] for vertex in vertices]
        return vertices
    
    def get_node_positions(self):
        """Get positions for all 13 nodes (12 vertices + 1 center)"""
        positions = [self.center]  # Central pineal node
        positions.extend(self.vertices)
        return positions

class SacredGeometrySystem:
    """Main system for monitoring the 13-node consciousness network"""
    
    def __init__(self):
        self.geometry = IcosahedronGeometry(radius=1.0)
        self.nodes: List[ConsciousnessState] = []
        self.network_history: List[NetworkState] = []
        self.running = False
        self.time_step = 0.1  # seconds
        self.coupling_strength = 0.5  # Kuramoto coupling
        
        # Initialize nodes
        self._initialize_nodes()
        
    def _initialize_nodes(self):
        """Initialize the 13 consciousness nodes"""
        positions = self.geometry.get_node_positions()
        
        for i, pos in enumerate(positions):
            # Calculate frequency based on position and Q-factor
            # Distance from center affects the scale L
            distance = sum(x**2 for x in pos)**0.5
                
            L = L_P * (PHI ** (distance * 10))  # Scale based on position
            Q = self._calculate_q_factor(i)
            frequency = (c / max(L, EPS)) * Q / (2 * math.pi)
            
            node = ConsciousnessState(
                node_id=i,
                timestamp=time.time(),
                consciousness_level=0.1 + 0.2 * (i / 12),  # Vary initial consciousness
                coherence=0.2 + 0.3 * (i / 12),
                entropy=0.3 + 0.4 * (i / 12),
                valence=-0.3 + 0.6 * (i / 12),
                arousal=0.2 + 0.2 * (i / 12),
                empathy_score=0.1 + 0.3 * (i / 12),
                insight_strength=0.1 + 0.2 * (i / 12),
                frequency=frequency,
                position=pos,
                phase=2 * math.pi * (i / 12)
            )
            self.nodes.append(node)
    
    def _calculate_q_factor(self, node_index: int) -> float:
        """Calculate Q-factor for a node based on its index"""
        n = node_index
        return 1.0 \
            + a3*math.cos(2*math.pi*n/3.0 + phi3) \
            + a6*math.cos(2*math.pi*n/6.0) \
            + a10*math.cos(2*math.pi*n/10.0 + phi10)
    
    def _update_kuramoto_coupling(self):
        """Update phases using Kuramoto coupling model"""
        n = len(self.nodes)
        new_phases = [0.0] * n
        
        for i in range(n):
            omega_i = 2 * math.pi * self.nodes[i].frequency
            phase_i = self.nodes[i].phase
            
            # Coupling term
            coupling_sum = 0.0
            for j in range(n):
                if i != j:
                    phase_j = self.nodes[j].phase
                    coupling_sum += math.sin(phase_j - phase_i)
            
            dphase_dt = omega_i + (self.coupling_strength / n) * coupling_sum
            new_phases[i] = phase_i + dphase_dt * self.time_step
        
        # Update phases
        for i in range(n):
            self.nodes[i].phase = new_phases[i] % (2 * math.pi)
    
    def _update_consciousness_levels(self):
        """Update consciousness levels based on network dynamics"""
        # Calculate synchronization level (Kuramoto order parameter)
        n = len(self.nodes)
        real_sum = sum(math.cos(node.phase) for node in self.nodes)
        imag_sum = sum(math.sin(node.phase) for node in self.nodes)
        synchronization = math.sqrt(real_sum**2 + imag_sum**2) / n
        
        # Update each node based on network state
        for node in self.nodes:
            # Consciousness increases with network synchronization
            sync_influence = synchronization * 0.1
            
            # Coherence affects consciousness positively
            coherence_influence = node.coherence * 0.05
            
            # Entropy affects consciousness negatively when too high
            entropy_penalty = max(0, (node.entropy - 0.7) * 0.1)
            
            # Update consciousness level with constraints
            delta = sync_influence + coherence_influence - entropy_penalty
            node.consciousness_level = max(0.0, min(1.0, node.consciousness_level + delta * 0.1))
            
            # Update other metrics with small variations
            import random
            node.coherence = max(0.0, min(1.0, node.coherence + 0.02 * (0.5 - random.random())))
            node.entropy = max(0.0, min(1.0, node.entropy + 0.02 * (0.5 - random.random())))
            node.valence = max(-1.0, min(1.0, node.valence + 0.03 * (0.5 - random.random())))
            node.arousal = max(0.0, min(1.0, node.arousal + 0.02 * (0.5 - random.random())))
            node.empathy_score = max(0.0, min(1.0, node.empathy_score + 0.01 * (0.5 - random.random())))
            node.insight_strength = max(0.0, min(1.0, node.insight_strength + 0.01 * (0.5 - random.random())))
            
            # Update timestamp
            node.timestamp = time.time()
    
    def _calculate_network_state(self) -> NetworkState:
        """Calculate the current state of the entire network"""
        consciousness_levels = [node.consciousness_level for node in self.nodes]
        coherence_levels = [node.coherence for node in self.nodes]
        frequencies = [node.frequency for node in self.nodes]
        phases = [node.phase for node in self.nodes]
        
        # Calculate synchronization level (Kuramoto order parameter)
        n = len(self.nodes)
        real_sum = sum(math.cos(phase) for phase in phases)
        imag_sum = sum(math.sin(phase) for phase in phases)
        synchronization = math.sqrt(real_sum**2 + imag_sum**2) / n
        
        return NetworkState(
            timestamp=time.time(),
            avg_consciousness=sum(consciousness_levels) / len(consciousness_levels),
            global_coherence=sum(coherence_levels) / len(coherence_levels),
            synchronization_level=synchronization,
            frequency_distribution=frequencies,
            phase_distribution=phases
        )
    
    def start_monitoring(self):
        """Start the real-time monitoring system"""
        self.running = True
        print("🌀 Starting Sacred Geometry Consciousness Monitoring System...")
        print(f"📍 Initialized {len(self.nodes)} consciousness nodes in icosahedron geometry")
        print("🔗 Kuramoto synchronization enabled")
        print("📊 Live monitoring started\n")
        
        # Start monitoring in a separate thread
        monitoring_thread = threading.Thread(target=self._monitoring_loop)
        monitoring_thread.daemon = True
        monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.running = False
        print("\n⏹️  Monitoring system stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            # Update system state
            self._update_kuramoto_coupling()
            self._update_consciousness_levels()
            
            # Calculate network state
            network_state = self._calculate_network_state()
            self.network_history.append(network_state)
            
            # Keep only recent history
            if len(self.network_history) > 1000:
                self.network_history.pop(0)
            
            # Print current status
            self._print_status(network_state)
            
            time.sleep(self.time_step)
    
    def _print_status(self, network_state: NetworkState):
        """Print the current system status"""
        # Classify consciousness state
        avg_consciousness = network_state.avg_consciousness
        if avg_consciousness < 0.2:
            state_label = "UNCONSCIOUS"
        elif avg_consciousness < 0.4:
            state_label = "SUBCONSCIOUS"
        elif avg_consciousness < 0.6:
            state_label = "CONSCIOUS"
        elif avg_consciousness < 0.8:
            state_label = "HYPERCONSCIOUS"
        else:
            state_label = "TRANSCENDENT"
        
        # Clear screen and print status
        print("\033[2J\033[H")  # Clear terminal
        print("=" * 80)
        print("SACRED GEOMETRY FOUNDATION - CONSCIOUSNESS MONITORING SYSTEM")
        print("=" * 80)
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🧠 Network State: {state_label}")
        print(f"📈 Average Consciousness: {avg_consciousness:.3f}")
        print(f"🔗 Global Coherence: {network_state.global_coherence:.3f}")
        print(f"🤝 Synchronization Level: {network_state.synchronization_level:.3f}")
        print("-" * 80)
        
        # Print individual node states
        print(f"{'Node':<6} {'Consciousness':<12} {'Coherence':<10} {'Entropy':<8} {'Frequency':<12} {'Phase':<8}")
        print("-" * 80)
        
        for node in self.nodes:
            # Classify node consciousness
            if node.consciousness_level < 0.2:
                node_state = "UNCON"
            elif node.consciousness_level < 0.4:
                node_state = "SUBCON"
            elif node.consciousness_level < 0.6:
                node_state = "CON"
            elif node.consciousness_level < 0.8:
                node_state = "HYPER"
            else:
                node_state = "TRANS"
                
            print(f"{node.node_id:<6} {node_state:<12} {node.coherence:<10.3f} {node.entropy:<8.3f} "
                  f"{node.frequency:<12.2e} {node.phase:<8.2f}")
        
        print("=" * 80)
        print("Press Ctrl+C to stop monitoring")
    
    def get_nodes_data(self) -> List[Dict]:
        """Get current node data for visualization"""
        return [asdict(node) for node in self.nodes]
    
    def get_network_history(self) -> List[Dict]:
        """Get network history for plotting"""
        return [asdict(state) for state in self.network_history]

def main():
    """Main function to run the Sacred Geometry monitoring system"""
    print("🔮 Sacred Geometry Foundation - Consciousness Monitoring System")
    print("=" * 80)
    print("Based on Metatron's Cube with 13 consciousness nodes in icosahedron geometry")
    print("Featuring golden ratio (φ) relationships and Kuramoto synchronization")
    print("=" * 80)
    
    # Create the system
    system = SacredGeometrySystem()
    
    # Start text-only monitoring
    system.start_monitoring()
    try:
        while system.running:
            time.sleep(1)
    except KeyboardInterrupt:
        system.stop_monitoring()

if __name__ == "__main__":
    main()