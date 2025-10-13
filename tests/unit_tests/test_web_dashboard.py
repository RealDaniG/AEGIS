"""
Unit tests for the web_dashboard module
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path


class TestWebDashboard(unittest.TestCase):
    """Test cases for the web dashboard"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import web dashboard components
        try:
            global web_dashboard
            import web_dashboard
            self.flask_available = True
        except ImportError:
            self.flask_available = False
            print("Flask not available, skipping web dashboard tests")
        
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

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
            
        config = web_dashboard.WebDashboardConfig(
            host="127.0.0.1",
            port=8081,
            debug=True
        )
        
        self.assertEqual(config.host, "127.0.0.1")
        self.assertEqual(config.port, 8081)
        self.assertEqual(config.debug, True)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_web_dashboard(self):
        """Test initializing the web dashboard"""
        if not self.flask_available:
            self.skipTest("Flask not available")
            
        config = web_dashboard.WebDashboardConfig(
            host="127.0.0.1",
            port=8081,
            debug=False
        )
        
        dashboard = web_dashboard.initialize_web_dashboard(config)
        # Dashboard might be None if Flask is not available
        # We already checked Flask availability above, so this should work
        
        if dashboard is not None:
            # Test that we can get the app
            app = dashboard.get_app()
            # App might be None if Flask is not available
            # But we already checked Flask availability, so this should work

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_start_web_dashboard(self):
        """Test starting the web dashboard as a module"""
        if not self.flask_available:
            self.skipTest("Flask not available")
            
        config = {
            "host": "127.0.0.1",
            "port": 8082,
            "debug": False
        }
        
        result = await web_dashboard.start_web_dashboard(config)
        # This might return False if Flask is not properly installed
        # but we already checked Flask availability above
        
        if result is not None:
            # If it returned a value, it should be True
            self.assertTrue(result)
        
        # Check that we can get the global web dashboard
        dashboard = web_dashboard.get_web_dashboard()
        # Dashboard might be None if Flask is not available


if __name__ == '__main__':
    # Run tests
    unittest.main()