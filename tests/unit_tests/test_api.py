import requests
import json

def test_unified_api():
    """Test the unified API server"""
    base_url = "http://localhost:8003"
    
    print("Testing Unified API Server on port 8003...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Root response: {json.dumps(data, indent=2)}")
        else:
            print(f"Root endpoint error: {response.text}")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"\nHealth endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Health response: {json.dumps(data, indent=2)}")
        else:
            print(f"Health endpoint error: {response.text}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
    
    # Test state endpoint
    try:
        response = requests.get(f"{base_url}/state")
        print(f"\nState endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"State response received")
        else:
            print(f"State endpoint error: {response.text}")
    except Exception as e:
        print(f"Error testing state endpoint: {e}")

if __name__ == "__main__":
    test_unified_api()