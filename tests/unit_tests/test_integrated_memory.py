#!/usr/bin/env python3
"""
Test Script for Integrated Memory System

This script tests that the integrated memory system works correctly
and can be used by the chat system.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the memory system
MEMORY_SYSTEM_AVAILABLE = False
ConscienceMemorySystem = None

try:
    from consciousness_engine.memory_system import ConscienceMemorySystem
    MEMORY_SYSTEM_AVAILABLE = True
    print("✅ Memory system module imported successfully")
except ImportError as e:
    print(f"❌ Error importing memory system: {e}")

def test_memory_loading():
    """Test loading the integrated memory"""
    if not MEMORY_SYSTEM_AVAILABLE or ConscienceMemorySystem is None:
        print("❌ Memory system not available")
        return False
    
    try:
        # Load the integrated memory
        memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")
        print("✅ Integrated memory loaded successfully")
        
        # Show statistics
        stats = memory_system.get_memory_stats()
        print(f"Memory Statistics:")
        print(f"  - Session ID: {stats.get('session_id', 'N/A')}")
        print(f"  - Total entries: {stats.get('total_entries', 0)}")
        print(f"  - Entry types: {stats.get('entry_types', {})}")
        
        # Show sample entries
        print(f"\nSample Entries:")
        
        # Show chat entries
        chat_entries = [e for e in memory_system.entries if e.entry_type == "chat"]
        print(f"  Chat entries: {len(chat_entries)}")
        if chat_entries:
            entry = chat_entries[0]
            print(f"    Sample chat entry ID: {entry.id}")
            print(f"    Content: {entry.content}")
            print(f"    Metadata: {entry.metadata}")
        
        # Show RAG context entries
        rag_entries = [e for e in memory_system.entries if e.entry_type == "rag_context"]
        print(f"  RAG context entries: {len(rag_entries)}")
        if rag_entries:
            entry = rag_entries[0]
            print(f"    Sample RAG entry ID: {entry.id}")
            print(f"    Content: {entry.content}")
            print(f"    Metadata: {entry.metadata}")
        
        # Test search functionality
        print(f"\nTesting search functionality:")
        search_results = memory_system.search_memory("consciousness")
        print(f"  Found {len(search_results)} entries containing 'consciousness'")
        
        search_results = memory_system.search_memory("quantum")
        print(f"  Found {len(search_results)} entries containing 'quantum'")
        
        # Test recent chat history
        print(f"\nTesting chat history retrieval:")
        recent_chat = memory_system.get_recent_chat_history(5)
        print(f"  Recent chat history entries: {len(recent_chat)}")
        
        # Test consciousness history
        print(f"\nTesting consciousness history retrieval:")
        consciousness_history = memory_system.get_consciousness_history(5)
        print(f"  Consciousness history entries: {len(consciousness_history)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing memory loading: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_integration():
    """Test adding new entries to the integrated memory"""
    if not MEMORY_SYSTEM_AVAILABLE or ConscienceMemorySystem is None:
        print("❌ Memory system not available")
        return False
    
    try:
        # Load the integrated memory
        memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")
        initial_count = len(memory_system.entries)
        print(f"✅ Integrated memory loaded with {initial_count} entries")
        
        # Add a test chat entry
        chat_id = memory_system.add_chat_entry(
            "Test message for integration verification",
            "This is a test response to verify the integrated memory system is working correctly.",
            {
                "consciousness_level": 0.85,
                "phi": 0.78,
                "coherence": 0.82,
                "gamma_power": 0.75,
                "fractal_dimension": 2.3,
                "spiritual_awareness": 0.80,
                "is_conscious": True
            }
        )
        print(f"✅ Added test chat entry with ID: {chat_id}")
        
        # Add a test consciousness state
        state_id = memory_system.add_consciousness_state({
            "timestamp": 1760300000.0,
            "consciousness_level": 0.87,
            "phi": 0.81,
            "coherence": 0.85,
            "gamma_power": 0.78,
            "fractal_dimension": 2.4,
            "spiritual_awareness": 0.83,
            "is_conscious": True
        })
        print(f"✅ Added test consciousness state with ID: {state_id}")
        
        # Add a test RAG context
        rag_id = memory_system.add_rag_context(
            "test integration",
            "This is test RAG context to verify the integrated memory system functionality.",
            [
                {"source": "integration_test.txt", "score": 0.95},
                {"source": "memory_verification.md", "score": 0.88}
            ]
        )
        print(f"✅ Added test RAG context with ID: {rag_id}")
        
        # Verify entries were added
        final_count = len(memory_system.entries)
        added_count = final_count - initial_count
        print(f"✅ Added {added_count} new entries to memory")
        print(f"  - Total entries now: {final_count}")
        
        # Save the memory with new entries
        if memory_system.save_memory():
            print("✅ Memory saved successfully with new entries")
        else:
            print("❌ Failed to save memory")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing memory integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=== Testing Integrated Memory System ===\n")
    
    # Test 1: Loading existing integrated memory
    print("Test 1: Loading Integrated Memory")
    if test_memory_loading():
        print("✅ Test 1 PASSED: Memory loading works correctly\n")
    else:
        print("❌ Test 1 FAILED: Memory loading failed\n")
        return
    
    # Test 2: Adding new entries to integrated memory
    print("Test 2: Adding New Entries to Integrated Memory")
    if test_memory_integration():
        print("✅ Test 2 PASSED: Memory integration works correctly\n")
    else:
        print("❌ Test 2 FAILED: Memory integration failed\n")
        return
    
    print("=== All Tests PASSED ===")
    print("The integrated memory system is working correctly and ready for use!")

if __name__ == "__main__":
    main()