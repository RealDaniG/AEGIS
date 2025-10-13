#!/usr/bin/env python3
"""
Logging configuration for Open-A.G.I to handle Unicode characters properly
"""

import sys
import logging
from loguru import logger
import os

def configure_unicode_logging():
    """Configure logging to handle Unicode characters properly"""
    # Remove default handlers
    logger.remove()
    
    # Add handler with UTF-8 encoding
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        level="INFO",
        enqueue=True
    )
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Also add file logging with UTF-8
    logger.add(
        "logs/open_agi.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="10 days",
        enqueue=True,
        encoding="utf-8"
    )
    
    return logger

def setup_unicode_console():
    """Setup console to handle Unicode properly on Windows"""
    if sys.platform == "win32":
        # Try to set console code page to UTF-8
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)  # UTF-8 code page
        except Exception:
            pass
        
        # Try to configure stdout encoding
        try:
            # Set environment variable for UTF-8
            os.environ['PYTHONIOENCODING'] = 'utf-8'
        except Exception:
            pass

# Configure logging when this module is imported
setup_unicode_console()

# Export the configured logger
logger = configure_unicode_logging()