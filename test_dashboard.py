import urllib.request

def test_dashboard():
    """Test which dashboard is being served"""
    try:
        # Test root endpoint
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        
        print(f"Content length: {len(content)} characters")
        
        # Check for specific titles or identifiers
        if 'Integrated Consciousness Monitor' in content:
            print("✅ Serving: Integrated Consciousness Monitor (Correct)")
        elif 'Harmonic' in content and 'Monitor' in content:
            print("❌ Serving: Harmonic Monitor (Incorrect)")
        elif 'Metatron' in content and 'Consciousness' in content:
            print("✅ Serving: Metatron Consciousness Engine")
        else:
            print("❓ Serving: Unknown dashboard")
            
        # Check for chat functionality
        if 'chat' in content.lower() or 'Chat' in content:
            print("✅ Chat functionality detected")
        else:
            print("❌ No chat functionality detected")
            
        # Check for metrics visualization
        if 'metric' in content.lower() or 'phi' in content.lower() or 'coherence' in content.lower():
            print("✅ Metrics visualization detected")
        else:
            print("❌ No metrics visualization detected")
            
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")

if __name__ == "__main__":
    test_dashboard()