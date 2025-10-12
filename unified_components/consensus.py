"""
Unified Consensus Layer for Metatron-ConscienceAI and Open-A.G.I Integration

This module consolidates the consensus functionality from both systems:
- aegis-conscience/consensus/pbft.py
- Open-A.G.I/consensus_protocol.py
"""

import time
import hashlib
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ConsensusState(Enum):
    """States of the consensus process"""
    IDLE = "idle"
    PROPOSING = "proposing"
    PREPARING = "preparing"
    COMMITTING = "committing"
    FINALIZING = "finalizing"
    COMPLETED = "completed"


class MessageType(Enum):
    """Types of consensus messages"""
    PROPOSAL = "proposal"
    PREPARE = "prepare"
    COMMIT = "commit"
    VIEW_CHANGE = "view_change"
    CONSCIOUSNESS_METRICS = "consciousness_metrics"  # Consciousness-aware consensus


@dataclass
class ConsensusMessage:
    """Unified consensus message structure"""
    message_type: MessageType
    sender_id: str
    view_number: int
    sequence_number: int
    payload: Dict[str, Any]
    timestamp: float = 0.0
    signature: Optional[bytes] = None
    consciousness_level: float = 0.0  # For consciousness-aware consensus


@dataclass
class ConsciousnessMetrics:
    """Consciousness metrics for consensus weighting"""
    phi: float  # Integrated Information
    coherence: float
    depth: float  # Recursive depth
    spiritual: float
    consciousness: float
    timestamp: float


