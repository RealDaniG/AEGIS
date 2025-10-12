#!/usr/bin/env python3
"""
Test script to verify that the dependency installation process works correctly.
This script simulates what the run_everything scripts do.
"""

import os
import subprocess
import sys

def test_requirements_file(file_path):
    """Test if a requirements file can be processed"""
    if not os.path.exists(file_path):
        print(f"⚠️  Requirements file not found: {file_path}")
        return True
    
    print(f"🔍 Testing requirements file: {file_path}")
    try:
        # Try to install with pip (dry run)
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--dry-run", "-r", file_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Requirements file {file_path} processed successfully")
            return True
        else:
            print(f"⚠️  Requirements file {file_path} had issues:")
            print(f"   stderr: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  Requirements file {file_path} processing timed out")
        return False
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Dependency Installation Process")
    print("=" * 50)
    
    # List of requirements files to test
    requirements_files = [
        "requirements.txt",
        "Metatron-ConscienceAI/requirements.txt",
        "Open-A.G.I/requirements.txt",
        "aegis-conscience/requirements.txt",
        "unified_requirements.txt"
    ]
    
    all_passed = True
    for req_file in requirements_files:
        if not test_requirements_file(req_file):
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All requirements files can be processed!")
        print("   The run_everything scripts should work correctly.")
    else:
        print("⚠️  Some requirements files had issues.")
        print("   The run_everything scripts will continue but with warnings.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)