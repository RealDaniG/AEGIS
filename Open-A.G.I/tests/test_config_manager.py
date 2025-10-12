"""
Unit tests for the config_manager module
"""

import unittest
import asyncio
import os
import tempfile
import json
from pathlib import Path

from config_manager import start_config_system, ConfigManagerConfig, initialize_config_manager, get_config_manager


class TestConfigManager(unittest.TestCase):
    """Test cases for the configuration manager"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.json")

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_config_manager_config_creation(self):
        """Test creation of ConfigManagerConfig object"""
        config_paths = [self.config_file]
        config = ConfigManagerConfig(
            config_paths=config_paths,
            auto_reload=False,
            reload_interval=60
        )
        
        self.assertEqual(config.config_paths, config_paths)
        self.assertEqual(config.auto_reload, False)
        self.assertEqual(config.reload_interval, 60)

    def test_initialize_config_manager(self):
        """Test initializing the config manager"""
        config = ConfigManagerConfig(
            config_paths=[self.config_file],
            auto_reload=False
        )
        
        manager = initialize_config_manager(config)
        self.assertIsNotNone(manager)
        
        # Test that we can get the configuration
        cfg = manager.get_config()
        self.assertIsInstance(cfg, dict)
        self.assertIn("app", cfg)

    def test_config_loading_and_merging(self):
        """Test loading configuration from files and merging"""
        # Create a test config file
        test_config = {
            "app": {
                "log_level": "DEBUG",
                "enable": {
                    "tor": False
                }
            },
            "custom": {
                "setting": "value"
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)
        
        config = ConfigManagerConfig(
            config_paths=[self.config_file],
            auto_reload=False
        )
        
        manager = initialize_config_manager(config)
        
        # Check that config was loaded correctly
        cfg = manager.get_config()
        self.assertEqual(cfg["app"]["log_level"], "DEBUG")
        self.assertEqual(cfg["app"]["enable"]["tor"], False)
        self.assertEqual(cfg["custom"]["setting"], "value")

    def test_config_value_getting_and_setting(self):
        """Test getting and setting configuration values"""
        config = ConfigManagerConfig(
            config_paths=[self.config_file],
            auto_reload=False
        )
        
        manager = initialize_config_manager(config)
        
        # Test setting and getting values
        manager.set_value("test.key", "test_value")
        value = manager.get_value("test.key")
        self.assertEqual(value, "test_value")
        
        # Test getting non-existent value with default
        default_value = manager.get_value("non.existent.key", "default")
        self.assertEqual(default_value, "default")

    def test_config_saving(self):
        """Test saving configuration to file"""
        config = ConfigManagerConfig(
            config_paths=[self.config_file],
            auto_reload=False
        )
        
        manager = initialize_config_manager(config)
        
        # Modify some values
        manager.set_value("test.save_key", "save_value")
        
        # Save config
        manager.save_config(self.config_file)
        
        # Check that file was created and contains the value
        self.assertTrue(os.path.exists(self.config_file))
        
        with open(self.config_file, 'r') as f:
            saved_config = json.load(f)
            self.assertEqual(saved_config["test"]["save_key"], "save_value")

    def test_environment_variable_override(self):
        """Test overriding config with environment variables"""
        # Set an environment variable
        os.environ["AEGIS_TEST_ENV_VAR"] = "env_value"
        
        config = ConfigManagerConfig(
            config_paths=[self.config_file],
            auto_reload=False
        )
        
        manager = initialize_config_manager(config)
        
        # Check that environment variable was loaded
        value = manager.get_value("test_env_var")
        self.assertEqual(value, "env_value")
        
        # Clean up environment variable
        del os.environ["AEGIS_TEST_ENV_VAR"]

    async def test_start_config_system(self):
        """Test starting the config system as a module"""
        config = {
            "config_paths": [self.config_file],
            "auto_reload": False
        }
        
        result = await start_config_system(config)
        self.assertTrue(result)
        
        # Check that we can get the global config manager
        manager = get_config_manager()
        self.assertIsNotNone(manager)
        
        # Check that config contains expected structure
        cfg = manager.get_config()
        self.assertIn("app", cfg)
        self.assertIn("tor", cfg)
        self.assertIn("p2p", cfg)


if __name__ == '__main__':
    # Run tests
    unittest.main()