"""
Unit tests for the web_dashboard module
"""

import unittest
import asyncio
import os
import sys
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, AsyncMock

# Add the integrated_components directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'integrated_components'))

from web_dashboard import start_web_dashboard, WebDashboardConfig, initialize_web_dashboard, get_web_dashboard


class TestWebDashboard(unittest.TestCase):
    """Test cases for the web dashboard"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import Flask components
        try:
            global web_dashboard
            import web_dashboard
            self.flask_available = True
        except ImportError:
            self.flask_available = False
            print("Flask not available, skipping web dashboard tests")

    def test_import_web_dashboard_module(self):
        """Test that the web_dashboard module can be imported"""
        try:
            import web_dashboard
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("Flask not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_web_dashboard_config_creation(self):
        """Test creation of WebDashboardConfig object"""
        if not self.flask_available:
            self.skipTest("Flask not available")
            
        config = WebDashboardConfig(
            host="127.0.0.1",
            port=8081,
            debug=False
        )
        
        self.assertEqual(config.host, "127.0.0.1")
        self.assertEqual(config.port, 8081)
        self.assertEqual(config.debug, False)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_web_dashboard(self):
        """Test initializing the web dashboard"""
        if not self.flask_available:
            self.skipTest("Flask not available")
            
        config = WebDashboardConfig(
            host="127.0.0.1",
            port=8081,
            debug=False
        )
        
        dashboard = initialize_web_dashboard(config)
        self.assertIsNotNone(dashboard)
        
        # Test that we can get the app
        app = dashboard.get_app()
        self.assertIsNotNone(app)


@pytest.mark.asyncio
async def test_start_web_dashboard():
    """Test starting the web dashboard as a module"""
    # Try to import Flask components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'integrated_components'))
        import web_dashboard
        flask_available = True
    except ImportError:
        flask_available = False
        pytest.skip("Flask not available")
        
    if not flask_available:
        pytest.skip("Flask not available")
        
    config = {
        "host": "127.0.0.1",
        "port": 8083,  # Use a different port to avoid conflicts
        "debug": False
    }
    
    # Mock the dashboard start to avoid actually starting the server
    with patch.object(web_dashboard.WebDashboard, 'start_dashboard', new_callable=AsyncMock) as mock_start:
        mock_start.return_value = True
        result = await web_dashboard.start_web_dashboard(config)
        # This might return False if Flask is not properly installed
        # but we already checked Flask availability above
        
        if result is not None:
            # If it returned a value, it should be True
            assert result
        
        # Check that we can get the global web dashboard
        dashboard = web_dashboard.get_web_dashboard()
        # Dashboard might be None if Flask is not available
        # But if Flask is available, it should not be None
        if flask_available:
            assert dashboard is not None


if __name__ == '__main__':
    # Run tests
    unittest.main()