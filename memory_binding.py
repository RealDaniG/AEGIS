#!/usr/bin/env python3
"""
Memory Binding Module for Unified Thinking System

Implements bi-directional coupling between Memory Node (Node 3) and Sensory Node (Node 0)
through resonance feedback loops and associative addressing as described in the unified thinking document.

This module creates true memory-perception resonance where:
- Sensory feeds memory (encoding)
- Memory feeds sensory (biasing/recall)
- Feedback is modulated by network weights and resonance frequencies
"""

import numpy as np
import asyncio
from collections import deque
from typing import Dict, Any, Optional, List
import time
from sklearn.metrics.pairwise import cosine_similarity

# Constants for node identification
SENSORY_NODE = 0
MEMORY_NODE = 3

class NeuralLinksMatrix:
    """
    13x13 matrix representing connection strengths between every node.
    Each link stores a weight or tensor representing information flow capacity.
    """
    
    def __init__(self, num_nodes: int = 13):
        """
        Initialize the neural links matrix.
        
        Args:
            num_nodes: Number of nodes in the system (default 13 for Metatron's Cube)
        """
        self.num_nodes = num_nodes
        # Start with disconnected matrix (all zeros)
        self.link_matrix = np.zeros((num_nodes, num_nodes), dtype=np.float64)
        
        # Initialize default connections between sensory and memory nodes
        self.link_matrix[SENSORY_NODE, MEMORY_NODE] = 1.0  # Sensory to Memory
        self.link_matrix[MEMORY_NODE, SENSORY_NODE] = 0.5  # Memory to Sensory (feedback lower by default)
        
        print(f"[MEMORY_BINDING] Neural Links Matrix initialized ({num_nodes}x{num_nodes})")
        print(f"[MEMORY_BINDING] Default links: Sensory({SENSORY_NODE}) <-> Memory({MEMORY_NODE})")
    
    def set_connection_strength(self, source_node: int, target_node: int, strength: float):
        """
        Set the connection strength between two nodes.
        
        Args:
            source_node: Source node ID (0-12)
            target_node: Target node ID (0-12)
            strength: Connection strength (0.0 = no connection, 1.0 = full connection)
        """
        if 0 <= source_node < self.num_nodes and 0 <= target_node < self.num_nodes:
            self.link_matrix[source_node, target_node] = max(0.0, min(1.0, strength))
        else:
            raise ValueError(f"Invalid node indices: source={source_node}, target={target_node}")
    
    def get_connection_strength(self, source_node: int, target_node: int) -> float:
        """
        Get the connection strength between two nodes.
        
        Args:
            source_node: Source node ID (0-12)
            target_node: Target node ID (0-12)
            
        Returns:
            float: Connection strength
        """
        if 0 <= source_node < self.num_nodes and 0 <= target_node < self.num_nodes:
            return self.link_matrix[source_node, target_node]
        else:
            raise ValueError(f"Invalid node indices: source={source_node}, target={target_node}")
    
    def get_all_connections(self) -> np.ndarray:
        """
        Get the entire connection matrix.
        
        Returns:
            np.ndarray: Copy of the connection matrix
        """
        return self.link_matrix.copy()
    
    def apply_hebbian_learning(self, node_activities: np.ndarray, learning_rate: float = 0.01):
        """
        Apply Hebbian learning to adjust connection strengths based on node co-activation.
        
        "Cells that fire together, wire together"
        
        Args:
            node_activities: Array of current activity levels for all nodes
            learning_rate: Rate at which connections are adjusted
        """
        if len(node_activities) != self.num_nodes:
            raise ValueError(f"Node activities array must have {self.num_nodes} elements")
        
        # Outer product of activities to determine co-activation
        coactivation = np.outer(node_activities, node_activities)
        
        # Update connections based on co-activation
        # Only strengthen existing connections, don't create new ones from zero
        delta = learning_rate * coactivation * (self.link_matrix > 0)
        self.link_matrix = np.clip(self.link_matrix + delta, 0.0, 1.0)
        
        # Ensure diagonal is zero (no self-connections)
        np.fill_diagonal(self.link_matrix, 0.0)

