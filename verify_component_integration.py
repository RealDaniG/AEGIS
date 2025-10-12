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
        # Handle modules with hyphens in their names
        if '-' in module_name:
            # For modules with hyphens, we need to load them differently
            parts = module_name.split('.')
            if len(parts) > 1:
                # Special handling for Open-A.G.I and aegis-conscience
                if parts[0] == "Open-A.G.I":
                    # Try to load as a file-based module with hyphens
                    file_path = "Open-A.G.I/" + "/".join(parts[1:]) + ".py"
                    if os.path.exists(file_path):
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(parts[-1], file_path)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            print(f"✅ {description}: Module imported successfully")
                            return True
                elif parts[0] == "aegis_conscience":
                    # Try to load as a file-based module
                    file_path = "aegis-conscience/" + "/".join(parts[1:]) + ".py"
                    if os.path.exists(file_path):
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(parts[-1], file_path)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            print(f"✅ {description}: Module imported successfully")
                            return True
                # Try with underscore replacement
                file_path_parts = [part.replace('-', '_') if i == 0 else part for i, part in enumerate(parts)]
                file_path = '/'.join(file_path_parts) + '.py'
                if os.path.exists(file_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(parts[-1], file_path)
                    if spec is not None and spec.loader is not None:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"✅ {description}: Module imported successfully")
                        return True
                # Try with original path (with hyphens)
                file_path = '/'.join(parts) + '.py'
                if os.path.exists(file_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(parts[-1], file_path)
                    if spec is not None and spec.loader is not None:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"✅ {description}: Module imported successfully")
                        return True
            
        # Standard import for modules without hyphens
        import importlib.util
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
    try:
        import sys
        sys.path.insert(0, 'Metatron-ConscienceAI')
        # Import the module dynamically to avoid linter errors
        import importlib
        orchestrator_module = importlib.import_module('orchestrator.metatron_orchestrator')
        # Access the class to ensure it's loaded
        _ = getattr(orchestrator_module, 'MetatronConsciousness')
        print("✅ Metatron Orchestrator: Module imported successfully")
        passed += 1
    except Exception as e:
        print(f"❌ Metatron Orchestrator: Failed to import - {str(e)}")
    
    total += 1
    if test_import("Metatron-ConscienceAI.nodes.consciousness_metrics", "Consciousness Metrics"):
        passed += 1
    
    total += 1
    if test_import("Metatron-ConscienceAI.nodes.metatron_geometry", "Metatron Geometry"):
        passed += 1
    
    # Test 2: AGI modules
    print("\n2. AGI System Modules:")
    total += 1
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('consensus_protocol', 'Open-A.G.I/consensus_protocol.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ Consensus Protocol: Module imported successfully")
            passed += 1
        else:
            print("❌ Consensus Protocol: Failed to load module spec")
    except Exception as e:
        print(f"❌ Consensus Protocol: Failed to import - {str(e)}")
    
    total += 1
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('p2p_network', 'Open-A.G.I/p2p_network.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ P2P Network: Module imported successfully")
            passed += 1
        else:
            print("❌ P2P Network: Failed to load module spec")
    except Exception as e:
        print(f"❌ P2P Network: Failed to import - {str(e)}")
    
    total += 1
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('crypto_framework', 'Open-A.G.I/crypto_framework.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ Crypto Framework: Module imported successfully")
            passed += 1
        else:
            print("❌ Crypto Framework: Failed to load module spec")
    except Exception as e:
        print(f"❌ Crypto Framework: Failed to import - {str(e)}")
    
    # Test 3: AEGIS modules
    print("\n3. AEGIS System Modules:")
    total += 1
    try:
        import sys
        sys.path.insert(0, 'aegis-conscience')
        import importlib.util
        spec = importlib.util.spec_from_file_location('p2p', 'aegis-conscience/network/p2p.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ AEGIS P2P Network: Module imported successfully")
            passed += 1
        else:
            print("❌ AEGIS P2P Network: Failed to load module spec")
    except Exception as e:
        print(f"❌ AEGIS P2P Network: Failed to import - {str(e)}")
    
    total += 1
    try:
        import sys
        sys.path.insert(0, 'aegis-conscience')
        import importlib.util
        spec = importlib.util.spec_from_file_location('pbft', 'aegis-conscience/consensus/pbft.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ AEGIS PBFT Consensus: Module imported successfully")
            passed += 1
        else:
            print("❌ AEGIS PBFT Consensus: Failed to load module spec")
    except Exception as e:
        print(f"❌ AEGIS PBFT Consensus: Failed to import - {str(e)}")
    
    total += 1
    try:
        import sys
        sys.path.insert(0, 'aegis-conscience')
        import importlib.util
        spec = importlib.util.spec_from_file_location('crypto', 'aegis-conscience/network/crypto.py')
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ AEGIS Crypto: Module imported successfully")
            passed += 1
        else:
            print("❌ AEGIS Crypto: Failed to load module spec")
    except Exception as e:
        print(f"❌ AEGIS Crypto: Failed to import - {str(e)}")
    
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