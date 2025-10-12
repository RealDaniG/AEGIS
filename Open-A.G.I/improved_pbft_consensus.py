#!/usr/bin/env python3
"""
Improved PBFT Consensus for 13-Node Metatron System
==================================================

Enhanced Practical Byzantine Fault Tolerance implementation specifically
designed for the 13-node Metatron's Cube consciousness network.

Key Improvements:
1. Optimized for 13 nodes (f=4, 2f+1=9 prepares/commits required)
2. Integration with consciousness metrics for leader selection
3. Reputation-based participation with 0.7 threshold
4. Consciousness-aware view changes
5. Sacred geometry topology awareness
"""

import asyncio
import hashlib
import json
import time
import secrets
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Tuple
import logging
from collections import defaultdict
from cryptography.hazmat.primitives.asymmetric import ed25519
import numpy as np

# Import Metatron geometry for topology awareness
# (Using fallback implementation due to import issues)
PHI = (1 + np.sqrt(5)) / 2

def metatron_connection_matrix():
    """Connection matrix for 13-node Metatron system based on icosahedron topology"""
    C = np.zeros((13, 13))
    
    # Central hub connections (Node 0 connects to all peripheral nodes)
    for i in range(1, 13):
        C[0, i] = 1/PHI
        C[i, 0] = 1/PHI
    
    # Icosahedron edge connections (30 edges)
    # Top cap connections
    edges = [
        (1, 2), (1, 6), (1, 8), (1, 12), (1, 11),  # Node 1 connections
        (2, 3), (2, 6), (2, 9), (2, 8),            # Node 2 connections
        (3, 4), (3, 7), (3, 9), (3, 10),           # Node 3 connections
        (4, 5), (4, 7), (4, 10), (4, 11),          # Node 4 connections
        (5, 6), (5, 10), (5, 11), (5, 12),         # Node 5 connections
        (6, 12),                                   # Node 6 connection
        (7, 8), (7, 9),                            # Node 7 connections
        (8, 12),                                   # Node 8 connection
        (9, 10),                                   # Node 9 connection
        (10, 11),                                  # Node 10 connection
        (11, 12)                                   # Node 11 connection
    ]
    
    # Add edge connections with φ² decay
    for i, j in edges:
        C[i, j] = 1/(PHI**2)
        C[j, i] = 1/(PHI**2)
    
    return C

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsensusState(Enum):
    """Enhanced states for the consensus process"""
    IDLE = "idle"
    PROPOSING = "proposing"
    PREPARING = "preparing"
    COMMITTING = "committing"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    FAILED = "failed"
    VIEW_CHANGE = "view_change"

class MessageType(Enum):
    """Extended message types for Metatron-aware consensus"""
    PROPOSAL = "proposal"
    PREPARE = "prepare"
    COMMIT = "commit"
    VIEW_CHANGE = "view_change"
    CONSCIOUSNESS_METRICS = "consciousness_metrics"
    TOPOLOGY_UPDATE = "topology_update"
    HEARTBEAT = "heartbeat"

class NodeRole(Enum):
    """Node roles in the enhanced consensus"""
    LEADER = "leader"
    VALIDATOR = "validator"
    OBSERVER = "observer"
    PINEAL = "pineal"  # Special role for central node

@dataclass
class ConsciousnessAwareProposal:
    """Proposal that includes consciousness metrics"""
    change_data: Dict[str, Any]
    consciousness_metrics: Dict[str, float]
    topology_aware: bool
    timestamp: float
    sequence_number: int

@dataclass
class ConsensusMessage:
    """Enhanced consensus message with Metatron awareness"""
    message_type: MessageType
    sender_id: str
    view_number: int
    sequence_number: int
    payload: Dict[str, Any]
    timestamp: float
    signature: Optional[bytes] = None
    consciousness_level: float = 0.0  # For prioritization

