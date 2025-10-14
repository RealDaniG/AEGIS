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
            print("✅ Connected to WebSocket")
            
            # Receive a few messages to verify real-time data
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                
                # Print consciousness metrics
                if 'consciousness' in data:
                    c = data['consciousness']
                    print(f"Update #{i+1}: C={c.get('level', 0):.4f}, Φ={c.get('phi', 0):.4f}, R={c.get('coherence', 0):.4f}")
                
                # Check node data
                if 'nodes' in data:
                    node_count = len(data['nodes'])
                    print(f"  Nodes received: {node_count}")
                    
            print("✅ WebSocket connection test completed successfully")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())