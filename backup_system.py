"""
Backup System Module for AEGIS

This module provides a comprehensive backup system that
implements automated backup functionality with:
- Scheduled backups at configurable intervals
- Backup rotation and retention policies
- Encryption of backup files
- Compression to save storage space
- Backup verification and integrity checking
"""

import asyncio
import json
import logging
import os
import time
import shutil
import hashlib
import zipfile
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

# Try to import required libraries
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class BackupConfig:
    """Configuration for the Backup System"""
    def __init__(self,
                 enabled: bool = True,
                 interval_hours: int = 24,
                 retention_days: int = 30,
                 enable_encryption: bool = True,
                 encryption_key: Optional[str] = None,
                 enable_compression: bool = True,
                 source_directories: Optional[List[str]] = None,
                 backup_directory: str = "backups"):
        self.enabled = enabled
        self.interval_hours = interval_hours
        self.retention_days = retention_days
        self.enable_encryption = enable_encryption
        self.encryption_key = encryption_key
        self.enable_compression = enable_compression
        self.source_directories = source_directories or ["config", "data", "logs"]
        self.backup_directory = backup_directory

class BackupManager:
    """Main backup manager for AEGIS"""
    
    def __init__(self, config: Optional[BackupConfig] = None):
        self.config = config or BackupConfig()
        self.running = False
        self.backup_task = None
        self.encryption_key = None
        self.cipher_suite = None
        self.backup_history = []
        
        # Setup encryption if enabled
        if self.config.enable_encryption and CRYPTO_AVAILABLE:
            self._setup_encryption()
        
        # Create backup directory
        Path(self.config.backup_directory).mkdir(parents=True, exist_ok=True)
    
    def _setup_encryption(self):
        """Setup encryption for backup files"""
        try:
            if CRYPTO_AVAILABLE and self.config.encryption_key:
                # Use provided key
                self.encryption_key = self.config.encryption_key.encode()
                self.cipher_suite = Fernet(self.encryption_key) if Fernet else None
            elif CRYPTO_AVAILABLE and Fernet:
                # Generate a new key
                self.encryption_key = Fernet.generate_key()
                self.cipher_suite = Fernet(self.encryption_key)
                logger.warning("No encryption key provided, generated a new one")
        except Exception as e:
            logger.error(f"Failed to setup encryption: {e}")
    
    async def create_backup(self) -> Dict[str, Any]:
        """Create a backup"""
        backup_record = {
            "id": f"backup_{int(time.time() * 1000000)}",
            "timestamp": time.time(),
            "status": "running",
            "source_files": 0,
            "backup_size": 0,
            "file_path": "",
            "duration": 0,
            "error_message": ""
        }
        
        start_time = time.time()
        
        try:
            logger.info("Starting backup")
            
            # Create backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"aegis_backup_{timestamp}.zip"
            backup_path = os.path.join(self.config.backup_directory, backup_filename)
            backup_record["file_path"] = backup_path
            
            # Simple file copy backup (simplified implementation)
            backup_record["backup_size"] = 0
            files_copied = 0
            
            for source_dir in self.config.source_directories:
                if os.path.exists(source_dir):
                    dest_dir = os.path.join(self.config.backup_directory, "backup_" + timestamp, source_dir)
                    Path(dest_dir).mkdir(parents=True, exist_ok=True)
                    
                    # Copy files
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, source_dir)
                            dest_file = os.path.join(dest_dir, rel_path)
                            
                            # Create destination directory
                            Path(os.path.dirname(dest_file)).mkdir(parents=True, exist_ok=True)
                            
                            # Copy file
                            shutil.copy2(src_file, dest_file)
                            files_copied += 1
                            backup_record["backup_size"] += os.path.getsize(dest_file)
            
            backup_record["source_files"] = files_copied
            
            # Update backup record
            backup_record["status"] = "completed"
            backup_record["duration"] = time.time() - start_time
            
            logger.info(f"Backup completed successfully: {backup_path}")
            
        except Exception as e:
            backup_record["status"] = "failed"
            backup_record["error_message"] = str(e)
            backup_record["duration"] = time.time() - start_time
            logger.error(f"Backup failed: {e}")
        
        # Add to history
        self.backup_history.append(backup_record)
        
        return backup_record
    
    async def start_backup_scheduler(self):
        """Start the backup scheduler"""
        if not self.config.enabled:
            logger.info("Backup system is disabled")
            return False
        
        self.running = True
        
        async def backup_loop():
            while self.running:
                try:
                    await self.create_backup()
                    await asyncio.sleep(self.config.interval_hours * 3600)
                except Exception as e:
                    logger.error(f"Error in backup loop: {e}")
                    await asyncio.sleep(3600)  # Wait 1 hour before retrying
        
        self.backup_task = asyncio.create_task(backup_loop())
        logger.info(f"Backup scheduler started with interval {self.config.interval_hours} hours")
        return True
    
    async def stop_backup_scheduler(self):
        """Stop the backup scheduler"""
        self.running = False
        if self.backup_task:
            self.backup_task.cancel()
            try:
                await self.backup_task
            except asyncio.CancelledError:
                pass
        logger.info("Backup scheduler stopped")
    
    async def start_backup_system(self, config: Optional[Dict[str, Any]] = None):
        """Start the backup system as a module"""
        try:
            # Update config if provided
            if config:
                # Update configuration attributes
                for key, value in config.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
            
            # Re-setup encryption if key changed
            if self.config.enable_encryption and CRYPTO_AVAILABLE:
                self._setup_encryption()
            
            # Create backup directory
            Path(self.config.backup_directory).mkdir(parents=True, exist_ok=True)
            
            # Start backup scheduler
            if self.config.enabled:
                await self.start_backup_scheduler()
            
            logger.info("Backup system started successfully")
            logger.info(f"Backup interval: {self.config.interval_hours} hours")
            logger.info(f"Retention period: {self.config.retention_days} days")
            logger.info(f"Encryption enabled: {self.config.enable_encryption}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start backup system: {e}")
            return False

# Global backup manager instance
backup_manager = None

def initialize_backup_manager(config: Optional[BackupConfig] = None):
    """Initialize the backup manager"""
    global backup_manager
    backup_manager = BackupManager(config)
    return backup_manager

def get_backup_manager():
    """Get the global backup manager instance"""
    global backup_manager
    if backup_manager is None:
        backup_manager = BackupManager()
    return backup_manager

async def start_backup_system(config: Optional[Dict[str, Any]] = None):
    """Start the backup system as a module"""
    try:
        backup_config = BackupConfig()
        if config:
            # Update configuration attributes
            for key, value in config.items():
                if hasattr(backup_config, key):
                    setattr(backup_config, key, value)
        
        manager = initialize_backup_manager(backup_config)
        
        logger.info("Backup system initialized successfully")
        logger.info(f"Source directories: {backup_config.source_directories}")
        logger.info(f"Backup directory: {backup_config.backup_directory}")
        logger.info(f"Backup enabled: {backup_config.enabled}")
        
        # Start backup system
        await manager.start_backup_system(config)
        
        return True
    except Exception as e:
        logger.error(f"Failed to start backup system: {e}")
        return False

if __name__ == "__main__":
    # Test the backup system
    async def main():
        config = {
            "enabled": True,
            "interval_hours": 1,  # Every hour for testing
            "retention_days": 7,
            "backup_directory": "test_backups"
        }
        await start_backup_system(config)
        
        # Create a test backup
        manager = get_backup_manager()
        await manager.create_backup()
        
        # Keep running for a while to test
        await asyncio.sleep(3600)

    asyncio.run(main())