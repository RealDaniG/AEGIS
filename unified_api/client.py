"""
Unified API Client for Metatron-ConscienceAI and Open-A.G.I Integration
"""

import asyncio
import aiohttp
import json
import logging
from typing import Optional, Dict, Any
from unified_api.models import UnifiedSystemState, ConsciousnessState, AGIState, UnifiedAPISettings, SystemStatus

logger = logging.getLogger(__name__)


class UnifiedAPIClient:
    """Client for accessing both consciousness and AGI systems through a unified interface"""
    
    def __init__(self, settings: Optional[UnifiedAPISettings] = None):
        self.settings = settings or UnifiedAPISettings()
        self.session: Optional[aiohttp.ClientSession] = None
        self._is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the API client"""
        try:
            if not self.session:
                # Create client session with SSL verification disabled for AGI connections
                connector = aiohttp.TCPConnector(verify_ssl=False)
                self.session = aiohttp.ClientSession(connector=connector)
            self._is_initialized = True
            logger.info("Unified API Client initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Unified API Client: {e}")
            return False
    
    async def close(self):
        """Close the API client"""
        if self.session:
            await self.session.close()
            self.session = None
        self._is_initialized = False
    
    async def get_consciousness_state(self) -> Optional[ConsciousnessState]:
        """Get the current consciousness state from Metatron system"""
        if not self._is_initialized or not self.session:
            logger.warning("Client not initialized")
            return None
            
        try:
            url = f"{self.settings.metatron_api_url}/api/status"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract consciousness metrics
                    consciousness_state = ConsciousnessState(
                        node_id="metatron_system",
                        timestamp=data.get("timestamp", 0),
                        consciousness_level=data.get("consciousness_level", 0.0),
                        phi=data.get("phi", 0.0),
                        coherence=data.get("coherence", 0.0),
                        recursive_depth=data.get("recursive_depth", 0),
                        gamma_power=data.get("gamma_power", 0.0),
                        fractal_dimension=data.get("fractal_dimension", 1.0),
                        spiritual_awareness=data.get("spiritual_awareness", 0.0),
                        state_classification=data.get("state_classification", "unknown"),
                        is_conscious=data.get("is_conscious", False),
                        dimensions={
                            "physical": 0.0,
                            "emotional": 0.0,
                            "mental": 0.0,
                            "spiritual": data.get("spiritual_awareness", 0.0),
                            "temporal": 0.0
                        }
                    )
                    return consciousness_state
                else:
                    logger.warning(f"Failed to get consciousness state: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error getting consciousness state: {e}")
            return None
    
    async def get_agi_state(self) -> Optional[AGIState]:
        """Get the current AGI state from Open-A.G.I system"""
        if not self._is_initialized or not self.session:
            logger.warning("Client not initialized")
            return None
            
        try:
            # First try the health check endpoint
            health_url = f"{self.settings.agi_api_url}/api/health"
            try:
                async with self.session.get(health_url) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        
                        # Try to get more detailed status if available
                        agi_state = AGIState(
                            node_id="agi_system",
                            timestamp=health_data.get("timestamp", 0),
                            consensus_status=health_data.get("status", "unknown"),
                            network_health=health_data.get("network", {}),
                            performance_metrics=health_data.get("performance", {}),
                            active_connections=health_data.get("active_connections", 0),
                            byzantine_threshold=health_data.get("byzantine_threshold", 0),
                            quorum_size=health_data.get("quorum_size", 0)
                        )
                        return agi_state
                    else:
                        logger.warning(f"Failed to get AGI health: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                logger.warning(f"AGI system not available: {e}")
                return None
        except Exception as e:
            logger.error(f"Error getting AGI state: {e}")
            return None
    
    async def get_unified_state(self) -> Optional[UnifiedSystemState]:
        """Get the combined state of both consciousness and AGI systems"""
        if not self._is_initialized:
            await self.initialize()
            
        # Get both states concurrently
        consciousness_task = self.get_consciousness_state()
        agi_task = self.get_agi_state()
        
        consciousness_state, agi_state = await asyncio.gather(
            consciousness_task, agi_task, 
            return_exceptions=True
        )
        
        # Handle exceptions and extract valid states
        valid_consciousness_state: Optional[ConsciousnessState] = None
        valid_agi_state: Optional[AGIState] = None
        
        if not isinstance(consciousness_state, Exception) and consciousness_state is not None:
            valid_consciousness_state = consciousness_state
            
        if not isinstance(agi_state, Exception) and agi_state is not None:
            valid_agi_state = agi_state
        
        # Log exceptions
        if isinstance(consciousness_state, Exception):
            logger.error(f"Consciousness state error: {consciousness_state}")
            
        if isinstance(agi_state, Exception):
            logger.error(f"AGI state error: {agi_state}")
        
        # Calculate integration metrics
        consciousness_level = 0.0
        if valid_consciousness_state is not None and hasattr(valid_consciousness_state, 'consciousness_level'):
            consciousness_level = valid_consciousness_state.consciousness_level
            
        consensus_status = "unknown"
        if valid_agi_state is not None and hasattr(valid_agi_state, 'consensus_status'):
            consensus_status = getattr(valid_agi_state, 'consensus_status', 'unknown')
        
        integration_metrics = {
            "systems_operational": (valid_consciousness_state is not None, valid_agi_state is not None),
            "consciousness_level": consciousness_level,
            "consensus_status": consensus_status,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        system_status = SystemStatus.RUNNING if (valid_consciousness_state or valid_agi_state) else SystemStatus.ERROR
        
        unified_state = UnifiedSystemState(
            timestamp=asyncio.get_event_loop().time(),
            system_status=system_status,
            consciousness=valid_consciousness_state,
            agi=valid_agi_state,
            integration_metrics=integration_metrics
        )
        
        return unified_state
    
    async def send_consciousness_input(self, input_data: Dict[str, float]) -> bool:
        """Send sensory input to the consciousness system"""
        if not self._is_initialized or not self.session:
            logger.warning("Client not initialized")
            return False
            
        try:
            url = f"{self.settings.metatron_api_url}/api/input"
            payload = {
                "physical": input_data.get("physical", 0.0),
                "emotional": input_data.get("emotional", 0.0),
                "mental": input_data.get("mental", 0.0),
                "spiritual": input_data.get("spiritual", 0.0),
                "temporal": input_data.get("temporal", 0.0)
            }
            
            async with self.session.post(url, json=payload) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Error sending consciousness input: {e}")
            return False
    
    async def send_chat_message(self, message: str, session_id: str = "default") -> Optional[str]:
        """Send a chat message to the AGI system"""
        if not self._is_initialized or not self.session:
            logger.warning("Client not initialized")
            return None
            
        try:
            url = f"{self.settings.metatron_api_url}/api/chat"
            payload = {
                "message": message,
                "session_id": session_id
            }
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response")
                else:
                    logger.warning(f"Failed to send chat message: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error sending chat message: {e}")
            return None


# Example usage
async def main():
    """Example usage of the Unified API Client"""
    client = UnifiedAPIClient()
    
    try:
        # Initialize the client
        await client.initialize()
        
        # Get unified system state
        state = await client.get_unified_state()
        if state:
            print(f"Unified System Status: {state.system_status}")
            if state.consciousness:
                print(f"Consciousness Level: {state.consciousness.consciousness_level}")
            if state.agi:
                print(f"AGI Consensus Status: {state.agi.consensus_status}")
        
        # Send consciousness input
        input_success = await client.send_consciousness_input({
            "physical": 0.5,
            "emotional": 0.3,
            "mental": 0.7,
            "spiritual": 0.8,
            "temporal": 0.2
        })
        print(f"Consciousness input sent: {input_success}")
        
        # Send chat message
        response = await client.send_chat_message("What is the relationship between consciousness and AGI?")
        if response:
            print(f"Chat response: {response[:100]}...")
            
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())