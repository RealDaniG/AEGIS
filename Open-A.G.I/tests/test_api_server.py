"""
Unit tests for the api_server module
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path


class TestAPIServer(unittest.TestCase):
    """Test cases for the API server"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import API server components
        try:
            global api_server
            import api_server
            self.fastapi_available = True
        except ImportError:
            self.fastapi_available = False
            print("FastAPI not available, skipping API server tests")
        
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_import_api_server_module(self):
        """Test that the api_server module can be imported"""
        try:
            import api_server
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("FastAPI not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_api_server_config_creation(self):
        """Test creation of APIServerConfig object"""
        if not self.fastapi_available:
            self.skipTest("FastAPI not available")
            
        config = api_server.APIServerConfig(
            host="127.0.0.1",
            port=8001,
            enable_cors=True,
            enable_auth=False
        )
        
        self.assertEqual(config.host, "127.0.0.1")
        self.assertEqual(config.port, 8001)
        self.assertEqual(config.enable_cors, True)
        self.assertEqual(config.enable_auth, False)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_api_server(self):
        """Test initializing the API server"""
        if not self.fastapi_available:
            self.skipTest("FastAPI not available")
            
        config = api_server.APIServerConfig(
            host="127.0.0.1",
            port=8001,
            enable_docs=False
        )
        
        server = api_server.initialize_api_server(config)
        self.assertIsNotNone(server)
        
        # Test that we can get the app
        if server is not None and hasattr(server, 'get_app'):
            app = server.get_app()
            self.assertIsNotNone(app)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_start_api_server(self):
        """Test starting the API server as a module"""
        if not self.fastapi_available:
            self.skipTest("FastAPI not available")
            
        config = {
            "host": "127.0.0.1",
            "port": 8002,
            "enable_docs": False,
            "enable_cors": False
        }
        
        result = await api_server.start_api_server(config)
        self.assertTrue(result)
        
        # Check that we can get the global API server
        server = api_server.get_api_server()
        self.assertIsNotNone(server)
        
        # Check configuration
        self.assertEqual(server.config.host, "127.0.0.1")
        self.assertEqual(server.config.port, 8002)


if __name__ == '__main__':
    # Run tests
    unittest.main()