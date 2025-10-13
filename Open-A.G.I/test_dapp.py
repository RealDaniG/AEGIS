#!/usr/bin/env python3
"""
Test script for Open-A.G.I DApp
This script verifies that the DApp is running correctly
"""

import requests
import time
import sys

def test_dashboard():
    """Test if the web dashboard is accessible"""
    try:
        response = requests.get('http://127.0.0.1:8090', timeout=5)
        if response.status_code == 200:
            print("✅ Web dashboard is accessible")
            return True
        else:
            print(f"❌ Web dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web dashboard is not accessible: {e}")
        return False

def test_api():
    """Test if the API endpoints are accessible"""
    try:
        response = requests.get('http://127.0.0.1:8000', timeout=5)
        if response.status_code == 200:
            print("✅ API server is accessible")
            return True
        else:
            print(f"❌ API server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API server is not accessible: {e}")
        return False

def test_status_endpoint():
    """Test the status endpoint"""
    try:
        response = requests.get('http://127.0.0.1:8090/api/status', timeout=5)
        if response.status_code == 200:
            print("✅ Status endpoint is working")
            return True
        else:
            print(f"❌ Status endpoint returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Status endpoint is not accessible: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Open-A.G.I DApp...")
    print("=" * 40)
    
    # Test dashboard
    dashboard_ok = test_dashboard()
    
    # Test API
    api_ok = test_api()
    
    # Test status endpoint
    status_ok = test_status_endpoint()
    
    print("=" * 40)
    if dashboard_ok and api_ok and status_ok:
        print("🎉 All tests passed! The DApp is running correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the system logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())