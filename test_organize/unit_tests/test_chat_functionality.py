#!/usr/bin/env python3
"""
Test script to verify chat functionality with the AEGIS system
"""

import asyncio
import aiohttp
import json

async def test_chat():
    """Test the chat functionality"""
    url = "http://localhost:8005/chat"
    
    # Test message
    message_data = {
        "message": "Hello, AEGIS system!",
        "session_id": "test_session_1"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=message_data) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    print(f"Response: {json.dumps(result, indent=2)}")
                    print("✅ Chat test PASSED - System is responding with 0 errors!")
                else:
                    error_text = await response.text()
                    print(f"❌ Chat test FAILED - Status {response.status}: {error_text}")
                    
    except Exception as e:
        print(f"❌ Chat test FAILED with exception: {e}")

async def test_health():
    """Test the health endpoint"""
    url = "http://localhost:8005/health"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"Health Status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    print(f"Health Response: {json.dumps(result, indent=2)}")
                    print("✅ Health check PASSED!")
                else:
                    error_text = await response.text()
                    print(f"❌ Health check FAILED - Status {response.status}: {error_text}")
                    
    except Exception as e:
        print(f"❌ Health check FAILED with exception: {e}")

async def main():
    """Main test function"""
    print("Testing AEGIS System Health and Chat Functionality")
    print("=" * 50)
    
    # Test health first
    await test_health()
    
    print("\n" + "=" * 50)
    
    # Test chat functionality
    await test_chat()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(main())