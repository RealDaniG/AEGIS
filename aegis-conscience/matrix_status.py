"""
Simple Matrix Status Checker for AEGIS-Conscience Network
"""

import json
import os
import sys

def check_matrix_status(filepath="./matrix_data.json"):
    """Check and display the current matrix status"""
    try:
        # Load matrix data
        if not os.path.exists(filepath):
            print(f"❌ Matrix data file not found: {filepath}")
            print("Run generate_matrix_example.py to create example data")
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        print("🔍 AEGIS-Conscience Network Matrix Status")
        print("=" * 50)
        
        # Display basic info
        total_nodes = data.get('total_nodes', 0)
        local_node = data.get('local_node_id', 'Unknown')
        local_connections = data.get('local_connections', 0)
        
        print(f"Total Nodes: {total_nodes}")
        print(f"Local Node: {local_node}")
        print(f"Local Connections: {local_connections}/{total_nodes-1 if total_nodes > 1 else 0}")
        
        if total_nodes > 0:
            connectivity = (local_connections / (total_nodes - 1)) * 100 if total_nodes > 1 else 100
            print(f"Connectivity: {connectivity:.1f}%")
        
        # Display connection matrix
        print("\n🔗 Connection Matrix:")
        matrix = data.get('connection_matrix', {})
        if matrix:
            # Get all nodes
            all_nodes = sorted(list(matrix.keys()))
            
            # Print header
            print(f"{'Node':<15}", end="")
            for node in all_nodes:
                print(f"{node[:12]:<15}", end="")
            print()
            
            # Print connections
            for row_node in all_nodes:
                print(f"{row_node[:12]:<15}", end="")
                for col_node in all_nodes:
                    if row_node == col_node:
                        print(f"{'●':<15}", end="")
                    elif col_node in matrix.get(row_node, []):
                        print(f"{'[OK]':<15}", end="")
                    else:
                        print(f"{'✗':<15}", end="")
                print()
        else:
            print("No connection matrix data available")
        
        # Display node details
        print("\n📋 Node Details:")
        nodes = data.get('known_nodes', {})
        for node_id, node_info in nodes.items():
            status = node_info.get('status', 'unknown')
            connections = len(matrix.get(node_id, []))
            print(f"  {node_id[:20]:<20} | Status: {status:<10} | Connections: {connections}")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error checking matrix status: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check AEGIS-Conscience Network Matrix Status")
    parser.add_argument("--file", "-f", default="./matrix_data.json", 
                       help="Path to matrix data JSON file")
    
    args = parser.parse_args()
    
    check_matrix_status(args.file)

if __name__ == "__main__":
    main()