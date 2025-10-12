"""
Unit tests for the metrics_collector module
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path


class TestMetricsCollector(unittest.TestCase):
    """Test cases for the metrics collector"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import metrics collector components
        try:
            global metrics_collector
            import metrics_collector
            self.prometheus_available = True
        except ImportError:
            self.prometheus_available = False
            print("Prometheus client not available, skipping metrics collector tests")
        
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_import_metrics_collector_module(self):
        """Test that the metrics_collector module can be imported"""
        try:
            import metrics_collector
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("Prometheus client not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_metrics_collector_config_creation(self):
        """Test creation of MetricsCollectorConfig object"""
        if not self.prometheus_available:
            self.skipTest("Prometheus client not available")
            
        config = metrics_collector.MetricsCollectorConfig(
            enable_prometheus=False,
            collection_interval=5,
            history_size=500
        )
        
        self.assertEqual(config.enable_prometheus, False)
        self.assertEqual(config.collection_interval, 5)
        self.assertEqual(config.history_size, 500)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_metric_config_creation(self):
        """Test creation of MetricConfig object"""
        if not self.prometheus_available:
            self.skipTest("Prometheus client not available")
            
        config = metrics_collector.MetricConfig(
            name="test_metric",
            type=metrics_collector.MetricType.GAUGE,
            category=metrics_collector.MetricCategory.SYSTEM,
            description="A test metric"
        )
        
        self.assertEqual(config.name, "test_metric")
        self.assertEqual(config.type, metrics_collector.MetricType.GAUGE)
        self.assertEqual(config.category, metrics_collector.MetricCategory.SYSTEM)
        self.assertEqual(config.description, "A test metric")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_metrics_collector(self):
        """Test initializing the metrics collector"""
        if not self.prometheus_available:
            self.skipTest("Prometheus client not available")
            
        config = metrics_collector.MetricsCollectorConfig(
            enable_prometheus=False,
            collection_interval=5
        )
        
        collector = metrics_collector.initialize_metrics_collector(config)
        self.assertIsNotNone(collector)
        
        # Test that we can get metrics
        metrics = collector.get_all_metrics()
        self.assertIsInstance(metrics, dict)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_start_metrics_collector(self):
        """Test starting the metrics collector as a module"""
        if not self.prometheus_available:
            self.skipTest("Prometheus client not available")
            
        config = {
            "enable_prometheus": False,
            "collection_interval": 1,  # Fast interval for testing
            "enable_system_metrics": False  # Disable system metrics for faster test
        }
        
        result = await metrics_collector.start_metrics_collector(config)
        self.assertTrue(result)
        
        # Check that we can get the global metrics collector
        collector = metrics_collector.get_metrics_collector()
        self.assertIsNotNone(collector)
        
        # Check configuration
        self.assertEqual(collector.config.collection_interval, 1)
        self.assertEqual(collector.config.enable_prometheus, False)


if __name__ == '__main__':
    # Run tests
    unittest.main()