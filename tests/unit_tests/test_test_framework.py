"""
Unit tests for the test_framework module
"""

import unittest
import asyncio
import tempfile
import os
import gc
import time
import sys
from pathlib import Path
import pytest

# Add the Open-A.G.I directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))


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
        # Force garbage collection to close file handles
        gc.collect()
        
        # Clean up test files with retry logic
        if os.path.exists(self.test_dir):
            for attempt in range(3):  # Try up to 3 times
                try:
                    for file in os.listdir(self.test_dir):
                        file_path = os.path.join(self.test_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(self.test_dir)
                    break  # Success, break out of retry loop
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        print(f"Warning: Failed to clean up test directory after 3 attempts: {e}")
                    else:
                        # Wait a bit before retrying
                        time.sleep(0.1)

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


@pytest.mark.asyncio
async def test_run_single_test():
    """Test running a single test"""
    # Try to import test framework components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
        import test_framework
        test_framework_available = True
    except ImportError:
        test_framework_available = False
        pytest.skip("Test framework components not available")
        
    if not test_framework_available:
        pytest.skip("Test framework components not available")
        
    test_dir = tempfile.mkdtemp()
    report_test_dir = os.path.join(test_dir, "test_reports")
    os.makedirs(report_test_dir, exist_ok=True)
    
    try:
        config = test_framework.TestConfig(
            parallel_tests=False,
            max_concurrent_tests=1,
            report_directory=report_test_dir
        )
        
        framework = test_framework.initialize_test_framework(config)
        
        # Define a simple test function
        def simple_test():
            assert 1 + 1 == 2
        
        # Run the test
        result = await framework._run_test(simple_test)
        
        assert result is not None
        if result is not None:
            assert result.status == test_framework.TestStatus.PASSED
    finally:
        # Clean up
        if os.path.exists(test_dir):
            for attempt in range(3):  # Try up to 3 times
                try:
                    for file in os.listdir(test_dir):
                        file_path = os.path.join(test_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(test_dir)
                    break  # Success, break out of retry loop
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        print(f"Warning: Failed to clean up test directory after 3 attempts: {e}")
                    else:
                        # Wait a bit before retrying
                        time.sleep(0.1)


@pytest.mark.asyncio
async def test_run_failing_test():
    """Test running a failing test"""
    # Try to import test framework components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
        import test_framework
        test_framework_available = True
    except ImportError:
        test_framework_available = False
        pytest.skip("Test framework components not available")
        
    if not test_framework_available:
        pytest.skip("Test framework components not available")
        
    test_dir = tempfile.mkdtemp()
    report_test_dir = os.path.join(test_dir, "test_reports")
    os.makedirs(report_test_dir, exist_ok=True)
    
    try:
        config = test_framework.TestConfig(
            parallel_tests=False,
            max_concurrent_tests=1,
            report_directory=report_test_dir
        )
        
        framework = test_framework.initialize_test_framework(config)
        
        # Define a failing test function
        def failing_test():
            assert 1 + 1 == 3  # This will fail
        
        # Run the test
        result = await framework._run_test(failing_test)
        
        assert result is not None
        if result is not None:
            assert result.status == test_framework.TestStatus.FAILED
    finally:
        # Clean up
        if os.path.exists(test_dir):
            for attempt in range(3):  # Try up to 3 times
                try:
                    for file in os.listdir(test_dir):
                        file_path = os.path.join(test_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(test_dir)
                    break  # Success, break out of retry loop
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        print(f"Warning: Failed to clean up test directory after 3 attempts: {e}")
                    else:
                        # Wait a bit before retrying
                        time.sleep(0.1)


@pytest.mark.asyncio
async def test_start_test_framework():
    """Test starting the test framework as a module"""
    # Try to import test framework components
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
        import test_framework
        test_framework_available = True
    except ImportError:
        test_framework_available = False
        pytest.skip("Test framework components not available")
        
    if not test_framework_available:
        pytest.skip("Test framework components not available")
        
    test_dir = tempfile.mkdtemp()
    report_test_dir = os.path.join(test_dir, "test_reports")
    os.makedirs(report_test_dir, exist_ok=True)
    
    try:
        config = {
            "parallel_tests": False,
            "max_concurrent_tests": 1,
            "report_directory": report_test_dir
        }
        
        result = await test_framework.start_test_framework(config)
        assert result
        
        # Check that we can get the global test framework
        framework = test_framework.get_test_framework()
        assert framework is not None
        
        # Check configuration
        assert framework.config.parallel_tests == False
        assert framework.config.max_concurrent_tests == 1
    finally:
        # Clean up
        if os.path.exists(test_dir):
            for attempt in range(3):  # Try up to 3 times
                try:
                    for file in os.listdir(test_dir):
                        file_path = os.path.join(test_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(test_dir)
                    break  # Success, break out of retry loop
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        print(f"Warning: Failed to clean up test directory after 3 attempts: {e}")
                    else:
                        # Wait a bit before retrying
                        time.sleep(0.1)


if __name__ == '__main__':
    # Run tests
    unittest.main()