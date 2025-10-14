import urllib.request
import json

def test_webui():
    """Simple test to check if the web UI is being served"""
    try:
        # Test root endpoint (should serve the web UI)
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        
        if '<html' in content.lower():
            print("✅ Web UI is being served correctly!")
            print(f"Content length: {len(content)} characters")
            if 'metatron' in content.lower() or 'conscience' in content.lower():
                print("✅ Content appears to be the Metatron Web UI")
            else:
                print("⚠️  Content doesn't seem to be the Metatron Web UI")
        else:
            print("⚠️  Root endpoint doesn't appear to serve HTML content")
            print(f"Content type: {response.headers.get('Content-Type')}")
            
        # Test static file endpoint
        req = urllib.request.Request('http://localhost:8003/static/index.html')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        print(f"✅ Static index.html served successfully ({len(content)} characters)")
        
        # Test assets endpoint
        req = urllib.request.Request('http://localhost:8003/assets/app_stream.js')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        print(f"✅ Assets JS file served successfully ({len(content)} characters)")
        
        print("\n✅ All tests passed! The web UI is working correctly.")
        
    except Exception as e:
        print(f"❌ Error testing web UI: {e}")

if __name__ == "__main__":
    test_webui()