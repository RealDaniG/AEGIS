"""
Unit tests for the logging_system module
"""

import unittest
import asyncio
import os
import tempfile
import json
from pathlib import Path

from logging_system import start_logging_system, LogConfig, initialize_logging, get_logger


class TestLoggingSystem(unittest.TestCase):
    """Test cases for the logging system"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test.log")

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_log_config_creation(self):
        """Test creation of LogConfig object"""
        config = LogConfig(
            log_level="DEBUG",
            log_file="test.log",
            log_dir=self.test_dir,
            max_file_size=5 * 1024 * 1024,  # 5MB
            backup_count=3
        )
        
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.log_file, "test.log")
        self.assertEqual(config.log_dir, self.test_dir)
        self.assertEqual(config.max_file_size, 5 * 1024 * 1024)
        self.assertEqual(config.backup_count, 3)

    def test_initialize_logging(self):
        """Test initializing the logging system"""
        config = LogConfig(
            log_level="INFO",
            log_file="test.log",
            log_dir=self.test_dir
        )
        
        logger_instance = initialize_logging(config)
        self.assertIsNotNone(logger_instance)
        
        # Test that we can log messages
        logger_instance.info("Test message")
        
        # Check that log file was created
        log_path = Path(self.test_dir) / "test.log"
        self.assertTrue(log_path.exists())

    def test_different_log_levels(self):
        """Test logging at different levels"""
        config = LogConfig(
            log_level="TRACE",
            log_file="test.log",
            log_dir=self.test_dir
        )
        
        logger_instance = initialize_logging(config)
        
        # Test all log levels
        logger_instance.trace("Trace message")
        logger_instance.debug("Debug message")
        logger_instance.info("Info message")
        logger_instance.success("Success message")
        logger_instance.warning("Warning message")
        logger_instance.error("Error message")
        logger_instance.critical("Critical message")
        
        # Check that log file contains messages
        log_path = Path(self.test_dir) / "test.log"
        self.assertTrue(log_path.exists())
        
        with open(log_path, 'r') as f:
            content = f.read()
            self.assertIn("Trace message", content)
            self.assertIn("Debug message", content)
            self.assertIn("Info message", content)
            self.assertIn("Success message", content)
            self.assertIn("Warning message", content)
            self.assertIn("Error message", content)
            self.assertIn("Critical message", content)

    def test_json_formatting(self):
        """Test JSON formatting of logs"""
        config = LogConfig(
            log_level="INFO",
            log_file="test.log",
            log_dir=self.test_dir,
            json_format=True
        )
        
        logger_instance = initialize_logging(config)
        logger_instance.info("Test JSON message")
        
        # Check that log file contains valid JSON
        log_path = Path(self.test_dir) / "test.log"
        self.assertTrue(log_path.exists())
        
        with open(log_path, 'r') as f:
            content = f.read()
            # Should be valid JSON
            try:
                log_entry = json.loads(content.strip())
                self.assertIn("message", log_entry)
                self.assertEqual(log_entry["message"], "Test JSON message")
                self.assertIn("level", log_entry)
                self.assertEqual(log_entry["level"], "INFO")
            except json.JSONDecodeError:
                self.fail("Log file does not contain valid JSON")

    def test_sensitive_data_filtering(self):
        """Test filtering of sensitive data"""
        config = LogConfig(
            log_level="INFO",
            log_file="test.log",
            log_dir=self.test_dir,
            sensitive_fields=["password", "secret", "token"]
        )
        
        logger_instance = initialize_logging(config)
        # Log a message with sensitive data
        logger_instance.info("User login", extra={"password": "secret123", "username": "testuser"})
        
        # Check that log file doesn't contain sensitive data
        log_path = Path(self.test_dir) / "test.log"
        self.assertTrue(log_path.exists())
        
        with open(log_path, 'r') as f:
            content = f.read()
            self.assertNotIn("secret123", content)
            self.assertIn("***MASKED***", content)
            self.assertIn("testuser", content)  # Non-sensitive data should still be there

    async def test_start_logging_system(self):
        """Test starting the logging system as a module"""
        config = {
            "log_level": "DEBUG",
            "log_file": "module_test.log",
            "log_dir": self.test_dir,
            "enable_console": False,  # Disable console to avoid output
            "enable_file": True
        }
        
        result = await start_logging_system(config)
        self.assertTrue(result)
        
        # Check that log file was created
        log_path = Path(self.test_dir) / "module_test.log"
        self.assertTrue(log_path.exists())
        
        # Check that test messages were logged
        with open(log_path, 'r') as f:
            content = f.read()
            self.assertIn("Logging system initialized successfully", content)


if __name__ == '__main__':
    # Run tests
    unittest.main()