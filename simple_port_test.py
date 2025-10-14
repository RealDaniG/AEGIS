#!/usr/bin/env python3
"""
Simple Port Test Script

This script verifies that the AEGIS system is correctly configured to use port 457.
"""

import requests
import json
import sys

def test_port_457():
    """Test that port 457 is working correctly"""
    print("Testing AEGIS system on port 457...")
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get("http://localhost:457/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok", False):
                print("   ✅ Health check passed")
            else:
                print(f"   ❌ Health check failed: {data}")
                return False
        else:
            print(f"   ❌ Health check failed with status {response.status_code}")
            return False
            
        # Test status endpoint
        print("2. Testing status endpoint...")
        response = requests.get("http://localhost:457/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "consciousness_level" in data:
                print(f"   ✅ Status check passed: C={data['consciousness_level']:.4f}")
            else:
                print(f"   ❌ Status check missing consciousness data")
                return False
        else:
            print(f"   ❌ Status check failed with status {response.status_code}")
            return False
            
        # Test root endpoint
        print("3. Testing root endpoint...")
        response = requests.get("http://localhost:457/", timeout=5)
        if response.status_code == 200:
            content = response.text
            if "Metatron" in content and "Consciousness" in content:
                print("   ✅ Root endpoint working correctly")
            else:
                print("   ⚠️  Root endpoint returned unexpected content")
        else:
            print(f"   ❌ Root endpoint failed with status {response.status_code}")
            return False
            
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ AEGIS system is correctly configured on port 457")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server may not be running on port 457")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        success = test_port_457()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        sys.exit(1)