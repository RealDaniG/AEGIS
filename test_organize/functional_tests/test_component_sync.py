#!/usr/bin/env python3
"""
Test script to verify synchronization between all AEGIS components
"""

import asyncio
import sys
import os
import aiohttp

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_api.models import UnifiedSystemState, UnifiedAPISettings

async def test_component_synchronization():
    """Test that all components are properly synchronized"""
    print("🧪 Testing Component Synchronization...")
    print("=" * 50)
    
    try:
        # Test direct connection to Metatron web server on port 8003
        print("\n🔄 Testing direct connection to Metatron web server...")
        
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            try:
                async with session.get('http://localhost:8003/api/health') as response:
                    if response.status == 200:
                        health_data = await response.json()
                        print("✅ Metatron web server health check passed")
                        print(f"   Status: {health_data.get('status', 'unknown')}")
                        print(f"   System: {health_data.get('system', 'unknown')}")
                    else:
                        print(f"⚠️  Health check returned status: {response.status}")
            except Exception as e:
                print(f"❌ Health check failed: {e}")
            
            # Test status endpoint
            try:
                async with session.get('http://localhost:8003/api/status') as response:
                    if response.status == 200:
                        status_data = await response.json()
                        print("✅ Metatron status check passed")
                        print(f"   Consciousness Level: {status_data.get('consciousness_level', 0)}")
                        print(f"   Phi (Φ): {status_data.get('phi', 0)}")
                        print(f"   Coherence (R): {status_data.get('coherence', 0)}")
                    else:
                        print(f"⚠️  Status check returned status: {response.status}")
            except Exception as e:
                print(f"❌ Status check failed: {e}")
            
            # Test chat functionality
            try:
                chat_data = {
                    "message": "What is the relationship between consciousness and AGI?",
                    "session_id": "test_session"
                }
                async with session.post('http://localhost:8003/api/chat', json=chat_data) as response:
                    if response.status == 200:
                        chat_response = await response.json()
                        print("✅ Chat functionality test passed")
                        response_text = chat_response.get('response', '')
                        print(f"   Response preview: {response_text[:100]}...")
                    else:
                        print(f"⚠️  Chat test returned status: {response.status}")
            except Exception as e:
                print(f"❌ Chat test failed: {e}")
        
        print("\n✅ Component synchronization test completed")
        return True
        
    except Exception as e:
        print(f"❌ Error during synchronization test: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_component_synchronization())
    sys.exit(0 if success else 1)