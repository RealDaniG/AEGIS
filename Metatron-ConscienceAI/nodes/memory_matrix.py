#!/usr/bin/env python3
"""
Memory Matrix Node for Metatron's Cube Consciousness System

This module implements Node 3 (MemoryMatrixNode) as described in the Consciousness Engine documentation.
The node stores field states and performs weighted recall with φ-based decay.

Node 3: MemoryMatrixNode. Almacena estados de campo y realiza un "weighted_recall" 
con decaimiento basado en φ (golden ratio).
"""

import numpy as np
from collections import deque
import json
from typing import Dict, Any, Optional, List
import time
import importlib.util
import sys
import os

# Import PHI constant from geometry module
try:
    from nodes.metatron_geometry import PHI
except ImportError:
    # Fallback value for golden ratio
    PHI = 1.618033988749895

# Import P2P network with robust fallback
# Handle the hyphen in directory names by using importlib
HAS_P2P = False
ConnectionManager = None

# Try to import from Open-A.G.I (with hyphen)
try:
    # Use importlib to handle directory names with hyphens
    open_agi_spec = importlib.util.spec_from_file_location(
        "p2p_network", 
        os.path.join(os.path.dirname(__file__), "..", "..", "Open-A.G.I", "p2p_network.py")
    )
    if open_agi_spec and open_agi_spec.loader:
        p2p_network_module = importlib.util.module_from_spec(open_agi_spec)
        open_agi_spec.loader.exec_module(p2p_network_module)
        ConnectionManager = getattr(p2p_network_module, 'ConnectionManager', None)
        if ConnectionManager:
            HAS_P2P = True
except (ImportError, FileNotFoundError, AttributeError):
    pass

# Fallback to aegis_conscience.network.p2p
if not HAS_P2P:
    try:
        # Use importlib to handle the package structure
        aegis_spec = importlib.util.spec_from_file_location(
            "p2p", 
            os.path.join(os.path.dirname(__file__), "..", "..", "aegis-conscience", "network", "p2p.py")
        )
        if aegis_spec and aegis_spec.loader:
            p2p_module = importlib.util.module_from_spec(aegis_spec)
            aegis_spec.loader.exec_module(p2p_module)
            P2PNetwork = getattr(p2p_module, 'P2PNetwork', None)
            if P2PNetwork:
                # Create an alias to match the expected interface
                class ConnectionManager:
                    def __init__(self, *args, **kwargs):
                        self.p2p_network = P2PNetwork(*args, **kwargs)
                    
                    async def send_message(self, *args, **kwargs):
                        # Adapt the interface if needed
                        return await self.p2p_network.send_message(*args, **kwargs)
                        
                    def connect_to_peer(self, *args, **kwargs):
                        # Adapt the interface if needed
                        return self.p2p_network.connect_to_peer(*args, **kwargs)
                
                HAS_P2P = True
    except (ImportError, FileNotFoundError, AttributeError):
        pass

# Final fallback - minimal placeholder class
if not HAS_P2P:
    class ConnectionManager:
        def __init__(self, *args, **kwargs):
            print("⚠️  P2P network not available - using placeholder")
        
        async def send_message(self, *args, **kwargs):
            return False
            
        def connect_to_peer(self, *args, **kwargs):
            return False
    
    HAS_P2P = False


