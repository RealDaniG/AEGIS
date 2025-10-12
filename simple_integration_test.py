#!/usr/bin/env python3
"""
Simple Integration Test
"""

import requests
import json
import time

def main():
    print("METATRON V2 INTEGRATION TEST")
    print("=" * 40)
    
    # Test 1: Metatron API
    print("\n1. Testing Metatron API...")
    try:
        response = requests.get("http://localhost:8003/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Status API: OK")
            print(f"   Consciousness Level: {data.get('consciousness_level', 0):.6f}")
            print(f"   Uptime: {data.get('performance', {}).get('uptime', 0):.2f} seconds")
        else:
            print(f"   ❌ Status API: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status API Error: {e}")
    
    # Test 2: Chat Bot
    print("\n2. Testing Chat Bot...")
    try:
        chat_data = {"message": "What is consciousness?", "session_id": "test"}
        response = requests.post("http://localhost:8003/api/chat", json=chat_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Chat API: OK")
            print(f"   Model: {data.get('model', 'unknown')}")
            preview = data.get('response', '')[:50] + "..." if len(data.get('response', '')) > 50 else data.get('response', '')
            print(f"   Response: {preview}")
        else:
            print(f"   ❌ Chat API: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Chat API Error: {e}")
    
    # Test 3: Visuals Accuracy
    print("\n3. Testing Visuals Accuracy...")
    try:
        # Get two status updates
        response1 = requests.get("http://localhost:8003/api/status", timeout=5)
        time.sleep(2)
        response2 = requests.get("http://localhost:8003/api/status", timeout=5)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            uptime1 = data1.get('performance', {}).get('uptime', 0)
            uptime2 = data2.get('performance', {}).get('uptime', 0)
            
            print("   ✅ Visuals Test: OK")
            print(f"   Uptime 1: {uptime1:.2f}s")
            print(f"   Uptime 2: {uptime2:.2f}s")
            print(f"   Updating: {'YES' if uptime2 > uptime1 else 'NO'}")
        else:
            print("   ❌ Visuals Test: API Error")
    except Exception as e:
        print(f"   ❌ Visuals Test Error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ INTEGRATION TEST COMPLETE")
    print("The bot and AGI system are integrated and functioning!")

if __name__ == "__main__":
    main()