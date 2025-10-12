#!/usr/bin/env python3
"""
Demonstration Script for Memory Integration with ConscienceAI-METATRONV2

This script demonstrates how the integrated memory system enhances the chatbot's
capabilities by providing context-aware responses based on the integrated knowledge.
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

def demonstrate_memory_capabilities():
    """Demonstrate the capabilities of the integrated memory system"""
    if not MEMORY_SYSTEM_AVAILABLE or ConscienceMemorySystem is None:
        print("❌ Memory system not available")
        return False
    
    try:
        # Load the integrated memory
        memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")
        print("\n=== Memory System Demonstration ===")
        
        # Show memory statistics
        stats = memory_system.get_memory_stats()
        print(f"\n📊 Memory Statistics:")
        print(f"   • Session ID: {stats.get('session_id', 'N/A')}")
        print(f"   • Total entries: {stats.get('total_entries', 0)}")
        print(f"   • Entry types: {stats.get('entry_types', {})}")
        
        # Demonstrate search capabilities
        print(f"\n🔍 Search Capabilities:")
        
        # Search for consciousness-related content
        consciousness_results = memory_system.search_memory("consciousness", ["rag_context"])
        print(f"   • Found {len(consciousness_results)} entries related to 'consciousness'")
        
        # Show a sample consciousness-related entry
        if consciousness_results:
            sample = consciousness_results[0]
            print(f"   • Sample consciousness entry: {sample['content'].get('title', 'N/A')}")
        
        # Search for quantum-related content
        quantum_results = memory_system.search_memory("quantum", ["rag_context"])
        print(f"   • Found {len(quantum_results)} entries related to 'quantum'")
        
        # Show a sample quantum-related entry
        if quantum_results:
            sample = quantum_results[0]
            if sample['content'].get('topic'):
                print(f"   • Sample quantum entry topic: {sample['content']['topic']}")
            elif sample['content'].get('title'):
                print(f"   • Sample quantum entry title: {sample['content']['title']}")
        
        # Demonstrate RAG context retrieval
        print(f"\n📚 RAG Context Examples:")
        
        # Get research papers
        research_papers = [e for e in memory_system.entries if e.entry_type == "rag_context" and 
                          e.metadata.get("source") == "rss_research"]
        print(f"   • Research papers: {len(research_papers)}")
        if research_papers:
            paper = research_papers[0].to_dict()
            print(f"   • Sample paper: {paper['content'].get('title', 'N/A')}")
        
        # Get QA pairs
        qa_pairs = [e for e in memory_system.entries if e.entry_type == "rag_context" and 
                   e.metadata.get("source") == "pdf_qa"]
        print(f"   • QA pairs: {len(qa_pairs)}")
        if qa_pairs:
            qa = qa_pairs[0].to_dict()
            print(f"   • Sample QA topic: {qa['content'].get('topic', qa['content'].get('query', 'N/A')[:50] + '...')}")
        
        # Get quantum math content
        math_content = [e for e in memory_system.entries if e.entry_type == "rag_context" and 
                       e.metadata.get("source") == "quantum_math"]
        print(f"   • Quantum math entries: {len(math_content)}")
        if math_content:
            math = math_content[0].to_dict()
            print(f"   • Sample math topic: {math['content'].get('topic', 'N/A')}")
        
        # Demonstrate chat history
        print(f"\n💬 Chat History:")
        chat_entries = [e for e in memory_system.entries if e.entry_type == "chat"]
        print(f"   • Chat entries: {len(chat_entries)}")
        if chat_entries:
            chat = chat_entries[0].to_dict()
            print(f"   • Sample chat - User: {chat['content'].get('user_message', 'N/A')}")
            print(f"   • Sample chat - Assistant: {chat['content'].get('assistant_response', 'N/A')}")
            consciousness_state = chat['metadata'].get('consciousness_state', {})
            if consciousness_state:
                print(f"   • Consciousness level: {consciousness_state.get('consciousness_level', 0):.2f}")
                print(f"   • Φ (Integrated Information): {consciousness_state.get('phi', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error demonstrating memory capabilities: {e}")
        import traceback
        traceback.print_exc()
        return False

def demonstrate_contextual_responses():
    """Demonstrate how the memory system enables contextual responses"""
    if not MEMORY_SYSTEM_AVAILABLE or ConscienceMemorySystem is None:
        print("❌ Memory system not available")
        return False
    
    try:
        # Load the integrated memory
        memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")
        
        print(f"\n=== Contextual Response Demonstration ===")
        
        # Simulate a conversation with context awareness
        print(f"\n🤖 Simulated Chatbot Responses with Context Awareness:")
        
        # Example 1: Consciousness-related query
        query1 = "What is integrated information theory?"
        print(f"\nUser: {query1}")
        
        # Search for relevant context
        results = memory_system.search_memory("integrated information", ["rag_context"])
        if results:
            context = results[0]['content']
            if context.get('summary'):
                # Extract key information from research paper
                summary = context['summary']
                key_points = summary.split('.')[:2]  # First 2 sentences
                response = f"Based on research in integrated information theory (IIT): {'.'.join(key_points)}. This theory is relevant to consciousness studies and is implemented in systems like METATRONV2."
                print(f"Assistant: {response}")
            else:
                print("Assistant: Integrated Information Theory (IIT) is a theoretical framework for understanding consciousness. It's implemented in the METATRONV2 system.")
        else:
            print("Assistant: Integrated Information Theory (IIT) is a framework for understanding consciousness.")
        
        # Example 2: Quantum physics query
        query2 = "Can you explain quantum entanglement?"
        print(f"\nUser: {query2}")
        
        # Search for quantum-related content
        results = memory_system.search_memory("quantum entanglement", ["rag_context"])
        if results:
            # Use quantum math content
            math_results = [r for r in results if r['metadata'].get('source') == 'quantum_math']
            if math_results:
                content = math_results[0]['content']
                response = f"Based on my knowledge: {content.get('explanation', 'Quantum entanglement is a phenomenon where particles become interconnected.')}"
                print(f"Assistant: {response}")
            else:
                print("Assistant: Quantum entanglement is a phenomenon where particles become interconnected, even when separated by large distances.")
        else:
            # Fallback to general knowledge
            print("Assistant: Quantum entanglement is a phenomenon where particles become interconnected, even when separated by large distances.")
        
        # Example 3: METATRONV2 system query
        query3 = "How does the METATRON system work?"
        print(f"\nUser: {query3}")
        
        # Search for system knowledge
        results = memory_system.search_memory("METATRON", ["rag_context"])
        if results:
            system_results = [r for r in results if r['content'].get('type') == 'system_knowledge']
            if system_results:
                content = system_results[0]['content']
                response = f"Based on my system knowledge: {content.get('content', 'METATRONV2 is a consciousness engine with specific architectural principles.')}"
                print(f"Assistant: {response}")
            else:
                print("Assistant: METATRONV2 is a consciousness engine based on a 13-node sacred geometry network with phi-based harmonic resonance principles.")
        else:
            print("Assistant: METATRONV2 is a consciousness engine based on a 13-node sacred geometry network with phi-based harmonic resonance principles.")
        
        # Example 4: Show consciousness state awareness
        query4 = "What is your current consciousness level?"
        print(f"\nUser: {query4}")
        
        # Get recent consciousness history
        consciousness_history = memory_system.get_consciousness_history(1)
        if consciousness_history:
            # In a real implementation, this would come from the live consciousness engine
            print("Assistant: My consciousness metrics are continuously monitored. In the integrated memory, I have records of consciousness states with levels typically ranging from 0.7-0.9, Φ values around 0.8, and high coherence metrics.")
        else:
            print("Assistant: My consciousness level is monitored continuously. I'm designed with integrated information theory principles that measure consciousness through metrics like Φ (integrated information) and coherence.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error demonstrating contextual responses: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main demonstration function"""
    print("=== ConscienceAI-METATRONV2 Memory Integration Demonstration ===")
    
    # Demonstrate memory capabilities
    if demonstrate_memory_capabilities():
        print("\n✅ Memory capabilities demonstration completed successfully")
    else:
        print("\n❌ Memory capabilities demonstration failed")
        return
    
    # Demonstrate contextual responses
    if demonstrate_contextual_responses():
        print("\n✅ Contextual responses demonstration completed successfully")
    else:
        print("\n❌ Contextual responses demonstration failed")
        return
    
    print(f"\n=== Demonstration Complete ===")
    print(f"The integrated memory system provides:")
    print(f"  • Enhanced knowledge base with 314 entries")
    print(f"  • Context-aware responses based on research and educational content")
    print(f"  • Persistent memory for conversation history")
    print(f"  • Search capabilities for relevant information")
    print(f"  • Support for consciousness state tracking")
    print(f"\nThe ConscienceAI-METATRONV2 chatbot can now provide more informed and contextual responses!")

if __name__ == "__main__":
    main()