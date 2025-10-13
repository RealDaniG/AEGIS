#!/usr/bin/env python3
"""
Simple script to check git status
"""

import subprocess
import os

def run_git_command(command):
    """Run a git command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=r"D:\metatronV2")
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("Checking Git Status for AEGIS Project")
    print("=" * 40)
    
    # Check current directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Change to project directory
    os.chdir(r"D:\metatronV2")
    print(f"Changed to project directory: {os.getcwd()}")
    
    # Check git status
    print("\n1. Git Status:")
    stdout, stderr, returncode = run_git_command("git status")
    if returncode == 0:
        print(stdout)
    else:
        print(f"Error: {stderr}")
    
    # Check what files would be added
    print("\n2. Git Diff (staged changes):")
    stdout, stderr, returncode = run_git_command("git diff --cached")
    if returncode == 0:
        print(stdout[:1000] + "..." if len(stdout) > 1000 else stdout)
    else:
        print(f"No staged changes or error: {stderr}")
    
    # Check what files would be added
    print("\n3. Git Diff (unstaged changes):")
    stdout, stderr, returncode = run_git_command("git diff")
    if returncode == 0:
        print(stdout[:1000] + "..." if len(stdout) > 1000 else stdout)
    else:
        print(f"No unstaged changes or error: {stderr}")

if __name__ == "__main__":
    main()