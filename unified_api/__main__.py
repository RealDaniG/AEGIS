"""
Main entry point for the Unified API Server
Allows running with: python -m unified_api
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .server import start_server
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Unified API Server...")
    try:
        # Start the server on port 8005 (as per project configuration)
        start_server("0.0.0.0", 8005)
        logger.info("Unified API Server started successfully on port 8005")
        
        # Keep the main thread alive
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Error starting Unified API Server: {e}")
        exit(1)