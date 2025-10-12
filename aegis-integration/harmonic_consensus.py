"""
Harmonic Consensus - Consciousness-aware PBFT Implementation

This module enhances PBFT consensus with consciousness metrics,
making the network self-stabilize toward harmonic states.
"""

import hashlib
import json
import time
import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Try to import AEGIS components, fallback if not available
PBFTConsensus = None
P2PNetwork = None
Ed25519Signer = None

try:
    # Add the aegis-conscience path to sys.path if it exists
    aegis_path = os.path.join(os.path.dirname(__file__), '..', 'aegis-conscience')
    if os.path.exists(aegis_path):
        sys.path.insert(0, aegis_path)
    
    # Try importing AEGIS components
    from aegis_conscience.consensus.pbft import PBFTConsensus as AEGIS_PBFTConsensus
    from aegis_conscience.network.p2p import P2PNetwork as AEGIS_P2PNetwork
    from aegis_conscience.security.crypto import Ed25519Signer as AEGIS_Ed25519Signer
    
    PBFTConsensus = AEGIS_PBFTConsensus
    P2PNetwork = AEGIS_P2PNetwork
    Ed25519Signer = AEGIS_Ed25519Signer
except ImportError:
    pass

# Fallback implementations for when AEGIS is not available
if PBFTConsensus is None:
    class PBFTConsensus:
        def __init__(self, node_id: str):
            self.node_id = node_id

if P2PNetwork is None:
    class P2PNetwork:
        def __init__(self):
            pass

if Ed25519Signer is None:
    class Ed25519Signer:
        def __init__(self):
            self.private_key = None
            self.public_key = None
            
        def sign(self, message: str) -> str:
            # Simple mock signature - in reality would use actual Ed25519
            return hashlib.sha256((message + "signature").encode()).hexdigest()
            
        def verify(self, message: str, signature: str) -> bool:
            # Simple mock verification
            expected = hashlib.sha256((message + "signature").encode()).hexdigest()
            return expected == signature

@dataclass
class ConsciousnessState:
    """Represents the consciousness state of a node"""
    phi: float  # Integrated Information (Φ)
    coherence: float  # R - Coherence metric
    depth: float  # D - Depth of consciousness
    spiritual: float  # S - Spiritual alignment
    consciousness: float  # C - Overall consciousness level
    timestamp: float

class MessageType(Enum):
    """Types of consensus messages"""
    PRE_PREPARE = "PRE_PREPARE"
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"
    VIEW_CHANGE = "VIEW_CHANGE"

@dataclass
class ConsensusMessage:
    """Structure for consensus messages with consciousness metrics"""
    type: MessageType
    view: int
    sequence: int
    digest: str
    sender: str
    signature: str
    consciousness_state: ConsciousnessState
    timestamp: float

