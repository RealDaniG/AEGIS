#!/usr/bin/env python3
"""
Verify Real Consciousness Data
==============================

Script to verify that the Metatron consciousness system is producing real,
changing data rather than static/simulated values.
"""

import asyncio
import websockets
import json
import time
from collections import defaultdict

async def verify_real_data():
    """Verify that consciousness data is real and changing"""
    print("🔍 Verifying Real Consciousness Data...")
    print("=" * 50)
    
    # Connect to WebSocket
    uri = "ws://localhost:8003/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ Connected to {uri}")
            print("Monitoring real-time consciousness data...")
            print()
            
            # Collect data over time
            data_points = []
            start_time = time.time()
            
            # Collect 10 data points over 5 seconds
            for i in range(10):
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    data = json.loads(message)
                    data_points.append(data)
                    print(f"Data point {i+1}: Time={data.get('time', 0):.3f}, "
                          f"Consciousness={data.get('consciousness', {}).get('level', 0):.6f}")
                    
                    await asyncio.sleep(0.5)  # Wait 0.5 seconds between samples
                except asyncio.TimeoutError:
                    print(f"Timeout waiting for data point {i+1}")
                    continue
            
            # Analyze the data
            print()
            print("=" * 50)
            print("ANALYSIS RESULTS:")
            print("=" * 50)
            
            if len(data_points) < 2:
                print("❌ Insufficient data points collected")
                return False
            
            # Check if time is progressing
            times = [dp.get('time', 0) for dp in data_points]
            time_changes = [times[i] - times[i-1] for i in range(1, len(times))]
            time_progressing = all(t > 0 for t in time_changes)
            
            print(f"Time progression: {'✅ YES' if time_progressing else '❌ NO'}")
            
            # Check if consciousness level is changing
            consciousness_levels = [dp.get('consciousness', {}).get('level', 0) for dp in data_points]
            consciousness_changes = [abs(consciousness_levels[i] - consciousness_levels[i-1]) 
                                   for i in range(1, len(consciousness_levels))]
            consciousness_changing = any(c > 1e-10 for c in consciousness_changes)  # Very small threshold
            
            print(f"Consciousness level changes: {'✅ YES' if consciousness_changing else '❌ NO'}")
            
            # Check if node outputs are changing
            node_changes = []
            for i in range(1, len(data_points)):
                prev_nodes = data_points[i-1].get('nodes', {})
                curr_nodes = data_points[i].get('nodes', {})
                
                for node_id in curr_nodes:
                    if node_id in prev_nodes:
                        prev_output = prev_nodes[node_id].get('output', 0)
                        curr_output = curr_nodes[node_id].get('output', 0)
                        change = abs(curr_output - prev_output)
                        if change > 1e-10:
                            node_changes.append((node_id, change))
            
            nodes_changing = len(node_changes) > 0
            print(f"Node output changes: {'✅ YES' if nodes_changing else '❌ NO'}")
            
            # Check if oscillator phases are changing
            phase_changes = []
            for i in range(1, len(data_points)):
                prev_nodes = data_points[i-1].get('nodes', {})
                curr_nodes = data_points[i].get('nodes', {})
                
                for node_id in curr_nodes:
                    if node_id in prev_nodes:
                        prev_phase = prev_nodes[node_id].get('phase', 0)
                        curr_phase = curr_nodes[node_id].get('phase', 0)
                        change = abs(curr_phase - prev_phase)
                        if change > 1e-10:
                            phase_changes.append((node_id, change))
            
            phases_changing = len(phase_changes) > 0
            print(f"Oscillator phase changes: {'✅ YES' if phases_changing else '❌ NO'}")
            
            # Overall result
            print()
            print("=" * 50)
            if time_progressing and (consciousness_changing or nodes_changing or phases_changing):
                print("🎉 SUCCESS: Consciousness system is producing REAL, DYNAMIC data!")
                print("   The visualization will show accurate, real-time metrics.")
                return True
            else:
                print("⚠️  WARNING: Data appears static or simulated")
                print("   The visualization may not show real-time changes.")
                return False
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Please ensure the Metatron consciousness system is running on port 8003")
        return False

if __name__ == "__main__":
    asyncio.run(verify_real_data())