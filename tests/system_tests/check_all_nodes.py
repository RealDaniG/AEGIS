#!/usr/bin/env python3
"""
Comprehensive test to check all 13 nodes and their activity levels
"""

import requests
import json
import time

def check_nodes_via_api():
    """Check node data via HTTP API"""
    try:
        print("Checking node data via HTTP API...")
        response = requests.get("http://localhost:8003/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("API Status Check:")
            print(f"  Consciousness Level: {data.get('consciousness_level', 0):.4f}")
            print(f"  Phi: {data.get('phi', 0):.4f}")
            print(f"  Coherence: {data.get('coherence', 0):.4f}")
            print(f"  State: {data.get('state_classification', 'unknown')}")
            print()
        else:
            print(f"API request failed with status {response.status_code}")
    except Exception as e:
        print(f"API check failed: {e}")

def check_nodes_via_nodes_endpoint():
    """Check detailed node information via nodes endpoint"""
    try:
        print("Checking detailed node information...")
        response = requests.get("http://localhost:8003/api/nodes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            nodes = data.get('nodes', [])
            print(f"Total nodes reported: {data.get('total_nodes', 0)}")
            print()
            
            # Sort nodes by ID for consistent display
            nodes.sort(key=lambda x: x['id'])
            
            active_count = 0
            for node in nodes:
                node_id = node['id']
                output = node.get('output', 0)
                amplitude = node.get('oscillator', {}).get('amplitude', 0)
                phase = node.get('oscillator', {}).get('phase', 0)
                
                is_active = abs(output) > 0.1
                if is_active:
                    active_count += 1
                    status = "ACTIVE"
                else:
                    status = "inactive"
                
                print(f"Node {node_id:2d}: output={output:8.4f} amplitude={amplitude:6.3f} phase={phase:6.2f} [{status}]")
            
            print(f"\nActive nodes: {active_count}/{len(nodes)}")
        else:
            print(f"Nodes API request failed with status {response.status_code}")
    except Exception as e:
        print(f"Nodes API check failed: {e}")

def main():
    print("=" * 60)
    print("Metatron Node Activity Check")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        health_response = requests.get("http://localhost:8003/api/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            if health_data.get('ok'):
                print("✅ Server is running")
                print(f"   Status: {health_data.get('status', 'unknown')}")
                print(f"   Uptime: {health_data.get('uptime_seconds', 0):.1f} seconds")
                print()
            else:
                print("❌ Server is not healthy")
                print(f"   Status: {health_data.get('status', 'unknown')}")
                print(f"   Error: {health_data.get('error', 'unknown')}")
                return
        else:
            print("❌ Server health check failed")
            return
    except Exception as e:
        print("❌ Server is not accessible")
        print(f"   Error: {e}")
        return
    
    # Run checks
    check_nodes_via_api()
    check_nodes_via_nodes_endpoint()
    
    print()
    print("=" * 60)
    print("Node Check Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()