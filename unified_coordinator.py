"""
Unified Coordinator for Metatron-Consciousness and Open-A.G.I Integration

This module coordinates all the unified components and provides a single interface
for managing the integrated system.
"""

import sys
import os

# Add the project root to the Python path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
import signal

from unified_api.server import app as unified_api_app
from unified_api.client import UnifiedAPIClient
from unified_components.network import UnifiedP2PNetwork
from unified_components.consensus import UnifiedConsensus
from cross_system_comm.protocols import CrossSystemCommunicator

logger = logging.getLogger(__name__)


class UnifiedSystemCoordinator:
    """Main coordinator for the unified Metatron-A.G.I system"""
    
    def __init__(self, node_id: str = "coordinator_1"):
        self.node_id = node_id
        self.api_client = UnifiedAPIClient()
        self.p2p_network = UnifiedP2PNetwork(node_id)
        self.consensus = UnifiedConsensus(node_id)
        self.communicator = CrossSystemCommunicator(node_id)
        
        # System state
        self.running = False
        self.start_time = 0.0
        self.system_metrics = {
            "uptime": 0.0,
            "components_initialized": 0,
            "total_decisions": 0,
            "messages_processed": 0
        }
        
        # Graceful shutdown handling
        self.shutdown_event = asyncio.Event()
        
        logger.info(f"Unified System Coordinator initialized for node {node_id}")
    
    async def initialize(self) -> bool:
        """Initialize all system components"""
        try:
            logger.info("Initializing Unified System Coordinator...")
            
            # Initialize API client
            if await self.api_client.initialize():
                self.system_metrics["components_initialized"] += 1
                logger.info("API Client initialized")
            else:
                logger.warning("Failed to initialize API Client")
            
            # Initialize P2P network
            if await self.p2p_network.start_server():
                self.system_metrics["components_initialized"] += 1
                logger.info("P2P Network initialized")
            else:
                logger.warning("Failed to initialize P2P Network")
            
            # Initialize cross-system communicator
            if await self.communicator.initialize():
                self.system_metrics["components_initialized"] += 1
                logger.info("Cross-System Communicator initialized")
            else:
                logger.warning("Failed to initialize Cross-System Communicator")
            
            # Set up signal handlers for graceful shutdown
            self._setup_signal_handlers()
            
            self.start_time = time.time()
            self.running = True
            
            logger.info(f"Unified System Coordinator initialized with {self.system_metrics['components_initialized']}/3 components")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Unified System Coordinator: {e}")
            return False
    
    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.shutdown_event.set()
        
        # Handle SIGINT (Ctrl+C) and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start_websocket_server(self, host: str = "localhost", port: int = 8006):
        """Start the WebSocket communication server"""
        try:
            # This would be implemented if we had a WebSocket server class
            logger.info(f"WebSocket server would start on {host}:{port} if implemented")
            return True
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
            return False
    
    async def run_system_loop(self):
        """Main system loop for continuous operation"""
        logger.info("Starting Unified System Loop...")
        
        try:
            while self.running and not self.shutdown_event.is_set():
                # Update system metrics
                self._update_system_metrics()
                
                # Process cross-system messages
                await self._process_cross_system_messages()
                
                # Broadcast system state periodically
                await self._broadcast_system_state()
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(1.0)
                
        except asyncio.CancelledError:
            logger.info("System loop cancelled")
        except Exception as e:
            logger.error(f"Error in system loop: {e}")
        # Note: We don't call shutdown here anymore as it's handled by the main script
    
    def _update_system_metrics(self):
        """Update system performance metrics"""
        if self.start_time > 0:
            self.system_metrics["uptime"] = time.time() - self.start_time
    
    async def _process_cross_system_messages(self):
        """Process cross-system messages"""
        # In a real implementation, this would process messages from the communicator
        # For now, we'll just update the counter
        comm_metrics = self.communicator.get_communication_metrics()
        self.system_metrics["messages_processed"] += comm_metrics.get("messages_received", 0)
    
    async def _broadcast_system_state(self):
        """Broadcast current system state periodically"""
        # Every 10 seconds, broadcast system state
        if int(time.time()) % 10 == 0:
            try:
                # Get unified system state
                state = await self.api_client.get_unified_state()
                if state:
                    # Broadcast via communicator
                    # This is a simplified implementation
                    logger.debug("System state broadcast would occur here")
            except Exception as e:
                logger.error(f"Error broadcasting system state: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            # Get unified state from API
            unified_state = await self.api_client.get_unified_state()
            
            # Get communication metrics
            comm_metrics = self.communicator.get_communication_metrics()
            
            # Get consensus health
            consensus_health = self.consensus.get_network_health()
            
            return {
                "timestamp": time.time(),
                "system_status": "running" if self.running else "stopped",
                "uptime": self.system_metrics["uptime"],
                "components_initialized": self.system_metrics["components_initialized"],
                "total_decisions": self.system_metrics["total_decisions"],
                "messages_processed": self.system_metrics["messages_processed"],
                "unified_state": unified_state,
                "communication_metrics": comm_metrics,
                "consensus_health": consensus_health,
                "system_metrics": self.system_metrics
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    async def shutdown(self):
        """Gracefully shutdown the system"""
        logger.info("Initiating graceful shutdown...")
        
        try:
            self.running = False
            
            # Shutdown components in reverse order
            await self.communicator.stop()
            logger.info("Cross-system communicator stopped")
            
            await self.p2p_network.stop()
            logger.info("P2P network stopped")
            
            await self.api_client.close()
            logger.info("API client closed")
            
            logger.info("Unified System Coordinator shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# Example usage and testing
async def main():
    """Example usage of the Unified System Coordinator"""
    # Create coordinator
    coordinator = UnifiedSystemCoordinator("test_coordinator")
    
    try:
        # Initialize system
        if not await coordinator.initialize():
            logger.error("Failed to initialize system coordinator")
            return
        
        # Start WebSocket server
        await coordinator.start_websocket_server()
        
        # Run system for a short time
        logger.info("System running. Press Ctrl+C to stop.")
        
        # Run the system loop
        await coordinator.run_system_loop()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        # Ensure proper shutdown
        await coordinator.shutdown()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the coordinator
    asyncio.run(main())