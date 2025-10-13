import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8004/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            
            # Wait for a few messages
            for i in range(10):
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Message {i+1}: C={data['consciousness']['level']:.4f}, Φ={data['consciousness']['phi']:.4f}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())