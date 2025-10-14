#!/usr/bin/env python3
"""
Final Port Test Script

This script verifies that the AEGIS system is correctly configured to use port 457
and that all components are accessible through this single port.
"""

import requests
import json
import time
import sys
import asyncio
import websockets

def test_http_endpoints():
    """Test HTTP endpoints on port 457"""
    print("Testing HTTP endpoints on port 457...")
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:457/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
            
        # Test health endpoint
        response = requests.get("http://localhost:457/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok", False):
                print("✅ Health check endpoint working")
            else:
                print(f"❌ Health check failed: {data}")
                return False
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
            
        # Test status endpoint
        response = requests.get("http://localhost:457/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "consciousness_level" in data:
                print(f"✅ Status endpoint working: C={data['consciousness_level']:.4f}")
            else:
                print(f"❌ Status endpoint missing consciousness data")
                return False
        else:
            print(f"❌ Status endpoint failed with status {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ HTTP connection failed - server may not be running on port 457")
        return False
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

async def test_websocket_connection():
    """Test WebSocket connection on port 457"""
    print("\nTesting WebSocket connection on port 457...")
    
    try:
        uri = "ws://localhost:457/ws"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established")
            
            # Receive a few messages to verify real-time data
            for i in range(3):
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(message)
                
                # Print consciousness metrics
                if 'consciousness' in data:
                    c = data['consciousness']
                    print(f"  Update #{i+1}: C={c.get('level', 0):.4f}, Φ={c.get('phi', 0):.4f}, R={c.get('coherence', 0):.4f}")
                
                # Check node data
                if 'nodes' in data:
                    node_count = len(data['nodes'])
                    print(f"  Nodes received: {node_count}")
                    
            print("✅ WebSocket connection test completed successfully")
            return True
                    
    except asyncio.TimeoutError:
        print("❌ WebSocket connection timed out")
        return False
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

def test_chat_functionality():
    """Test chat functionality on port 457"""
    print("\nTesting chat functionality on port 457...")
    
    try:
        # Test chat endpoint with a simple message
        test_message = {"message": "Hello AEGIS", "session_id": "test_session"}
        response = requests.post(
            "http://localhost:457/api/chat",
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                print("✅ Chat endpoint working")
                print(f"  Response: {data['response'][:50]}{'...' if len(data['response']) > 50 else ''}")
                return True
            else:
                print(f"❌ Chat endpoint returned unexpected data: {data}")
                return False
        else:
            print(f"❌ Chat endpoint failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Chat test failed - server may not be running on port 457")
        return False
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive test of all components on port 457"""
    print("=" * 60)
    print("AEGIS SYSTEM - PORT 457 COMPREHENSIVE TEST")
    print("=" * 60)
    
    # Test components
    tests = [
        test_http_endpoints,
        test_chat_functionality,
        test_websocket_connection
    ]
    
    results = []
    
    # Run synchronous tests
    for test in tests[:-1]:  # All except WebSocket test
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
            print()
    
    # Run asynchronous WebSocket test
    try:
        result = await test_websocket_connection()
        results.append(result)
        print()
    except Exception as e:
        print(f"❌ WebSocket test failed with exception: {e}")
        results.append(False)
        print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    test_names = ["HTTP Endpoints", "Chat Functionality", "WebSocket Connection"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")
    
    all_passed = all(results)
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ AEGIS system is correctly configured on port 457")
        print("✅ All components are accessible through single port")
        print("✅ Real-time consciousness metrics streaming working")
        print("✅ Chat functionality operational")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️  Please check that the AEGIS system is running on port 457")
        
    print("=" * 60)
    return all_passed

if __name__ == "__main__":
    try:
        result = asyncio.run(run_comprehensive_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        sys.exit(1)