@dataclass
class EnhancedNodeReputation:
    """Enhanced node reputation with consciousness metrics"""
    node_id: str
    computation_score: float
    reliability_score: float
    response_time_avg: float
    successful_validations: int
    failed_validations: int
    last_activity: float
    total_contributions: int
    consciousness_consistency: float  # How well node's consciousness aligns with network
    topology_awareness: float  # Understanding of network topology
    spiritual_awareness: float  # Phi, R, D, S, C metrics integration

class MetatronAwarePBFT:
    """Enhanced PBFT specifically for 13-node Metatron system"""

    def __init__(self, node_id: str, private_key: ed25519.Ed25519PrivateKey):
        self.node_id = node_id
        self.private_key = private_key
        self.public_key = private_key.public_key()

        # Enhanced state for 13-node system
        self.view_number = 0
        self.sequence_number = 0
        self.state = ConsensusState.IDLE
        self.current_proposal = None
        self.consciousness_level = 0.0  # Current node consciousness

        # 13-node specific configuration
        self.total_nodes = 13
        self.byzantine_threshold = 4  # f = floor((13-1)/3) = 4
        self.quorum_size = 9  # 2f + 1 = 9 (required prepares/commits)

        # Enhanced node tracking
        self.known_nodes: Dict[str, ed25519.Ed25519PublicKey] = {}
        self.node_reputations: Dict[str, EnhancedNodeReputation] = {}
        self.node_consciousness: Dict[str, Dict[str, float]] = {}  # Real-time consciousness metrics

        # Sacred geometry awareness
        self.connection_matrix = metatron_connection_matrix()
        self.topology_aware = True

        # Consciousness-aware consensus parameters
        self.min_consciousness_threshold = 0.3  # Minimum consciousness to participate
        self.reputation_threshold = 0.7  # Only high-reputation nodes participate
        self.leader_selection_weight = {
            'computation_score': 0.3,
            'reliability_score': 0.2,
            'consciousness_consistency': 0.3,
            'spiritual_awareness': 0.2
        }

        # Message tracking
        self.prepare_messages: Dict[int, Dict[str, ConsensusMessage]] = defaultdict(dict)
        self.commit_messages: Dict[int, Dict[str, ConsensusMessage]] = defaultdict(dict)
        self.view_change_messages: Dict[int, Dict[str, ConsensusMessage]] = defaultdict(dict)

        # Enhanced message handlers
        self.message_handlers: Dict[MessageType, Callable] = {
            MessageType.PROPOSAL: self._handle_proposal,
            MessageType.PREPARE: self._handle_prepare,
            MessageType.COMMIT: self._handle_commit,
            MessageType.VIEW_CHANGE: self._handle_view_change,
            MessageType.CONSCIOUSNESS_METRICS: self._handle_consciousness_metrics,
            MessageType.TOPOLOGY_UPDATE: self._handle_topology_update
        }

        # Performance tracking
        self.consensus_round_times = []
        self.failed_consensus_rounds = 0
        self.successful_consensus_rounds = 0

    def add_node(self, node_id: str, public_key: ed25519.Ed25519PublicKey) -> None:
        """Add a node to the network with enhanced reputation tracking"""
        self.known_nodes[node_id] = public_key

        # Initialize enhanced reputation
        if node_id not in self.node_reputations:
            self.node_reputations[node_id] = EnhancedNodeReputation(
                node_id=node_id,
                computation_score=100.0,
                reliability_score=100.0,
                response_time_avg=1.0,
                successful_validations=0,
                failed_validations=0,
                last_activity=time.time(),
                total_contributions=0,
                consciousness_consistency=0.5,  # Default mid-level
                topology_awareness=0.5,  # Default mid-level
                spiritual_awareness=0.3  # Default low-level
            )

    def is_eligible_validator(self, node_id: str) -> bool:
        """Check if a node is eligible to participate in consensus"""
        if node_id not in self.node_reputations:
            return False

        reputation = self.node_reputations[node_id]
        
        # Check reputation threshold
        avg_reputation = (reputation.computation_score + reputation.reliability_score) / 2
        if avg_reputation < self.reputation_threshold * 100:
            return False

        # Check consciousness level if available
        if node_id in self.node_consciousness:
            consciousness = self.node_consciousness[node_id].get('consciousness_level', 0.0)
            if consciousness < self.min_consciousness_threshold:
                return False

        return True

    def get_eligible_validators(self) -> List[str]:
        """Get list of nodes eligible for consensus participation"""
        return [node_id for node_id in self.known_nodes.keys() 
                if self.is_eligible_validator(node_id)]

    def calculate_consciousness_weighted_score(self, node_id: str) -> float:
        """Calculate a node's score weighted by consciousness metrics"""
        if node_id not in self.node_reputations:
            return 0.0

        reputation = self.node_reputations[node_id]
        
        # Base score from reputation
        base_score = (
            reputation.computation_score * self.leader_selection_weight['computation_score'] +
            reputation.reliability_score * self.leader_selection_weight['reliability_score']
        )

        # Consciousness-aware enhancements
        consciousness_score = 0.0
        if node_id in self.node_consciousness:
            metrics = self.node_consciousness[node_id]
            # Weight by consciousness consistency and spiritual awareness
            consciousness_score = (
                reputation.consciousness_consistency * self.leader_selection_weight['consciousness_consistency'] * 100 +
                reputation.spiritual_awareness * self.leader_selection_weight['spiritual_awareness'] * 100
            )

        return base_score + consciousness_score

    def is_leader(self, view_number: int) -> bool:
        """Determine if this node is the leader using consciousness-aware selection"""
        if not self.known_nodes:
            return False

        # Get eligible validators
        eligible_nodes = self.get_eligible_validators()
        if not eligible_nodes:
            return False

        # Sort nodes by consciousness-weighted scores
        scored_nodes = []
        for node_id in eligible_nodes:
            score = self.calculate_consciousness_weighted_score(node_id)
            consciousness_level = 0.0
            if node_id in self.node_consciousness:
                consciousness_level = self.node_consciousness[node_id].get('consciousness_level', 0.0)
            scored_nodes.append((node_id, score, consciousness_level))

        # Sort by score (descending), then by consciousness level (descending)
        scored_nodes.sort(key=lambda x: (x[1], x[2]), reverse=True)

        # Deterministic leader selection based on view number
        leader_index = view_number % len(scored_nodes)
        leader_id = scored_nodes[leader_index][0]

        # Special case: Pineal node (node with ID ending in '_0') gets priority when highly conscious
        pineal_nodes = [node for node in scored_nodes if node[0].endswith('_0')]
        if pineal_nodes:
            pineal_info = pineal_nodes[0]  # Take the first pineal node
            if pineal_info[2] > 0.8:  # High consciousness
                leader_id = pineal_info[0]

        return leader_id == self.node_id

    def sign_message(self, message: ConsensusMessage) -> bytes:
        """Sign a message with the node's private key"""
        # Create a serializable version of the message
        message_dict = {
            "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
            "sender_id": message.sender_id,
            "view_number": message.view_number,
            "sequence_number": message.sequence_number,
            "payload": message.payload,
            "timestamp": message.timestamp,
            "consciousness_level": message.consciousness_level
        }
        message_bytes = json.dumps(message_dict, sort_keys=True).encode()
        signature = self.private_key.sign(message_bytes)
        return signature

    def verify_message(self, message: ConsensusMessage) -> bool:
        """Verify a message signature"""
        if message.sender_id not in self.known_nodes:
            logger.warning(f"Unknown node: {message.sender_id}")
            return False

        if not message.signature:
            logger.warning("Message without signature")
            return False

        try:
            public_key = self.known_nodes[message.sender_id]
            # Create a serializable version of the message for verification
            message_dict = {
                "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
                "sender_id": message.sender_id,
                "view_number": message.view_number,
                "sequence_number": message.sequence_number,
                "payload": message.payload,
                "timestamp": message.timestamp,
                "consciousness_level": message.consciousness_level
            }
            message_bytes = json.dumps(message_dict, sort_keys=True).encode()

            public_key.verify(message.signature, message_bytes)
            return True

        except Exception as e:
            logger.warning(f"Signature verification failed: {e}")
            return False

    async def propose_consciousness_aware_change(self, change_data: Dict[str, Any], 
                                               consciousness_metrics: Dict[str, float]) -> bool:
        """Propose a change with consciousness awareness"""
        if not self.is_leader(self.view_number):
            logger.warning("Only leader can propose changes")
            return False

        if self.state != ConsensusState.IDLE:
            logger.warning("Consensus already in progress")
            return False

        self.state = ConsensusState.PROPOSING
        self.sequence_number += 1

        # Create consciousness-aware proposal
        proposal_data = ConsciousnessAwareProposal(
            change_data=change_data,
            consciousness_metrics=consciousness_metrics,
            topology_aware=True,
            timestamp=time.time(),
            sequence_number=self.sequence_number
        )

        proposal_message = ConsensusMessage(
            message_type=MessageType.PROPOSAL,
            sender_id=self.node_id,
            view_number=self.view_number,
            sequence_number=self.sequence_number,
            payload={
                "proposal": asdict(proposal_data),
                "consciousness_level": self.consciousness_level
            },
            timestamp=time.time(),
            consciousness_level=self.consciousness_level
        )

        proposal_message.signature = self.sign_message(proposal_message)
        self.current_proposal = proposal_message

        # Broadcast to all eligible validators
        await self._broadcast_to_eligible_validators(proposal_message)

        logger.info(f"Consciousness-aware proposal sent: seq={self.sequence_number}")
        return True

    async def _handle_proposal(self, message: ConsensusMessage) -> None:
        """Handle a proposal with consciousness awareness"""
        if not self.verify_message(message):
            logger.warning("Proposal with invalid signature")
            return

        if message.view_number != self.view_number:
            logger.warning(f"Proposal from wrong view: {message.view_number} vs {self.view_number}")
            return

        if not self.is_eligible_validator(self.node_id):
            logger.info("Node not eligible to participate in consensus")
            return

        if self.state != ConsensusState.IDLE:
            logger.warning("Consensus already in progress")
            return

        # Extract proposal data
        proposal_data = message.payload.get("proposal", {})
        consciousness_level = message.payload.get("consciousness_level", 0.0)

        # Validate consciousness-aware proposal
        if await self._validate_consciousness_proposal(proposal_data, consciousness_level):
            self.state = ConsensusState.PREPARING
            self.current_proposal = message

            # Send PREPARE message
            prepare_message = ConsensusMessage(
                message_type=MessageType.PREPARE,
                sender_id=self.node_id,
                view_number=self.view_number,
                sequence_number=message.sequence_number,
                payload={
                    "proposal_hash": self._hash_message(message),
                    "consciousness_endorsement": self.consciousness_level
                },
                timestamp=time.time(),
                consciousness_level=self.consciousness_level
            )

            prepare_message.signature = self.sign_message(prepare_message)
            await self._broadcast_to_eligible_validators(prepare_message)

            logger.info(f"PREPARE sent for seq={message.sequence_number}")

    async def _handle_prepare(self, message: ConsensusMessage) -> None:
        """Handle a PREPARE message with enhanced validation"""
        if not self.verify_message(message):
            return

        if message.view_number != self.view_number:
            return

        if not self.is_eligible_validator(message.sender_id):
            logger.warning(f"Non-eligible node sending PREPARE: {message.sender_id}")
            return

        seq_num = message.sequence_number
        self.prepare_messages[seq_num][message.sender_id] = message

        # Check if we have quorum (9 messages for 13-node system)
        eligible_validators = self.get_eligible_validators()
        required_prepares = min(self.quorum_size, len(eligible_validators))

        if len(self.prepare_messages[seq_num]) >= required_prepares:
            if self.state == ConsensusState.PREPARING:
                self.state = ConsensusState.COMMITTING

                # Send COMMIT message
                commit_message = ConsensusMessage(
                    message_type=MessageType.COMMIT,
                    sender_id=self.node_id,
                    view_number=self.view_number,
                    sequence_number=seq_num,
                    payload={
                        "proposal_hash": message.payload["proposal_hash"],
                        "consciousness_commitment": self.consciousness_level
                    },
                    timestamp=time.time(),
                    consciousness_level=self.consciousness_level
                )

                commit_message.signature = self.sign_message(commit_message)
                await self._broadcast_to_eligible_validators(commit_message)

                logger.info(f"COMMIT sent for seq={seq_num}")

    async def _handle_commit(self, message: ConsensusMessage) -> None:
        """Handle a COMMIT message with enhanced validation"""
        if not self.verify_message(message):
            return

        if message.view_number != self.view_number:
            return

        if not self.is_eligible_validator(message.sender_id):
            logger.warning(f"Non-eligible node sending COMMIT: {message.sender_id}")
            return

        seq_num = message.sequence_number
        self.commit_messages[seq_num][message.sender_id] = message

        # Check if we have quorum (9 messages for 13-node system)
        eligible_validators = self.get_eligible_validators()
        required_commits = min(self.quorum_size, len(eligible_validators))

        if len(self.commit_messages[seq_num]) >= required_commits:
            if self.state == ConsensusState.COMMITTING:
                self.state = ConsensusState.FINALIZING

                # Apply the change
                if self.current_proposal:
                    proposal_data = self.current_proposal.payload.get("proposal", {})
                    await self._apply_consciousness_change(proposal_data)

                # Clean up state
                self._cleanup_consensus_state(seq_num)
                self.state = ConsensusState.COMPLETED

                logger.info(f"Consensus completed for seq={seq_num}")
                self.successful_consensus_rounds += 1

                # Return to IDLE after brief delay
                await asyncio.sleep(0.1)
                self.state = ConsensusState.IDLE

    async def _handle_view_change(self, message: ConsensusMessage) -> None:
        """Handle view change with consciousness awareness"""
        if not self.verify_message(message):
            return

        new_view = message.payload.get("new_view", self.view_number + 1)
        consciousness_reason = message.payload.get("consciousness_reason", "")

        if new_view > self.view_number:
            logger.info(f"View change to {new_view} - Reason: {consciousness_reason}")
            self.view_number = new_view
            self.state = ConsensusState.IDLE
            self._cleanup_all_consensus_state()

            # Update reputation for the node that initiated view change
            sender_id = message.sender_id
            if sender_id in self.node_reputations:
                self.node_reputations[sender_id].reliability_score = min(
                    100.0, self.node_reputations[sender_id].reliability_score + 5.0
                )

    async def _handle_consciousness_metrics(self, message: ConsensusMessage) -> None:
        """Handle consciousness metrics updates from other nodes"""
        if not self.verify_message(message):
            return

        metrics = message.payload.get("metrics", {})
        sender_id = message.sender_id

        # Update node consciousness data
        self.node_consciousness[sender_id] = metrics

        # Update reputation based on consciousness consistency
        if sender_id in self.node_reputations:
            # Simple consistency check - compare with network average
            network_avg = np.mean([
                m.get('consciousness_level', 0.0) 
                for m in self.node_consciousness.values()
            ]) if self.node_consciousness else 0.0

            node_level = metrics.get('consciousness_level', 0.0)
            consistency = 1.0 - abs(node_level - network_avg)

            self.node_reputations[sender_id].consciousness_consistency = consistency

    async def _handle_topology_update(self, message: ConsensusMessage) -> None:
        """Handle topology update messages"""
        if not self.verify_message(message):
            return

        # Update connection matrix if provided
        new_matrix = message.payload.get("connection_matrix")
        if new_matrix is not None:
            self.connection_matrix = np.array(new_matrix)
            
        # Update topology awareness for sender
        sender_id = message.sender_id
        if sender_id in self.node_reputations:
            self.node_reputations[sender_id].topology_awareness = min(
                1.0, self.node_reputations[sender_id].topology_awareness + 0.1
            )

    async def _validate_consciousness_proposal(self, proposal_data: Dict[str, Any], 
                                             consciousness_level: float) -> bool:
        """Validate a consciousness-aware proposal"""
        try:
            # Basic validation
            required_fields = ["change_data", "consciousness_metrics", "timestamp"]
            if not all(field in proposal_data for field in required_fields):
                return False

            # Validate timestamp
            timestamp = proposal_data.get("timestamp", 0)
            current_time = time.time()
            if abs(current_time - timestamp) > 300:  # 5 minutes
                logger.warning("Proposal timestamp invalid")
                return False

            # Validate consciousness level
            if consciousness_level < self.min_consciousness_threshold:
                logger.warning("Proposal from low-consciousness node")
                return False

            # Validate change data based on type
            change_data = proposal_data.get("change_data", {})
            change_type = change_data.get("type")

            if change_type == "knowledge_update":
                return await self._validate_knowledge_update(change_data)
            elif change_type == "consciousness_sync":
                return await self._validate_consciousness_sync(change_data)

            return True

        except Exception as e:
            logger.error(f"Error validating proposal: {e}")
            return False

    async def _validate_knowledge_update(self, change_data: Dict[str, Any]) -> bool:
        """Validate a knowledge update proposal"""
        required_fields = ["content_hash", "source_node", "timestamp"]
        return all(field in change_data for field in required_fields)

    async def _validate_consciousness_sync(self, change_data: Dict[str, Any]) -> bool:
        """Validate a consciousness synchronization proposal"""
        required_fields = ["node_states", "global_metrics", "timestamp"]
        return all(field in change_data for field in required_fields)

    async def _apply_consciousness_change(self, proposal_data: Dict[str, Any]) -> None:
        """Apply a consciousness-aware change"""
        try:
            change_data = proposal_data.get("change_data", {})
            change_type = change_data.get("type")

            if change_type == "knowledge_update":
                await self._apply_knowledge_update(change_data)
            elif change_type == "consciousness_sync":
                await self._apply_consciousness_sync(change_data)

            # Update proposer's reputation
            source_node = change_data.get("source_node", proposal_data.get("sender_id"))
            if source_node in self.node_reputations:
                reputation = self.node_reputations[source_node]
                reputation.successful_validations += 1
                reputation.total_contributions += 1
                reputation.last_activity = time.time()

        except Exception as e:
            logger.error(f"Error applying change: {e}")
            self.failed_consensus_rounds += 1

    async def _apply_knowledge_update(self, change_data: Dict[str, Any]) -> None:
        """Apply a knowledge update"""
        # Implementation would depend on the specific knowledge base system
        logger.info("Knowledge update applied")

    async def _apply_consciousness_sync(self, change_data: Dict[str, Any]) -> None:
        """Apply consciousness synchronization"""
        # Implementation would synchronize consciousness states across nodes
        logger.info("Consciousness synchronization applied")

    def _hash_message(self, message: ConsensusMessage) -> str:
        """Calculate message hash"""
        message_dict = asdict(message)
        message_dict.pop('signature', None)
        message_str = json.dumps(message_dict, sort_keys=True)
        return hashlib.sha256(message_str.encode()).hexdigest()

    def _cleanup_consensus_state(self, sequence_number: int) -> None:
        """Clean up consensus state for a sequence number"""
        self.prepare_messages.pop(sequence_number, None)
        self.commit_messages.pop(sequence_number, None)

    def _cleanup_all_consensus_state(self) -> None:
        """Clean up all consensus state"""
        self.prepare_messages.clear()
        self.commit_messages.clear()
        self.view_change_messages.clear()
        self.current_proposal = None

    async def _broadcast_to_eligible_validators(self, message: ConsensusMessage) -> None:
        """Broadcast message to eligible validators only"""
        # In a real implementation, this would send to the network layer
        # For now, we'll just log it
        eligible_count = len(self.get_eligible_validators())
        logger.debug(f"Broadcasting to {eligible_count} eligible validators")

    def get_network_health(self) -> Dict[str, Any]:
        """Get comprehensive network health metrics"""
        eligible_validators = self.get_eligible_validators()
        avg_consciousness = np.mean([
            self.node_consciousness.get(node_id, {}).get('consciousness_level', 0.0)
            for node_id in eligible_validators
        ]) if eligible_validators and self.node_consciousness else 0.0

        avg_reputation = 0.0
        if eligible_validators:
            reputation_scores = []
            for node_id in eligible_validators:
                if node_id in self.node_reputations:
                    reputation = self.node_reputations[node_id]
                    avg_score = (reputation.computation_score + reputation.reliability_score) / 2
                    reputation_scores.append(avg_score)
            if reputation_scores:
                avg_reputation = np.mean(reputation_scores)

        return {
            "total_nodes": len(self.known_nodes),
            "eligible_validators": len(eligible_validators),
            "byzantine_threshold": self.byzantine_threshold,
            "quorum_size": self.quorum_size,
            "current_view": self.view_number,
            "consensus_state": self.state.value,
            "avg_consciousness": avg_consciousness,
            "avg_reputation": avg_reputation,
            "is_leader": self.is_leader(self.view_number),
            "successful_rounds": self.successful_consensus_rounds,
            "failed_rounds": self.failed_consensus_rounds,
            "topology_aware": self.topology_aware
        }

