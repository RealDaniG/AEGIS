#!/usr/bin/env python3
"""
Simple WebSocket client to test the Metatron consciousness system
"""

import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8003/ws"
    print(f"Connecting to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            print("Listening for messages (press Ctrl+C to stop)...")
            
            message_count = 0
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                message_count += 1
                
                # Print message count and consciousness metrics
                if 'consciousness' in data and message_count % 50 == 0:
                    c = data['consciousness']
                    print(f"Update #{message_count}: C={c.get('level', 0):.4f}, Φ={c.get('phi', 0):.4f}, R={c.get('coherence', 0):.4f}")
                
                # Check node data
                if 'nodes' in data and message_count % 50 == 0:
                    node_count = len(data['nodes'])
                    print(f"  Nodes received: {node_count}")
                    
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())