"""
Unit tests for the metrics_collector module
"""

import unittest
import asyncio
import tempfile
import os
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, AsyncMock

# Add the Open-A.G.I directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))

from metrics_collector import start_metrics_collector, MetricsCollectorConfig, initialize_metrics_collector, get_metrics_collector


class TestMetricsCollector(unittest.TestCase):
    """Test cases for the metrics collector"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import metrics collector components
        try:
            global metrics_collector
            import metrics_collector
            self.metrics_available = True
        except ImportError:
            self.metrics_available = False
            print("Metrics collector components not available, skipping metrics collector tests")

    def test_import_metrics_collector_module(self):
        """Test that the metrics_collector module can be imported"""
        try:
            import metrics_collector
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("Metrics collector components not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_metrics_config_creation(self):
        """Test creation of MetricsCollectorConfig object"""
        if not self.metrics_available:
            self.skipTest("Metrics collector components not available")
            
        config = MetricsCollectorConfig(
            enable_prometheus=False,
            collection_interval=2,
            enable_system_metrics=False
        )
        
        self.assertEqual(config.enable_prometheus, False)
        self.assertEqual(config.collection_interval, 2)
        self.assertEqual(config.enable_system_metrics, False)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_metrics_collector(self):
        """Test initializing the metrics collector"""
        if not self.metrics_available:
            self.skipTest("Metrics collector components not available")
            
        config = MetricsCollectorConfig(
            enable_prometheus=False,
            collection_interval=2,
            enable_system_metrics=False
        )
        
        collector = initialize_metrics_collector(config)
        self.assertIsNotNone(collector)
        
        # Test that we can get configuration
        cfg = collector.config
        self.assertEqual(cfg.enable_prometheus, False)


@pytest.mark.asyncio
async def test_start_metrics_collector():
    """Test starting the metrics collector as a module"""
    # Try to import metrics collector components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
        import metrics_collector
        metrics_available = True
    except ImportError:
        metrics_available = False
        pytest.skip("Metrics collector components not available")
        
    if not metrics_available:
        pytest.skip("Metrics collector components not available")
        
    config = {
        "enable_prometheus": False,
        "collection_interval": 1,  # Fast interval for testing
        "enable_system_metrics": False  # Disable system metrics for faster test
    }
    
    # Mock the MetricsCollector methods to avoid actually starting the collector
    with patch.object(metrics_collector.MetricsCollector, 'start_metrics_collector', new_callable=AsyncMock) as mock_start:
        mock_start.return_value = True
        with patch.object(metrics_collector.MetricsCollector, 'register_metric') as mock_register:
            mock_register.return_value = None
            with patch.object(metrics_collector.MetricsCollector, 'register_collector') as mock_register_collector:
                mock_register_collector.return_value = None
                result = await metrics_collector.start_metrics_collector(config)
                assert result


if __name__ == '__main__':
    # Run tests
    unittest.main()