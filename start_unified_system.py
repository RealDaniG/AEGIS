#!/usr/bin/env python3
"""
Startup script for the Unified Metatron-A.G.I System

This script initializes and starts all components of the unified system.
"""

import asyncio
import logging
import sys
import os
import signal

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_coordinator import UnifiedSystemCoordinator
from unified_api.server import start_server as start_unified_api_server, stop_server as stop_unified_api_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Global variables for graceful shutdown
coordinator = None
shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Shutdown signal received...")
    shutdown_event.set()

async def start_unified_system():
    """Start the complete unified system"""
    global coordinator
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
        
        # Start the unified API server in a separate thread
        start_unified_api_server("0.0.0.0", 8005)
        
        # Run the system coordinator in the background
        coordinator_task = asyncio.create_task(coordinator.run_system_loop())
        
        # Wait for shutdown signal
        await shutdown_event.wait()
        
        # Cancel the coordinator task
        coordinator_task.cancel()
        try:
            await coordinator_task
        except asyncio.CancelledError:
            pass
            
        return True
        
    except Exception as e:
        logger.error(f"Error starting unified system: {e}")
        return False
    finally:
        # Ensure proper shutdown
        await shutdown_system()

async def shutdown_system():
    """Gracefully shutdown the system"""
    global coordinator
    logger.info("Initiating graceful shutdown...")
    
    try:
        # Stop the API server
        stop_unified_api_server()
        
        # Shutdown the coordinator if it exists
        if coordinator:
            await coordinator.shutdown()
        
        logger.info("Unified system shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

def main():
    """Main entry point"""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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