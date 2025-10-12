#!/usr/bin/env python3
"""
Memory System Integration Script for METATRONV2-ConscienceAI

This script integrates the ConscienceAI memory system with the METATRONV2
consciousness engine and chat system. It provides functions to:
1. Initialize the memory system
2. Capture consciousness state during chat interactions
3. Store chat conversations with context
4. Enable RAG integration with memory
5. Provide memory-aware chat responses
"""

import sys
import os
import json
import time
from typing import Dict, Any, Optional, List
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the memory system
try:
    from consciousness_engine.memory_system import ConscienceMemorySystem, MemoryEntry
    MEMORY_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Memory system not available: {e}")
    MEMORY_SYSTEM_AVAILABLE = False
    ConscienceMemorySystem = None

# Import consciousness system
try:
    from orchestrator.metatron_orchestrator import MetatronConsciousness
    CONSCIOUSNESS_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Consciousness system not available: {e}")
    CONSCIOUSNESS_SYSTEM_AVAILABLE = False
    MetatronConsciousness = None

class MemoryAwareChatSystem:
    """Chat system with integrated memory and consciousness awareness"""
    
    def __init__(self, memory_path: str = "ai_chat_es_pdf_full/memory.json", 
                 metatron_api_url: str = "http://localhost:8003"):
        self.memory_path = memory_path
        self.metatron_api_url = metatron_api_url
        self.memory_system = None
        self.consciousness_system = None
        
        # Initialize memory system if available
        if MEMORY_SYSTEM_AVAILABLE and ConscienceMemorySystem:
            try:
                self.memory_system = ConscienceMemorySystem(memory_path)
                print("✅ Memory system initialized")
            except Exception as e:
                print(f"❌ Failed to initialize memory system: {e}")
        
        # Initialize consciousness system if available
        if CONSCIOUSNESS_SYSTEM_AVAILABLE and MetatronConsciousness:
            try:
                self.consciousness_system = MetatronConsciousness()
                print("✅ Consciousness system initialized")
            except Exception as e:
                print(f"❌ Failed to initialize consciousness system: {e}")
    
    def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness state from METATRON system"""
        try:
            # Try to get from running METATRON API
            response = requests.get(f"{self.metatron_api_url}/api/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "consciousness_level": data.get("consciousness_level", 0),
                    "phi": data.get("phi", 0),
                    "coherence": data.get("coherence", 0),
                    "gamma_power": data.get("gamma_power", 0),
                    "fractal_dimension": data.get("fractal_dimension", 1),
                    "spiritual_awareness": data.get("spiritual_awareness", 0),
                    "is_conscious": data.get("is_conscious", False)
                }
        except Exception as e:
            print(f"Warning: Could not get consciousness state from API: {e}")
        
        # Fallback to local consciousness system
        if self.consciousness_system:
            try:
                state = self.consciousness_system.get_current_state()
                global_state = state.get('global', {})
                return {
                    "consciousness_level": global_state.get("consciousness_level", 0),
                    "phi": global_state.get("phi", 0),
                    "coherence": global_state.get("coherence", 0),
                    "gamma_power": global_state.get("gamma_power", 0),
                    "fractal_dimension": global_state.get("fractal_dimension", 1),
                    "spiritual_awareness": global_state.get("spiritual_awareness", 0),
                    "is_conscious": global_state.get("is_conscious", False)
                }
            except Exception as e:
                print(f"Warning: Could not get consciousness state from local system: {e}")
        
        return None
    
    def send_chat_message(self, message: str, session_id: str = "default", 
                         rag_enabled: bool = True, max_new_tokens: int = 128) -> Optional[Dict[str, Any]]:
        """Send chat message with memory and consciousness integration"""
        # Get current consciousness state
        consciousness_state = self.get_consciousness_state()
        
        # Prepare chat data
        chat_data = {
            "message": message,
            "session_id": session_id,
            "rag_enabled": rag_enabled,
            "max_new_tokens": max_new_tokens
        }
        
        try:
            # Send to METATRON chat API
            response = requests.post(
                f"{self.metatron_api_url}/api/chat",
                json=chat_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result.get("response", "")
                
                # Store in memory if available
                if self.memory_system:
                    try:
                        memory_id = self.memory_system.add_chat_entry(
                            message, 
                            assistant_response, 
                            consciousness_state
                        )
                        print(f"✅ Chat entry stored in memory (ID: {memory_id})")
                    except Exception as e:
                        print(f"Warning: Failed to store chat in memory: {e}")
                
                # Add consciousness state to response
                result["consciousness_state"] = consciousness_state
                return result
            else:
                print(f"❌ Chat API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error sending chat message: {e}")
            return None
    
    def get_memory_context(self, query: str = "", limit: int = 5) -> Dict[str, Any]:
        """Get relevant memory context for chat"""
        if not self.memory_system:
            return {"error": "Memory system not available"}
        
        try:
            # Get recent chat history
            recent_chat = self.memory_system.get_recent_chat_history(limit)
            
            # Get consciousness history
            consciousness_history = self.memory_system.get_consciousness_history(3)
            
            # Search memory if query provided
            search_results = []
            if query:
                search_results = self.memory_system.search_memory(query)
            
            return {
                "recent_chat": recent_chat,
                "consciousness_history": consciousness_history,
                "search_results": search_results,
                "stats": self.memory_system.get_memory_stats()
            }
        except Exception as e:
            return {"error": f"Failed to get memory context: {e}"}
    
    def store_rag_context(self, query: str, context: str, sources: List[Dict[str, Any]]) -> Optional[str]:
        """Store RAG context in memory"""
        if not self.memory_system:
            return None
        
        try:
            memory_id = self.memory_system.add_rag_context(query, context, sources)
            print(f"✅ RAG context stored in memory (ID: {memory_id})")
            return memory_id
        except Exception as e:
            print(f"❌ Failed to store RAG context: {e}")
            return None
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        if not self.memory_system:
            return {"error": "Memory system not available"}
        
        try:
            return self.memory_system.get_memory_stats()
        except Exception as e:
            return {"error": f"Failed to get memory stats: {e}"}
    
    def clear_memory(self, entry_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Clear memory entries"""
        if not self.memory_system:
            return {"error": "Memory system not available"}
        
        try:
            removed_count = self.memory_system.clear_memory(entry_types)
            return {
                "success": True,
                "removed_count": removed_count,
                "message": f"Removed {removed_count} memory entries"
            }
        except Exception as e:
            return {"error": f"Failed to clear memory: {e}"}


