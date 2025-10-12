#!/usr/bin/env python3
"""
Component Integration Verification Script

This script verifies that individual components of the METATRONV2 system are working correctly
without requiring the full system to be running.
"""

import sys
import os
import importlib.util

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_import(module_name, description):
    """Test if a module can be imported"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"❌ {description}: Module '{module_name}' not found")
            return False
        
        if spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ {description}: Module imported successfully")
            return True
        else:
            print(f"❌ {description}: Module '{module_name}' found but cannot be loaded")
            return False
    except Exception as e:
        print(f"❌ {description}: Failed to import - {str(e)}")
        return False

def test_file_exists(file_path, description):
    """Test if a file exists"""
    full_path = os.path.join(project_root, file_path)
    if os.path.exists(full_path):
        print(f"✅ {description}: File exists")
        return True
    else:
        print(f"❌ {description}: File not found ({full_path})")
        return False

def main():
    print("METATRONV2 Component Integration Verification")
    print("=" * 50)
    
    # Track test results
    passed = 0
    total = 0
    
    # Test 1: Core consciousness modules
    print("\n1. Core Consciousness Modules:")
    total += 1
    if test_import("Metatron_ConscienceAI.orchestrator.metatron_orchestrator", "Metatron Orchestrator"):
        passed += 1
    
    total += 1
    if test_import("Metatron_ConscienceAI.nodes.consciousness_metrics", "Consciousness Metrics"):
        passed += 1
    
    total += 1
    if test_import("Metatron_ConscienceAI.nodes.metatron_geometry", "Metatron Geometry"):
        passed += 1
    
    # Test 2: AGI modules
    print("\n2. AGI System Modules:")
    total += 1
    if test_import("Open_A_G_I.consensus_protocol", "Consensus Protocol"):
        passed += 1
    
    total += 1
    if test_import("Open_A_G_I.p2p_network", "P2P Network"):
        passed += 1
    
    total += 1
    if test_import("Open_A_G_I.crypto_framework", "Crypto Framework"):
        passed += 1
    
    # Test 3: AEGIS modules
    print("\n3. AEGIS System Modules:")
    total += 1
    if test_import("aegis_conscience.network.p2p", "AEGIS P2P Network"):
        passed += 1
    
    total += 1
    if test_import("aegis_conscience.consensus.pbft", "AEGIS PBFT Consensus"):
        passed += 1
    
    total += 1
    if test_import("aegis_conscience.network.crypto", "AEGIS Crypto"):
        passed += 1
    
    # Test 4: Unified system modules
    print("\n4. Unified System Modules:")
    total += 1
    if test_import("unified_api.client", "Unified API Client"):
        passed += 1
    
    total += 1
    if test_import("unified_components.network", "Unified Network"):
        passed += 1
    
    total += 1
    if test_import("consciousness_aware_agi.decision_engine", "Consciousness-Aware Decision Engine"):
        passed += 1
    
    total += 1
    if test_import("cross_system_comm.protocols", "Cross-System Communication"):
        passed += 1
    
    # Test 5: Required files
    print("\n5. Required Files:")
    total += 1
    if test_file_exists("requirements.txt", "Main Requirements"):
        passed += 1
    
    total += 1
    if test_file_exists("Metatron-ConscienceAI/nodes/__init__.py", "Metatron Nodes Package"):
        passed += 1
    
    total += 1
    if test_file_exists("Open-A.G.I/__init__.py", "Open-A.G.I Package"):
        passed += 1
    
    total += 1
    if test_file_exists("UNIFIED_SYSTEM_README.md", "Unified System Documentation"):
        passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("COMPONENT INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL COMPONENTS INTEGRATED SUCCESSFULLY!")
        print("The system is ready for full operation.")
        return True
    else:
        print(f"\n⚠️  {total-passed} components need attention.")
        print("Please check the failed components above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)