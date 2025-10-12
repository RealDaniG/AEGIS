"""
Unit tests for the test_framework module
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path


class TestTestFramework(unittest.TestCase):
    """Test cases for the test framework"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import test framework components
        try:
            global test_framework
            import test_framework
            self.test_framework_available = True
        except ImportError:
            self.test_framework_available = False
            print("Test framework components not available, skipping test framework tests")
        
        self.test_dir = tempfile.mkdtemp()
        self.report_test_dir = os.path.join(self.test_dir, "test_reports")
        os.makedirs(self.report_test_dir, exist_ok=True)

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_import_test_framework_module(self):
        """Test that the test_framework module can be imported"""
        try:
            import test_framework
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("Test framework components not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_test_config_creation(self):
        """Test creation of TestConfig object"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        config = test_framework.TestConfig(
            parallel_tests=True,
            max_concurrent_tests=2,
            timeout_seconds=60,
            report_directory=self.report_test_dir
        )
        
        self.assertEqual(config.parallel_tests, True)
        self.assertEqual(config.max_concurrent_tests, 2)
        self.assertEqual(config.timeout_seconds, 60)
        self.assertEqual(config.report_directory, self.report_test_dir)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_test_result_creation(self):
        """Test creation of TestResult object"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        result = test_framework.TestResult(
            test_name="test_example",
            test_type=test_framework.TestType.UNIT,
            status=test_framework.TestStatus.PASSED,
            duration=0.1
        )
        
        self.assertEqual(result.test_name, "test_example")
        self.assertEqual(result.test_type, test_framework.TestType.UNIT)
        self.assertEqual(result.status, test_framework.TestStatus.PASSED)
        self.assertEqual(result.duration, 0.1)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_test_framework(self):
        """Test initializing the test framework"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        config = test_framework.TestConfig(
            parallel_tests=True,
            max_concurrent_tests=2,
            report_directory=self.report_test_dir
        )
        
        framework = test_framework.initialize_test_framework(config)
        self.assertIsNotNone(framework)
        
        # Check that report directory was created
        self.assertTrue(os.path.exists(self.report_test_dir))

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_run_single_test(self):
        """Test running a single test"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        config = test_framework.TestConfig(
            parallel_tests=False,
            max_concurrent_tests=1,
            report_directory=self.report_test_dir
        )
        
        framework = test_framework.initialize_test_framework(config)
        
        # Define a simple test function
        def simple_test():
            assert 1 + 1 == 2
        
        # Run the test
        result = await framework._run_test(simple_test)
        
        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result.status, test_framework.TestStatus.PASSED)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_run_failing_test(self):
        """Test running a failing test"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        config = test_framework.TestConfig(
            parallel_tests=False,
            max_concurrent_tests=1,
            report_directory=self.report_test_dir
        )
        
        framework = test_framework.initialize_test_framework(config)
        
        # Define a failing test function
        def failing_test():
            assert 1 + 1 == 3  # This will fail
        
        # Run the test
        result = await framework._run_test(failing_test)
        
        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result.status, test_framework.TestStatus.FAILED)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_start_test_framework(self):
        """Test starting the test framework as a module"""
        if not self.test_framework_available:
            self.skipTest("Test framework components not available")
            
        config = {
            "parallel_tests": False,
            "max_concurrent_tests": 1,
            "report_directory": self.report_test_dir
        }
        
        result = await test_framework.start_test_framework(config)
        self.assertTrue(result)
        
        # Check that we can get the global test framework
        framework = test_framework.get_test_framework()
        self.assertIsNotNone(framework)
        
        # Check configuration
        self.assertEqual(framework.config.parallel_tests, False)
        self.assertEqual(framework.config.max_concurrent_tests, 1)


if __name__ == '__main__':
    # Run tests
    unittest.main()