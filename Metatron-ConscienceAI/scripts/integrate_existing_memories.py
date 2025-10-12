#!/usr/bin/env python3
"""
Script to Integrate Existing Memories into ConscienceAI-METATRONV2 System

This script loads existing data from the ai_chat_es_pdf_full directory and integrates
it into the ConscienceAI memory system for use with the METATRONV2 consciousness engine.

The script processes:
1. Existing memory.json file with chat/consciousness data
2. RSS research papers on AI and consciousness
3. PDF QA pairs with quantum physics and unified field theory content
4. Sample quantum math content

This integration enables the chatbot to have enhanced context awareness and knowledge.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List, Optional
import uuid

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the memory system
MEMORY_SYSTEM_AVAILABLE = False
ConscienceMemorySystem = None
MemoryEntry = None

try:
    from consciousness_engine.memory_system import ConscienceMemorySystem, MemoryEntry
    MEMORY_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Error: Memory system not available: {e}")

def load_json_file(file_path: str) -> Optional[Dict]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_jsonl_file(file_path: str) -> List[Dict]:
    """Load JSONL file (one JSON object per line)"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    if line.strip():
                        results.append(json.loads(line.strip()))
                except Exception as e:
                    print(f"Warning: Skipping invalid JSON on line {line_num} in {file_path}: {e}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    
    print(f"Loaded {len(results)} entries from {file_path}")
    return results

def integrate_existing_memory(memory_system, 
                            memory_file: str = "ai_chat_es_pdf_full/memory.json") -> int:
    """Integrate existing memory entries from memory.json"""
    print("Integrating existing memory entries...")
    
    # Check if MemoryEntry is available
    if MemoryEntry is None:
        print("MemoryEntry class not available, skipping integration")
        return 0
    
    existing_memory = load_json_file(memory_file)
    if not existing_memory:
        print("No existing memory file found or error loading it")
        return 0
    
    integrated_count = 0
    
    # Process existing entries
    for entry_data in existing_memory.get("entries", []):
        try:
            entry = MemoryEntry.from_dict(entry_data)
            memory_system.entries.append(entry)
            integrated_count += 1
        except Exception as e:
            print(f"Warning: Failed to integrate entry {entry_data.get('id', 'unknown')}: {e}")
    
    print(f"Integrated {integrated_count} existing memory entries")
    return integrated_count

def integrate_rss_research(memory_system, 
                          rss_file: str = "ai_chat_es_pdf_full/rss_research.jsonl") -> int:
    """Integrate RSS research papers as RAG context"""
    print("Integrating RSS research papers...")
    
    # Check if MemoryEntry is available
    if MemoryEntry is None:
        print("MemoryEntry class not available, skipping integration")
        return 0
    
    research_papers = load_jsonl_file(rss_file)
    integrated_count = 0
    
    for paper in research_papers:
        try:
            # Create RAG context entry for each research paper
            title = paper.get("title", "Untitled Research Paper")
            summary = paper.get("summary", "")
            link = paper.get("link", "")
            
            # Extract key information for metadata
            topics = paper.get("topics", [])
            published = paper.get("published", "")
            
            content = {
                "title": title,
                "summary": summary,
                "link": link,
                "type": "research_paper"
            }
            
            metadata = {
                "source": "rss_research",
                "topics": topics,
                "published": published,
                "ingested_at": paper.get("ingested_at", time.time()),
                "priority": paper.get("source_priority", "normal")
            }
            
            entry = MemoryEntry("rag_context", content, metadata)
            memory_system.entries.append(entry)
            integrated_count += 1
            
            # Limit to first 100 papers to avoid overwhelming the system
            if integrated_count >= 100:
                print(f"Limiting to first 100 papers for performance")
                break
                
        except Exception as e:
            print(f"Warning: Failed to integrate research paper: {e}")
    
    print(f"Integrated {integrated_count} RSS research papers")
    return integrated_count

def integrate_pdf_qa_pairs(memory_system,
                          qa_file: str = "ai_chat_es_pdf_full/pdf_es_qa.jsonl") -> int:
    """Integrate PDF QA pairs as RAG context"""
    print("Integrating PDF QA pairs...")
    
    # Check if MemoryEntry is available
    if MemoryEntry is None:
        print("MemoryEntry class not available, skipping integration")
        return 0
    
    qa_pairs = load_jsonl_file(qa_file)
    integrated_count = 0
    
    for qa in qa_pairs:
        try:
            instruction = qa.get("instruction", "")
            input_text = qa.get("input", "")
            response = qa.get("response", "")
            
            # Combine instruction and input for the query
            query = f"{instruction}\n\n{input_text}" if input_text else instruction
            
            content = {
                "query": query,
                "response": response,
                "type": "qa_pair"
            }
            
            metadata = {
                "source": "pdf_qa",
                "integrated_at": time.time(),
                "entry_type": "educational_content"
            }
            
            entry = MemoryEntry("rag_context", content, metadata)
            memory_system.entries.append(entry)
            integrated_count += 1
            
            # Limit to first 200 QA pairs to avoid overwhelming the system
            if integrated_count >= 200:
                print(f"Limiting to first 200 QA pairs for performance")
                break
                
        except Exception as e:
            print(f"Warning: Failed to integrate QA pair: {e}")
    
    print(f"Integrated {integrated_count} PDF QA pairs")
    return integrated_count

def integrate_quantum_math_content(memory_system,
                                 math_file: str = "ai_chat_es_pdf_full/sample_quantum_math_es.jsonl") -> int:
    """Integrate quantum math content as educational context"""
    print("Integrating quantum math content...")
    
    # Check if MemoryEntry is available
    if MemoryEntry is None:
        print("MemoryEntry class not available, skipping integration")
        return 0
    
    math_content = load_jsonl_file(math_file)
    integrated_count = 0
    
    for item in math_content:
        try:
            instruction = item.get("instruction", "")
            response = item.get("response", "")
            
            content = {
                "topic": instruction,
                "explanation": response,
                "type": "educational_content"
            }
            
            metadata = {
                "source": "quantum_math",
                "integrated_at": time.time(),
                "category": "physics_mathematics"
            }
            
            entry = MemoryEntry("rag_context", content, metadata)
            memory_system.entries.append(entry)
            integrated_count += 1
                
        except Exception as e:
            print(f"Warning: Failed to integrate math content: {e}")
    
    print(f"Integrated {integrated_count} quantum math entries")
    return integrated_count

def add_system_knowledge_entries(memory_system) -> int:
    """Add key system knowledge about the METATRONV2 and ConscienceAI integration"""
    print("Adding system knowledge entries...")
    
    # Check if MemoryEntry is available
    if MemoryEntry is None:
        print("MemoryEntry class not available, skipping integration")
        return 0
    
    knowledge_entries = [
        {
            "topic": "METATRONV2 Consciousness Engine",
            "content": "METATRONV2 is a consciousness engine based on a 13-node sacred geometry network implementing integrated information theory (IIT) with phi-based harmonic resonance principles. It measures consciousness through metrics like Φ (integrated information), coherence, and gamma power.",
            "type": "system_knowledge"
        },
        {
            "topic": "ConscienceAI Memory System",
            "content": "ConscienceAI uses a persistent memory system that stores chat conversations, consciousness state metrics, and RAG context. Memory entries are categorized by type (chat, consciousness_state, rag_context) and can be searched for context-aware responses.",
            "type": "system_knowledge"
        },
        {
            "topic": "Harmonic Resonance Principles",
            "content": "The unified field theory implemented in this system proposes that mass, consciousness, and reality emerge from structured harmonic vacuum dynamics. The Golden Ratio (φ) governs recursive feedback in the electromagnetic resonance field that constitutes space itself.",
            "type": "system_knowledge"
        }
    ]
    
    integrated_count = 0
    for knowledge in knowledge_entries:
        try:
            content = {
                "topic": knowledge["topic"],
                "content": knowledge["content"],
                "type": knowledge["type"]
            }
            
            metadata = {
                "source": "system_knowledge",
                "integrated_at": time.time(),
                "category": "foundational_principles"
            }
            
            entry = MemoryEntry("rag_context", content, metadata)
            memory_system.entries.append(entry)
            integrated_count += 1
        except Exception as e:
            print(f"Warning: Failed to add system knowledge entry: {e}")
    
    print(f"Added {integrated_count} system knowledge entries")
    return integrated_count

def main():
    """Main function to integrate all existing memories"""
    print("=== ConscienceAI-METATRONV2 Memory Integration Script ===")
    print("Loading existing memories from ai_chat_es_pdf_full directory...\n")
    
    # Initialize memory system
    if not MEMORY_SYSTEM_AVAILABLE or not ConscienceMemorySystem or MemoryEntry is None:
        print("❌ Memory system not available. Cannot proceed with integration.")
        return
    
    try:
        # Create memory system instance
        memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")
        print("✅ Memory system initialized successfully")
        
        # Track integration statistics
        stats = {
            "existing_memory": 0,
            "rss_research": 0,
            "pdf_qa": 0,
            "quantum_math": 0,
            "system_knowledge": 0,
            "total": 0
        }
        
        # Integrate different types of content
        stats["existing_memory"] = integrate_existing_memory(memory_system)
        stats["rss_research"] = integrate_rss_research(memory_system)
        stats["pdf_qa"] = integrate_pdf_qa_pairs(memory_system)
        stats["quantum_math"] = integrate_quantum_math_content(memory_system)
        stats["system_knowledge"] = add_system_knowledge_entries(memory_system)
        
        # Calculate total
        stats["total"] = sum(stats.values())
        
        # Save integrated memory
        print("\nSaving integrated memory...")
        if memory_system.save_memory():
            print("✅ Integrated memory saved successfully")
        else:
            print("❌ Failed to save integrated memory")
            return
        
        # Display final statistics
        print("\n=== Integration Complete ===")
        print(f"Total entries integrated: {stats['total']}")
        print(f"  - Existing memory entries: {stats['existing_memory']}")
        print(f"  - RSS research papers: {stats['rss_research']}")
        print(f"  - PDF QA pairs: {stats['pdf_qa']}")
        print(f"  - Quantum math content: {stats['quantum_math']}")
        print(f"  - System knowledge: {stats['system_knowledge']}")
        
        # Show memory stats
        memory_stats = memory_system.get_memory_stats()
        print(f"\nMemory system statistics:")
        print(f"  - Session ID: {memory_stats.get('session_id', 'N/A')}")
        print(f"  - Total entries: {memory_stats.get('total_entries', 0)}")
        print(f"  - Entry types: {memory_stats.get('entry_types', {})}")
        
        print("\n✅ Memory integration completed successfully!")
        print("The integrated memory is now available for use with the chat system.")
        
    except Exception as e:
        print(f"❌ Error during memory integration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()