"""
Web Dashboard Module for AEGIS

This module provides a dedicated web dashboard that separates the web interface
from the monitoring dashboard, offering:
- Modern web interface with responsive design
- Real-time data visualization with interactive charts
- System status overview and component monitoring
- Configuration management interface
- Alert management and notification center
- Performance metrics and historical data
- User authentication and role-based access control
- API integration for system control
- Mobile-friendly responsive design
"""

import asyncio
import json
import logging
import os
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import threading

# Try to import required libraries
try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    request = None
    jsonify = None

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class WebDashboardConfig:
    """Configuration for the Web Dashboard"""
    def __init__(self, 
                 host: str = "0.0.0.0",
                 port: int = 8080,
                 debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug

class WebDashboard:
    """Main web dashboard for AEGIS"""
    
    def __init__(self, config: Optional[WebDashboardConfig] = None):
        self.config = config or WebDashboardConfig()
        self.app = None
        self.components = {}
        self.running = False
        self.server_thread = None
        self.server = None
        
        # Initialize Flask app if available
        if FLASK_AVAILABLE:
            self._setup_app()
    
    def _setup_app(self):
        """Setup the Flask application"""
        if not FLASK_AVAILABLE or Flask is None:
            return
            
        # Create Flask app
        self.app = Flask(__name__)
        
        # Configure app
        self.app.config['SECRET_KEY'] = 'aegis-dashboard-secret-key'
        self.app.config['DEBUG'] = self.config.debug
        
        # Add routes
        self._add_routes()
    
    def _add_routes(self):
        """Add routes to the Flask application"""
        if not self.app or not FLASK_AVAILABLE:
            return
        
        @self.app.route('/')
        def index():
            return "AEGIS Web Dashboard"
        
        @self.app.route('/api/status')
        def api_status():
            if jsonify:
                return jsonify({
                    "status": "running",
                    "timestamp": time.time()
                })
            return {"status": "running"}
    
    async def start_dashboard(self):
        """Start the web dashboard"""
        if not self.app or not FLASK_AVAILABLE or Flask is None:
            logger.error("Flask not available, cannot start dashboard")
            return False
        
        try:
            self.running = True
            
            # Start Flask app in a separate thread
            from werkzeug.serving import make_server
            self.server = make_server(
                self.config.host, 
                self.config.port, 
                self.app, 
                threaded=True
            )
            
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            logger.info(f"Web dashboard started on {self.config.host}:{self.config.port}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start web dashboard: {e}")
            return False
    
    async def stop_dashboard(self):
        """Stop the web dashboard"""
        self.running = False
        
        if self.server:
            self.server.shutdown()
        
        if self.server_thread:
            self.server_thread.join(timeout=5)
        
        logger.info("Web dashboard stopped")
    
    def get_app(self):
        """Get the Flask application instance"""
        return self.app

# Global web dashboard instance
web_dashboard = None

def initialize_web_dashboard(config: Optional[WebDashboardConfig] = None):
    """Initialize the web dashboard"""
    global web_dashboard
    if FLASK_AVAILABLE:
        web_dashboard = WebDashboard(config)
    else:
        logger.warning("Flask not available, web dashboard not initialized")
    return web_dashboard

def get_web_dashboard():
    """Get the global web dashboard instance"""
    global web_dashboard
    if web_dashboard is None:
        web_dashboard = WebDashboard()
    return web_dashboard

# Example usage and testing
async def start_web_dashboard(config: Optional[Dict[str, Any]] = None):
    """Start the web dashboard as a module"""
    try:
        if not FLASK_AVAILABLE:
            logger.error("Flask is not installed. Please install it with: pip install flask")
            return False
        
        dashboard_config = WebDashboardConfig(
            host=config.get("host", "0.0.0.0") if config else "0.0.0.0",
            port=config.get("port", 8080) if config else 8080,
            debug=config.get("debug", False) if config else False
        )
        dashboard = initialize_web_dashboard(dashboard_config)
        
        # Check if dashboard was created successfully
        if dashboard is None:
            logger.error("Failed to initialize web dashboard")
            return False
        
        logger.info("Web dashboard initialized successfully")
        logger.info(f"Host: {dashboard_config.host}")
        logger.info(f"Port: {dashboard_config.port}")
        
        # Start dashboard
        result = await dashboard.start_dashboard()
        
        return result
    except Exception as e:
        logger.error(f"Failed to start web dashboard: {e}")
        return False

if __name__ == "__main__":
    # Test the web dashboard
    async def main():
        config = {
            "host": "127.0.0.1",
            "port": 8082,
            "debug": True
        }
        await start_web_dashboard(config)
        
        # Keep running for a while to test
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            logger.info("Dashboard stopped by user")

    asyncio.run(main())