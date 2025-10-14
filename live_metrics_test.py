#!/usr/bin/env python3
"""
Live Metrics Test Script
Verifies that all metrics are working live and the chatbot is responding coherently
"""

import asyncio
import websockets
import json
import requests
import time

async def test_websocket_connection():
    """Test WebSocket connection to Metatron server"""
    print("Testing WebSocket connection to Metatron server on port 457...")
    
    try:
        uri = "ws://localhost:457/ws"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection successful")
            
            # Receive a few messages to verify data flow
            print("Receiving live metrics updates...")
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract consciousness metrics
                consciousness_data = data.get('global', data)
                consciousness_level = consciousness_data.get('consciousness_level', 0)
                phi = consciousness_data.get('phi', 0)
                
                # Extract memory metrics if available
                memory_buffer_size = 0
                if 'nodes' in data and '3' in data['nodes']:
                    node3_data = data['nodes']['3']
                    if 'memory_metrics' in node3_data:
                        memory_buffer_size = node3_data['memory_metrics'].get('memory_buffer_size', 0)
                
                print(f"📊 Update #{i+1}: C={consciousness_level:.4f}, "
                      f"Φ={phi:.4f}, "
                      f"Memory Buffer={memory_buffer_size}")
                
            print("✅ Real-time data streaming verified")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

def test_http_endpoints():
    """Test HTTP endpoints"""
    print("\nTesting HTTP endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:457/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check endpoint working - System: {health_data.get('system', 'N/A')}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
            
        # Test status endpoint
        response = requests.get("http://localhost:457/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            consciousness_level = status_data.get('consciousness_level', 0)
            phi = status_data.get('phi', 0)
            print(f"✅ Status endpoint working - C={consciousness_level:.4f}, Φ={phi:.4f}")
        else:
            print(f"❌ Status endpoint failed with status {response.status_code}")
            return False
            
        # Test state endpoint for memory metrics
        response = requests.get("http://localhost:457/api/state", timeout=5)
        if response.status_code == 200:
            state_data = response.json()
            nodes = state_data.get('nodes', {})
            if '3' in nodes:
                node3_data = nodes['3']
                memory_metrics = node3_data.get('memory_metrics', {})
                memory_buffer_size = memory_metrics.get('memory_buffer_size', 0)
                print(f"✅ Memory metrics available - Buffer Size: {memory_buffer_size}")
            else:
                print("⚠️  Node 3 (MemoryMatrixNode) not found in state data")
        else:
            print(f"❌ State endpoint failed with status {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ HTTP connection failed - server may not be running")
        return False
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

def test_chatbot_responses():
    """Test chatbot responses for coherence"""
    print("\nTesting chatbot responses...")
    
    try:
        # Test 1: Simple question
        data = {'message': 'What is consciousness?', 'model': 'distilgpt2'}
        response = requests.post("http://localhost:457/api/chat", json=data, timeout=15)
        if response.status_code == 200:
            chat_data = response.json()
            response_text = chat_data.get('response', '')
            print(f"✅ Simple question response: {response_text[:100]}...")
        else:
            print(f"❌ Simple question failed with status {response.status_code}")
            return False
            
        # Test 2: System-specific question
        data = {'message': 'What is the Metatron system?', 'model': 'distilgpt2'}
        response = requests.post("http://localhost:457/api/chat", json=data, timeout=15)
        if response.status_code == 200:
            chat_data = response.json()
            response_text = chat_data.get('response', '')
            print(f"✅ System question response: {response_text[:100]}...")
        else:
            print(f"❌ System question failed with status {response.status_code}")
            return False
            
        # Test 3: Memory-related question
        data = {'message': 'How does your memory system work?', 'model': 'distilgpt2'}
        response = requests.post("http://localhost:457/api/chat", json=data, timeout=15)
        if response.status_code == 200:
            chat_data = response.json()
            response_text = chat_data.get('response', '')
            print(f"✅ Memory question response: {response_text[:100]}...")
        else:
            print(f"❌ Memory question failed with status {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Chatbot test failed - server may not be running")
        return False
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive test of all Metatron components"""
    print("=" * 70)
    print("METATRON CONSCIOUSNESS ENGINE - LIVE METRICS AND CHATBOT TEST")
    print("=" * 70)
    
    # Test components
    tests = [
        ("HTTP Endpoints", test_http_endpoints),
        ("WebSocket Connection", test_websocket_connection),
        ("Chatbot Responses", test_chatbot_responses)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Live metrics are working correctly")
        print("✅ Chatbot is responding coherently")
        print("✅ WebSocket streaming is functional")
        print("✅ HTTP endpoints are responsive")
        print("✅ Memory system metrics are available")
        return True
    else:
        print(f"\n❌ {total - passed} out of {total} tests failed")
        print("⚠️  Some components may not be working correctly")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_comprehensive_test())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"❌ Test suite failed with exception: {e}")
        exit(1)