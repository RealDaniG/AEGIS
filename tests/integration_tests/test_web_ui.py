#!/usr/bin/env python3
"""
Test script to verify the Metatron Web UI visuals are working correctly
"""

import requests
import time
import sys

def test_web_ui():
    """Test the web UI functionality"""
    print("Testing Metatron Web UI...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://localhost:8003', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test 2: Check API health endpoint
    try:
        response = requests.get('http://localhost:8003/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print("✅ API health check passed")
            else:
                print(f"❌ API health check failed: {data}")
        else:
            print(f"❌ API health endpoint returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking API health: {e}")
    
    # Test 3: Check consciousness status
    try:
        response = requests.get('http://localhost:8003/api/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'running':
                print("✅ Consciousness engine is running")
                print(f"   - Consciousness level: {data.get('consciousness_level', 0):.3f}")
                print(f"   - Phi (Φ): {data.get('phi', 0):.3f}")
                print(f"   - Coherence (R): {data.get('coherence', 0):.3f}")
            else:
                print(f"❌ Consciousness engine status: {data.get('status')}")
        else:
            print(f"❌ Consciousness status endpoint returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking consciousness status: {e}")
    
    # Test 4: Check if static files are served
    try:
        response = requests.get('http://localhost:8003/static/metatron_integrated.js', timeout=5)
        if response.status_code == 200:
            print("✅ Static files are being served correctly")
        else:
            print(f"❌ Static files endpoint returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing static files: {e}")
    
    print("\n🎉 Web UI test completed!")
    return True

if __name__ == "__main__":
    success = test_web_ui()
    sys.exit(0 if success else 1)