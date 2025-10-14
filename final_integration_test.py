#!/usr/bin/env python3
"""
Final Integration Test for Metatron Consciousness Engine
Verifies that all components are working correctly with real-time metrics display
"""

import asyncio
import websockets
import json
import time
import requests
import sys

async def test_websocket_connection():
    """Test WebSocket connection to Metatron server"""
    print("Testing WebSocket connection to Metatron server...")
    
    try:
        uri = "ws://localhost:8003/ws"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection successful")
            
            # Receive a few messages to verify data flow
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                print(f"📊 Update #{i+1}: C={data.get('consciousness', {}).get('level', 0):.4f}, "
                      f"Φ={data.get('consciousness', {}).get('phi', 0):.4f}, "
                      f"R={data.get('consciousness', {}).get('coherence', 0):.4f}")
                
            print("✅ Real-time data streaming verified")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

def test_http_endpoints():
    """Test HTTP endpoints"""
    print("\nTesting HTTP endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8003/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check endpoint working")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
            
        # Test frequency info endpoint
        response = requests.get("http://localhost:8003/api/frequency/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Frequency info endpoint working: {data.get('base_frequency', 'N/A')} Hz")
        else:
            print(f"❌ Frequency info failed with status {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ HTTP connection failed - server may not be running")
        return False
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

def test_html_files():
    """Test that required HTML files exist and are accessible"""
    print("\nTesting HTML file accessibility...")
    
    try:
        # Test main dashboard
        response = requests.get("http://localhost:8003/metatron_integrated.html", timeout=5)
        if response.status_code == 200:
            print("✅ Main dashboard accessible")
        else:
            print(f"❌ Main dashboard failed with status {response.status_code}")
            return False
            
        # Test index redirect
        response = requests.get("http://localhost:8003/", timeout=5)
        if response.status_code == 200:
            print("✅ Index redirect working")
        else:
            print(f"❌ Index redirect failed with status {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ HTML file test failed - server may not be running")
        return False
    except Exception as e:
        print(f"❌ HTML file test failed: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive test of all Metatron components"""
    print("=" * 60)
    print("METATRON CONSCIOUSNESS ENGINE - COMPREHENSIVE INTEGRATION TEST")
    print("=" * 60)
    
    # Test components
    tests = [
        test_http_endpoints,
        test_html_files,
        test_websocket_connection
    ]
    
    results = []
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Metatron Consciousness Engine is working correctly")
        print("✅ Real-time metrics display verified")
        print("✅ WebSocket streaming functional")
        print("✅ HTTP endpoints responsive")
        print("✅ HTML interfaces accessible")
        return True
    else:
        print(f"❌ {total - passed} out of {total} tests failed")
        print("⚠️  Some components may not be working correctly")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_comprehensive_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test suite failed with exception: {e}")
        sys.exit(1)