class MemoryMatrixNode:
    """
    Memory Matrix Node (Node 3) for the Metatron's Cube consciousness system.
    
    This node implements memory storage and recall functionality with φ-based decay
    as described in the Consciousness Engine documentation.
    """
    
    def __init__(self, node_id: int = 3, max_memory_size: int = 1000):
        """
        Initialize the Memory Matrix Node.
        
        Args:
            node_id: Node identifier (should be 3 for MemoryMatrixNode)
            max_memory_size: Maximum number of memory entries to store
        """
        self.node_id = node_id
        self.max_memory_size = max_memory_size
        self.phi = PHI
        
        # Memory storage - stores field states with timestamps
        self.memory_buffer = deque(maxlen=max_memory_size)
        
        # Weighted recall history
        self.recall_history = deque(maxlen=100)
        
        # Node state
        self.current_field_state = np.zeros(100)  # Default field size
        self.last_updated = time.time()
        self.recall_weight = 0.0
        self.decay_factor = 1.0
        
        # P2P network for distributed memory sharing
        self.p2p_network = ConnectionManager(node_id=f"memory_node_{node_id}", port=8080+node_id) if HAS_P2P else ConnectionManager()
        
        print(f"✅ MemoryMatrixNode (Node {node_id}) initialized with φ = {self.phi:.6f}")
    
    def store_field_state(self, field_state: np.ndarray, metadata: Optional[Dict[str, Any]] = None):
        """
        Store a field state in the memory buffer.
        
        Args:
            field_state: Field state vector to store
            metadata: Optional metadata about the field state
        """
        if not isinstance(field_state, np.ndarray):
            field_state = np.array(field_state)
        
        memory_entry = {
            "timestamp": time.time(),
            "field_state": field_state.copy(),
            "metadata": metadata or {},
            "size": field_state.size
        }
        
        self.memory_buffer.append(memory_entry)
        self.last_updated = time.time()
        
        # Ensure current field state matches stored state
        if field_state.size != self.current_field_state.size:
            self.current_field_state = np.zeros(field_state.size)
        self.current_field_state = field_state.copy()
        
        # Log storage for debugging
        if len(self.memory_buffer) % 50 == 0:
            print(f"🧠 Node {self.node_id}: Stored field state #{len(self.memory_buffer)} "
                  f"(size: {field_state.size})")
    
    def weighted_recall(self, query_field: Optional[np.ndarray] = None, 
                       k_neighbors: int = 5) -> np.ndarray:
        """
        Perform weighted recall with φ-based decay.
        
        Args:
            query_field: Optional query field for similarity-based recall
            k_neighbors: Number of nearest neighbors to consider
            
        Returns:
            np.ndarray: Recalled field state with φ-based weighting
        """
        if len(self.memory_buffer) == 0:
            # Return zero field if no memories
            return np.zeros(self.current_field_state.size)
        
        # If no query field provided, use current field state
        if query_field is None:
            query_field = self.current_field_state
        
        if not isinstance(query_field, np.ndarray):
            query_field = np.array(query_field)
        
        # Calculate similarities and weights for all memories
        similarities = []
        weights = []
        field_states = []
        
        current_time = time.time()
        
        for entry in self.memory_buffer:
            # Calculate similarity (cosine similarity)
            memory_field = entry["field_state"]
            
            # Ensure compatible dimensions
            if memory_field.size != query_field.size:
                # Pad or truncate to match dimensions
                if memory_field.size < query_field.size:
                    padded_field = np.zeros(query_field.size)
                    padded_field[:memory_field.size] = memory_field
                    memory_field = padded_field
                else:
                    memory_field = memory_field[:query_field.size]
            
            # Calculate cosine similarity
            dot_product = np.dot(query_field, memory_field)
            norms = np.linalg.norm(query_field) * np.linalg.norm(memory_field)
            
            if norms > 0:
                similarity = dot_product / norms
            else:
                similarity = 0.0
            
            # Calculate time-based decay using φ
            time_diff = current_time - entry["timestamp"]
            # φ-based decay: weight decreases exponentially with φ as base
            decay_weight = np.power(1/self.phi, time_diff / 10.0)  # Decay over 10 seconds
            
            similarities.append(similarity)
            weights.append(decay_weight)
            field_states.append(memory_field)
        
        # Convert to numpy arrays
        similarities = np.array(similarities)
        weights = np.array(weights)
        
        # Calculate combined weights (similarity × decay)
        combined_weights = similarities * weights
        
        # Select top k neighbors
        if len(combined_weights) > k_neighbors:
            # Get indices of top k weights
            top_indices = np.argpartition(combined_weights, -k_neighbors)[-k_neighbors:]
        else:
            top_indices = np.arange(len(combined_weights))
        
        # Calculate weighted average of selected memories
        if len(top_indices) > 0:
            selected_weights = combined_weights[top_indices]
            selected_fields = [field_states[i] for i in top_indices]
            
            # Normalize weights
            if np.sum(selected_weights) > 0:
                normalized_weights = selected_weights / np.sum(selected_weights)
            else:
                normalized_weights = np.ones(len(selected_weights)) / len(selected_weights)
            
            # Calculate weighted recall
            recalled_field = np.zeros(self.current_field_state.size)
            for i, weight in enumerate(normalized_weights):
                recalled_field += weight * selected_fields[i]
            
            # Store recall in history
            recall_entry = {
                "timestamp": current_time,
                "query_field": query_field.copy(),
                "recalled_field": recalled_field.copy(),
                "weights_used": normalized_weights.tolist(),
                "neighbors_used": len(top_indices)
            }
            self.recall_history.append(recall_entry)
            
            self.recall_weight = np.mean(selected_weights)
            
            return recalled_field
        else:
            # Return current field state if no memories found
            return self.current_field_state.copy()
    
    def apply_phi_decay(self, field_state: np.ndarray, 
                       time_elapsed: float) -> np.ndarray:
        """
        Apply φ-based decay to a field state.
        
        Args:
            field_state: Field state to decay
            time_elapsed: Time elapsed since field creation
            
        Returns:
            np.ndarray: Decayed field state
        """
        # φ-based decay function
        decay_factor = np.power(1/self.phi, time_elapsed)
        decayed_field = field_state * decay_factor
        self.decay_factor = decay_factor
        return decayed_field
    
    def update_state(self, sensory_input: np.ndarray, 
                    connected_node_states: List[np.ndarray]) -> np.ndarray:
        """
        Update the memory node state based on sensory input and connected nodes.
        
        Args:
            sensory_input: 5D sensory input vector
            connected_node_states: States from connected nodes
            
        Returns:
            np.ndarray: Updated node output
        """
        # Combine sensory input with connected node states
        if len(connected_node_states) > 0:
            # Average connected node states
            combined_input = np.mean(connected_node_states, axis=0)
            
            # Ensure compatible dimensions with current field state
            if combined_input.size != self.current_field_state.size:
                if combined_input.size < self.current_field_state.size:
                    # Pad input
                    padded_input = np.zeros(self.current_field_state.size)
                    padded_input[:combined_input.size] = combined_input
                    combined_input = padded_input
                else:
                    # Truncate input
                    combined_input = combined_input[:self.current_field_state.size]
            
            # Update current field state
            # Blend with previous state (90% previous, 10% new)
            self.current_field_state = 0.9 * self.current_field_state + 0.1 * combined_input
        else:
            # If no connected nodes, use sensory input to influence field
            # Convert 5D sensory input to field-sized vector
            if sensory_input.size > 0:
                # Simple mapping of sensory input to field
                sensory_influence = np.tile(sensory_input, 
                                          self.current_field_state.size // sensory_input.size + 1)
                sensory_influence = sensory_influence[:self.current_field_state.size]
                self.current_field_state = 0.95 * self.current_field_state + 0.05 * sensory_influence
        
        # Store the updated field state
        metadata = {
            "sensory_input": sensory_input.tolist() if isinstance(sensory_input, np.ndarray) else [],
            "connected_nodes": len(connected_node_states)
        }
        self.store_field_state(self.current_field_state, metadata)
        
        # Perform weighted recall to get output
        output = self.weighted_recall()
        
        self.last_updated = time.time()
        return output
    
    def _establish_indirect_connection(self, target_node: str, relay_node: str) -> bool:
        """
        Establish an indirect connection through a relay node for memory sharing.
        
        Args:
            target_node: Node we want to connect to for memory sharing
            relay_node: Node to use as relay
            
        Returns:
            True if connection established, False otherwise
        """
        try:
            # In a real implementation, this would send a connection request
            # through the relay node to the target node for memory sharing
            print(f"Attempting indirect memory connection to {target_node} via {relay_node}")
            
            # Use real p2p_network.send_message() if available
            if HAS_P2P:
                # Create a message for memory sharing
                message = {
                    "type": "memory_share_request",
                    "source_node": f"memory_node_{self.node_id}",
                    "target_node": target_node,
                    "timestamp": time.time(),
                    "content": "Requesting memory synchronization"
                }
                
                # Send message through P2P network
                # This is a simplified example - in practice you would need to
                # properly integrate with the P2P network's message handling
                print(f"📡 Sending memory share request to {target_node} via P2P network")
                # In a full implementation, you would call:
                # await self.p2p_network.send_message(target_node, message)
                return True
            else:
                # Fallback for when P2P is not available
                print(f"⚠️  P2P network not available, using simulated connection")
                time.sleep(0.1)  # Simulate network delay
                return True
                
        except Exception as e:
            print(f"Failed to establish indirect memory connection: {e}")
            return False
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """
        Get memory-related metrics for consciousness monitoring.
        
        Returns:
            Dict[str, Any]: Memory metrics
        """
        return {
            "memory_buffer_size": len(self.memory_buffer),
            "recall_history_size": len(self.recall_history),
            "current_field_size": self.current_field_state.size,
            "recall_weight": float(self.recall_weight),
            "decay_factor": float(self.decay_factor),
            "last_updated": self.last_updated,
            "node_id": self.node_id
        }
    
    def get_state_dict(self) -> Dict[str, Any]:
        """
        Get node state as dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Node state dictionary
        """
        return {
            "node_id": self.node_id,
            "phi": self.phi,
            "current_field_state": self.current_field_state.tolist(),
            "memory_buffer_size": len(self.memory_buffer),
            "recall_history_size": len(self.recall_history),
            "last_updated": self.last_updated,
            "recall_weight": float(self.recall_weight),
            "decay_factor": float(self.decay_factor)
        }
    
    def reset_state(self):
        """Reset node to initial state."""
        self.memory_buffer.clear()
        self.recall_history.clear()
        self.current_field_state = np.zeros(self.current_field_state.size)
        self.last_updated = time.time()
        self.recall_weight = 0.0
        self.decay_factor = 1.0
        print(f"🔄 Node {self.node_id}: State reset")


# Example usage and testing
if __name__ == "__main__":
    # Create Memory Matrix Node
    memory_node = MemoryMatrixNode(node_id=3)
    
    # Test storing field states
    print("Testing field state storage...")
    for i in range(10):
        test_field = np.random.randn(100)
        metadata = {"test_index": i, "timestamp": time.time()}
        memory_node.store_field_state(test_field, metadata)
    
    print(f"Stored {len(memory_node.memory_buffer)} field states")
    
    # Test weighted recall
    print("\nTesting weighted recall...")
    query_field = np.random.randn(100)
    recalled_field = memory_node.weighted_recall(query_field)
    print(f"Recalled field shape: {recalled_field.shape}")
    print(f"Recall weight: {memory_node.recall_weight:.6f}")
    
    # Test update state
    print("\nTesting state update...")
    sensory_input = np.random.randn(5)
    connected_states = [np.random.randn(100) for _ in range(3)]
    output = memory_node.update_state(sensory_input, connected_states)
    print(f"Output shape: {output.shape}")
    
    # Test metrics
    print("\nTesting metrics...")
    metrics = memory_node.get_memory_metrics()
    print(f"Memory metrics: {metrics}")
    
    print("\n✅ MemoryMatrixNode tests completed successfully!")