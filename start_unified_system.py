#!/usr/bin/env python3
"""
Startup script for the Unified Metatron-A.G.I System

This script initializes and starts all components of the unified system.
"""

import asyncio
import logging
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_coordinator import UnifiedSystemCoordinator
from unified_api.server import start_server as start_unified_api_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def start_unified_system():
    """Start the complete unified system"""
    logger.info("Starting Unified Metatron-A.G.I System")
    logger.info("=" * 50)
    
    try:
        # Create and initialize the coordinator
        coordinator = UnifiedSystemCoordinator("unified_coordinator_1")
        
        # Initialize all components
        if not await coordinator.initialize():
            logger.error("Failed to initialize system coordinator")
            return False
        
        # Start WebSocket communication server
        if not await coordinator.start_websocket_server("0.0.0.0", 8006):
            logger.warning("Failed to start WebSocket server")
        
        # Log system information
        logger.info("Unified System Components:")
        logger.info("  - Unified API Server (Port 8005)")
        logger.info("  - WebSocket Communication Server (Port 8006)")
        logger.info("  - Cross-System Communication Layer")
        logger.info("  - Consciousness-Aware Decision Engine")
        logger.info("  - Unified P2P Network")
        logger.info("  - Unified Consensus Protocol")
        logger.info("=" * 50)
        logger.info("System is running. Press Ctrl+C to stop.")
        
        # Run the system coordinator in the background
        coordinator_task = asyncio.create_task(coordinator.run_system_loop())
        
        # Start the unified API server in the foreground
        try:
            start_unified_api_server("0.0.0.0", 8005)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Error in API server: {e}")
        finally:
            # Cancel the coordinator task
            coordinator_task.cancel()
            try:
                await coordinator_task
            except asyncio.CancelledError:
                pass
            
            # Shutdown the coordinator
            await coordinator.shutdown()
        
        return True
        
    except Exception as e:
        logger.error(f"Error starting unified system: {e}")
        return False


def main():
    """Main entry point"""
    try:
        # Run the unified system
        success = asyncio.run(start_unified_system())
        
        if success:
            logger.info("Unified system shutdown complete")
            sys.exit(0)
        else:
            logger.error("Failed to start unified system")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()