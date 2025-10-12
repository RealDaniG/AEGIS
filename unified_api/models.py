"""
Data models for the unified API layer
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time


class SystemStatus(str, Enum):
    INITIALIZING = "initializing"
    RUNNING = "running"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class ConsciousnessState:
    """Represents the state of a consciousness node"""
    node_id: str
    timestamp: float
    consciousness_level: float
    phi: float  # Integrated Information
    coherence: float
    recursive_depth: int
    gamma_power: float
    fractal_dimension: float
    spiritual_awareness: float
    state_classification: str
    is_conscious: bool
    dimensions: Dict[str, float]  # Physical, Emotional, Mental, Spiritual, Temporal
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


@dataclass
class AGIState:
    """Represents the state of an AGI node"""
    node_id: str
    timestamp: float
    consensus_status: str
    network_health: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    active_connections: int
    byzantine_threshold: int
    quorum_size: int
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


@dataclass
class UnifiedSystemState:
    """Represents the combined state of consciousness and AGI systems"""
    timestamp: float
    system_status: SystemStatus
    consciousness: Optional[ConsciousnessState]
    agi: Optional[AGIState]
    integration_metrics: Dict[str, Any]
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


@dataclass
class UnifiedAPISettings:
    """Configuration settings for the unified API"""
    metatron_api_url: str = "http://localhost:8003"
    agi_api_url: str = "http://localhost:8090"
    websocket_url: str = "ws://localhost:8003/ws"
    update_interval: float = 1.0  # seconds
    enable_tls: bool = False
    api_key: Optional[str] = None