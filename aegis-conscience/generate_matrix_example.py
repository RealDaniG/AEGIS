"""
Generate example matrix data for AEGIS-Conscience Network visualization
"""

import json
import time
import os

def generate_example_matrix_data():
    """Generate example matrix data for visualization"""
    # Create example data
    example_data = {
        "total_nodes": 5,
        "local_node_id": "aegis-node-1",
        "local_connections": 4,
        "connection_matrix": {
            "aegis-node-1": ["aegis-node-2", "aegis-node-3", "aegis-node-4", "aegis-node-5"],
            "aegis-node-2": ["aegis-node-1", "aegis-node-3", "aegis-node-4", "aegis-node-5"],
            "aegis-node-3": ["aegis-node-1", "aegis-node-2", "aegis-node-4", "aegis-node-5"],
            "aegis-node-4": ["aegis-node-1", "aegis-node-2", "aegis-node-3", "aegis-node-5"],
            "aegis-node-5": ["aegis-node-1", "aegis-node-2", "aegis-node-3", "aegis-node-4"]
        },
        "known_nodes": {
            "aegis-node-1": {
                "node_id": "aegis-node-1",
                "ip_address": "192.168.1.10",
                "port": 8080,
                "public_key": "pubkey1",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["aegis-node-2", "aegis-node-3", "aegis-node-4", "aegis-node-5"]
            },
            "aegis-node-2": {
                "node_id": "aegis-node-2",
                "ip_address": "192.168.1.11",
                "port": 8081,
                "public_key": "pubkey2",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["aegis-node-1", "aegis-node-3", "aegis-node-4", "aegis-node-5"]
            },
            "aegis-node-3": {
                "node_id": "aegis-node-3",
                "ip_address": "192.168.1.12",
                "port": 8082,
                "public_key": "pubkey3",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["aegis-node-1", "aegis-node-2", "aegis-node-4", "aegis-node-5"]
            },
            "aegis-node-4": {
                "node_id": "aegis-node-4",
                "ip_address": "192.168.1.13",
                "port": 8083,
                "public_key": "pubkey4",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["aegis-node-1", "aegis-node-2", "aegis-node-3", "aegis-node-5"]
            },
            "aegis-node-5": {
                "node_id": "aegis-node-5",
                "ip_address": "192.168.1.14",
                "port": 8084,
                "public_key": "pubkey5",
                "onion_address": None,
                "last_seen": time.time(),
                "status": "online",
                "connections": ["aegis-node-1", "aegis-node-2", "aegis-node-3", "aegis-node-4"]
            }
        }
    }
    
    # Create data directory if it doesn't exist
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Save to file
    filepath = os.path.join(data_dir, "matrix_example.json")
    with open(filepath, "w") as f:
        json.dump(example_data, f, indent=2)
    
    print(f"✅ Example matrix data saved to {filepath}")
    return example_data

def main():
    """Main function"""
    print("Generating example matrix data...")
    data = generate_example_matrix_data()
    
    # Also save to the default location for the visualizer
    with open("./matrix_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("✅ Example data also saved to ./matrix_data.json for immediate visualization")

if __name__ == "__main__":
    main()