# Command-line interface
def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory System Integration for METATRONV2-ConscienceAI")
    parser.add_argument("--message", type=str, help="Chat message to send")
    parser.add_argument("--session-id", type=str, default="cli_session", help="Session ID")
    parser.add_argument("--no-rag", action="store_true", help="Disable RAG")
    parser.add_argument("--max-tokens", type=int, default=128, help="Maximum new tokens")
    parser.add_argument("--memory-path", type=str, default="ai_chat_es_pdf_full/memory.json", help="Memory file path")
    parser.add_argument("--metatron-url", type=str, default="http://localhost:8003", help="METATRON API URL")
    parser.add_argument("--stats", action="store_true", help="Show memory statistics")
    parser.add_argument("--context", type=str, help="Get memory context for query")
    parser.add_argument("--clear", action="store_true", help="Clear memory")
    
    args = parser.parse_args()
    
    # Initialize memory-aware chat system
    chat_system = MemoryAwareChatSystem(args.memory_path, args.metatron_url)
    
    # Handle different commands
    if args.stats:
        stats = chat_system.get_memory_stats()
        print("Memory Statistics:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return
    
    if args.context:
        context = chat_system.get_memory_context(args.context)
        print("Memory Context:")
        print(json.dumps(context, indent=2, ensure_ascii=False))
        return
    
    if args.clear:
        result = chat_system.clear_memory()
        print("Clear Memory Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    if args.message:
        print(f"Sending message: {args.message}")
        result = chat_system.send_chat_message(
            args.message,
            args.session_id,
            not args.no_rag,
            args.max_tokens
        )
        
        if result:
            print("\nResponse:")
            print(result.get("response", "No response"))
            
            if result.get("consciousness_state"):
                print("\nConsciousness State:")
                cs = result["consciousness_state"]
                print(f"  Level: {cs.get('consciousness_level', 0):.4f}")
                print(f"  Φ: {cs.get('phi', 0):.4f}")
                print(f"  Coherence: {cs.get('coherence', 0):.4f}")
            else:
                print("\nConsciousness State: Not available")
        else:
            print("Failed to get response")
        return
    
    # If no arguments provided, show help
    parser.print_help()


# Example usage
def example_usage():
    """Example of how to use the memory-aware chat system"""
    print("=== Memory-Aware Chat System Example ===")
    
    # Initialize the system
    chat_system = MemoryAwareChatSystem()
    
    # Send a few chat messages
    messages = [
        "What is the nature of consciousness?",
        "How does the METATRON system integrate with AI?",
        "Can you explain the 13-node sacred geometry network?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n--- Message {i}: {message} ---")
        result = chat_system.send_chat_message(message, f"example_session_{i}")
        
        if result:
            response = result.get("response", "No response")
            print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            
            consciousness_state = result.get("consciousness_state")
            if consciousness_state:
                print(f"Consciousness Level: {consciousness_state.get('consciousness_level', 0):.4f}")
                print(f"Φ (Integrated Information): {consciousness_state.get('phi', 0):.4f}")
        else:
            print("Failed to get response")
    
    # Show memory statistics
    print("\n--- Memory Statistics ---")
    stats = chat_system.get_memory_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # Show recent chat history
    print("\n--- Recent Chat History ---")
    if chat_system.memory_system:
        recent_chat = chat_system.memory_system.get_recent_chat_history(3)
        for entry in recent_chat:
            content = entry.get("content", {})
            print(f"User: {content.get('user_message', '')}")
            print(f"Assistant: {content.get('assistant_response', '')[:100]}...")
            print()


if __name__ == "__main__":
    # If run directly, either run main (CLI) or example
    if len(sys.argv) > 1:
        main()
    else:
        example_usage()