import urllib.request
import sys

def check_dashboard():
    """Check which dashboard is being served"""
    try:
        # Test root endpoint
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        
        print(f"Response status: {response.status}")
        print(f"Content length: {len(content)} characters")
        
        # Check for specific titles
        if 'Integrated Consciousness Monitor' in content:
            print("✅ SUCCESS: Serving Integrated Consciousness Monitor (Correct)")
            return True
        elif 'Harmonic Monitor' in content:
            print("❌ ISSUE: Serving Harmonic Monitor (Incorrect)")
            return False
        elif 'Metatron' in content and 'Consciousness' in content:
            print("✅ PARTIAL: Serving Metatron Consciousness Engine")
            return True
        else:
            print("❓ UNKNOWN: Serving unknown content")
            # Print first 500 characters for debugging
            print("First 500 characters:")
            print(content[:500])
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = check_dashboard()
    sys.exit(0 if success else 1)