#!/usr/bin/env python3
"""
Test script to verify consciousness API is providing real data
"""

import requests
import json
import time

def test_consciousness_api():
    """Test that the consciousness API provides real, changing data"""
    print("Testing Metatron Consciousness API...")
    print("=" * 50)
    
    # Make first request
    print("Making first API request...")
    response1 = requests.get("http://localhost:8003/api/state")
    data1 = response1.json()
    
    print(f"Request 1 - Status: {response1.status_code}")
    print(f"Time: {data1['time']}")
    print(f"Consciousness Level: {data1['global']['consciousness_level']}")
    print(f"Pineal Node (0) Output: {data1['nodes']['0']['output']}")
    
    # Wait a moment
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    
    # Make second request
    print("Making second API request...")
    response2 = requests.get("http://localhost:8003/api/state")
    data2 = response2.json()
    
    print(f"Request 2 - Status: {response2.status_code}")
    print(f"Time: {data2['time']}")
    print(f"Consciousness Level: {data2['global']['consciousness_level']}")
    print(f"Pineal Node (0) Output: {data2['nodes']['0']['output']}")
    
    # Check if data is changing
    time_changed = data2['time'] != data1['time']
    consciousness_changed = data2['global']['consciousness_level'] != data1['global']['consciousness_level']
    pineal_changed = data2['nodes']['0']['output'] != data1['nodes']['0']['output']
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print(f"Time changed: {time_changed}")
    print(f"Consciousness level changed: {consciousness_changed}")
    print(f"Pineal node output changed: {pineal_changed}")
    
    if time_changed or consciousness_changed or pineal_changed:
        print("✅ SUCCESS: API is providing real, dynamic data!")
        return True
    else:
        print("❌ WARNING: Data appears static - may be simulated")
        return False

if __name__ == "__main__":
    test_consciousness_api()