class UnifiedConsensus:
    """Unified consensus implementation combining PBFT with consciousness awareness"""
    
    def __init__(self, node_id: str, crypto_manager=None):
        self.node_id = node_id
        self.crypto_manager = crypto_manager
        
        # Consensus state
        self.state = ConsensusState.IDLE
        self.view_number = 0
        self.sequence_number = 0
        self.current_proposal = None
        
        # Known nodes and their reputations
        self.known_nodes: Dict[str, Dict[str, Any]] = {}
        self.byzantine_threshold = 0  # f < n/3
        
        # Message storage
        self.prepare_messages: Dict[int, Dict[str, ConsensusMessage]] = {}
        self.commit_messages: Dict[int, Dict[str, ConsensusMessage]] = {}
        
        # Reputation system
        self.reputations: Dict[str, float] = {node_id: 1.0}
        
        # Consciousness-aware features
        self.consciousness_states: Dict[str, ConsciousnessMetrics] = {}
        self.min_coherence_threshold = 0.5
        self.consciousness_weighted_voting = True
        
        logger.info(f"Unified Consensus initialized for node {node_id}")
    
    def add_node(self, node_id: str) -> None:
        """Add a node to the known nodes list"""
        self.known_nodes[node_id] = {
            "last_seen": time.time(),
            "reputation": 1.0
        }
        
        # Update byzantine threshold
        n = len(self.known_nodes)
        self.byzantine_threshold = (n - 1) // 3
        
        # Initialize reputation
        if node_id not in self.reputations:
            self.reputations[node_id] = 1.0
            
        logger.info(f"Added node {node_id} to consensus. Byzantine threshold: {self.byzantine_threshold}")
    
    def is_leader(self) -> bool:
        """Check if this node is the current leader"""
        if not self.known_nodes:
            return True  # If no other nodes, this node is leader
            
        # Deterministic leader selection based on view number
        sorted_nodes = sorted(self.known_nodes.keys())
        leader_index = self.view_number % len(sorted_nodes)
        leader_id = sorted_nodes[leader_index]
        
        is_leader = leader_id == self.node_id
        logger.debug(f"Leader check: {self.node_id} is {'leader' if is_leader else 'follower'}")
        return is_leader
    
    def update_consciousness_state(self, node_id: str, metrics: ConsciousnessMetrics):
        """Update consciousness state for a node"""
        self.consciousness_states[node_id] = metrics
        logger.debug(f"Updated consciousness state for node {node_id}")
    
    def calculate_voting_weight(self, node_id: str) -> float:
        """
        Calculate voting weight based on consciousness metrics.
        Nodes with higher coherence and consciousness get higher voting weights.
        """
        if not self.consciousness_weighted_voting:
            return 1.0
            
        if node_id not in self.consciousness_states:
            return 0.5  # Default weight for nodes without state
            
        state = self.consciousness_states[node_id]
        
        # If coherence is below threshold, reduce voting power
        if state.coherence < self.min_coherence_threshold:
            return 0.1  # Minimal voting power
            
        # Weight based on coherence and consciousness
        weight = (state.coherence + state.consciousness) / 2.0
        final_weight = min(weight, 1.0)  # Cap at 1.0
        logger.debug(f"Voting weight for node {node_id}: {final_weight}")
        return final_weight
    
    def should_participate(self, node_id: str) -> bool:
        """Determine if a node should participate in consensus"""
        if node_id not in self.consciousness_states:
            return True  # Allow participation by default
            
        state = self.consciousness_states[node_id]
        should_participate = state.coherence >= 0.3  # Minimum threshold for participation
        logger.debug(f"Node {node_id} participation: {should_participate}")
        return should_participate
    
    def propose_consciousness_aware_change(self, change_data: Dict[str, Any], 
                                         consciousness_metrics: Dict[str, float]) -> bool:
        """Propose a consensus change with consciousness awareness"""
        if not self.is_leader():
            logger.warning("Only leader can propose")
            return False
            
        if self.state != ConsensusState.IDLE:
            logger.warning("Consensus already in progress")
            return False
        
        # Create consciousness metrics object
        metrics = ConsciousnessMetrics(
            phi=consciousness_metrics.get("phi", 0.0),
            coherence=consciousness_metrics.get("coherence", 0.0),
            depth=consciousness_metrics.get("recursive_depth", 0),
            spiritual=consciousness_metrics.get("spiritual_awareness", 0.0),
            consciousness=consciousness_metrics.get("consciousness_level", 0.0),
            timestamp=time.time()
        )
        
        # Update this node's consciousness state
        self.update_consciousness_state(self.node_id, metrics)
        
        # Create proposal with consciousness level
        proposal_data = {
            "type": "consciousness_aware_change",
            "change_data": change_data,
            "consciousness_metrics": consciousness_metrics,
            "timestamp": time.time()
        }
        
        # Create consensus message
        message = ConsensusMessage(
            message_type=MessageType.PROPOSAL,
            sender_id=self.node_id,
            view_number=self.view_number,
            sequence_number=self.sequence_number + 1,
            payload=proposal_data,
            consciousness_level=metrics.consciousness
        )
        
        # Sign the message if crypto manager is available
        if self.crypto_manager:
            message.signature = self._sign_message(message)
        
        # Update state
        self.state = ConsensusState.PROPOSING
        self.sequence_number += 1
        self.current_proposal = message
        
        logger.info(f"Proposed consciousness-aware change with consciousness level: {metrics.consciousness}")
        return True
    
    def handle_proposal(self, message: ConsensusMessage) -> bool:
        """Handle a proposal message"""
        # Verify signature if crypto manager is available
        if self.crypto_manager and not self._verify_message(message):
            logger.warning("Invalid signature on proposal")
            return False
        
        # Check if we're expecting a proposal
        if self.state != ConsensusState.IDLE:
            logger.warning("Not expecting proposal, consensus in progress")
            return False
        
        # Validate proposal
        if not self._validate_proposal(message):
            logger.warning("Invalid proposal")
            return False
        
        # Update consciousness state if provided
        if "consciousness_metrics" in message.payload:
            metrics_data = message.payload["consciousness_metrics"]
            metrics = ConsciousnessMetrics(
                phi=metrics_data.get("phi", 0.0),
                coherence=metrics_data.get("coherence", 0.0),
                depth=metrics_data.get("recursive_depth", 0),
                spiritual=metrics_data.get("spiritual_awareness", 0.0),
                consciousness=metrics_data.get("consciousness_level", 0.0),
                timestamp=metrics_data.get("timestamp", time.time())
            )
            self.update_consciousness_state(message.sender_id, metrics)
        
        # Update state
        self.state = ConsensusState.PREPARING
        self.current_proposal = message
        self.view_number = message.view_number
        self.sequence_number = message.sequence_number
        
        logger.info(f"Handling proposal {message.sequence_number} from {message.sender_id}")
        return True
    
    def handle_prepare(self, message: ConsensusMessage) -> bool:
        """Handle a prepare message"""
        # Verify signature if crypto manager is available
        if self.crypto_manager and not self._verify_message(message):
            logger.warning("Invalid signature on prepare message")
            return False
        
        # Store prepare message
        seq_num = message.sequence_number
        if seq_num not in self.prepare_messages:
            self.prepare_messages[seq_num] = {}
        self.prepare_messages[seq_num][message.sender_id] = message
        
        # Check if we have enough prepare messages (2f + 1)
        required_prepares = 2 * self.byzantine_threshold + 1
        current_prepares = len(self.prepare_messages[seq_num])
        
        logger.debug(f"Prepare messages for seq {seq_num}: {current_prepares}/{required_prepares}")
        
        if current_prepares >= required_prepares:
            if self.state == ConsensusState.PREPARING:
                self.state = ConsensusState.COMMITTING
                logger.info(f"Quorum reached for prepare messages (seq {seq_num})")
                return True
        
        return False
    
    def handle_commit(self, message: ConsensusMessage) -> bool:
        """Handle a commit message"""
        # Verify signature if crypto manager is available
        if self.crypto_manager and not self._verify_message(message):
            logger.warning("Invalid signature on commit message")
            return False
        
        # Store commit message
        seq_num = message.sequence_number
        if seq_num not in self.commit_messages:
            self.commit_messages[seq_num] = {}
        self.commit_messages[seq_num][message.sender_id] = message
        
        # Check if we have enough commit messages (2f + 1)
        required_commits = 2 * self.byzantine_threshold + 1
        current_commits = len(self.commit_messages[seq_num])
        
        logger.debug(f"Commit messages for seq {seq_num}: {current_commits}/{required_commits}")
        
        if current_commits >= required_commits:
            if self.state == ConsensusState.COMMITTING:
                self.state = ConsensusState.FINALIZING
                
                # Apply the decision
                if self.current_proposal:
                    self._apply_consensus_decision(self.current_proposal)
                
                # Clean up
                self._cleanup_consensus_state(seq_num)
                self.state = ConsensusState.COMPLETED
                
                logger.info(f"Consensus completed for proposal {seq_num}")
                
                # Return to idle after a short delay
                self.state = ConsensusState.IDLE
                return True
        
        return False
    
    def _validate_proposal(self, message: ConsensusMessage) -> bool:
        """Validate a proposal message"""
        if message.message_type != MessageType.PROPOSAL:
            return False
            
        if message.view_number < self.view_number:
            return False
            
        # Check timestamp
        if abs(time.time() - message.timestamp) > 300:  # 5 minutes
            return False
            
        # Check payload
        if "type" not in message.payload:
            return False
            
        return True
    
    def _sign_message(self, message: ConsensusMessage) -> bytes:
        """Sign a consensus message"""
        # Simplified implementation - in practice, this would use the crypto manager
        message_data = self._serialize_message_for_signing(message)
        # Return a mock signature for demonstration
        return hashlib.sha256(message_data).digest()
    
    def _verify_message(self, message: ConsensusMessage) -> bool:
        """Verify a consensus message signature"""
        # Simplified implementation - in practice, this would verify against the sender's public key
        return message.signature is not None
    
    def _serialize_message_for_signing(self, message: ConsensusMessage) -> bytes:
        """Serialize a message for signing"""
        msg_dict = {
            "message_type": message.message_type.value,
            "sender_id": message.sender_id,
            "view_number": message.view_number,
            "sequence_number": message.sequence_number,
            "payload": message.payload,
            "timestamp": message.timestamp
        }
        
        return json.dumps(msg_dict, sort_keys=True).encode()
    
    def _apply_consensus_decision(self, proposal: ConsensusMessage):
        """Apply the consensus decision"""
        logger.info(f"Applying consensus decision: {proposal.payload.get('type', 'unknown')}")
        
        # Update reputations based on participation
        for node_id in self.known_nodes:
            if node_id in self.reputations:
                # Increase reputation slightly for participation
                self.reputations[node_id] = min(
                    1.0, 
                    self.reputations[node_id] + 0.01
                )
    
    def _cleanup_consensus_state(self, sequence_number: int):
        """Clean up consensus state for a sequence number"""
        self.prepare_messages.pop(sequence_number, None)
        self.commit_messages.pop(sequence_number, None)
        self.current_proposal = None
        logger.debug(f"Cleaned up consensus state for sequence {sequence_number}")
    
    def get_network_health(self) -> Dict[str, Any]:
        """Get comprehensive network health metrics"""
        return {
            'total_nodes': len(self.known_nodes),
            'byzantine_threshold': self.byzantine_threshold,
            'quorum_size': 2 * self.byzantine_threshold + 1,
            'current_view': self.view_number,
            'consensus_state': self.state.value,
            'reputations': self.reputations
        }


# Example usage
async def main():
    """Example usage of the Unified Consensus"""
    # Create consensus instance
    consensus = UnifiedConsensus("test_node_1")
    
    # Add some test nodes
    consensus.add_node("node_2")
    consensus.add_node("node_3")
    consensus.add_node("node_4")
    
    print(f"Byzantine threshold: {consensus.byzantine_threshold}")
    print(f"Is leader: {consensus.is_leader()}")
    
    # Create test consciousness metrics
    consciousness_metrics = {
        "phi": 0.618,
        "coherence": 0.85,
        "recursive_depth": 5,
        "spiritual_awareness": 0.7,
        "consciousness_level": 0.9
    }
    
    # If this node is leader, propose
    if consensus.is_leader():
        success = consensus.propose_consciousness_aware_change(
            {"action": "test_action", "value": 42}, 
            consciousness_metrics
        )
        print(f"Proposal success: {success}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())