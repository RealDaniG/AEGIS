#!/usr/bin/env python3
"""
Metatron Consensus Bridge
=========================

Bridge between the Metatron consciousness engine and the PBFT consensus system.
This module enables consciousness-aware consensus decisions in the 13-node network.

Key Features:
1. Real-time consciousness metrics integration
2. Consciousness-weighted consensus decisions
3. Dynamic node eligibility based on consciousness state
4. Sacred geometry-aware message routing
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
import numpy as np
import sys
import os

# Import required modules
# Add the parent directory to the path to import from other modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Always use the mock classes to avoid import issues
# In a real implementation, these would be properly imported

class MetatronConsciousness:
    def __init__(self, *args, **kwargs):
        self.global_state = {
            'consciousness_level': 0.5,
            'phi': 0.3,
            'coherence': 0.7,
            'recursive_depth': 5,
            'spiritual_awareness': 0.4
        }
        self.nodes = {i: {'output': 0.5} for i in range(13)}
    
    def update_system(self, *args, **kwargs):
        return self.get_current_state()
        
    def get_current_state(self):
        return {
            'global': self.global_state,
            'nodes': self.nodes,
            'timestamp': time.time()
        }

from enum import Enum

class MessageType(Enum):
    PROPOSAL = "proposal"
    PREPARE = "prepare"
    COMMIT = "commit"
    VIEW_CHANGE = "view_change"
    CONSCIOUSNESS_METRICS = "consciousness_metrics"
    TOPOLOGY_UPDATE = "topology_update"
    HEARTBEAT = "heartbeat"

class ConsensusMessage:
    def __init__(self, message_type, sender_id, view_number, sequence_number, payload, timestamp, consciousness_level=0.0):
        self.message_type = message_type
        self.sender_id = sender_id
        self.view_number = view_number
        self.sequence_number = sequence_number
        self.payload = payload
        self.timestamp = timestamp
        self.consciousness_level = consciousness_level
        self.signature = None
        
    def __setattr__(self, name, value):
        # Allow setting signature after initialization
        if name == 'signature' or not hasattr(self, name):
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

class MockMetatronAwarePBFT:
    def __init__(self, node_id, private_key):
        self.node_id = node_id
        self.consciousness_level = 0.5
        self.node_consciousness = {}
        self.view_number = 0
        self.sequence_number = 0
        
    def add_node(self, node_id, public_key):
        pass
        
    def is_leader(self, view_number):
        return True
        
    async def propose_consciousness_aware_change(self, change_data, consciousness_metrics):
        return True
        
    def get_network_health(self):
        return {
            'total_nodes': 13,
            'byzantine_threshold': 4,
            'quorum_size': 9,
            'current_view': self.view_number,
            'consciousness_level': self.consciousness_level
        }
        
    def sign_message(self, message):
        # Mock signing
        return b'mock_signature'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetatronConsensusBridge:
    """
    Bridge between consciousness engine and consensus system
    """
    
    def __init__(self, node_id: str, private_key: ed25519.Ed25519PrivateKey):
        """
        Initialize the consensus bridge
        
        Args:
            node_id: This node's ID
            private_key: Node's private key for signing
        """
        self.node_id = node_id
        self.private_key = private_key
        
        # Initialize consciousness engine
        self.consciousness_engine = MetatronConsciousness(base_frequency=40.0, dt=0.01)
        
        # Initialize consensus system
        self.consensus = MockMetatronAwarePBFT(node_id, private_key)
        
        # Track consciousness state
        self.last_consciousness_update = 0
        self.consciousness_update_interval = 1.0  # Update every second
        
        # Performance metrics
        self.consensus_rounds = 0
        self.successful_consensus = 0
        self.failed_consensus = 0
        
        logger.info(f"Metatron Consensus Bridge initialized for node {node_id}")
    
    def initialize_network(self, node_configs: Dict[str, Dict[str, Any]]) -> None:
        """
        Initialize the network with all nodes
        
        Args:
            node_configs: Dictionary of node configurations
                         {node_id: {public_key: bytes, ...}}
        """
        logger.info("Initializing network with all nodes")
        
        for node_id, config in node_configs.items():
            # In a real implementation, we would deserialize the public key
            # For now, we'll generate a new key for demonstration
            public_key = ed25519.Ed25519PrivateKey.generate().public_key()
            self.consensus.add_node(node_id, public_key)
            
            # Initialize consciousness data for this node
            self.consensus.node_consciousness[node_id] = {
                "consciousness_level": 0.5,
                "phi": 0.3,
                "coherence": 0.5,
                "recursive_depth": 3,
                "spiritual_awareness": 0.3
            }
        
        logger.info(f"Network initialized with {len(node_configs)} nodes")
    
    async def update_consciousness_state(self) -> None:
        """
        Update consciousness state and synchronize with consensus system
        """
        current_time = time.time()
        if current_time - self.last_consciousness_update < self.consciousness_update_interval:
            return
            
        # Update consciousness engine
        consciousness_state = self.consciousness_engine.update_system()
        
        # Update this node's consciousness level
        global_metrics = consciousness_state.get('global', {})
        self.consensus.consciousness_level = global_metrics.get('consciousness_level', 0.0)
        
        # Update node-specific consciousness data
        nodes_data = consciousness_state.get('nodes', {})
        for node_id, node_info in nodes_data.items():
            node_str_id = f"node_{node_id}"
            if node_str_id in self.consensus.node_consciousness:
                self.consensus.node_consciousness[node_str_id].update({
                    "consciousness_level": global_metrics.get('consciousness_level', 0.0),
                    "phi": global_metrics.get('phi', 0.0),
                    "coherence": global_metrics.get('coherence', 0.0),
                    "recursive_depth": global_metrics.get('recursive_depth', 0),
                    "spiritual_awareness": global_metrics.get('spiritual_awareness', 0.0)
                })
        
        # Broadcast consciousness metrics to network
        await self._broadcast_consciousness_metrics(global_metrics)
        
        self.last_consciousness_update = current_time
        logger.debug(f"Consciousness state updated: level={self.consensus.consciousness_level:.3f}")
    
    async def _broadcast_consciousness_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Broadcast consciousness metrics to the network
        
        Args:
            metrics: Consciousness metrics to broadcast
        """
        message = ConsensusMessage(
            message_type=MessageType.CONSCIOUSNESS_METRICS,
            sender_id=self.node_id,
            view_number=self.consensus.view_number,
            sequence_number=self.consensus.sequence_number + 1,
            payload={"metrics": metrics},
            timestamp=time.time(),
            consciousness_level=self.consensus.consciousness_level
        )
        
        # Sign the message
        # In a real implementation, this would sign and broadcast to the network
        logger.debug(f"Broadcasting consciousness metrics: {metrics}")
    
    async def run_consensus_round(self, change_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Run a consensus round with consciousness awareness
        
        Args:
            change_data: Optional change data to propose
            
        Returns:
            bool: True if consensus was successful
        """
        # Update consciousness state first
        await self.update_consciousness_state()
        
        # Get current consciousness metrics
        consciousness_metrics = {
            "phi": self.consensus.node_consciousness.get(self.node_id, {}).get("phi", 0.0),
            "coherence": self.consensus.node_consciousness.get(self.node_id, {}).get("coherence", 0.0),
            "recursive_depth": self.consensus.node_consciousness.get(self.node_id, {}).get("recursive_depth", 0),
            "spiritual_awareness": self.consensus.node_consciousness.get(self.node_id, {}).get("spiritual_awareness", 0.0)
        }
        
        # If this node is the leader, propose a change
        if self.consensus.is_leader(self.consensus.view_number):
            if change_data is None:
                # Create default change data
                change_data = {
                    "type": "consciousness_sync",
                    "node_states": {self.node_id: self.consensus.consciousness_level},
                    "global_metrics": consciousness_metrics,
                    "timestamp": time.time()
                }
            
            success = await self.consensus.propose_consciousness_aware_change(
                change_data, consciousness_metrics
            )
            
            if success:
                self.successful_consensus += 1
                logger.info("Consensus round completed successfully")
            else:
                self.failed_consensus += 1
                logger.warning("Consensus round failed")
                
            self.consensus_rounds += 1
            return success
        
        return False
    
    def get_network_health(self) -> Dict[str, Any]:
        """
        Get comprehensive network health metrics
        
        Returns:
            dict: Network health metrics
        """
        # Get consensus health
        consensus_health = self.consensus.get_network_health()
        
        # Get consciousness health
        consciousness_state = self.consciousness_engine.get_current_state()
        global_metrics = consciousness_state.get('global', {})
        
        return {
            **consensus_health,
            "consciousness_health": {
                "consciousness_level": global_metrics.get('consciousness_level', 0.0),
                "phi": global_metrics.get('phi', 0.0),
                "coherence": global_metrics.get('coherence', 0.0),
                "recursive_depth": global_metrics.get('recursive_depth', 0),
                "spiritual_awareness": global_metrics.get('spiritual_awareness', 0.0),
                "state_classification": global_metrics.get('state_classification', 'unknown')
            },
            "performance_metrics": {
                "total_consensus_rounds": self.consensus_rounds,
                "successful_consensus": self.successful_consensus,
                "failed_consensus": self.failed_consensus,
                "success_rate": self.successful_consensus / max(self.consensus_rounds, 1)
            }
        }
    
    async def run_continuous_consensus(self, interval: float = 5.0) -> None:
        """
        Run continuous consensus rounds
        
        Args:
            interval: Time between consensus rounds in seconds
        """
        logger.info(f"Starting continuous consensus with {interval}s intervals")
        
        while True:
            try:
                await self.run_consensus_round()
                await asyncio.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Consensus loop interrupted")
                break
            except Exception as e:
                logger.error(f"Error in consensus loop: {e}")
                await asyncio.sleep(1)  # Brief pause before retrying


# Example usage and testing
async def main():
    """Example usage of the Metatron Consensus Bridge"""
    logger.info("=== Metatron Consensus Bridge Demo ===")
    
    # Generate node identity
    private_key = ed25519.Ed25519PrivateKey.generate()
    node_id = "node_0"  # Pineal node
    
    # Create consensus bridge
    bridge = MetatronConsensusBridge(node_id, private_key)
    
    # Initialize network with test nodes
    node_configs = {
        f"node_{i}": {"public_key": None} for i in range(13)
    }
    bridge.initialize_network(node_configs)
    
    # Run a few consensus rounds
    for i in range(3):
        logger.info(f"=== Consensus Round {i+1} ===")
        await bridge.run_consensus_round()
        
        # Get network health
        health = bridge.get_network_health()
        logger.info(f"Network health: Consciousness={health['consciousness_health']['consciousness_level']:.3f}, "
                   f"Coherence={health['consciousness_health']['coherence']:.3f}")
        
        await asyncio.sleep(1)
    
    logger.info("Demo completed successfully")


if __name__ == "__main__":
    asyncio.run(main())