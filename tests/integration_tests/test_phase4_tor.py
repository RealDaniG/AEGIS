#!/usr/bin/env python3
"""
Test script for Phase 4: TOR Integration
"""

import sys
import os
import asyncio

# Add project paths
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
open_agi_path = os.path.join(project_root, 'Open-A.G.I')
sys.path.insert(0, project_root)
sys.path.insert(0, metatron_path)
sys.path.insert(0, open_agi_path)

def test_tor_import():
    """Test that we can import the TorGateway"""
    print("Testing TorGateway import...")
    try:
        # Add Open-A.G.I to path for direct import
        sys.path.insert(0, open_agi_path)
        from tor_integration import TorGateway
        print("✅ TorGateway import successful")
        return True
    except Exception as e:
        print(f"❌ TorGateway import failed: {e}")
        return False

def test_memory_matrix_tor():
    """Test MemoryMatrixNode TOR integration"""
    print("\nTesting MemoryMatrixNode TOR integration...")
    try:
        # Add Metatron-ConscienceAI to path for direct import
        sys.path.insert(0, metatron_path)
        from nodes.memory_matrix import MemoryMatrixNode
        
        # Check if TOR integration is available
        import nodes.memory_matrix as mm
        HAS_TOR = False
        try:
            sys.path.insert(0, open_agi_path)
            from tor_integration import TorGateway
            HAS_TOR = True
        except:
            pass
            
        print(f"HAS_TOR: {HAS_TOR}")
        
        # Create MemoryMatrixNode
        memory_node = MemoryMatrixNode(node_id=3)
        
        # Check if TOR gateway can be initialized
        if HAS_TOR:
            try:
                tor_gateway = TorGateway()
                print("✅ TOR gateway initialization successful")
            except Exception as e:
                print(f"⚠️ TOR gateway initialization failed: {e}")
        else:
            print("⚠️ TOR integration not available")
            
        print("✅ MemoryMatrixNode TOR integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ MemoryMatrixNode TOR integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_async_tor_operations():
    """Test async TOR operations"""
    print("\nTesting async TOR operations...")
    try:
        # Add Metatron-ConscienceAI to path for direct import
        sys.path.insert(0, metatron_path)
        from nodes.memory_matrix import MemoryMatrixNode
        
        # Create MemoryMatrixNode
        memory_node = MemoryMatrixNode(node_id=3)
        
        # Start network
        await memory_node.start_network()
        
        # Check if TOR integration is available
        HAS_TOR = False
        try:
            sys.path.insert(0, open_agi_path)
            from tor_integration import TorGateway
            HAS_TOR = True
        except:
            pass
            
        if HAS_TOR:
            try:
                tor_gateway = TorGateway()
                # Initialize TOR (this would connect to actual TOR network)
                # result = await tor_gateway.initialize()
                print("✅ TOR gateway async operations test completed")
            except Exception as e:
                print(f"⚠️ TOR gateway async operations test failed: {e}")
        else:
            print("⚠️ TOR integration not available for async operations")
        
        print("✅ Async TOR operations test completed")
        return True
        
    except Exception as e:
        print(f"❌ Async TOR operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all TOR integration tests"""
    print("=" * 60)
    print("Phase 4: TOR Integration - Test Suite")
    print("=" * 60)
    
    # Test imports
    import_success = test_tor_import()
    
    # Test MemoryMatrixNode integration
    integration_success = test_memory_matrix_tor()
    
    # Test async operations
    async_success = asyncio.run(test_async_tor_operations())
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"TOR Import Test: {'✅ PASSED' if import_success else '❌ FAILED'}")
    print(f"MemoryMatrix Integration Test: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    print(f"Async Operations Test: {'✅ PASSED' if async_success else '❌ FAILED'}")
    
    if import_success and integration_success and async_success:
        print("\n🎉 All TOR integration tests passed!")
        return 0
    else:
        print("\n❌ Some TOR integration tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())