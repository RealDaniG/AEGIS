#!/usr/bin/env python3
"""
Test script to verify that all 13 nodes are being sent from the backend
"""

import asyncio
import websockets
import json

async def test_node_data():
    uri = "ws://localhost:8003/ws"
    print(f"Connecting to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            print("Listening for node data (press Ctrl+C to stop)...")
            
            message_count = 0
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                message_count += 1
                
                # Print message count and consciousness metrics
                if 'consciousness' in data:
                    c = data['consciousness']
                    print(f"Update #{message_count}: C={c.get('level', 0):.4f}, Φ={c.get('phi', 0):.4f}, R={c.get('coherence', 0):.4f}")
                
                # Check node data
                if 'nodes' in data:
                    node_count = len(data['nodes'])
                    print(f"  Nodes received: {node_count}")
                    
                    # Print data for each node
                    for node_id in sorted(data['nodes'].keys(), key=int):
                        node_data = data['nodes'][node_id]
                        output = node_data.get('output', 0)
                        phase = node_data.get('phase', 0)
                        amplitude = node_data.get('amplitude', 0)
                        print(f"    Node {node_id}: output={output:.4f}, phase={phase:.2f}, amplitude={amplitude:.4f}")
                    
                    # Check if all 13 nodes are present
                    if node_count == 13:
                        print("  ✅ All 13 nodes present")
                    else:
                        print(f"  ❌ Expected 13 nodes, got {node_count}")
                        missing_nodes = set(map(str, range(13))) - set(data['nodes'].keys())
                        if missing_nodes:
                            print(f"  Missing nodes: {', '.join(sorted(missing_nodes))}")
                
                print()  # Empty line for readability
                
                # Stop after 20 messages to avoid too much output
                if message_count >= 20:
                    break
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_node_data())