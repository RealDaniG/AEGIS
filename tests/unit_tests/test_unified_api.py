import urllib.request
import json

def test_unified_api():
    """Simple test to check if the unified API is working"""
    try:
        # Test root endpoint
        req = urllib.request.Request('http://localhost:8005/')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print("Unified API Root Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        # Test health endpoint
        req = urllib.request.Request('http://localhost:8005/health')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print("\nUnified API Health Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        # Test state endpoint
        req = urllib.request.Request('http://localhost:8005/state')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print("\nUnified API State Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        print("\n✅ Unified API is working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing Unified API: {e}")

if __name__ == "__main__":
    test_unified_api()