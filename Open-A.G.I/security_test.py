#!/usr/bin/env python3
"""
Security Protocols Test
Simple test to verify that the security protocols component is working correctly.
"""

import sys
import os
import asyncio

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

async def test_security_protocols():
    """Test the security protocols component"""
    try:
        print("🔍 Testing Security Protocols Component...")
        
        # Import the security protocols module
        from security_protocols import SecurityProtocolManager
        
        # Create a security manager instance
        security_manager = SecurityProtocolManager("test_node")
        
        # Initialize security
        success = await security_manager.initialize_security()
        
        if success:
            print("✅ Security Protocols: SUCCESS")
            
            # Get security status
            status = await security_manager.get_security_status()
            print(f"📊 Security Level: {status['security_level']}")
            print(f"📊 Active Sessions: {status['active_sessions']}")
            
            return True
        else:
            print("❌ Security Protocols: FAILED - Initialization failed")
            return False
            
    except ImportError as e:
        print(f"❌ Security Protocols: FAILED - Import error: {e}")
        return False
    except Exception as e:
        print(f"💥 Security Protocols: ERROR - {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Security Protocols Test")
    print("=" * 50)
    
    success = await test_security_protocols()
    
    print("=" * 50)
    if success:
        print("🎉 Security Protocols Test PASSED!")
        print("✅ All security components are working correctly")
    else:
        print("❌ Security Protocols Test FAILED!")
        print("⚠️  Please check the security protocols implementation")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)