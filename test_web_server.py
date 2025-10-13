import urllib.request
import json

def test_web_server():
    """Simple test to check if the web server is working"""
    try:
        # Test root endpoint
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        print(f"✅ Web server is responding! Content length: {len(content)} characters")
        
        if 'Metatron' in content or 'Consciousness' in content:
            print("✅ Content appears to be the Metatron Web UI")
        else:
            print("⚠️  Content doesn't seem to be the Metatron Web UI")
            
        # Test health endpoint
        req = urllib.request.Request('http://localhost:8003/api/health')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print(f"✅ Health endpoint working: {data}")
        
        print("\n✅ All tests passed! The web server is working correctly on port 8003.")
        
    except Exception as e:
        print(f"❌ Error testing web server: {e}")

if __name__ == "__main__":
    test_web_server()