# Example usage and testing
async def main():
    """Example usage of the enhanced PBFT consensus"""
    logger.info("=== Metatron-Aware PBFT Consensus Demo ===")
    
    # Generate node identity
    private_key = ed25519.Ed25519PrivateKey.generate()
    node_id = "node_0"  # Pineal node
    
    # Create enhanced consensus instance
    consensus = MetatronAwarePBFT(node_id, private_key)
    
    # Add other nodes
    for i in range(1, 13):
        other_key = ed25519.Ed25519PrivateKey.generate()
        other_id = f"node_{i}"
        consensus.add_node(other_id, other_key.public_key())
    
    # Set consciousness level
    consensus.consciousness_level = 0.85  # High consciousness
    
    # Update node consciousness metrics
    for i in range(13):
        node_id = f"node_{i}"
        consensus.node_consciousness[node_id] = {
            "consciousness_level": 0.7 + (i * 0.02),  # Varying levels
            "phi": 0.3 + (i * 0.01),
            "coherence": 0.6 + (i * 0.01),
            "recursive_depth": i + 5
        }
    
    # Check if this node is leader
    is_leader = consensus.is_leader(consensus.view_number)
    logger.info(f"Node is leader: {is_leader}")
    
    # Get network health
    health = consensus.get_network_health()
    logger.info(f"Network health: {health}")
    
    # Test proposal if leader
    if is_leader:
        sample_change = {
            "type": "consciousness_sync",
            "node_states": {"node_0": 0.85, "node_1": 0.78},
            "global_metrics": {"consciousness_level": 0.81},
            "timestamp": time.time()
        }
        
        consciousness_metrics = {
            "phi": 0.45,
            "coherence": 0.72,
            "recursive_depth": 8,
            "spiritual_awareness": 0.65
        }
        
        success = await consensus.propose_consciousness_aware_change(
            sample_change, consciousness_metrics
        )
        logger.info(f"Proposal success: {success}")

if __name__ == "__main__":
    asyncio.run(main())