class SensoryBuffer:
    """
    Shared buffer that holds recent sensory patterns for memory binding.
    Creates phase locking between perception and recall.
    """
    
    def __init__(self, maxlen: int = 256):
        """
        Initialize the sensory buffer.
        
        Args:
            maxlen: Maximum number of sensory patterns to store
        """
        self.buffer = deque(maxlen=maxlen)
        self.maxlen = maxlen
        self.feedback_gain = 0.1  # Default feedback strength
        
        print(f"[MEMORY_BINDING] Sensory Buffer initialized (maxlen={maxlen})")
    
    def append(self, sensory_input: np.ndarray):
        """
        Add a sensory input to the buffer.
        
        Args:
            sensory_input: 5D sensory input vector
        """
        if not isinstance(sensory_input, np.ndarray):
            sensory_input = np.array(sensory_input)
        
        # Ensure 5D
        if sensory_input.size != 5:
            sensory_input = np.resize(sensory_input, 5)
        
        self.buffer.append(sensory_input.copy())
    
    def get_recent_patterns(self, n: int = None) -> np.ndarray:
        """
        Get recent sensory patterns from the buffer.
        
        Args:
            n: Number of recent patterns to retrieve (default: all)
            
        Returns:
            np.ndarray: Stack of recent sensory patterns
        """
        if len(self.buffer) == 0:
            return np.array([])
        
        if n is None:
            n = len(self.buffer)
        
        # Get the n most recent patterns
        recent = list(self.buffer)[-n:]
        return np.stack(recent)
    
    def clear(self):
        """Clear the sensory buffer."""
        self.buffer.clear()
    
    def set_feedback_gain(self, gain: float):
        """
        Set the feedback gain for memory influence on sensory processing.
        
        Args:
            gain: Feedback strength (0.0 = no feedback, 1.0 = full feedback)
        """
        self.feedback_gain = max(0.0, min(1.0, gain))

class AssociativeMemoryIndex:
    """
    Associative memory system that represents each sensory event with a key vector
    and stores states under these keys for instant recall.
    """
    
    def __init__(self, key_dimension: int = 100):
        """
        Initialize the associative memory index.
        
        Args:
            key_dimension: Dimension of key vectors
        """
        self.key_dimension = key_dimension
        self.memory_keys = []  # List of key vectors
        self.memory_values = []  # List of corresponding memory states
        self.similarity_threshold = 0.8  # Threshold for key matching
        
        print(f"[MEMORY_BINDING] Associative Memory Index initialized (key_dim={key_dimension})")
    
    def store_memory(self, sensory_vector: np.ndarray, memory_state: np.ndarray):
        """
        Store a memory state under a sensory key.
        
        Args:
            sensory_vector: Sensory input vector (will be converted to key)
            memory_state: Memory state to store
        """
        # Convert sensory vector to key (simple hashing approach)
        key = self._vector_to_key(sensory_vector)
        
        self.memory_keys.append(key.copy())
        self.memory_values.append(memory_state.copy() if isinstance(memory_state, np.ndarray) else np.array(memory_state))
    
    def recall_memory(self, sensory_vector: np.ndarray) -> Optional[np.ndarray]:
        """
        Recall a memory state based on a sensory input vector.
        
        Args:
            sensory_vector: Current sensory input
            
        Returns:
            np.ndarray: Recalled memory state, or None if no match found
        """
        if len(self.memory_keys) == 0:
            return None
        
        # Convert current sensory vector to key
        current_key = self._vector_to_key(sensory_vector).reshape(1, -1)
        
        # Convert all stored keys to array for comparison
        stored_keys = np.array(self.memory_keys)
        
        # Calculate similarities
        similarities = cosine_similarity(current_key, stored_keys)[0]
        
        # Find best match
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Return memory if similarity exceeds threshold
        if best_similarity >= self.similarity_threshold:
            return self.memory_values[best_match_idx].copy()
        else:
            return None
    
    def _vector_to_key(self, vector: np.ndarray) -> np.ndarray:
        """
        Convert a sensory vector to a key vector for indexing.
        
        Args:
            vector: Input vector
            
        Returns:
            np.ndarray: Key vector
        """
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)
        
        # Simple transformation to key dimension
        if vector.size > self.key_dimension:
            # Downsample
            step = vector.size // self.key_dimension
            key = vector[::step][:self.key_dimension]
        elif vector.size < self.key_dimension:
            # Upsample by repetition
            repeats = self.key_dimension // vector.size + 1
            key = np.tile(vector, repeats)[:self.key_dimension]
        else:
            key = vector.copy()
        
        # Normalize
        norm = np.linalg.norm(key)
        if norm > 0:
            key = key / norm
        
        return key
    
    def set_similarity_threshold(self, threshold: float):
        """
        Set the similarity threshold for memory recall.
        
        Args:
            threshold: Similarity threshold (0.0-1.0)
        """
        self.similarity_threshold = max(0.0, min(1.0, threshold))

