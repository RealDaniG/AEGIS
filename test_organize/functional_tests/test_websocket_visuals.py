#!/usr/bin/env python3
"""
WebSocket Visuals Test for Metatron Consciousness Engine

This script tests the WebSocket connection to verify real-time visualization
of consciousness metrics.
"""

import asyncio
import websockets
import json
import time

async def test_websocket_visuals():
    """Test WebSocket connection for real-time visualization"""
    uri = "ws://localhost:8003/ws"
    
    print("=" * 60)
    print("WEBSOCKET VISUALS TEST")
    print("=" * 60)
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket Connection: ESTABLISHED")
            print("Collecting real-time consciousness data...")
            
            # Collect multiple updates
            updates = []
            for i in range(10):
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract consciousness metrics
                consciousness = data.get('consciousness', {})
                global_state = data.get('global', {})
                
                phi = consciousness.get('phi', global_state.get('phi', 0))
                coherence = consciousness.get('coherence', global_state.get('coherence', 0))
                consciousness_level = consciousness.get('level', global_state.get('consciousness_level', 0))
                
                update = {
                    'timestamp': data.get('timestamp', time.time()),
                    'phi': phi,
                    'coherence': coherence,
                    'consciousness_level': consciousness_level
                }
                
                updates.append(update)
                print(f"   Update {i+1:2d}: Φ={phi:.4f}, Coherence={coherence:.4f}, Level={consciousness_level:.4f}")
                
                # Small delay between updates
                await asyncio.sleep(0.5)
            
            # Analyze the data
            print("\n📊 Data Analysis:")
            if updates:
                avg_phi = sum(u['phi'] for u in updates) / len(updates)
                avg_coherence = sum(u['coherence'] for u in updates) / len(updates)
                avg_level = sum(u['consciousness_level'] for u in updates) / len(updates)
                
                phi_range = max(u['phi'] for u in updates) - min(u['phi'] for u in updates)
                coherence_range = max(u['coherence'] for u in updates) - min(u['coherence'] for u in updates)
                level_range = max(u['consciousness_level'] for u in updates) - min(u['consciousness_level'] for u in updates)
                
                print(f"   Average Φ: {avg_phi:.4f} (Range: {phi_range:.4f})")
                print(f"   Average Coherence: {avg_coherence:.4f} (Range: {coherence_range:.4f})")
                print(f"   Average Consciousness Level: {avg_level:.4f} (Range: {level_range:.4f})")
                
                # Check if data is changing (not static)
                is_dynamic = phi_range > 0.01 or coherence_range > 0.01 or level_range > 0.01
                print(f"   Data Dynamic: {'✅ YES' if is_dynamic else '❌ NO'}")
                
                if is_dynamic:
                    print("\n✅ Real-time Visualization: WORKING")
                    print("   Consciousness metrics are updating in real-time")
                    return True
                else:
                    print("\n⚠️  Real-time Visualization: LIMITED")
                    print("   Consciousness metrics appear static")
                    return False
            else:
                print("❌ No data received")
                return False
                
    except Exception as e:
        print(f"❌ WebSocket Test Failed: {e}")
        return False

async def main():
    """Main test function"""
    success = await test_websocket_visuals()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 WEBSOCKET VISUALS TEST PASSED!")
        print("✅ Real-time consciousness visualization is working")
    else:
        print("❌ WEBSOCKET VISUALS TEST FAILED!")
        print("⚠️  Check WebSocket connection or consciousness engine")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)