"""
PBFT (Practical Byzantine Fault Tolerance) Consensus for AEGIS-Conscience Network
Leader-based PBFT for small networks (<10 nodes)
"""

import time
import hashlib
import json
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from enum import Enum

from schemas import ConsciousnessState
from network.crypto import CryptoManager


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


class ConsensusMessage:
    """Message used in the consensus protocol"""
    
    def __init__(self, message_type: MessageType, sender_id: str, 
                 view_number: int, sequence_number: int, payload: Dict[str, Any],
                 timestamp: float = 0.0, signature: Optional[bytes] = None):
        self.message_type = message_type
        self.sender_id = sender_id
        self.view_number = view_number
        self.sequence_number = sequence_number
        self.payload = payload
        self.timestamp = timestamp or time.time()
        self.signature = signature


class PBFTConsensus:
    """PBFT consensus implementation for consciousness network"""
    
    def __init__(self, node_id: str, crypto_manager: CryptoManager):
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
    
    def is_leader(self) -> bool:
        """Check if this node is the current leader"""
        if not self.known_nodes:
            return True  # If no other nodes, this node is leader
            
        # Deterministic leader selection based on view number
        sorted_nodes = sorted(self.known_nodes.keys())
        leader_index = self.view_number % len(sorted_nodes)
        leader_id = sorted_nodes[leader_index]
        
        return leader_id == self.node_id
    
    def propose_global_coherence(self, consciousness_states: List[ConsciousnessState]) -> bool:
        """Propose a global coherence value based on collected states"""
        if not self.is_leader():
            print("Only leader can propose")
            return False
            
        if self.state != ConsensusState.IDLE:
            print("Consensus already in progress")
            return False
        
        # Calculate global coherence
        global_coherence = self._calculate_global_coherence(consciousness_states)
        
        # Create proposal
        proposal_data = {
            "type": "global_coherence",
            "value": global_coherence,
            "states_count": len(consciousness_states),
            "timestamp": time.time()
        }
        
        # Create consensus message
        message = ConsensusMessage(
            message_type=MessageType.PROPOSAL,
            sender_id=self.node_id,
            view_number=self.view_number,
            sequence_number=self.sequence_number + 1,
            payload=proposal_data
        )
        
        # Sign the message
        message.signature = self._sign_message(message)
        
        # Update state
        self.state = ConsensusState.PROPOSING
        self.sequence_number += 1
        self.current_proposal = message
        
        print(f"Proposed global coherence: {global_coherence}")
        return True
    
    def handle_proposal(self, message: ConsensusMessage) -> bool:
        """Handle a proposal message"""
        # Verify signature
        if not self._verify_message(message):
            print("Invalid signature on proposal")
            return False
        
        # Check if we're expecting a proposal
        if self.state != ConsensusState.IDLE:
            print("Not expecting proposal, consensus in progress")
            return False
        
        # Validate proposal
        if not self._validate_proposal(message):
            print("Invalid proposal")
            return False
        
        # Update state
        self.state = ConsensusState.PREPARING
        self.current_proposal = message
        self.view_number = message.view_number
        self.sequence_number = message.sequence_number
        
        # Send prepare message
        prepare_msg = self._create_prepare_message(message)
        print(f"Sending PREPARE for proposal {message.sequence_number}")
        return True
    
    def handle_prepare(self, message: ConsensusMessage) -> bool:
        """Handle a prepare message"""
        # Verify signature
        if not self._verify_message(message):
            print("Invalid signature on prepare message")
            return False
        
        # Store prepare message
        seq_num = message.sequence_number
        if seq_num not in self.prepare_messages:
            self.prepare_messages[seq_num] = {}
        self.prepare_messages[seq_num][message.sender_id] = message
        
        # Check if we have enough prepare messages (2f + 1)
        required_prepares = 2 * self.byzantine_threshold + 1
        if len(self.prepare_messages[seq_num]) >= required_prepares:
            if self.state == ConsensusState.PREPARING:
                self.state = ConsensusState.COMMITTING
                
                # Send commit message
                commit_msg = self._create_commit_message(message)
                print(f"Sending COMMIT for proposal {seq_num}")
                return True
        
        return False
    
    def handle_commit(self, message: ConsensusMessage) -> bool:
        """Handle a commit message"""
        # Verify signature
        if not self._verify_message(message):
            print("Invalid signature on commit message")
            return False
        
        # Store commit message
        seq_num = message.sequence_number
        if seq_num not in self.commit_messages:
            self.commit_messages[seq_num] = {}
        self.commit_messages[seq_num][message.sender_id] = message
        
        # Check if we have enough commit messages (2f + 1)
        required_commits = 2 * self.byzantine_threshold + 1
        if len(self.commit_messages[seq_num]) >= required_commits:
            if self.state == ConsensusState.COMMITTING:
                self.state = ConsensusState.FINALIZING
                
                # Apply the decision
                if self.current_proposal:
                    self._apply_consensus_decision(self.current_proposal)
                
                # Clean up
                self._cleanup_consensus_state(seq_num)
                self.state = ConsensusState.COMPLETED
                
                print(f"Consensus completed for proposal {seq_num}")
                
                # Return to idle after a short delay
                self.state = ConsensusState.IDLE
                return True
        
        return False
    
    def _calculate_global_coherence(self, consciousness_states: List[ConsciousnessState]) -> float:
        """Calculate global coherence as average of local coherences"""
        if not consciousness_states:
            return 0.0
        
        # Filter by reputation (only include trusted nodes)
        trusted_states = [
            state for state in consciousness_states 
            if self.reputations.get(state.node_id, 0) > 0.7
        ]
        
        if not trusted_states:
            return 0.0
        
        # Calculate weighted average based on reputation
        total_weighted_coherence = 0.0
        total_weight = 0.0
        
        for state in trusted_states:
            weight = self.reputations.get(state.node_id, 0)
            total_weighted_coherence += state.coherence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_weighted_coherence / total_weight
    
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
        if "type" not in message.payload or "value" not in message.payload:
            return False
            
        return True
    
    def _create_prepare_message(self, proposal: ConsensusMessage) -> ConsensusMessage:
        """Create a prepare message for a proposal"""
        prepare_msg = ConsensusMessage(
            message_type=MessageType.PREPARE,
            sender_id=self.node_id,
            view_number=proposal.view_number,
            sequence_number=proposal.sequence_number,
            payload={
                "proposal_hash": self._hash_message(proposal)
            }
        )
        
        prepare_msg.signature = self._sign_message(prepare_msg)
        return prepare_msg
    
    def _create_commit_message(self, prepare: ConsensusMessage) -> ConsensusMessage:
        """Create a commit message"""
        commit_msg = ConsensusMessage(
            message_type=MessageType.COMMIT,
            sender_id=self.node_id,
            view_number=prepare.view_number,
            sequence_number=prepare.sequence_number,
            payload=prepare.payload  # Same payload as prepare
        )
        
        commit_msg.signature = self._sign_message(commit_msg)
        return commit_msg
    
    def _sign_message(self, message: ConsensusMessage) -> bytes:
        """Sign a consensus message"""
        message_data = self._serialize_message_for_signing(message)
        return self.crypto_manager.sign_state(
            ConsciousnessState(
                node_id=message.sender_id,
                timestamp=message.timestamp,
                entropy=0.0,
                valence=0.0,
                arousal=0.0,
                coherence=0.0,
                empathy_score=0.0,
                insight_strength=0.0
            )
        )
    
    def _verify_message(self, message: ConsensusMessage) -> bool:
        """Verify a consensus message signature"""
        # This is a simplified implementation
        # In practice, you would verify against the sender's public key
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
    
    def _hash_message(self, message: ConsensusMessage) -> str:
        """Calculate hash of a message"""
        msg_bytes = self._serialize_message_for_signing(message)
        return hashlib.sha256(msg_bytes).hexdigest()
    
    def _apply_consensus_decision(self, proposal: ConsensusMessage):
        """Apply the consensus decision"""
        if proposal.payload["type"] == "global_coherence":
            global_coherence = proposal.payload["value"]
            print(f"Global coherence agreed upon: {global_coherence}")
            
            # Update reputations based on participation
            # This is a simplified implementation
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
    
    def get_reputation(self, node_id: str) -> float:
        """Get reputation score for a node"""
        return self.reputations.get(node_id, 0.0)
    
    def update_reputation(self, node_id: str, score_delta: float):
        """Update reputation score for a node"""
        if node_id in self.reputations:
            self.reputations[node_id] = max(
                0.0, 
                min(1.0, self.reputations[node_id] + score_delta)
            )


# Example usage
if __name__ == "__main__":
    # Create crypto manager and PBFT consensus
    crypto = CryptoManager("test_node_1")
    pbft = PBFTConsensus("test_node_1", crypto)
    
    # Add some test nodes
    pbft.add_node("node_2")
    pbft.add_node("node_3")
    pbft.add_node("node_4")
    
    print(f"Byzantine threshold: {pbft.byzantine_threshold}")
    print(f"Is leader: {pbft.is_leader()}")
    
    # Create test consciousness states
    states = [
        ConsciousnessState("node_2", time.time(), 0.5, 0.3, 0.7, 0.8, 0.6, 0.4),
        ConsciousnessState("node_3", time.time(), 0.4, 0.2, 0.6, 0.7, 0.5, 0.3),
        ConsciousnessState("node_4", time.time(), 0.6, 0.4, 0.8, 0.9, 0.7, 0.5)
    ]
    
    # If this node is leader, propose
    if pbft.is_leader():
        pbft.propose_global_coherence(states)