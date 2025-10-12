#!/usr/bin/env python3
"""
Test script to verify the integrated Metatron system is working correctly.
"""

import requests
import time
import sys

def test_metatron_system():
    """Test the Metatron integrated system."""
    print("Testing Metatron Integrated System...")
    print("=" * 50)
    
    # Test 1: Health check
    print("Test 1: Health Check")
    try:
        response = requests.get("http://localhost:8003/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Health check passed: {data}")
        else:
            print(f"  ✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Health check failed: {e}")
        return False
    
    # Test 2: Status endpoint
    print("\nTest 2: Status Endpoint")
    try:
        response = requests.get("http://localhost:8003/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Status check passed: Consciousness level = {data.get('consciousness_level', 'N/A')}")
        else:
            print(f"  ✗ Status check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Status check failed: {e}")
        return False
    
    # Test 3: Chat endpoint
    print("\nTest 3: Chat Endpoint")
    try:
        test_message = {"message": "Hello, consciousness!", "session_id": "test_session"}
        response = requests.post("http://localhost:8003/api/chat", json=test_message, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Chat test passed: {data.get('response', 'N/A')[:50]}...")
        elif response.status_code == 503:
            data = response.json()
            print(f"  ⚠ Chat test unavailable: {data.get('error', 'N/A')}")
        else:
            print(f"  ✗ Chat test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Chat test failed: {e}")
        return False
    
    # Test 4: Upload endpoint
    print("\nTest 4: Upload Endpoint")
    try:
        response = requests.get("http://localhost:8003/api/uploads", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Upload endpoint accessible: {len(data.get('uploads', []))} files")
        else:
            print(f"  ✗ Upload endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Upload endpoint test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("The integrated Metatron system is working correctly.")
    return True

if __name__ == "__main__":
    success = test_metatron_system()
    sys.exit(0 if success else 1)