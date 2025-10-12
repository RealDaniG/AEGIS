#!/usr/bin/env python3
"""
Simple test script to start the API server directly
"""

import asyncio
import uvicorn
from unified_api.server import app

if __name__ == "__main__":
    # Run the server directly
    uvicorn.run(app, host="0.0.0.0", port=8005, log_level="info")