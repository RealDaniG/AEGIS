#!/usr/bin/env python3
"""
Simple WebSocket test for the Unified API
"""

import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8005/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")
            
            # Receive a message
            message = await websocket.recv()
            print("✅ Received message from server")
            
            # Parse the message
            data = json.loads(message)
            print(f"✅ Parsed message: {list(data.keys())}")
            
            # Close the connection
            await websocket.close()
            print("✅ Connection closed")
            
            return True
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Simple WebSocket Test ===")
    result = asyncio.run(test_websocket())
    if result:
        print("🎉 WebSocket test passed!")
    else:
        print("❌ WebSocket test failed!")