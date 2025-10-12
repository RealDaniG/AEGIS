"""
Simple test to demonstrate onion address display without running the full node
"""

import sys
import os

# Add the aegis-conscience directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'aegis-conscience'))

from network.tor_gateway import TORGateway
import asyncio


async def test_onion_creation():
    """Test creating an onion service and displaying its address"""
    print("=== TOR Onion Service Test ===\n")
    
    # Create TOR gateway
    tor = TORGateway()
    
    # Try to initialize
    print("1. Initializing TOR gateway...")
    success = await tor.initialize()
    
    if success:
        print("✅ TOR gateway initialized successfully!")
        
        # Try to create an onion service
        print("\n2. Creating onion service...")
        authorized_clients = ["client_1", "client_2"]
        onion_address = await tor.create_onion_service(
            8080, 
            authorized_clients=authorized_clients
        )
        
        if onion_address:
            print(f"✅ Onion service created successfully!")
            print(f"   Onion Address: {onion_address}:8080")
            print(f"   Authorized Clients: {authorized_clients}")
        else:
            print("⚠️  Failed to create onion service (TOR may not be running)")
            print("   This is expected if TOR is not installed or running")
    else:
        print("⚠️  TOR gateway initialization failed")
        print("   This is expected if stem library is not installed or TOR is not running")
    
    # Clean up
    print("\n3. Cleaning up...")
    await tor.cleanup()
    print("✅ Cleanup completed")
    
    print("\n=== Test Complete ===")
    print("\nTo enable TOR functionality:")
    print("1. Install TOR: https://www.torproject.org/download/")
    print("2. Install stem library: pip install stem")
    print("3. Start TOR service")
    print("4. Run this test again")


if __name__ == "__main__":
    asyncio.run(test_onion_creation())