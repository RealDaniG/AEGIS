from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import time


@dataclass
class ConsciousnessState:
    """Represents the state of a consciousness node"""
    node_id: str               # Ed25519 public key
    timestamp: float
    entropy: float
    valence: float
    arousal: float
    coherence: float
    empathy_score: float
    insight_strength: float
    signature: Optional[bytes] = None    # Ed25519 signature


@dataclass
class NetworkMessage:
    """Represents a message exchanged between nodes"""
    message_id: str
    sender_id: str
    recipient_id: str          # "*" for broadcast
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    ttl: int = 60
    signature: Optional[bytes] = None
    route_path: Optional[List[str]] = None


@dataclass
class PeerInfo:
    """Information about a network peer"""
    peer_id: str
    ip_address: str
    port: int
    public_key: str
    last_seen: float
    connection_status: str
    reputation_score: float
    latency: float