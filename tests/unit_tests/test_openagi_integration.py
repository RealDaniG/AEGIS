#!/usr/bin/env python3
"""
Test script for Open-A.G.I integration components
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test importing all Open-A.G.I integration components"""
    print("Testing Open-A.G.I integration component imports...")
    
    components = [
        {
            'name': 'Deployment Adapter',
            'module': 'aegis_integration.deploy.deployment_adapter',
            'imports': ['DeploymentAdapter', 'AEGISNodeConfig']
        },
        {
            'name': 'TOR Adapter',
            'module': 'cross_system_comm.tor_adapter',
            'imports': ['TorAdapter', 'AEGISTorConfig']
        },
        {
            'name': 'Metrics Bridge',
            'module': 'visualization_tools.metrics_bridge',
            'imports': ['MetricsBridge', 'AEGISMetricsConfig']
        }
    ]
    
    success_count = 0
    total_count = len(components)
    
    for component in components:
        try:
            # Import the module
            module = __import__(component['module'], fromlist=component['imports'])
            
            # Check if specific classes/funcs can be accessed
            for item in component['imports']:
                getattr(module, item)
            
            print(f"  ✅ {component['name']}: Import successful")
            success_count += 1
            
        except ImportError as e:
            print(f"  ❌ {component['name']}: Import failed - {e}")
        except AttributeError as e:
            print(f"  ❌ {component['name']}: Missing component - {e}")
        except Exception as e:
            print(f"  ❌ {component['name']}: Unexpected error - {e}")
    
    print(f"\nResults: {success_count}/{total_count} components imported successfully")
    return success_count == total_count

def test_file_existence():
    """Test if required files exist"""
    print("\nTesting required file existence...")
    
    required_files = [
        'aegis-integration/deploy/deployment_adapter.py',
        'cross_system_comm/tor_adapter.py',
        'visualization_tools/metrics_bridge.py',
        '.github/workflows/ci.yml',
        'deploy/Dockerfile',
        'deploy/docker-compose.dev.yml',
        'deploy/torrc',
        'requirements-optional.txt',
        'docs/openagi_integration_guide.md'
    ]
    
    success_count = 0
    total_count = len(required_files)
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}: File exists")
            success_count += 1
        else:
            print(f"  ❌ {file_path}: File not found")
    
    print(f"\nResults: {success_count}/{total_count} files found")
    return success_count == total_count

def main():
    """Main test function"""
    print("=" * 60)
    print("Open-A.G.I Integration Components Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test file existence
    files_ok = test_file_existence()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if imports_ok and files_ok:
        print("🎉 All tests passed! Open-A.G.I integration is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())