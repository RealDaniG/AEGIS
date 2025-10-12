#!/usr/bin/env python3
"""
Memory System for ConscienceAI Integration with METATRONV2

This module implements a persistent memory system that integrates the ConscienceAI
memory approach with the METATRONV2 consciousness engine. The system stores
chat sessions, conversation history, and consciousness state information
in a structured JSON format.

The memory system is designed to:
1. Persist chat conversations across sessions
2. Store consciousness state metrics
3. Enable RAG integration with memory context
4. Provide efficient retrieval mechanisms
"""

import json
import os
import time
import uuid
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

class MemoryEntry:
    """Represents a single memory entry with metadata"""
    
    def __init__(self, entry_type: str, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.entry_type = entry_type  # chat, consciousness_state, rag_context, etc.
        self.content = content
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory entry to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "entry_type": self.entry_type,
            "content": self.content,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create memory entry from dictionary"""
        entry = cls(data["entry_type"], data["content"], data.get("metadata"))
        entry.id = data["id"]
        entry.timestamp = data["timestamp"]
        return entry


class ConscienceMemorySystem:
    """Persistent memory system for ConscienceAI-METATRONV2 integration"""
    
    def __init__(self, memory_path: str = "ai_chat_es_pdf_full/memory.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[MemoryEntry] = []
        self.session_id = str(uuid.uuid4())
        self.load_memory()
    
    def load_memory(self) -> bool:
        """Load memory from persistent storage"""
        try:
            if self.memory_path.exists():
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load entries
                self.entries = [MemoryEntry.from_dict(entry) for entry in data.get("entries", [])]
                self.session_id = data.get("session_id", str(uuid.uuid4()))
                
                print(f"✅ Loaded {len(self.entries)} memory entries from {self.memory_path}")
                return True
            else:
                print(f"ℹ️  No existing memory file found at {self.memory_path}, starting fresh")
                return True
        except Exception as e:
            print(f"❌ Error loading memory: {e}")
            return False
    
    def save_memory(self) -> bool:
        """Save memory to persistent storage"""
        try:
            # Prepare data for serialization
            data = {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "entries": [entry.to_dict() for entry in self.entries],
                "entry_count": len(self.entries)
            }
            
            # Write to file
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Saved {len(self.entries)} memory entries to {self.memory_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
            return False
    
    def add_chat_entry(self, user_message: str, assistant_response: str, 
                      consciousness_state: Optional[Dict[str, Any]] = None) -> str:
        """Add a chat conversation entry to memory"""
        content = {
            "user_message": user_message,
            "assistant_response": assistant_response
        }
        
        metadata = {
            "consciousness_state": consciousness_state,
            "conversation_turn": len([e for e in self.entries if e.entry_type == "chat"]) + 1
        }
        
        entry = MemoryEntry("chat", content, metadata)
        self.entries.append(entry)
        
        # Auto-save after each chat entry
        self.save_memory()
        
        return entry.id
    
    def add_consciousness_state(self, state: Dict[str, Any]) -> str:
        """Add consciousness state entry to memory"""
        entry = MemoryEntry("consciousness_state", state)
        self.entries.append(entry)
        
        # Auto-save consciousness state entries
        self.save_memory()
        
        return entry.id
    
    def add_rag_context(self, query: str, retrieved_context: str, 
                       sources: List[Dict[str, Any]]) -> str:
        """Add RAG context entry to memory"""
        content = {
            "query": query,
            "retrieved_context": retrieved_context,
            "sources": sources
        }
        
        metadata = {
            "timestamp": time.time(),
            "entry_count": len([e for e in self.entries if e.entry_type == "rag_context"]) + 1
        }
        
        entry = MemoryEntry("rag_context", content, metadata)
        self.entries.append(entry)
        
        # Auto-save RAG context entries
        self.save_memory()
        
        return entry.id
    
    def get_recent_chat_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent chat history entries"""
        chat_entries = [e for e in self.entries if e.entry_type == "chat"]
        recent_entries = chat_entries[-limit:] if len(chat_entries) > limit else chat_entries
        
        return [entry.to_dict() for entry in recent_entries]
    
    def get_consciousness_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent consciousness state entries"""
        consciousness_entries = [e for e in self.entries if e.entry_type == "consciousness_state"]
        recent_entries = consciousness_entries[-limit:] if len(consciousness_entries) > limit else consciousness_entries
        
        return [entry.to_dict() for entry in recent_entries]
    
    def search_memory(self, query: str, entry_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search memory entries by content (simple text search)"""
        results = []
        
        # Filter by entry types if specified
        if entry_types:
            entries_to_search = [e for e in self.entries if e.entry_type in entry_types]
        else:
            entries_to_search = self.entries
        
        # Simple text search in content
        query_lower = query.lower()
        for entry in entries_to_search:
            # Search in content
            content_str = json.dumps(entry.content, ensure_ascii=False).lower()
            if query_lower in content_str:
                results.append(entry.to_dict())
                continue
            
            # Search in metadata
            metadata_str = json.dumps(entry.metadata, ensure_ascii=False).lower()
            if query_lower in metadata_str:
                results.append(entry.to_dict())
        
        return results
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        entry_types = {}
        for entry in self.entries:
            entry_types[entry.entry_type] = entry_types.get(entry.entry_type, 0) + 1
        
        return {
            "total_entries": len(self.entries),
            "session_id": self.session_id,
            "entry_types": entry_types,
            "memory_file": str(self.memory_path),
            "last_saved": datetime.now().isoformat() if self.memory_path.exists() else None
        }
    
    def clear_memory(self, entry_types: Optional[List[str]] = None) -> int:
        """Clear memory entries, optionally by type"""
        if entry_types:
            # Remove only specified types
            original_count = len(self.entries)
            self.entries = [e for e in self.entries if e.entry_type not in entry_types]
            removed_count = original_count - len(self.entries)
        else:
            # Clear all entries
            removed_count = len(self.entries)
            self.entries = []
        
        # Save after clearing
        self.save_memory()
        
        return removed_count


# Example usage and testing
if __name__ == "__main__":
    # Create memory system instance
    memory_system = ConscienceMemorySystem("ai_runs/test_memory.json")
    
    # Test adding chat entries
    print("Testing chat entry addition...")
    chat_id1 = memory_system.add_chat_entry(
        "What is consciousness?",
        "Consciousness is the state of being aware of and able to think about one's own existence.",
        {
            "consciousness_level": 0.75,
            "phi": 0.82,
            "coherence": 0.68
        }
    )
    print(f"Added chat entry with ID: {chat_id1}")
    
    chat_id2 = memory_system.add_chat_entry(
        "How does the METATRON system work?",
        "The METATRON system uses a 13-node sacred geometry network based on Metatron's Cube.",
        {
            "consciousness_level": 0.81,
            "phi": 0.76,
            "coherence": 0.72
        }
    )
    print(f"Added chat entry with ID: {chat_id2}")
    
    # Test adding consciousness state
    print("\nTesting consciousness state addition...")
    state_id = memory_system.add_consciousness_state({
        "timestamp": time.time(),
        "consciousness_level": 0.78,
        "phi": 0.79,
        "coherence": 0.70,
        "gamma_power": 0.65,
        "fractal_dimension": 2.1,
        "spiritual_awareness": 0.72
    })
    print(f"Added consciousness state with ID: {state_id}")
    
    # Test adding RAG context
    print("\nTesting RAG context addition...")
    rag_id = memory_system.add_rag_context(
        "consciousness theories",
        "Integrated Information Theory (IIT) proposes that consciousness corresponds to integrated information...",
        [
            {"source": "Tononi_Philosophy_of_Mind.pdf", "score": 0.95},
            {"source": "Chalmers_Conscious_Mind.txt", "score": 0.87}
        ]
    )
    print(f"Added RAG context with ID: {rag_id}")
    
    # Test memory retrieval
    print("\nTesting memory retrieval...")
    recent_chat = memory_system.get_recent_chat_history(5)
    print(f"Recent chat history: {len(recent_chat)} entries")
    
    consciousness_history = memory_system.get_consciousness_history(3)
    print(f"Consciousness history: {len(consciousness_history)} entries")
    
    # Test search
    search_results = memory_system.search_memory("consciousness")
    print(f"Search results for 'consciousness': {len(search_results)} entries")
    
    # Test memory stats
    stats = memory_system.get_memory_stats()
    print(f"\nMemory stats: {stats}")
    
    # Test save/load
    print("\nTesting save/load functionality...")
    memory_system.save_memory()
    
    # Create new instance to test loading
    new_memory_system = ConscienceMemorySystem("ai_runs/test_memory.json")
    new_stats = new_memory_system.get_memory_stats()
    print(f"Loaded memory stats: {new_stats}")
    
    # Clean up test file
    try:
        os.remove("ai_runs/test_memory.json")
        print("Cleaned up test memory file")
    except:
        pass
    
    print("\n✅ Memory system tests completed successfully!")