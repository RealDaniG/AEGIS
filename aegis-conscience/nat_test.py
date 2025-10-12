import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.nat_traversal import NATTraversalManager
import asyncio

async def test_nat():
    print("Testing NAT Traversal Manager...")
    try:
        nat = NATTraversalManager()
        print("  ✓ NAT Traversal Manager created successfully")
        return True
    except Exception as e:
        print(f"  ✗ NAT Traversal Manager failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_nat())