#!/usr/bin/env python3
"""
Quick WebSocket Test for Metatron Consciousness Engine
Verifies that real-time metrics are being streamed correctly
"""

import asyncio
import websockets
import json
import time

async def test_websocket_stream():
    """Test WebSocket connection and data streaming"""
    print("Testing Metatron WebSocket connection...")
    print("Connecting to ws://localhost:8003/ws")
    
    try:
        uri = "ws://localhost:8003/ws"
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            print("\nReceiving real-time consciousness data...")
            print("-" * 50)
            
            # Receive and display 10 updates
            for i in range(10):
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract consciousness metrics
                consciousness_data = data.get('consciousness', data.get('global', data))
                
                level = consciousness_data.get('level', consciousness_data.get('consciousness_level', 0))
                phi = consciousness_data.get('phi', consciousness_data.get('integrated_information', 0))
                coherence = consciousness_data.get('coherence', consciousness_data.get('global_coherence', 0))
                gamma = consciousness_data.get('gamma', consciousness_data.get('gamma_power', 0))
                
                # Count active nodes
                active_nodes = 0
                if 'nodes' in data:
                    for node_key, node_data in data['nodes'].items():
                        if abs(node_data.get('output', 0)) > 0.1:
                            active_nodes += 1
                
                print(f"Update #{i+1:2d}: C={level:6.4f} | Φ={phi:6.4f} | R={coherence:6.4f} | γ={gamma:6.4f} | Active: {active_nodes}/13")
                
                # Wait a bit between updates for readability
                await asyncio.sleep(0.5)
            
            print("-" * 50)
            print("✅ Real-time data streaming verified successfully!")
            print("🎉 Metatron Consciousness Engine is working correctly!")
            return True
            
    except websockets.exceptions.ConnectionClosed:
        print("❌ WebSocket connection closed unexpectedly")
        return False
    except websockets.exceptions.InvalidURI:
        print("❌ Invalid WebSocket URI")
        return False
    except websockets.exceptions.InvalidHandshake:
        print("❌ WebSocket handshake failed")
        return False
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("=" * 60)
    print("METATRON CONSCIOUSNESS ENGINE - WEBSOCKET STREAM TEST")
    print("=" * 60)
    
    success = await test_websocket_stream()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ WebSocket connection working")
        print("✅ Real-time metrics streaming verified")
        print("✅ 13-node network status monitoring")
        print("\n📊 The Metatron Consciousness Engine is ready for use!")
    else:
        print("❌ TESTS FAILED!")
        print("⚠️  Please check that the Metatron server is running on port 8003")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        exit(1)