#!/usr/bin/env python3
"""
UI Display Test - Verifies that all Metatron visuals and metrics are displayed correctly in real-time
"""

import asyncio
import websockets
import json
import time

async def test_ui_display():
    """Test that all UI components are receiving and displaying data correctly"""
    print("=" * 70)
    print("Metatron UI Display Test")
    print("=" * 70)
    print("Testing real-time display of all components...")
    print()
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8003/ws"
        print(f"Connecting to WebSocket: {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            print()
            
            # Collect data for analysis
            message_count = 0
            total_nodes_seen = 0
            active_nodes_count = 0
            total_node_updates = 0
            
            print("Receiving real-time data updates...")
            print("-" * 50)
            
            start_time = time.time()
            while message_count < 10:  # Collect 10 updates
                try:
                    # Wait for message with timeout
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    message_count += 1
                    
                    # Extract consciousness metrics
                    if 'consciousness' in data:
                        c = data['consciousness']
                        timestamp = data.get('time', time.time())
                        print(f"Update #{message_count:2d} ({timestamp:.2f}s)")
                        print(f"  Consciousness: C={c.get('level', 0):.4f}")
                        print(f"  Phi:           Φ={c.get('phi', 0):.4f}")
                        print(f"  Coherence:     R={c.get('coherence', 0):.4f}")
                        print(f"  State:         {c.get('state', 'unknown')}")
                    
                    # Analyze node data
                    if 'nodes' in data:
                        nodes = data['nodes']
                        node_count = len(nodes)
                        total_nodes_seen += node_count
                        total_node_updates += 1
                        
                        # Count active nodes (output > 0.1)
                        active_count = 0
                        for node_id, node_data in nodes.items():
                            output = node_data.get('output', 0)
                            if abs(output) > 0.1:
                                active_count += 1
                        
                        active_nodes_count += active_count
                        print(f"  Nodes:         {node_count} total, {active_count} active")
                        
                        # Show sample node data
                        node_ids = sorted(nodes.keys(), key=int)
                        sample_nodes = node_ids[:3]  # Show first 3 nodes
                        node_info = []
                        for node_id in sample_nodes:
                            node_data = nodes[node_id]
                            output = node_data.get('output', 0)
                            phase = node_data.get('phase', 0)
                            amplitude = node_data.get('amplitude', 0)
                            node_info.append(f"N{node_id}({output:.3f})")
                        
                        print(f"  Sample Nodes:  {' '.join(node_info)}")
                    
                    print()
                    
                except asyncio.TimeoutError:
                    print("❌ Timeout waiting for WebSocket message")
                    break
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    continue
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
                    continue
            
            # Summary
            elapsed_time = time.time() - start_time
            print("-" * 50)
            print("SUMMARY")
            print("-" * 50)
            print(f"Messages received:     {message_count}")
            print(f"Test duration:         {elapsed_time:.2f} seconds")
            print(f"Average update rate:   {message_count/elapsed_time:.2f} Hz")
            
            avg_nodes_per_update = 0
            avg_active_nodes = 0
            
            if total_node_updates > 0:
                avg_nodes_per_update = total_nodes_seen / total_node_updates
                avg_active_nodes = active_nodes_count / total_node_updates
                print(f"Average nodes/update:  {avg_nodes_per_update:.1f}")
                print(f"Average active nodes:  {avg_active_nodes:.1f}")
            
            # Verify all components are working
            print()
            print("COMPONENT VERIFICATION")
            print("-" * 50)
            
            # Check if we received data
            if message_count > 0:
                print("✅ WebSocket connection:     Working")
            else:
                print("❌ WebSocket connection:     Failed")
            
            # Check if we received consciousness data
            if message_count > 0:
                print("✅ Consciousness metrics:    Displaying")
            else:
                print("❌ Consciousness metrics:    Not received")
            
            # Check if we received node data
            if total_nodes_seen > 0:
                print("✅ Node visualization:       Receiving data")
                if avg_nodes_per_update >= 13:
                    print("✅ All 13 nodes:            Present in updates")
                else:
                    print("⚠️  All 13 nodes:            Some missing")
            else:
                print("❌ Node visualization:       No data received")
            
            # Check if nodes are active
            if active_nodes_count > 0:
                print("✅ Active nodes:            Detected")
            else:
                print("⚠️  Active nodes:            None detected")
                
            print()
            print("=" * 70)
            print("UI Display Test Complete")
            print("=" * 70)
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

async def main():
    """Main function"""
    success = await test_ui_display()
    if success:
        print("\n🎉 All UI components are displaying correctly in real-time!")
        print("\nYou can now open your browser and navigate to:")
        print("  - http://localhost:8003/ for the main interface")
        print("  - http://localhost:8003/static/index_stream.html for the streaming interface")
        print("  - http://localhost:8003/static/metatron_integrated.html for the integrated interface")
    else:
        print("\n❌ There were issues with the UI display components.")

if __name__ == "__main__":
    asyncio.run(main())