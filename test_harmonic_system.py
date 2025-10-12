#!/usr/bin/env python3
"""
Test script to verify the Harmonic Orchestrator Monitoring System
"""

import sys
import os
import time
import json
import requests
import websocket

def test_web_server():
    """Test if the web server is running"""
    try:
        response = requests.get("http://localhost:8003", timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running")
            return True
        else:
            print(f"❌ Web server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Web server is not accessible")
        return False
    except Exception as e:
        print(f"❌ Error testing web server: {e}")
        return False

def test_api_server():
    """Test if the API server is running"""
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API server is not accessible")
        return False
    except Exception as e:
        print(f"❌ Error testing API server: {e}")
        return False

def test_websocket_connection():
    """Test WebSocket connection to the unified API"""
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:8005/ws")
        print("✅ WebSocket connection established")
        
        # Try to receive a message
        try:
            result = ws.recv()
            print("✅ WebSocket data received")
            data = json.loads(result)
            print(f"   Sample data keys: {list(data.keys())}")
        except websocket.WebSocketTimeoutException:
            print("⚠️  No data received within timeout")
        except Exception as e:
            print(f"⚠️  Error receiving data: {e}")
        
        ws.close()
        return True
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("=== Harmonic Orchestrator Monitoring System Test ===\n")
    
    # Test web server
    print("1. Testing Web Server (Port 8003)...")
    web_server_ok = test_web_server()
    
    # Test API server
    print("\n2. Testing API Server (Port 8005)...")
    api_server_ok = test_api_server()
    
    # Test WebSocket connection
    print("\n3. Testing WebSocket Connection...")
    websocket_ok = test_websocket_connection()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Web Server:     {'✅ PASS' if web_server_ok else '❌ FAIL'}")
    print(f"API Server:     {'✅ PASS' if api_server_ok else '❌ FAIL'}")
    print(f"WebSocket:      {'✅ PASS' if websocket_ok else '❌ FAIL'}")
    
    if web_server_ok and api_server_ok and websocket_ok:
        print("\n🎉 All tests passed! The Harmonic Orchestrator Monitoring System is ready.")
        print("\nAccess the dashboard at: http://localhost:8003")
        print("Connect via WebSocket: ws://localhost:8005/ws")
        return True
    else:
        print("\n❌ Some tests failed. Please check the system setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)