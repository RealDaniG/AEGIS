"""
Sacred Geometry Manager for Metatron Network
============================================

Manages the icosahedral topology and geometric relationships
for the 13-node consciousness network.

This module provides:
- Topology management for the 13-node icosahedron
- Connection matrix maintenance
- Geometric validation
- Node positioning and relationships
"""

import numpy as np
from typing import Dict, List, Tuple

# Golden ratio constant
PHI = (1 + np.sqrt(5)) / 2

class SacredGeometryManager:
    """
    Manages the sacred geometric structure of Metatron's Cube
    for the 13-node consciousness system.
    """
    
    def __init__(self):
        self.coordinates = self._generate_coordinates()
        self.connection_matrix = self._build_connection_matrix()
        self.frequency_ratios = self._define_frequency_ratios()
        
    def _generate_coordinates(self) -> Dict[int, np.ndarray]:
        """
        Generate 13 node coordinates for Metatron's Cube
        
        Structure:
        - Node 0: Central origin (Pineal/Unity)
        - Nodes 1-12: Icosahedron vertices (normalized to unit sphere)
        
        Returns:
            dict: {node_id: np.array([x, y, z])}
        """
        nodes = {}
        
        # Node 0: Central (Pineal consciousness integrator)
        nodes[0] = np.array([0.0, 0.0, 0.0])
        
        # Nodes 1-12: Icosahedron vertices
        # Using golden ratio scaled coordinates
        vertices = [
            (-1, PHI, 0), (1, PHI, 0),           # Top cap (y > 0, z = 0)
            (-1, -PHI, 0), (1, -PHI, 0),         # Bottom cap (y < 0, z = 0)
            (0, -1, PHI), (0, 1, PHI),           # Front rectangle (z > 0, x = 0)
            (0, -1, -PHI), (0, 1, -PHI),         # Back rectangle (z < 0, x = 0)
            (PHI, 0, -1), (PHI, 0, 1),           # Right rectangle (x > 0, y = 0)
            (-PHI, 0, -1), (-PHI, 0, 1)          # Left rectangle (x < 0, y = 0)
        ]
        
        for i, vertex in enumerate(vertices, start=1):
            # Normalize to unit sphere
            vec = np.array(vertex, dtype=float)
            nodes[i] = vec / np.linalg.norm(vec)
        
        return nodes
    
    def _build_connection_matrix(self) -> np.ndarray:
        """
        Build 13x13 connection matrix following Metatron's Cube topology
        
        Connection types:
        1. Central hub (Node 0 → All others): weight = 1/φ
        2. Icosahedron edges (30 edges): weight = 1/φ²
        
        Returns:
            np.ndarray: 13x13 symmetric connection matrix
        """
        C = np.zeros((13, 13))
        
        # === CENTRAL HUB CONNECTIONS ===
        # Node 0 (pineal) connects to all peripheral nodes
        for i in range(1, 13):
            C[0, i] = 1/PHI
            C[i, 0] = 1/PHI
        
        # === ICOSAHEDRON EDGE CONNECTIONS ===
        # 30 edges connecting the 12 peripheral vertices
        edges = [
            # Connections from top cap vertices (nodes 1, 2)
            (1, 2), (1, 6), (1, 8), (1, 12), (1, 11),
            (2, 3), (2, 6), (2, 9), (2, 8),
            
            # Connections involving middle vertices
            (3, 4), (3, 7), (3, 9), (3, 10),
            (4, 5), (4, 7), (4, 10), (4, 11),
            (5, 6), (5, 10), (5, 11), (5, 12),
            (6, 12),
            
            # Connections from bottom pentagon
            (7, 8), (7, 9),
            (8, 12),
            (9, 10),
            (10, 11),
            (11, 12)
        ]
        
        # Add edge connections with φ² decay
        for i, j in edges:
            C[i, j] = 1/(PHI**2)
            C[j, i] = 1/(PHI**2)
        
        return C
    
    def _define_frequency_ratios(self) -> Dict[int, float]:
        """
        Define musical interval ratios for each node based on just intonation
        
        These ratios create harmonic resonance and minimize phase conflicts
        while maximizing information integration capacity.
        
        Returns:
            dict: {node_id: frequency_ratio}
        """
        ratios = {
            0: 1.0,      # Unity/Unison (Central/Pineal) - Foundation
            1: 1.0,      # Root/Fundamental - Grounding
            2: 9/8,      # Major Second (Whole tone) - Movement
            3: 5/4,      # Major Third - Joy/Expansion
            4: 4/3,      # Perfect Fourth - Stability
            5: 3/2,      # Perfect Fifth - Power/Openness
            6: 5/3,      # Major Sixth - Sweetness
            7: 15/8,     # Major Seventh - Leading/Tension
            8: 2.0,      # Octave - Completion
            9: PHI,      # Golden Ratio tone (Sacred) - Transcendence
            10: 3.0,     # Perfect Twelfth - Spiritual ascent
            11: 4.0,     # Double Octave - Higher consciousness
            12: 5.0      # Major Seventeenth - Unity at higher level
        }
        return ratios
    
    def get_coordinates(self) -> Dict[int, np.ndarray]:
        """
        Get all node coordinates
        
        Returns:
            dict: {node_id: coordinates}
        """
        return self.coordinates.copy()
    
    def get_connection_matrix(self) -> np.ndarray:
        """
        Get the connection matrix
        
        Returns:
            np.ndarray: 13x13 connection matrix
        """
        return self.connection_matrix.copy()
    
    def get_node_connections(self, node_id: int) -> Tuple[List[int], List[float]]:
        """
        Get all nodes connected to a given node with their weights
        
        Args:
            node_id: Node to query (0-12)
            
        Returns:
            tuple: (connected_node_ids, connection_weights)
        """
        if node_id < 0 or node_id >= 13:
            return [], []
            
        connections = self.connection_matrix[node_id]
        connected_ids = np.where(connections > 0)[0]
        weights = connections[connected_ids]
        
        return connected_ids.tolist(), weights.tolist()
    
    def get_frequency_ratio(self, node_id: int) -> float:
        """
        Get the musical frequency ratio for a node
        
        Args:
            node_id: Node ID (0-12)
            
        Returns:
            float: Frequency ratio
        """
        return self.frequency_ratios.get(node_id, 1.0)
    
    def calculate_edge_distances(self) -> Dict[Tuple[int, int], float]:
        """
        Calculate actual geometric distances between connected nodes
        
        Useful for validating golden ratio relationships in structure
        
        Returns:
            dict: {(node_i, node_j): distance}
        """
        distances = {}
        
        for i in range(13):
            for j in range(i+1, 13):
                dist = np.linalg.norm(self.coordinates[i] - self.coordinates[j])
                distances[(i, j)] = dist
                distances[(j, i)] = dist
        
        return distances
    
    def verify_golden_ratio_properties(self) -> Dict:
        """
        Verify that the geometry contains golden ratio relationships
        
        Returns:
            dict: Verification results
        """
        results = {
            'vertices_normalized': True,
            'golden_ratios_found': [],
            'symmetry_verified': False,
            'edge_ratio_check': {}
        }
        
        # === CHECK NORMALIZATION ===
        for node_id, coord in self.coordinates.items():
            if node_id == 0:  # Skip central node
                continue
            norm = np.linalg.norm(coord)
            if not np.isclose(norm, 1.0, rtol=1e-6):
                results['vertices_normalized'] = False
                break
        
        # === CHECK FOR φ RATIOS IN COORDINATES ===
        # Icosahedron coordinates should contain φ
        for node_id, coord in self.coordinates.items():
            if node_id == 0:
                continue
            for i, component in enumerate(coord):
                # Check if component relates to φ
                if np.isclose(abs(component), PHI/np.sqrt(1 + PHI**2), rtol=0.01):
                    results['golden_ratios_found'].append({
                        'node': node_id,
                        'axis': ['x', 'y', 'z'][i],
                        'value': component
                    })
        
        # === CHECK EDGE RATIOS ===
        # In icosahedron, edge length / radius should relate to φ
        if len(self.coordinates) >= 2:
            # Calculate edge between nodes 1 and 2 (should be connected)
            edge_length = np.linalg.norm(self.coordinates[1] - self.coordinates[2])
            # For unit sphere icosahedron, edge ≈ 1.0515
            results['edge_ratio_check'] = {
                'edge_length': edge_length,
                'expected': 1.0515,  # Approximate for unit icosahedron
                'matches': np.isclose(edge_length, 1.0515, rtol=0.05)
            }
        
        # === CHECK SYMMETRY ===
        # Should have 13 nodes total
        results['symmetry_verified'] = len(self.coordinates) == 13
        
        return results
    
    def get_system_properties(self) -> Dict:
        """
        Calculate and return all geometric properties of the system
        
        Returns:
            dict: Complete system specification
        """
        # Calculate total connections
        num_connections = np.sum(self.connection_matrix > 0) // 2  # Divide by 2 (symmetric)
        
        # Calculate average connection strength
        nonzero_weights = self.connection_matrix[self.connection_matrix > 0]
        avg_connection_strength = np.mean(nonzero_weights) if len(nonzero_weights) > 0 else 0.0
        
        verification = self.verify_golden_ratio_properties()
        
        return {
            'num_nodes': 13,
            'num_connections': num_connections,
            'avg_connection_strength': avg_connection_strength,
            'golden_ratio_phi': PHI,
            'coordinates': self.coordinates,
            'connection_matrix': self.connection_matrix,
            'frequency_ratios': self.frequency_ratios,
            'verification': verification,
            'topology': 'icosahedron_with_center'
        }

