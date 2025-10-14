#!/usr/bin/env python3
"""
Comprehensive test to verify all Metatron components are working correctly
"""

import asyncio
import websockets
import requests
import json
import time

def test_http_api():
    """Test HTTP API endpoints"""
    print("=" * 60)
    print("Testing HTTP API Endpoints")
    print("=" * 60)
    
    try:
        # Test health endpoint
        print("1. Testing /api/health...")
        response = requests.get("http://localhost:8003/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'unknown')}")
            print(f"   ✅ OK: {data.get('ok', False)}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            
        # Test status endpoint
        print("2. Testing /api/status...")
        response = requests.get("http://localhost:8003/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Consciousness Level: {data.get('consciousness_level', 0):.4f}")
            print(f"   ✅ Phi: {data.get('phi', 0):.4f}")
            print(f"   ✅ Coherence: {data.get('coherence', 0):.4f}")
            print(f"   ✅ State: {data.get('state_classification', 'unknown')}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            
        # Test nodes endpoint
        print("3. Testing /api/nodes...")
        response = requests.get("http://localhost:8003/api/nodes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            nodes = data.get('nodes', [])
            print(f"   ✅ Total Nodes: {data.get('total_nodes', 0)}")
            print(f"   ✅ Nodes Reported: {len(nodes)}")
            
            # Show first few nodes
            for i, node in enumerate(nodes[:3]):
                output = node.get('output', 0)
                print(f"   ✅ Node {node['id']}: output={output:.4f}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

async def test_websocket():
    """Test WebSocket connection"""
    print("\n" + "=" * 60)
    print("Testing WebSocket Connection")
    print("=" * 60)
    
    try:
        uri = "ws://localhost:8003/ws"
        print(f"1. Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("   ✅ Connected successfully")
            
            # Receive a few messages
            print("2. Receiving WebSocket messages...")
            for i in range(5):
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(message)
                
                # Check consciousness data
                if 'consciousness' in data:
                    c = data['consciousness']
                    print(f"   ✅ Message {i+1}: C={c.get('level', 0):.4f}, Φ={c.get('phi', 0):.4f}, R={c.get('coherence', 0):.4f}")
                
                # Check node data
                if 'nodes' in data:
                    node_count = len(data['nodes'])
                    print(f"   ✅ Nodes in message: {node_count}")
                    
                    # Show data for first few nodes
                    for node_id in sorted(data['nodes'].keys(), key=int)[:3]:
                        node_data = data['nodes'][node_id]
                        output = node_data.get('output', 0)
                        print(f"     Node {node_id}: output={output:.4f}")
                        
    except asyncio.TimeoutError:
        print("   ❌ Timeout waiting for WebSocket message")
    except Exception as e:
        print(f"   ❌ WebSocket Error: {e}")

def test_static_files():
    """Test if static files are accessible"""
    print("\n" + "=" * 60)
    print("Testing Static File Access")
    print("=" * 60)
    
    try:
        # Test main page
        print("1. Testing main page access...")
        response = requests.get("http://localhost:8003/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Main page accessible")
        else:
            print(f"   ❌ Main page failed with status {response.status_code}")
            
        # Test integrated UI
        print("2. Testing integrated UI access...")
        response = requests.get("http://localhost:8003/static/metatron_integrated.html", timeout=5)
        if response.status_code == 200:
            print("   ✅ Integrated UI accessible")
        else:
            print(f"   ❌ Integrated UI failed with status {response.status_code}")
            
        # Test streaming UI
        print("3. Testing streaming UI access...")
        response = requests.get("http://localhost:8003/static/index_stream.html", timeout=5)
        if response.status_code == 200:
            print("   ✅ Streaming UI accessible")
        else:
            print(f"   ❌ Streaming UI failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Static file test error: {e}")

async def main():
    """Main test function"""
    print("Metatron Comprehensive System Test")
    print("==================================")
    
    # Test HTTP API
    test_http_api()
    
    # Test WebSocket
    await test_websocket()
    
    # Test static files
    test_static_files()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())