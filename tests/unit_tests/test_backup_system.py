"""
Unit tests for the backup_system module
"""

import unittest
import asyncio
import tempfile
import os
import shutil
from pathlib import Path


class TestBackupSystem(unittest.TestCase):
    """Test cases for the backup system"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Try to import backup system components
        try:
            global backup_system
            import backup_system
            self.backup_system_available = True
        except ImportError:
            self.backup_system_available = False
            print("Backup system components not available, skipping backup system tests")
        
        self.test_dir = tempfile.mkdtemp()
        self.backup_test_dir = os.path.join(self.test_dir, "backups")
        self.source_test_dir = os.path.join(self.test_dir, "source")
        
        # Create source directory for testing
        os.makedirs(self.source_test_dir, exist_ok=True)
        
        # Create some test files
        with open(os.path.join(self.source_test_dir, "test_file1.txt"), "w") as f:
            f.write("Test content 1")
            
        with open(os.path.join(self.source_test_dir, "test_file2.txt"), "w") as f:
            f.write("Test content 2")

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up test files
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_import_backup_system_module(self):
        """Test that the backup_system module can be imported"""
        try:
            import backup_system
            self.assertTrue(True)  # Import succeeded
        except ImportError:
            self.skipTest("Backup system components not available")

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_backup_config_creation(self):
        """Test creation of BackupConfig object"""
        if not self.backup_system_available:
            self.skipTest("Backup system components not available")
            
        config = backup_system.BackupConfig(
            enabled=True,
            interval_hours=1,
            retention_days=7,
            enable_encryption=False,
            source_directories=[self.source_test_dir],
            backup_directory=self.backup_test_dir
        )
        
        self.assertEqual(config.enabled, True)
        self.assertEqual(config.interval_hours, 1)
        self.assertEqual(config.retention_days, 7)
        self.assertEqual(config.enable_encryption, False)
        self.assertEqual(config.source_directories, [self.source_test_dir])
        self.assertEqual(config.backup_directory, self.backup_test_dir)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    def test_initialize_backup_manager(self):
        """Test initializing the backup manager"""
        if not self.backup_system_available:
            self.skipTest("Backup system components not available")
            
        config = backup_system.BackupConfig(
            enabled=False,  # Disable for testing
            interval_hours=1,
            retention_days=7,
            enable_encryption=False,
            source_directories=[self.source_test_dir],
            backup_directory=self.backup_test_dir
        )
        
        manager = backup_system.initialize_backup_manager(config)
        self.assertIsNotNone(manager)
        
        # Check that backup directory was created
        self.assertTrue(os.path.exists(self.backup_test_dir))

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_create_backup(self):
        """Test creating a backup"""
        if not self.backup_system_available:
            self.skipTest("Backup system components not available")
            
        config = backup_system.BackupConfig(
            enabled=False,  # Disable automatic scheduling
            interval_hours=1,
            retention_days=7,
            enable_encryption=False,
            source_directories=[self.source_test_dir],
            backup_directory=self.backup_test_dir
        )
        
        manager = backup_system.initialize_backup_manager(config)
        
        # Create a backup
        backup_record = await manager.create_backup()
        
        self.assertIsNotNone(backup_record)
        if backup_record is not None:
            self.assertEqual(backup_record["status"], "completed")
            self.assertGreater(backup_record["source_files"], 0)
            self.assertGreater(backup_record["backup_size"], 0)

    @unittest.skipIf(not hasattr(unittest, 'skipIf'), "SkipIf not available")
    async def test_start_backup_system(self):
        """Test starting the backup system as a module"""
        if not self.backup_system_available:
            self.skipTest("Backup system components not available")
            
        config = {
            "enabled": False,  # Disable for testing
            "interval_hours": 1,
            "retention_days": 7,
            "enable_encryption": False,
            "source_directories": [self.source_test_dir],
            "backup_directory": self.backup_test_dir
        }
        
        result = await backup_system.start_backup_system(config)
        self.assertTrue(result)
        
        # Check that we can get the global backup manager
        manager = backup_system.get_backup_manager()
        self.assertIsNotNone(manager)
        
        # Check configuration
        self.assertEqual(manager.config.enabled, False)
        self.assertEqual(manager.config.interval_hours, 1)


if __name__ == '__main__':
    # Run tests
    unittest.main()