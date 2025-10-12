#!/usr/bin/env python3
"""
Verification script to ensure the AEGIS system is running with 0 errors
"""

import asyncio
import aiohttp
import json
import sys

async def verify_system():
    """Verify the system is running with 0 errors"""
    health_url = "http://localhost:8005/health"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(health_url) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("status") == "healthy":
                        print("✅ SUCCESS: AEGIS system is running with 0 errors!")
                        print(f"   System Status: {result['status']}")
                        print(f"   API Client: {'Initialized' if result['api_client_initialized'] else 'Not Initialized'}")
                        print(f"   Timestamp: {result['timestamp']}")
                        return True
                    else:
                        print(f"❌ FAILURE: System reports unhealthy status: {result.get('status')}")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ FAILURE: Health check failed with status {response.status}: {error_text}")
                    return False
                    
    except aiohttp.ClientConnectorError as e:
        print(f"❌ FAILURE: Cannot connect to AEGIS system at {health_url}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILURE: Unexpected error during system verification: {e}")
        return False

async def main():
    """Main verification function"""
    print("Verifying AEGIS System - Zero Error Test")
    print("=" * 40)
    
    success = await verify_system()
    
    if success:
        print("\n🎉 VERIFICATION COMPLETE: System is running with 0 errors!")
        sys.exit(0)
    else:
        print("\n💥 VERIFICATION FAILED: System has errors!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())