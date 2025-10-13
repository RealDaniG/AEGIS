#!/usr/bin/env python3
"""
Memory Integration Module for Open-A.G.I Framework

This module provides integration between the Open-A.G.I framework and 
the ConscienceAI-METATRONV2 memory system, enabling persistent memory 
storage and retrieval for distributed AI systems.

Author: AEGIS Framework
Date: 2025-10-13
"""

import sys
import os
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
import numpy as np

# Add Metatron-ConscienceAI to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
sys.path.insert(0, metatron_path)

# Import ConscienceAI memory system
MEMORY_SYSTEM_AVAILABLE = False
ConscienceMemorySystem = None
MemoryEntry = None

try:
    from consciousness_engine.memory_system import ConscienceMemorySystem, MemoryEntry
    MEMORY_SYSTEM_AVAILABLE = True
    logging.info("✅ ConscienceAI Memory System imported successfully")
except ImportError as e:
    logging.error(f"❌ Failed to import ConscienceAI Memory System: {e}")

# Import Open-A.G.I components
P2P_AVAILABLE = False
EnhancedP2PWrapper = None
NodeIdentity = None
SecureMessage = None
ConsensusEngine = None

try:
    from p2p_network import P2PNetwork  # Use the correct class name
    from crypto_framework import NodeIdentity, SecureMessage
    from consensus_algorithm import ConsensusEngine
    P2P_AVAILABLE = True
    logging.info("✅ Open-A.G.I components imported successfully")
except ImportError as e:
    logging.error(f"❌ Failed to import Open-A.G.I components: {e}")
    # Create placeholder classes
    class P2PNetwork:
        def __init__(self, *args, **kwargs):
            pass
        async def start_network(self):
            pass
        async def send_message(self, *args, **kwargs):
            return False
        def register_message_handler(self, *args, **kwargs):
            pass
    
    class NodeIdentity:
        def __init__(self, *args, **kwargs):
            pass
        def export_public_identity(self):
            return {"node_id": "open_agi_memory_node"}
    
    class SecureMessage:
        def __init__(self, *args, **kwargs):
            pass
    
    class ConsensusEngine:
        def __init__(self, *args, **kwargs):
            pass

