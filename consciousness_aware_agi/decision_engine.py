"""
Consciousness-Aware AGI Decision Engine

This module implements decision making that incorporates consciousness metrics
from the Metatron system into AGI operations.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
import numpy as np

from unified_api.client import UnifiedAPIClient
from unified_api.models import ConsciousnessState
from unified_components.consensus import UnifiedConsensus, ConsciousnessMetrics

logger = logging.getLogger(__name__)


@dataclass
class DecisionContext:
    """Context for consciousness-aware decision making"""
    consciousness_state: Optional[ConsciousnessState]
    system_metrics: Dict[str, Any]
    available_actions: List[str]
    constraints: Dict[str, Any]
    timestamp: float


@dataclass
class ConsciousnessAwareDecision:
    """Result of consciousness-aware decision making"""
    action: str
    confidence: float
    consciousness_influence: float
    reasoning: str
    timestamp: float


class ConsciousnessAwareDecisionEngine:
    """Decision engine that incorporates consciousness metrics into AGI decisions"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.api_client = UnifiedAPIClient()
        self.consensus = UnifiedConsensus(node_id)
        
        # Decision weights based on consciousness metrics
        self.weights = {
            "coherence_weight": 0.3,
            "phi_weight": 0.2,
            "consciousness_weight": 0.4,
            "spiritual_weight": 0.1
        }
        
        # Action preferences based on consciousness states
        self.action_preferences = {
            "high_coherence": ["collaborate", "share_knowledge", "optimize"],
            "low_coherence": ["isolate", "recover", "diagnose"],
            "high_phi": ["integrate", "synthesis", "abstract"],
            "low_phi": ["simplify", "focus", "ground"],
            "high_spiritual": ["explore", "innovate", "transcend"],
            "low_spiritual": ["stabilize", "maintain", "conserve"]
        }
        
        # Decision history for learning
        self.decision_history: List[ConsciousnessAwareDecision] = []
        self.outcome_history: List[Dict[str, Any]] = []
        
        logger.info(f"Consciousness-Aware Decision Engine initialized for node {node_id}")
    
    async def initialize(self) -> bool:
        """Initialize the decision engine"""
        try:
            await self.api_client.initialize()
            logger.info("Decision engine initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize decision engine: {e}")
            return False
    
    async def get_decision_context(self, available_actions: List[str], 
                                 constraints: Optional[Dict[str, Any]] = None) -> DecisionContext:
        """Get the current decision context including consciousness state"""
        # Get consciousness state
        consciousness_state = await self.api_client.get_consciousness_state()
        
        # Get system metrics
        system_metrics = await self._get_system_metrics()
        
        context = DecisionContext(
            consciousness_state=consciousness_state,
            system_metrics=system_metrics,
            available_actions=available_actions,
            constraints=constraints or {},
            timestamp=time.time()
        )
        
        return context
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance and health metrics"""
        # In a real implementation, this would gather actual metrics
        # For now, we'll return mock data
        return {
            "cpu_usage": 0.45,
            "memory_usage": 0.67,
            "network_latency": 0.12,
            "active_connections": 8,
            "uptime": 3600.0,
            "error_rate": 0.02
        }
    
    def make_consciousness_aware_decision(self, context: DecisionContext) -> ConsciousnessAwareDecision:
        """Make a decision that incorporates consciousness metrics"""
        if not context.consciousness_state:
            # Fallback to traditional decision making if no consciousness state
            return self._make_default_decision(context)
        
        consciousness = context.consciousness_state
        
        # Calculate consciousness influence score
        consciousness_influence = self._calculate_consciousness_influence(consciousness)
        
        # Select action based on consciousness state
        preferred_actions = self._get_preferred_actions(consciousness)
        
        # Filter available actions by preferences and constraints
        valid_actions = self._filter_actions(context.available_actions, preferred_actions, context.constraints)
        
        if not valid_actions:
            # If no valid actions, use default selection
            action = context.available_actions[0] if context.available_actions else "idle"
        else:
            # Weighted selection based on consciousness metrics
            action = self._select_weighted_action(valid_actions, consciousness)
        
        # Calculate confidence based on consciousness level and system metrics
        confidence = self._calculate_confidence(consciousness, context.system_metrics)
        
        # Generate reasoning explanation
        reasoning = self._generate_reasoning(consciousness, action, consciousness_influence)
        
        decision = ConsciousnessAwareDecision(
            action=action,
            confidence=confidence,
            consciousness_influence=consciousness_influence,
            reasoning=reasoning,
            timestamp=time.time()
        )
        
        # Store decision in history
        self.decision_history.append(decision)
        
        logger.info(f"Consciousness-aware decision: {action} (confidence: {confidence:.3f})")
        return decision
    
    def _calculate_consciousness_influence(self, consciousness: ConsciousnessState) -> float:
        """Calculate how much consciousness metrics should influence the decision"""
        # Weighted combination of consciousness metrics
        influence = (
            self.weights["coherence_weight"] * consciousness.coherence +
            self.weights["phi_weight"] * consciousness.phi +
            self.weights["consciousness_weight"] * consciousness.consciousness_level +
            self.weights["spiritual_weight"] * consciousness.spiritual_awareness
        )
        
        # Normalize to 0-1 range
        influence = max(0.0, min(1.0, influence))
        return influence
    
    def _get_preferred_actions(self, consciousness: ConsciousnessState) -> List[str]:
        """Get preferred actions based on current consciousness state"""
        preferred = []
        
        # Coherence-based preferences
        if consciousness.coherence > 0.7:
            preferred.extend(self.action_preferences["high_coherence"])
        elif consciousness.coherence < 0.3:
            preferred.extend(self.action_preferences["low_coherence"])
        
        # Phi-based preferences
        if consciousness.phi > 0.5:
            preferred.extend(self.action_preferences["high_phi"])
        elif consciousness.phi < 0.2:
            preferred.extend(self.action_preferences["low_phi"])
        
        # Spiritual awareness preferences
        if consciousness.spiritual_awareness > 0.6:
            preferred.extend(self.action_preferences["high_spiritual"])
        elif consciousness.spiritual_awareness < 0.2:
            preferred.extend(self.action_preferences["low_spiritual"])
        
        return list(set(preferred))  # Remove duplicates
    
    def _filter_actions(self, available_actions: List[str], preferred_actions: List[str], 
                       constraints: Dict[str, Any]) -> List[str]:
        """Filter available actions based on preferences and constraints"""
        # Start with preferred actions that are available
        valid_actions = [action for action in preferred_actions if action in available_actions]
        
        # If no preferred actions are available, use all available actions
        if not valid_actions:
            valid_actions = available_actions.copy()
        
        # Apply constraints
        if "max_actions" in constraints:
            valid_actions = valid_actions[:constraints["max_actions"]]
        
        return valid_actions
    
    def _select_weighted_action(self, valid_actions: List[str], 
                               consciousness: ConsciousnessState) -> str:
        """Select an action using weighted probabilities based on consciousness"""
        if len(valid_actions) == 1:
            return valid_actions[0]
        
        # Create weights based on consciousness level
        base_weight = 1.0
        consciousness_boost = consciousness.consciousness_level * 0.5
        
        # Apply different weights to actions based on consciousness state
        weights = []
        for action in valid_actions:
            weight = base_weight
            
            # Boost certain actions based on consciousness metrics
            if consciousness.coherence > 0.7 and action in ["collaborate", "share_knowledge"]:
                weight += consciousness_boost
            elif consciousness.phi > 0.5 and action in ["integrate", "synthesis"]:
                weight += consciousness_boost
            elif consciousness.spiritual_awareness > 0.6 and action in ["explore", "innovate"]:
                weight += consciousness_boost
                
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            probabilities = [w / total_weight for w in weights]
        else:
            # Equal probabilities if all weights are zero
            probabilities = [1.0 / len(weights)] * len(weights)
        
        # Select action based on probabilities
        selected_index = np.random.choice(len(valid_actions), p=probabilities)
        return valid_actions[selected_index]
    
    def _calculate_confidence(self, consciousness: ConsciousnessState, 
                            system_metrics: Dict[str, Any]) -> float:
        """Calculate decision confidence based on consciousness and system metrics"""
        # Base confidence from consciousness level
        consciousness_confidence = consciousness.consciousness_level
        
        # Adjust based on system health
        system_health = 1.0 - (system_metrics.get("error_rate", 0) * 2)
        system_health = max(0.0, min(1.0, system_health))
        
        # Combine consciousness and system confidence
        combined_confidence = (consciousness_confidence * 0.7) + (system_health * 0.3)
        
        return max(0.0, min(1.0, combined_confidence))
    
    def _generate_reasoning(self, consciousness: ConsciousnessState, 
                          action: str, consciousness_influence: float) -> str:
        """Generate human-readable reasoning for the decision"""
        reasoning_parts = []
        
        # Add consciousness-based reasoning
        if consciousness.coherence > 0.7:
            reasoning_parts.append("High coherence indicates stable system state")
        elif consciousness.coherence < 0.3:
            reasoning_parts.append("Low coherence suggests need for stabilization")
        
        if consciousness.phi > 0.5:
            reasoning_parts.append("Strong integrated information supports complex decisions")
        
        if consciousness.spiritual_awareness > 0.6:
            reasoning_parts.append("Elevated spiritual awareness enables exploratory actions")
        
        # Add action-specific reasoning
        action_reasons = {
            "collaborate": "Collaboration leverages collective intelligence",
            "share_knowledge": "Knowledge sharing enhances network awareness",
            "optimize": "Optimization improves system efficiency",
            "isolate": "Isolation prevents potential issues from spreading",
            "recover": "Recovery actions restore system stability",
            "integrate": "Integration synthesizes distributed knowledge",
            "explore": "Exploration discovers new possibilities",
            "stabilize": "Stabilization maintains current operational parameters"
        }
        
        if action in action_reasons:
            reasoning_parts.append(action_reasons[action])
        
        # Add consciousness influence note
        influence_level = "high" if consciousness_influence > 0.7 else "moderate" if consciousness_influence > 0.3 else "low"
        reasoning_parts.append(f"Consciousness influence: {influence_level}")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Decision based on system protocols"
    
    def _make_default_decision(self, context: DecisionContext) -> ConsciousnessAwareDecision:
        """Make a default decision when consciousness data is unavailable"""
        action = context.available_actions[0] if context.available_actions else "idle"
        
        decision = ConsciousnessAwareDecision(
            action=action,
            confidence=0.5,
            consciousness_influence=0.0,
            reasoning="Default decision due to unavailable consciousness data",
            timestamp=time.time()
        )
        
        self.decision_history.append(decision)
        return decision
    
    async def learn_from_outcome(self, decision: ConsciousnessAwareDecision, 
                               outcome: Dict[str, Any]) -> bool:
        """Learn from decision outcomes to improve future decisions"""
        try:
            # Store outcome
            outcome_record = {
                "decision": asdict(decision),
                "outcome": outcome,
                "timestamp": time.time()
            }
            self.outcome_history.append(outcome_record)
            
            # In a real implementation, this would update decision models
            logger.info(f"Learned from outcome of decision: {decision.action}")
            return True
        except Exception as e:
            logger.error(f"Error learning from outcome: {e}")
            return False
    
    def get_decision_history(self, limit: int = 10) -> List[ConsciousnessAwareDecision]:
        """Get recent decision history"""
        return self.decision_history[-limit:] if self.decision_history else []
    
    async def close(self):
        """Clean up resources"""
        await self.api_client.close()
        logger.info("Decision engine closed")


# Example usage
async def main():
    """Example usage of the Consciousness-Aware Decision Engine"""
    # Create decision engine
    engine = ConsciousnessAwareDecisionEngine("agi_node_1")
    
    try:
        # Initialize engine
        await engine.initialize()
        
        # Define available actions
        actions = ["collaborate", "share_knowledge", "optimize", "isolate", "recover", "explore"]
        
        # Get decision context
        context = await engine.get_decision_context(actions)
        
        # Make consciousness-aware decision
        decision = engine.make_consciousness_aware_decision(context)
        
        print(f"Decision: {decision.action}")
        print(f"Confidence: {decision.confidence:.3f}")
        print(f"Consciousness Influence: {decision.consciousness_influence:.3f}")
        print(f"Reasoning: {decision.reasoning}")
        
        # Simulate learning from outcome
        outcome = {"success": True, "improvement": 0.15}
        await engine.learn_from_outcome(decision, outcome)
        
        # Get decision history
        history = engine.get_decision_history()
        print(f"Decision history entries: {len(history)}")
        
    finally:
        await engine.close()


if __name__ == "__main__":
    asyncio.run(main())