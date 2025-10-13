import urllib.request
import json

def test_api():
    """Simple test to check if the API is working"""
    try:
        # Test root endpoint
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print("API Root Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        # Test health endpoint
        req = urllib.request.Request('http://localhost:8003/health')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print("\nAPI Health Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        print("\n✅ API is working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_api()