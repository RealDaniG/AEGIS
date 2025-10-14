import urllib.request
import json
import time

def test_complete_system():
    """Test all components of the unified system"""
    print("🧪 Testing Complete Unified AI System")
    print("=" * 50)
    
    # Test 1: Metatron Web Server (Port 8003)
    print("\n1. Testing Metatron Web Server (Port 8003)...")
    try:
        req = urllib.request.Request('http://localhost:8003/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        print(f"   ✅ Web server responding ({len(content)} characters)")
        
        req = urllib.request.Request('http://localhost:8003/api/health')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print(f"   ✅ Health endpoint: {data['status']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Open-A.G.I Monitoring Dashboard (Port 5000)
    print("\n2. Testing Open-A.G.I Monitoring Dashboard (Port 5000)...")
    try:
        req = urllib.request.Request('http://localhost:5000/')
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        print(f"   ✅ Dashboard responding ({len(content)} characters)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Unified API Server (Port 8005)
    print("\n3. Testing Unified API Server (Port 8005)...")
    try:
        req = urllib.request.Request('http://localhost:8005/health')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print(f"   ✅ Health endpoint: {data['status']}")
        
        req = urllib.request.Request('http://localhost:8005/state')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        print(f"   ✅ State endpoint: System status is {data['system_status']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 System test completed!")
    print("\n🌐 Access the system at:")
    print("   Main Interface: http://localhost:8003/")
    print("   API Documentation: http://localhost:8005/docs")
    print("   Monitoring Dashboard: http://localhost:5000/")

if __name__ == "__main__":
    test_complete_system()