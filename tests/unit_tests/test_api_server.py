"""
Unit tests for the api_server module
"""

import unittest
import asyncio
import os
import sys
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, AsyncMock

# Add the Open-A.G.I directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))

from api_server import start_api_server, APIServerConfig, initialize_api_server, get_api_server


class TestAPIServer(unittest.TestCase):
    """Test cases for the API server"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import FastAPI components
        try:
            global api_server
            import api_server
            self.fastapi_available = True
        except ImportError:
            self.fastapi_available = False
            print("FastAPI not available, skipping API server tests")

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
            
        config = APIServerConfig(
            host="127.0.0.1",
            port=8001,
            enable_docs=False,
            enable_cors=False
        )
        
        self.assertEqual(config.host, "127.0.0.1")
        self.assertEqual(config.port, 8001)
        self.assertEqual(config.enable_docs, False)
        self.assertEqual(config.enable_cors, False)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_api_server(self):
        """Test initializing the API server"""
        if not self.fastapi_available:
            self.skipTest("FastAPI not available")
            
        config = APIServerConfig(
            host="127.0.0.1",
            port=8001,
            enable_docs=False,
            enable_cors=False
        )
        
        server = initialize_api_server(config)
        self.assertIsNotNone(server)
        
        # Test that we can get the app
        app = server.get_app()
        self.assertIsNotNone(app)


@pytest.mark.asyncio
async def test_start_api_server():
    """Test starting the API server as a module"""
    # Try to import FastAPI components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
        import api_server
        fastapi_available = True
    except ImportError:
        fastapi_available = False
        pytest.skip("FastAPI not available")
        
    if not fastapi_available:
        pytest.skip("FastAPI not available")
        
    config = {
        "host": "127.0.0.1",
        "port": 8003,  # Use a different port to avoid conflicts
        "enable_docs": False,
        "enable_cors": False
    }
    
    # Mock the server start to avoid actually starting the server
    with patch.object(api_server.APIServer, 'start_server', new_callable=AsyncMock) as mock_start:
        mock_start.return_value = True
        result = await api_server.start_api_server(config)
        assert result
        
        # Check that we can get the global API server
        server = api_server.get_api_server()
        assert server is not None
        
        # Check configuration
        assert server.config.host == "127.0.0.1"
        assert server.config.port == 8003


if __name__ == '__main__':
    # Run tests
    unittest.main()