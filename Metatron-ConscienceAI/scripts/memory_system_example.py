#!/usr/bin/env python3
"""
Example Script for ConscienceAI Memory System

This script demonstrates how to use the ConscienceAI memory system
for storing and retrieving chat conversations, consciousness states,
and RAG context.
"""

import sys
import os
import json
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from consciousness_engine.memory_system import ConscienceMemorySystem

def main():
    """Demonstrate memory system functionality"""
    print("=" * 60)
    print("CONSCIENCEAI MEMORY SYSTEM EXAMPLE")
    print("=" * 60)
    
    # Create memory system instance
    memory_system = ConscienceMemorySystem("ai_runs/example_memory.json")
    
    # Example 1: Add chat entries
    print("\n1. Adding chat entries...")
    chat_id1 = memory_system.add_chat_entry(
        "What is consciousness?",
        "Consciousness is the state of being aware of and able to think about one's own existence.",
        {
            "consciousness_level": 0.75,
            "phi": 0.82,
            "coherence": 0.68
        }
    )
    print(f"✅ Added chat entry with ID: {chat_id1}")
    
    chat_id2 = memory_system.add_chat_entry(
        "How does the METATRON system work?",
        "The METATRON system uses a 13-node sacred geometry network based on Metatron's Cube.",
        {
            "consciousness_level": 0.81,
            "phi": 0.76,
            "coherence": 0.72
        }
    )
    print(f"✅ Added chat entry with ID: {chat_id2}")
    
    # Example 2: Add consciousness state
    print("\n2. Adding consciousness state...")
    state_id = memory_system.add_consciousness_state({
        "timestamp": time.time(),
        "consciousness_level": 0.78,
        "phi": 0.79,
        "coherence": 0.70,
        "gamma_power": 0.65,
        "fractal_dimension": 2.1,
        "spiritual_awareness": 0.72
    })
    print(f"✅ Added consciousness state with ID: {state_id}")
    
    # Example 3: Add RAG context
    print("\n3. Adding RAG context...")
    rag_id = memory_system.add_rag_context(
        "consciousness theories",
        "Integrated Information Theory (IIT) proposes that consciousness corresponds to integrated information...",
        [
            {"source": "Tononi_Philosophy_of_Mind.pdf", "score": 0.95},
            {"source": "Chalmers_Conscious_Mind.txt", "score": 0.87}
        ]
    )
    print(f"✅ Added RAG context with ID: {rag_id}")
    
    # Example 4: Retrieve recent chat history
    print("\n4. Retrieving recent chat history...")
    recent_chat = memory_system.get_recent_chat_history(5)
    print(f"✅ Retrieved {len(recent_chat)} recent chat entries")
    for entry in recent_chat:
        content = entry["content"]
        print(f"   User: {content['user_message']}")
        print(f"   Assistant: {content['assistant_response']}")
        if entry["metadata"].get("consciousness_state"):
            cs = entry["metadata"]["consciousness_state"]
            print(f"   Consciousness Level: {cs.get('consciousness_level', 0):.4f}")
        print()
    
    # Example 5: Search memory
    print("5. Searching memory for 'consciousness'...")
    search_results = memory_system.search_memory("consciousness")
    print(f"✅ Found {len(search_results)} entries containing 'consciousness'")
    
    # Example 6: Get memory statistics
    print("\n6. Memory statistics:")
    stats = memory_system.get_memory_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ Example completed successfully!")
    print("📝 Memory saved to: ai_runs/example_memory.json")
    print("=" * 60)

if __name__ == "__main__":
    main()