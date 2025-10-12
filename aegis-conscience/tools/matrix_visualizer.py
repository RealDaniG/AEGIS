"""
Matrix Visualizer for AEGIS-Conscience Network
Visualizes the connection matrix between all nodes in the network
"""

import json
import time
from typing import Dict, List, Set
import argparse


class MatrixVisualizer:
    """Visualizes the connection matrix between nodes"""
    
    def __init__(self):
        self.connection_matrix: Dict[str, Set[str]] = {}
        self.node_statuses: Dict[str, str] = {}
        self.node_info: Dict[str, Dict] = {}
    
    def load_matrix_data(self, data: Dict):
        """Load matrix data from network topology information"""
        self.connection_matrix = {}
        self.node_statuses = {}
        self.node_info = {}
        
        # Parse connection matrix
        matrix_data = data.get('connection_matrix', {})
        for node_id, connections in matrix_data.items():
            self.connection_matrix[node_id] = set(connections)
        
        # Parse node information
        nodes_data = data.get('known_nodes', {})
        for node_id, node_data in nodes_data.items():
            self.node_info[node_id] = node_data
            self.node_statuses[node_id] = node_data.get('status', 'unknown')
    
    def load_from_file(self, filepath: str):
        """Load matrix data from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.load_matrix_data(data)
            print(f"✅ Loaded matrix data from {filepath}")
        except Exception as e:
            print(f"❌ Error loading matrix data: {e}")
    
    def visualize_matrix(self):
        """Visualize the connection matrix as a text-based diagram"""
        if not self.connection_matrix:
            print("No matrix data available")
            return
        
        print("\n" + "="*80)
        print("AEGIS-CONSCIENCE NETWORK - CONNECTION MATRIX")
        print("="*80)
        
        # Get all node IDs
        all_nodes = sorted(list(self.connection_matrix.keys()))
        
        if not all_nodes:
            print("No nodes in the network")
            return
        
        # Print header
        print(f"{'Node':<15}", end="")
        for node_id in all_nodes:
            # Truncate long node IDs for display
            display_id = node_id[:12] + "..." if len(node_id) > 15 else node_id
            print(f"{display_id:<15}", end="")
        print()
        print("-" * (15 + 15 * len(all_nodes)))
        
        # Print connection matrix
        for row_node in all_nodes:
            # Truncate long node IDs for display
            display_id = row_node[:12] + "..." if len(row_node) > 15 else row_node
            print(f"{display_id:<15}", end="")
            
            for col_node in all_nodes:
                if row_node == col_node:
                    # Node connecting to itself (always connected)
                    print(f"{'●':<15}", end="")
                elif col_node in self.connection_matrix.get(row_node, set()):
                    # Connected
                    print(f"{'✓':<15}", end="")
                else:
                    # Not connected
                    print(f"{'✗':<15}", end="")
            print()
        
        # Print node status legend
        print("\n" + "-"*50)
        print("Node Status Legend:")
        print("● = Self")
        print("✓ = Connected")
        print("✗ = Not Connected")
        
        # Print detailed node information
        print("\n" + "-"*50)
        print("Node Details:")
        for node_id in all_nodes:
            status = self.node_statuses.get(node_id, 'unknown')
            connections = len(self.connection_matrix.get(node_id, set()))
            total_nodes = len(all_nodes)
            connectivity = (connections / (total_nodes - 1) * 100) if total_nodes > 1 else 100
            
            print(f"  {node_id[:30]:<30} | Status: {status:<10} | Connections: {connections:>2}/{total_nodes-1} ({connectivity:>5.1f}%)")
        
        print("="*80)
    
    def get_network_statistics(self) -> Dict:
        """Get network statistics"""
        if not self.connection_matrix:
            return {}
        
        all_nodes = list(self.connection_matrix.keys())
        total_nodes = len(all_nodes)
        
        if total_nodes == 0:
            return {}
        
        # Calculate connectivity statistics
        total_possible_connections = total_nodes * (total_nodes - 1)  # Directed graph
        actual_connections = sum(len(connections) for connections in self.connection_matrix.values())
        
        # Calculate connectivity percentage
        connectivity_percentage = (actual_connections / total_possible_connections * 100) if total_possible_connections > 0 else 0
        
        # Find most/least connected nodes
        connection_counts = {node: len(connections) for node, connections in self.connection_matrix.items()}
        most_connected = max(connection_counts, key=connection_counts.get) if connection_counts else None
        least_connected = min(connection_counts, key=connection_counts.get) if connection_counts else None
        
        return {
            'total_nodes': total_nodes,
            'total_possible_connections': total_possible_connections,
            'actual_connections': actual_connections,
            'connectivity_percentage': connectivity_percentage,
            'most_connected_node': most_connected,
            'most_connected_count': connection_counts.get(most_connected, 0) if most_connected else 0,
            'least_connected_node': least_connected,
            'least_connected_count': connection_counts.get(least_connected, 0) if least_connected else 0
        }
    
    def print_statistics(self):
        """Print network statistics"""
        stats = self.get_network_statistics()
        if not stats:
            print("No statistics available")
            return
        
        print("\n" + "="*60)
        print("NETWORK STATISTICS")
        print("="*60)
        print(f"Total Nodes:                 {stats['total_nodes']}")
        print(f"Total Possible Connections:  {stats['total_possible_connections']}")
        print(f"Actual Connections:          {stats['actual_connections']}")
        print(f"Network Connectivity:        {stats['connectivity_percentage']:.2f}%")
        
        if stats['most_connected_node']:
            print(f"Most Connected Node:         {stats['most_connected_node'][:30]} ({stats['most_connected_count']} connections)")
        
        if stats['least_connected_node']:
            print(f"Least Connected Node:        {stats['least_connected_node'][:30]} ({stats['least_connected_count']} connections)")
        
        print("="*60)


def main():
    """Main function for matrix visualization"""
    parser = argparse.ArgumentParser(description="Visualize AEGIS-Conscience Network Connection Matrix")
    parser.add_argument("--file", "-f", help="Path to matrix data JSON file")
    parser.add_argument("--stats", "-s", action="store_true", help="Show network statistics only")
    
    args = parser.parse_args()
    
    # Create visualizer
    visualizer = MatrixVisualizer()
    
    # Load data
    if args.file:
        visualizer.load_from_file(args.file)
    else:
        # Try to load from default location
        default_files = [
            "./matrix_data.json",
            "./data/matrix_data.json",
            "./network/matrix_data.json"
        ]
        
        loaded = False
        for filepath in default_files:
            try:
                visualizer.load_from_file(filepath)
                loaded = True
                break
            except:
                continue
        
        if not loaded:
            print("⚠️  No matrix data file specified and no default files found")
            print("Please provide a matrix data file using --file option")
            return
    
    # Display visualization
    if not args.stats:
        visualizer.visualize_matrix()
    
    # Display statistics
    visualizer.print_statistics()


# Example matrix data generator
def generate_example_matrix():
    """Generate example matrix data for testing"""
    example_data = {
        "total_nodes": 5,
        "local_node_id": "node-1",
        "local_connections": 4,
        "connection_matrix": {
            "node-1": ["node-2", "node-3", "node-4", "node-5"],
            "node-2": ["node-1", "node-3", "node-4"],
            "node-3": ["node-1", "node-2", "node-5"],
            "node-4": ["node-1", "node-2"],
            "node-5": ["node-1", "node-3"]
        },
        "known_nodes": {
            "node-1": {
                "node_id": "node-1",
                "ip_address": "192.168.1.10",
                "port": 8080,
                "public_key": "key1",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["node-2", "node-3", "node-4", "node-5"]
            },
            "node-2": {
                "node_id": "node-2",
                "ip_address": "192.168.1.11",
                "port": 8080,
                "public_key": "key2",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["node-1", "node-3", "node-4"]
            },
            "node-3": {
                "node_id": "node-3",
                "ip_address": "192.168.1.12",
                "port": 8080,
                "public_key": "key3",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["node-1", "node-2", "node-5"]
            },
            "node-4": {
                "node_id": "node-4",
                "ip_address": "192.168.1.13",
                "port": 8080,
                "public_key": "key4",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["node-1", "node-2"]
            },
            "node-5": {
                "node_id": "node-5",
                "ip_address": "192.168.1.14",
                "port": 8080,
                "public_key": "key5",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["node-1", "node-3"]
            }
        }
    }
    
    # Save example data
    with open("./example_matrix_data.json", "w") as f:
        json.dump(example_data, f, indent=2)
    
    print("✅ Example matrix data saved to ./example_matrix_data.json")
    return example_data


if __name__ == "__main__":
    # Check if we want to generate example data
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-example":
        generate_example_matrix()
    else:
        main()