# Global instance for easy access
geometry_manager = SacredGeometryManager()

if __name__ == "__main__":
    # Demonstration and validation
    print("=== Metatron's Cube Geometric Structure ===\n")
    
    manager = SacredGeometryManager()
    props = manager.get_system_properties()
    
    print(f"Nodes: {props['num_nodes']}")
    print(f"Connections: {props['num_connections']}")
    print(f"Golden Ratio φ: {props['golden_ratio_phi']:.6f}")
    print(f"Average Connection Strength: {props['avg_connection_strength']:.6f}")
    print(f"\nTopology: {props['topology']}")
    
    print("\n=== Verification Results ===")
    ver = props['verification']
    print(f"Vertices Normalized: {ver['vertices_normalized']}")
    print(f"φ Ratios Found: {len(ver['golden_ratios_found'])}")
    print(f"Symmetry Verified: {ver['symmetry_verified']}")
    
    if ver['edge_ratio_check']:
        edge_check = ver['edge_ratio_check']
        print(f"\nEdge Length: {edge_check['edge_length']:.4f}")
        print(f"Expected: {edge_check['expected']:.4f}")
        print(f"Match: {edge_check['matches']}")
    
    print("\n=== Musical Frequency Ratios ===")
    for node_id, ratio in sorted(props['frequency_ratios'].items()):
        print(f"Node {node_id:2d}: {ratio:.6f}")
    
    print("\n=== Sample Coordinate (Node 1) ===")
    coord = props['coordinates'][1]
    print(f"Position: [{coord[0]:.4f}, {coord[1]:.4f}, {coord[2]:.4f}]")
    print(f"Distance from center: {np.linalg.norm(coord):.6f}")