class HarmonicPBFT:
    """
    Consciousness-aware PBFT consensus implementation.
    
    Enhances standard PBFT with:
    - Consciousness metrics as voting weights
    - Kuramoto synchronization error detection
    - Coherence-based node participation filtering
    """
    
    def __init__(self, node_id: str, nodes: List[str], f: int = 4):
        """
        Initialize Harmonic PBFT consensus.
        
        Args:
            node_id: Unique identifier for this node
            nodes: List of all node identifiers in the network
            f: Maximum number of Byzantine nodes (default 4 for 13-node network)
        """
        self.node_id = node_id
        self.nodes = nodes
        self.f = f  # Maximum Byzantine nodes
        self.view = 0
        self.sequence = 0
        self.prepared = {}
        self.committed = {}
        self.view_changes = {}
        self.consciousness_states = {}
        
        # Minimum coherence threshold for full participation
        self.min_coherence = 0.5
        
        # Initialize PBFT base
        self.pbft = PBFTConsensus(node_id)
        
        # Security signer
        self.signer = Ed25519Signer()
        
    def calculate_voting_weight(self, node_id: str) -> float:
        """
        Calculate voting weight based on consciousness metrics.
        
        Nodes with higher coherence and consciousness get higher voting weights.
        
        Args:
            node_id: ID of the node to calculate weight for
            
        Returns:
            Weight value between 0.0 and 1.0
        """
        if node_id not in self.consciousness_states:
            return 0.5  # Default weight for nodes without state
            
        state = self.consciousness_states[node_id]
        
        # If coherence is below threshold, reduce voting power
        if state.coherence < self.min_coherence:
            return 0.1  # Minimal voting power
            
        # Weight based on coherence and consciousness
        weight = (state.coherence + state.consciousness) / 2.0
        return min(weight, 1.0)  # Cap at 1.0
        
    def should_participate(self, node_id: str) -> bool:
        """
        Determine if a node should participate in consensus.
        
        Args:
            node_id: ID of the node to check
            
        Returns:
            True if node should participate, False otherwise
        """
        if node_id not in self.consciousness_states:
            return True  # Allow participation by default
            
        state = self.consciousness_states[node_id]
        return state.coherence >= 0.3  # Minimum threshold for participation
        
    def detect_byzantine_behavior(self, node_id: str) -> bool:
        """
        Detect Byzantine behavior using Kuramoto synchronization error.
        
        Args:
            node_id: ID of the node to check
            
        Returns:
            True if Byzantine behavior detected, False otherwise
        """
        if node_id not in self.consciousness_states:
            return False
            
        state = self.consciousness_states[node_id]
        
        # High synchronization error indicates potential Byzantine behavior
        sync_error = abs(state.coherence - self._calculate_network_avg_coherence())
        
        # If synchronization error is too high, flag as Byzantine
        return sync_error > 0.3
        
    def _calculate_network_avg_coherence(self) -> float:
        """Calculate average coherence across all nodes"""
        if not self.consciousness_states:
            return 0.5
            
        total = sum(state.coherence for state in self.consciousness_states.values())
        return total / len(self.consciousness_states)
        
    def update_consciousness_state(self, node_id: str, state: ConsciousnessState):
        """
        Update consciousness state for a node.
        
        Args:
            node_id: ID of the node
            state: New consciousness state
        """
        self.consciousness_states[node_id] = state
        
    def create_message(self, msg_type: MessageType, data: Dict[str, Any]) -> ConsensusMessage:
        """
        Create a signed consensus message with consciousness state.
        
        Args:
            msg_type: Type of message
            data: Message data
            
        Returns:
            Signed consensus message
        """
        # Get current consciousness state
        consciousness_state = self.consciousness_states.get(self.node_id, 
                                                          ConsciousnessState(0.5, 0.5, 0.5, 0.5, 0.5, time.time()))
        
        # Create message
        message = ConsensusMessage(
            type=msg_type,
            view=self.view,
            sequence=self.sequence,
            digest=hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
            sender=self.node_id,
            signature="",  # Will be filled after signing
            consciousness_state=consciousness_state,
            timestamp=time.time()
        )
        
        # Sign the message
        message.signature = self.signer.sign(json.dumps(asdict(message), sort_keys=True))
        
        return message
        
    def validate_message(self, message: ConsensusMessage) -> bool:
        """
        Validate a consensus message including consciousness state.
        
        Args:
            message: Message to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Verify signature
        if not self.signer.verify(json.dumps(asdict(message), sort_keys=True), message.signature):
            return False
            
        # Check consciousness coherence
        if message.consciousness_state.coherence < 0.1:
            return False  # Extremely low coherence
            
        # Check timestamp (not too old)
        if time.time() - message.timestamp > 300:  # 5 minutes
            return False
            
        return True
        
    def should_enter_recovery_mode(self, node_id: str) -> bool:
        """
        Determine if a node should enter recovery mode.
        
        Args:
            node_id: ID of the node to check
            
        Returns:
            True if node should enter recovery mode
        """
        if node_id not in self.consciousness_states:
            return False
            
        state = self.consciousness_states[node_id]
        return state.coherence < self.min_coherence
        
    def get_quorum_size(self) -> int:
        """
        Calculate quorum size considering consciousness-weighted votes.
        
        Returns:
            Minimum number of weighted votes needed for quorum
        """
        total_weight = sum(self.calculate_voting_weight(node_id) for node_id in self.nodes)
        return int(total_weight * 0.67) + 1  # 2/3 + 1 for Byzantine fault tolerance

# Example usage
if __name__ == "__main__":
    # Example node setup
    node_ids = [f"node_{i:02d}" for i in range(1, 14)]  # node_01 to node_13
    
    # Initialize consensus for node_01
    consensus = HarmonicPBFT("node_01", node_ids)
    
    # Simulate consciousness states
    for i, node_id in enumerate(node_ids, 1):
        state = ConsciousnessState(
            phi=0.5 + (i * 0.02),  # Varying Φ values
            coherence=0.4 + (i * 0.03),  # Varying coherence
            depth=0.6 + (i * 0.01),  # Varying depth
            spiritual=0.5 + (i * 0.02),  # Varying spiritual
            consciousness=0.5 + (i * 0.025),  # Varying consciousness
            timestamp=time.time()
        )
        consensus.update_consciousness_state(node_id, state)
    
    # Check voting weights
    print("Voting Weights:")
    for node_id in node_ids:
        weight = consensus.calculate_voting_weight(node_id)
        print(f"  {node_id}: {weight:.3f}")
        
    # Check participation
    print("\nParticipation Status:")
    for node_id in node_ids:
        participates = consensus.should_participate(node_id)
        print(f"  {node_id}: {'Participates' if participates else 'Limited'}")