class OpenAGIMemoryIntegration:
    """Integration between Open-A.G.I and ConscienceAI Memory System"""
    
    def __init__(self, memory_path: str = "ai_chat_es_pdf_full/memory.json"):
        """
        Initialize the memory integration
        
        Args:
            memory_path (str): Path to the memory storage file
        """
        self.memory_path = memory_path
        self.memory_system = None
        self.p2p_network = None
        self.node_identity = None
        self.consensus_engine = None
        
        # Initialize memory system if available
        if MEMORY_SYSTEM_AVAILABLE and ConscienceMemorySystem:
            try:
                self.memory_system = ConscienceMemorySystem(memory_path)
                logging.info("✅ ConscienceAI Memory System initialized")
            except Exception as e:
                logging.error(f"❌ Failed to initialize ConscienceAI Memory System: {e}")
                self.memory_system = None
        
        # Initialize P2P network if available
        if P2P_AVAILABLE and EnhancedP2PWrapper:
            try:
                self.p2p_network = EnhancedP2PWrapper(node_id="open_agi_memory_node", port=8282)
                logging.info("✅ P2P Network initialized")
            except Exception as e:
                logging.error(f"❌ Failed to initialize P2P Network: {e}")
                self.p2p_network = None
        
        # Register message handlers
        if self.p2p_network:
            self.p2p_network.register_message_handler("memory_share", self._handle_memory_share_request)
            self.p2p_network.register_message_handler("memory_sync", self._handle_memory_sync_request)
            self.p2p_network.register_message_handler("memory_query", self._handle_memory_query_request)
        
        logging.info("Open-A.G.I Memory Integration initialized")
    
    async def start_network(self):
        """Start the P2P network"""
        if self.p2p_network:
            try:
                await self.p2p_network.start_network()
                logging.info("✅ P2P Network started")
                return True
            except Exception as e:
                logging.error(f"❌ Failed to start P2P Network: {e}")
                return False
        return False
    
    def add_chat_entry(self, user_message: str, assistant_response: str, 
                      consciousness_state: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a chat conversation entry to memory
        
        Args:
            user_message (str): User's message
            assistant_response (str): Assistant's response
            consciousness_state (dict, optional): Consciousness state metrics
            
        Returns:
            str: Entry ID
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return ""
        
        try:
            entry_id = self.memory_system.add_chat_entry(
                user_message, assistant_response, consciousness_state
            )
            logging.info(f"Added chat entry with ID: {entry_id}")
            return entry_id
        except Exception as e:
            logging.error(f"Failed to add chat entry: {e}")
            return ""
    
    def add_consciousness_state(self, state: Dict[str, Any]) -> str:
        """
        Add consciousness state entry to memory
        
        Args:
            state (dict): Consciousness state metrics
            
        Returns:
            str: Entry ID
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return ""
        
        try:
            entry_id = self.memory_system.add_consciousness_state(state)
            logging.info(f"Added consciousness state with ID: {entry_id}")
            return entry_id
        except Exception as e:
            logging.error(f"Failed to add consciousness state: {e}")
            return ""
    
    def add_rag_context(self, query: str, retrieved_context: str, 
                       sources: List[Dict[str, Any]]) -> str:
        """
        Add RAG context entry to memory
        
        Args:
            query (str): Query that retrieved the context
            retrieved_context (str): Retrieved context
            sources (list): List of source information
            
        Returns:
            str: Entry ID
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return ""
        
        try:
            entry_id = self.memory_system.add_rag_context(query, retrieved_context, sources)
            logging.info(f"Added RAG context with ID: {entry_id}")
            return entry_id
        except Exception as e:
            logging.error(f"Failed to add RAG context: {e}")
            return ""
    
    def search_memory(self, query: str, entry_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search memory entries by content
        
        Args:
            query (str): Search query
            entry_types (list, optional): Entry types to search
            
        Returns:
            list: Search results
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return []
        
        try:
            results = self.memory_system.search_memory(query, entry_types)
            logging.info(f"Found {len(results)} memory entries for query: {query}")
            return results
        except Exception as e:
            logging.error(f"Failed to search memory: {e}")
            return []
    
    def get_recent_chat_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent chat history entries
        
        Args:
            limit (int): Maximum number of entries to retrieve
            
        Returns:
            list: Recent chat history
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return []
        
        try:
            history = self.memory_system.get_recent_chat_history(limit)
            logging.info(f"Retrieved {len(history)} chat history entries")
            return history
        except Exception as e:
            logging.error(f"Failed to get chat history: {e}")
            return []
    
    def get_consciousness_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent consciousness state entries
        
        Args:
            limit (int): Maximum number of entries to retrieve
            
        Returns:
            list: Recent consciousness history
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return []
        
        try:
            history = self.memory_system.get_consciousness_history(limit)
            logging.info(f"Retrieved {len(history)} consciousness history entries")
            return history
        except Exception as e:
            logging.error(f"Failed to get consciousness history: {e}")
            return []
    
    async def share_memory_with_peer(self, peer_id: str, entry_id: str) -> bool:
        """
        Share a memory entry with a specific peer
        
        Args:
            peer_id (str): Peer identifier
            entry_id (str): Memory entry ID
            
        Returns:
            bool: True if shared successfully
        """
        if not self.p2p_network or not self.memory_system:
            logging.warning("P2P network or memory system not available")
            return False
        
        try:
            # Find the memory entry
            entry = None
            for mem_entry in self.memory_system.entries:
                if mem_entry.id == entry_id:
                    entry = mem_entry.to_dict()
                    break
            
            if not entry:
                logging.warning(f"Memory entry with ID {entry_id} not found")
                return False
            
            # Prepare memory data for secure transmission
            memory_data = {
                "timestamp": entry.get("timestamp", 0),
                "entry_type": entry.get("entry_type", ""),
                "content": entry.get("content", {}),
                "metadata": entry.get("metadata", {})
            }
            
            # Create message payload
            payload = {
                "memory_data": memory_data,
                "sender_identity": self.node_identity.export_public_identity() if self.node_identity else {"node_id": "open_agi_memory_node"}
            }
            
            message = {
                "type": "memory",
                "subtype": "share",
                "source_node": "open_agi_memory_node",
                "target_node": peer_id,
                "payload": payload,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            success = await self.p2p_network.send_message(peer_id, message)
            if success:
                logging.info(f"Shared memory entry {entry_id} with peer {peer_id}")
            else:
                logging.warning(f"Failed to share memory entry {entry_id} with peer {peer_id}")
            return success
        except Exception as e:
            logging.error(f"Failed to share memory with peer: {e}")
            return False
    
    async def request_memory_sync(self, peer_id: str) -> bool:
        """
        Request memory synchronization with a specific peer
        
        Args:
            peer_id (str): Peer identifier
            
        Returns:
            bool: True if request sent successfully
        """
        if not self.p2p_network:
            logging.warning("P2P network not available")
            return False
        
        try:
            message = {
                "type": "memory",
                "subtype": "sync_request",
                "source_node": "open_agi_memory_node",
                "target_node": peer_id,
                "payload": {"request": "memory_sync"},
                "timestamp": asyncio.get_event_loop().time()
            }
            success = await self.p2p_network.send_message(peer_id, message)
            if success:
                logging.info(f"Requested memory sync with peer {peer_id}")
            else:
                logging.warning(f"Failed to request memory sync with peer {peer_id}")
            return success
        except Exception as e:
            logging.error(f"Failed to request memory sync: {e}")
            return False
    
    async def _handle_memory_share_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming memory share requests from other nodes
        
        Args:
            peer_id (str): Peer identifier
            message (dict): Memory share message
        """
        try:
            # Extract memory data from message
            memory_data = message.get('payload', {}).get('memory_data')
            if memory_data and self.memory_system:
                # Convert to MemoryEntry and store
                entry_type = memory_data.get("entry_type", "unknown")
                content = memory_data.get("content", {})
                metadata = memory_data.get("metadata", {})
                
                # Create and store memory entry
                if entry_type == "chat":
                    self.memory_system.add_chat_entry(
                        content.get("user_message", ""),
                        content.get("assistant_response", ""),
                        metadata.get("consciousness_state")
                    )
                elif entry_type == "consciousness_state":
                    self.memory_system.add_consciousness_state(content)
                elif entry_type == "rag_context":
                    self.memory_system.add_rag_context(
                        content.get("query", ""),
                        content.get("retrieved_context", ""),
                        content.get("sources", [])
                    )
                else:
                    # Generic entry
                    memory_entry = MemoryEntry(entry_type, content, metadata)
                    self.memory_system.entries.append(memory_entry)
                    self.memory_system.save_memory()
                
                # Send acknowledgment
                response = {
                    "type": "memory",
                    "subtype": "share_ack",
                    "source_node": "open_agi_memory_node",
                    "target_node": peer_id,
                    "payload": {"status": "accepted", "timestamp": asyncio.get_event_loop().time()},
                    "timestamp": asyncio.get_event_loop().time()
                }
                await self.p2p_network.send_message(peer_id, response)
                logging.info(f"Received memory share from {peer_id}")
        except Exception as e:
            logging.error(f"Failed to handle memory share request: {e}")
    
    async def _handle_memory_sync_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming memory sync requests from other nodes
        
        Args:
            peer_id (str): Peer identifier
            message (dict): Memory sync message
        """
        try:
            if not self.memory_system:
                return
            
            # Send our memory buffer to the requesting peer
            memory_snapshot = [entry.to_dict() for entry in self.memory_system.entries]
            response = {
                "type": "memory",
                "subtype": "sync_data",
                "source_node": "open_agi_memory_node",
                "target_node": peer_id,
                "payload": {"memory_data": memory_snapshot, "timestamp": asyncio.get_event_loop().time()},
                "timestamp": asyncio.get_event_loop().time()
            }
            await self.p2p_network.send_message(peer_id, response)
            logging.info(f"Synced memory with {peer_id}")
        except Exception as e:
            logging.error(f"Failed to handle memory sync request: {e}")
    
    async def _handle_memory_query_request(self, peer_id: str, message: Dict[str, Any]):
        """
        Handle incoming memory query requests from other nodes
        
        Args:
            peer_id (str): Peer identifier
            message (dict): Memory query message
        """
        try:
            if not self.memory_system:
                return
            
            # Extract query from message
            query_data = message.get('payload', {}).get('query_data', {})
            query = query_data.get('query', '')
            entry_types = query_data.get('entry_types', None)
            
            # Search memory
            results = self.memory_system.search_memory(query, entry_types)
            
            # Send results back
            response = {
                "type": "memory",
                "subtype": "query_results",
                "source_node": "open_agi_memory_node",
                "target_node": peer_id,
                "payload": {"results": results, "timestamp": asyncio.get_event_loop().time()},
                "timestamp": asyncio.get_event_loop().time()
            }
            await self.p2p_network.send_message(peer_id, response)
            logging.info(f"Responded to memory query from {peer_id}")
        except Exception as e:
            logging.error(f"Failed to handle memory query request: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory system statistics
        
        Returns:
            dict: Memory statistics
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return {}
        
        try:
            stats = self.memory_system.get_memory_stats()
            logging.info("Retrieved memory statistics")
            return stats
        except Exception as e:
            logging.error(f"Failed to get memory stats: {e}")
            return {}
    
    def save_memory(self) -> bool:
        """
        Save memory to persistent storage
        
        Returns:
            bool: True if saved successfully
        """
        if not self.memory_system:
            logging.warning("Memory system not available")
            return False
        
        try:
            result = self.memory_system.save_memory()
            if result:
                logging.info("Memory saved successfully")
            else:
                logging.warning("Failed to save memory")
            return result
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")
            return False

# Example usage and testing
async def main():
    """Example usage of Open-A.G.I Memory Integration"""
    print("=== Open-A.G.I Memory Integration Demo ===")
    
    # Initialize integration
    integration = OpenAGIMemoryIntegration("ai_runs/open_agi_memory.json")
    
    # Start network
    await integration.start_network()
    
    # Add sample chat entry
    print("\nAdding sample chat entry...")
    chat_id = integration.add_chat_entry(
        "What is consciousness?",
        "Consciousness is the state of being aware of and able to think about one's own existence.",
        {
            "consciousness_level": 0.75,
            "phi": 0.82,
            "coherence": 0.68
        }
    )
    print(f"Added chat entry with ID: {chat_id}")
    
    # Add consciousness state
    print("\nAdding consciousness state...")
    state_id = integration.add_consciousness_state({
        "timestamp": asyncio.get_event_loop().time(),
        "consciousness_level": 0.78,
        "phi": 0.79,
        "coherence": 0.70,
        "gamma_power": 0.65,
        "fractal_dimension": 2.1,
        "spiritual_awareness": 0.72
    })
    print(f"Added consciousness state with ID: {state_id}")
    
    # Add RAG context
    print("\nAdding RAG context...")
    rag_id = integration.add_rag_context(
        "consciousness theories",
        "Integrated Information Theory (IIT) proposes that consciousness corresponds to integrated information...",
        [
            {"source": "Tononi_Philosophy_of_Mind.pdf", "score": 0.95},
            {"source": "Chalmers_Conscious_Mind.txt", "score": 0.87}
        ]
    )
    print(f"Added RAG context with ID: {rag_id}")
    
    # Search memory
    print("\nSearching memory for 'consciousness'...")
    results = integration.search_memory("consciousness")
    print(f"Found {len(results)} entries")
    
    # Get chat history
    print("\nGetting recent chat history...")
    chat_history = integration.get_recent_chat_history(5)
    print(f"Retrieved {len(chat_history)} chat entries")
    
    # Get consciousness history
    print("\nGetting consciousness history...")
    consciousness_history = integration.get_consciousness_history(3)
    print(f"Retrieved {len(consciousness_history)} consciousness entries")
    
    # Get memory stats
    print("\nGetting memory statistics...")
    stats = integration.get_memory_stats()
    print(f"Memory stats: {stats}")
    
    # Save memory
    print("\nSaving memory...")
    save_result = integration.save_memory()
    print(f"Memory save result: {save_result}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    asyncio.run(main())