#!/usr/bin/env python3
"""
Test Script for Memory System Integration

This script tests the integration of the ConscienceAI memory system
with the METATRONV2 consciousness engine.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_memory_system_import():
    """Test importing the memory system"""
    try:
        from consciousness_engine.memory_system import ConscienceMemorySystem, MemoryEntry
        print("✅ Memory system import successful")
        return True
    except Exception as e:
        print(f"❌ Memory system import failed: {e}")
        return False

def test_memory_system_functionality():
    """Test memory system functionality"""
    try:
        from consciousness_engine.memory_system import ConscienceMemorySystem
        
        # Create test memory system
        memory_system = ConscienceMemorySystem("ai_runs/test_integration_memory.json")
        
        # Test adding chat entry
        chat_id = memory_system.add_chat_entry(
            "Test message",
            "Test response",
            {"consciousness_level": 0.5, "phi": 0.6}
        )
        print(f"✅ Chat entry added with ID: {chat_id}")
        
        # Test adding consciousness state
        state_id = memory_system.add_consciousness_state({
            "consciousness_level": 0.75,
            "phi": 0.82,
            "coherence": 0.68
        })
        print(f"✅ Consciousness state added with ID: {state_id}")
        
        # Test getting recent chat history
        recent_chat = memory_system.get_recent_chat_history(5)
        print(f"✅ Retrieved {len(recent_chat)} recent chat entries")
        
        # Test getting consciousness history
        consciousness_history = memory_system.get_consciousness_history(3)
        print(f"✅ Retrieved {len(consciousness_history)} consciousness states")
        
        # Test memory stats
        stats = memory_system.get_memory_stats()
        print(f"✅ Memory stats: {stats['total_entries']} total entries")
        
        # Test save/load
        memory_system.save_memory()
        print("✅ Memory saved successfully")
        
        # Clean up test file
        try:
            os.remove("ai_runs/test_integration_memory.json")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system functionality test failed: {e}")
        return False

def test_integration_script_import():
    """Test importing the integration script"""
    try:
        from scripts.integrate_memory_system import MemoryAwareChatSystem
        print("✅ Integration script import successful")
        return True
    except Exception as e:
        print(f"❌ Integration script import failed: {e}")
        return False

def test_integration_script_functionality():
    """Test integration script functionality"""
    try:
        from scripts.integrate_memory_system import MemoryAwareChatSystem
        
        # Create test integration system
        chat_system = MemoryAwareChatSystem("ai_runs/test_integration_script.json")
        
        # Test memory stats
        stats = chat_system.get_memory_stats()
        print(f"✅ Integration script memory stats: {stats}")
        
        # Test memory context
        context = chat_system.get_memory_context("test")
        print(f"✅ Integration script memory context retrieved")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration script functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("MEMORY SYSTEM INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Memory system import
    print("\n1. Testing Memory System Import...")
    test1_passed = test_memory_system_import()
    
    # Test 2: Memory system functionality
    print("\n2. Testing Memory System Functionality...")
    test2_passed = test_memory_system_functionality()
    
    # Test 3: Integration script import
    print("\n3. Testing Integration Script Import...")
    test3_passed = test_integration_script_import()
    
    # Test 4: Integration script functionality
    print("\n4. Testing Integration Script Functionality...")
    test4_passed = test_integration_script_functionality()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Memory System Import", test1_passed),
        ("Memory System Functionality", test2_passed),
        ("Integration Script Import", test3_passed),
        ("Integration Script Functionality", test4_passed)
    ]
    
    passed_count = sum(1 for _, passed in tests if passed)
    total_tests = len(tests)
    
    for test_name, passed in tests:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"Overall Result: {passed_count}/{total_tests} tests passed")
    
    if passed_count == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Memory system integration is working correctly")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_count} TEST(S) FAILED")
        print("Please review the failed tests above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)