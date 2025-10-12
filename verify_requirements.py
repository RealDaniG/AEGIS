#!/usr/bin/env python3
"""
Verification script for all required dependencies in the Metatron V2 + Open A.G.I system.
This script checks if all required Python packages are installed and working correctly.
"""

import sys
import importlib
import subprocess
import os

def check_python_version():
    """Check if Python version is sufficient"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python version too old: {version.major}.{version.minor}.{version.micro}")
        print("   Please install Python 3.8 or higher")
        return False
    else:
        print(f"✅ Python version OK: {version.major}.{version.minor}.{version.micro}")
        return True

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} is installed and working")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed or not working")
        return False

def check_requirements_file(file_path):
    """Check all packages listed in a requirements file"""
    if not os.path.exists(file_path):
        print(f"⚠️  Requirements file not found: {file_path}")
        return True  # Not an error, just a warning
    
    print(f"\n--- Checking {file_path} ---")
    all_good = True
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Extract package name (before version specifier)
                    package_name = line.split('>=')[0].split('==')[0].split('>')[0].split('<')[0].split('<=')[0].split('~=')[0]
                    if not check_package(package_name):
                        all_good = False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    return all_good

def main():
    """Main verification function"""
    print("🔍 Verifying Metatron V2 + Open A.G.I System Requirements")
    print("=" * 60)
    
    # Check Python version
    python_ok = check_python_version()
    
    if not python_ok:
        print("\n❌ Python version check failed. Exiting.")
        return False
    
    # Check all requirements files
    requirements_files = [
        "requirements.txt",
        "Metatron-ConscienceAI/requirements.txt",
        "Open-A.G.I/requirements.txt",
        "aegis-conscience/requirements.txt",
        "unified_requirements.txt"
    ]
    
    all_requirements_ok = True
    for req_file in requirements_files:
        if not check_requirements_file(req_file):
            all_requirements_ok = False
    
    print("\n" + "=" * 60)
    if python_ok and all_requirements_ok:
        print("✅ All requirements checks passed!")
        print("   You're ready to run the Metatron V2 + Open A.G.I system.")
        return True
    else:
        print("❌ Some requirements checks failed!")
        print("   Please install the missing packages before running the system.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)