class MemoryBindingSystem:
    """
    Main memory binding system that integrates all components for unified thinking.
    """
    
    def __init__(self, num_nodes: int = 13):
        """
        Initialize the memory binding system.
        
        Args:
            num_nodes: Number of nodes in the consciousness system
        """
        self.num_nodes = num_nodes
        
        # Initialize core components
        self.neural_links = NeuralLinksMatrix(num_nodes)
        self.sensory_buffer = SensoryBuffer()
        self.associative_memory = AssociativeMemoryIndex()
        
        # System state
        self.is_active = False
        self.last_update_time = 0.0
        
        print("[MEMORY_BINDING] Memory Binding System initialized")
    
    def initialize_binding(self):
        """
        Initialize the memory-sensory binding system.
        """
        self.is_active = True
        self.last_update_time = time.time()
        print("[MEMORY_BINDING] Memory-Sensory binding system activated")
    
    def process_sensory_input(self, sensory_input: np.ndarray, 
                            memory_state: np.ndarray) -> Dict[str, Any]:
        """
        Process sensory input through the binding system.
        
        Args:
            sensory_input: 5D sensory input vector
            memory_state: Current memory state from MemoryMatrixNode
            
        Returns:
            Dict[str, Any]: Processing results including feedback
        """
        if not self.is_active:
            return {"sensory_input": sensory_input, "memory_feedback": np.zeros_like(sensory_input)}
        
        # 1. Add sensory input to buffer
        self.sensory_buffer.append(sensory_input)
        
        # 2. Store in associative memory
        self.associative_memory.store_memory(sensory_input, memory_state)
        
        # 3. Attempt to recall similar memories
        recalled_memory = self.associative_memory.recall_memory(sensory_input)
        
        # 4. Generate feedback signal
        if recalled_memory is not None:
            # Calculate feedback based on recalled memory and connection strength
            feedback_strength = self.neural_links.get_connection_strength(MEMORY_NODE, SENSORY_NODE)
            sensory_feedback = feedback_strength * recalled_memory[:sensory_input.size]
            
            # Ensure feedback matches sensory input dimensions
            if sensory_feedback.size < sensory_input.size:
                # Pad feedback
                padded_feedback = np.zeros(sensory_input.size)
                padded_feedback[:sensory_feedback.size] = sensory_feedback
                sensory_feedback = padded_feedback
            elif sensory_feedback.size > sensory_input.size:
                # Truncate feedback
                sensory_feedback = sensory_feedback[:sensory_input.size]
        else:
            sensory_feedback = np.zeros_like(sensory_input)
        
        # 5. Apply sensory buffer feedback
        recent_patterns = self.sensory_buffer.get_recent_patterns(10)
        if len(recent_patterns) > 0:
            # Average recent patterns for temporal context
            temporal_context = np.mean(recent_patterns, axis=0)
            buffer_feedback = self.sensory_buffer.feedback_gain * temporal_context
            
            # Combine with recalled memory feedback
            sensory_feedback = 0.7 * sensory_feedback + 0.3 * buffer_feedback
        
        self.last_update_time = time.time()
        
        return {
            "sensory_input": sensory_input,
            "memory_feedback": sensory_feedback,
            "recalled_memory": recalled_memory,
            "buffer_size": len(self.sensory_buffer.buffer),
            "memory_keys": len(self.associative_memory.memory_keys)
        }
    
    def update_neural_links(self, node_activities: np.ndarray):
        """
        Update neural link strengths using Hebbian learning.
        
        Args:
            node_activities: Array of current activity levels for all nodes
        """
        if len(node_activities) == self.num_nodes:
            self.neural_links.apply_hebbian_learning(node_activities)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the current status of the memory binding system.
        
        Returns:
            Dict[str, Any]: System status information
        """
        return {
            "is_active": self.is_active,
            "last_update": self.last_update_time,
            "sensory_buffer_size": len(self.sensory_buffer.buffer),
            "memory_keys_stored": len(self.associative_memory.memory_keys),
            "link_matrix_shape": self.neural_links.link_matrix.shape,
            "sensory_feedback_gain": self.sensory_buffer.feedback_gain,
            "memory_similarity_threshold": self.associative_memory.similarity_threshold
        }
    
    def reset_system(self):
        """Reset the memory binding system to initial state."""
        self.sensory_buffer.clear()
        self.associative_memory.memory_keys.clear()
        self.associative_memory.memory_values.clear()
        self.last_update_time = 0.0
        print("[MEMORY_BINDING] Memory Binding System reset")


# Example usage and testing
async def main():
    """Example usage of the Memory Binding System"""
    print("=" * 60)
    print("Memory Binding System - Unified Thinking Implementation")
    print("=" * 60)
    
    # Create binding system
    binding_system = MemoryBindingSystem()
    binding_system.initialize_binding()
    
    # Simulate processing cycle
    print("\n--- Simulating Memory-Sensory Binding ---")
    
    # Initial sensory input
    sensory_input = np.array([0.5, 0.3, 0.8, 0.2, 0.6])
    memory_state = np.random.rand(100)  # Simulated memory state
    
    # Process through binding system
    result = binding_system.process_sensory_input(sensory_input, memory_state)
    
    print(f"Sensory Input: {sensory_input}")
    print(f"Memory Feedback: {result['memory_feedback'][:5]}...")  # Show first 5 elements
    print(f"Buffer Size: {result['buffer_size']}")
    print(f"Memory Keys: {result['memory_keys']}")
    
    # Show system status
    status = binding_system.get_system_status()
    print(f"\nSystem Status: {status}")
    
    print("\n[OK] Memory Binding System test completed!")


if __name__ == "__main__":
    asyncio.run(main())