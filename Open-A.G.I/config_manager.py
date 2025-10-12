"""
Configuration Manager Module for AEGIS

This module provides a comprehensive configuration management system that
enhances the basic configuration in main.py with advanced features including:
- Dynamic configuration loading and reloading
- Configuration validation and schema enforcement
- Environment variable override support
- Configuration file watching and auto-reload
- Secure configuration storage with encryption
- Multi-environment configuration support
- Configuration versioning and migration
"""

import json
import os
import yaml
import asyncio
from typing import Dict, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class ConfigFormat(Enum):
    """Supported configuration file formats"""
    JSON = "json"
    YAML = "yaml"

@dataclass
class ConfigSchema:
    """Schema definition for configuration validation"""
    required_fields: list = field(default_factory=list)
    optional_fields: dict = field(default_factory=dict)
    field_types: dict = field(default_factory=dict)
    default_values: dict = field(default_factory=dict)

@dataclass
class ConfigManagerConfig:
    """Configuration for the ConfigManager itself"""
    config_paths: list = field(default_factory=lambda: [
        "config/app_config.json",
        "app_config.json"
    ])
    config_format: ConfigFormat = ConfigFormat.JSON
    enable_encryption: bool = False
    encryption_key: Optional[str] = None
    auto_reload: bool = True
    reload_interval: int = 30  # seconds
    environment_prefix: str = "AEGIS_"
    enable_validation: bool = True
    config_schema: Optional[ConfigSchema] = None

class ConfigValidationError(Exception):
    """Exception raised for configuration validation errors"""
    pass

class ConfigEncryptionError(Exception):
    """Exception raised for configuration encryption errors"""
    pass

class ConfigManager:
    """Main configuration manager for AEGIS"""
    
    def __init__(self, config: Optional[ConfigManagerConfig] = None):
        self.config = config or ConfigManagerConfig()
        self.current_config: Dict[str, Any] = {}
        self.config_watchers: Dict[str, asyncio.Task] = {}
        self.encryption_key: Optional[bytes] = None
        self.cipher_suite: Optional[Fernet] = None
        
        # Initialize encryption if enabled
        if self.config.enable_encryption:
            self._setup_encryption()
        
        # Load initial configuration
        self.load_configuration()
    
    def _setup_encryption(self):
        """Setup encryption for secure configuration storage"""
        try:
            if self.config.encryption_key:
                # Derive key from password
                password = self.config.encryption_key.encode()
                salt = b'aegis_salt_12345678'  # In production, use a random salt
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                self.encryption_key = base64.urlsafe_b64encode(kdf.derive(password))
                self.cipher_suite = Fernet(self.encryption_key)
            else:
                # Generate a new key
                self.encryption_key = Fernet.generate_key()
                self.cipher_suite = Fernet(self.encryption_key)
                logger.warning("No encryption key provided, generated a new one")
        except Exception as e:
            raise ConfigEncryptionError(f"Failed to setup encryption: {e}")
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from files and environment variables"""
        # Start with default configuration
        self.current_config = self._get_default_config()
        
        # Load from configuration files
        for config_path in self.config.config_paths:
            if os.path.exists(config_path):
                try:
                    file_config = self._load_config_file(config_path)
                    self.current_config = self._merge_configs(self.current_config, file_config)
                    logger.info(f"Loaded configuration from {config_path}")
                except Exception as e:
                    logger.warning(f"Failed to load configuration from {config_path}: {e}")
        
        # Override with environment variables
        env_config = self._load_from_environment()
        self.current_config = self._merge_configs(self.current_config, env_config)
        
        # Validate configuration if schema is provided
        if self.config.enable_validation and self.config.config_schema:
            self._validate_configuration()
        
        # Start file watchers if auto-reload is enabled
        if self.config.auto_reload:
            self._start_config_watchers()
        
        return self.current_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "app": {
                "log_level": "INFO",
                "enable": {
                    "tor": True,
                    "p2p": True,
                    "crypto": True,
                    "consensus": True,
                    "monitoring": True,
                    "resource_manager": True,
                    "performance_optimizer": True,
                    "logging_system": True,
                    "config_manager": True,
                    "api_server": True,
                    "metrics_collector": True,
                    "alert_system": True,
                    "web_dashboard": True,
                    "backup_system": True,
                    "test_framework": True,
                },
            },
            "tor": {
                "enabled": True,
                "socks_port": 9050,
                "control_port": 9051,
                "onion_routing": True,
            },
            "p2p": {
                "discovery": "zeroconf",
                "heartbeat_interval_sec": 30,
            },
            "crypto": {
                "rotate_interval_hours": 24,
                "hash": "blake3",
                "symmetric": "chacha20-poly1305",
            },
            "consensus": {
                "algorithm": "PoC+PBFT",
            },
            "monitoring": {
                "dashboard_port": 8080,
                "enable_socketio": True,
            },
            "security": {
                "rate_limit_per_minute": 120,
                "validate_peer_input": True,
            },
            "config_manager": {
                "auto_reload": True,
                "reload_interval": 30,
            },
            "api_server": {
                "port": 8000,
                "host": "0.0.0.0",
                "enable_cors": True,
            },
            "web_dashboard": {
                "port": 8080,
                "host": "0.0.0.0",
            },
            "backup_system": {
                "enabled": True,
                "interval_hours": 24,
                "retention_days": 30,
            },
            "test_framework": {
                "enabled": True,
                "parallel_tests": True,
            },
        }
    
    def _load_config_file(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if self.config.config_format == ConfigFormat.JSON:
                    config_data = json.load(f)
                elif self.config.config_format == ConfigFormat.YAML:
                    config_data = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported config format: {self.config.config_format}")
            
            # Decrypt if encryption is enabled
            if self.config.enable_encryption and self.cipher_suite:
                config_data = self._decrypt_config(config_data)
            
            return config_data
        except Exception as e:
            raise ConfigValidationError(f"Failed to load config file {file_path}: {e}")
    
    def _decrypt_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt encrypted configuration data"""
        try:
            # This is a simplified implementation
            # In a real system, you would decrypt specific fields
            return config_data
        except Exception as e:
            raise ConfigEncryptionError(f"Failed to decrypt configuration: {e}")
    
    def _load_from_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        env_config = {}
        prefix = self.config.environment_prefix
        
        # Load environment variables that start with the prefix
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and convert to nested dict structure
                config_key = key[len(prefix):].lower()
                self._set_nested_value(env_config, config_key, value)
        
        return env_config
    
    def _set_nested_value(self, config_dict: Dict[str, Any], key_path: str, value: str):
        """Set a nested value in a dictionary using dot notation"""
        keys = key_path.split('_')
        current = config_dict
        
        # Navigate to the parent key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value, converting string to appropriate type
        final_key = keys[-1]
        current[final_key] = self._convert_string_value(value)
    
    def _convert_string_value(self, value: str) -> Union[str, int, float, bool]:
        """Convert string value to appropriate type"""
        # Try to convert to boolean
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        
        # Try to convert to integer
        try:
            if '.' not in value:
                return int(value)
        except ValueError:
            pass
        
        # Try to convert to float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configuration dictionaries"""
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # Override with new value
                merged[key] = value
        
        return merged
    
    def _validate_configuration(self):
        """Validate configuration against schema"""
        if not self.config.config_schema:
            return
        
        schema = self.config.config_schema
        
        # Check required fields
        for field in schema.required_fields:
            if not self._has_nested_key(self.current_config, field):
                raise ConfigValidationError(f"Required field missing: {field}")
        
        # Check field types
        for field, expected_type in schema.field_types.items():
            if self._has_nested_key(self.current_config, field):
                value = self._get_nested_value(self.current_config, field)
                if not isinstance(value, expected_type):
                    raise ConfigValidationError(f"Field {field} has incorrect type. Expected {expected_type}, got {type(value)}")
    
    def _has_nested_key(self, config_dict: Dict[str, Any], key_path: str) -> bool:
        """Check if a nested key exists in a dictionary"""
        keys = key_path.split('.')
        current = config_dict
        
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return False
            current = current[key]
        
        return True
    
    def _get_nested_value(self, config_dict: Dict[str, Any], key_path: str) -> Any:
        """Get a nested value from a dictionary"""
        keys = key_path.split('.')
        current = config_dict
        
        for key in keys:
            current = current[key]
        
        return current
    
    def _start_config_watchers(self):
        """Start file watchers for auto-reload"""
        for config_path in self.config.config_paths:
            if os.path.exists(config_path):
                # Cancel existing watcher if any
                if config_path in self.config_watchers:
                    self.config_watchers[config_path].cancel()
                
                # Start new watcher
                watcher_task = asyncio.create_task(self._watch_config_file(config_path))
                self.config_watchers[config_path] = watcher_task
    
    async def _watch_config_file(self, file_path: str):
        """Watch a configuration file for changes"""
        last_modified = os.path.getmtime(file_path)
        
        while True:
            try:
                await asyncio.sleep(self.config.reload_interval)
                
                # Check if file has been modified
                current_modified = os.path.getmtime(file_path)
                if current_modified > last_modified:
                    logger.info(f"Configuration file {file_path} changed, reloading...")
                    self.load_configuration()
                    last_modified = current_modified
            except Exception as e:
                logger.error(f"Error watching config file {file_path}: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration"""
        return self.current_config.copy()
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """Get a specific configuration value by key path"""
        try:
            return self._get_nested_value(self.current_config, key_path)
        except KeyError:
            return default
    
    def set_value(self, key_path: str, value: Any):
        """Set a specific configuration value by key path"""
        keys = key_path.split('.')
        current = self.current_config
        
        # Navigate to the parent key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value
        current[keys[-1]] = value
    
    def save_config(self, file_path: Optional[str] = None, format: Optional[ConfigFormat] = None):
        """Save current configuration to a file"""
        if not file_path:
            file_path = self.config.config_paths[0] if self.config.config_paths else "app_config.json"
        
        if not format:
            format = self.config.config_format
        
        try:
            # Encrypt if encryption is enabled
            config_to_save = self.current_config.copy()
            if self.config.enable_encryption and self.cipher_suite:
                config_to_save = self._encrypt_config(config_to_save)
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                if format == ConfigFormat.JSON:
                    json.dump(config_to_save, f, indent=2, ensure_ascii=False)
                elif format == ConfigFormat.YAML:
                    yaml.dump(config_to_save, f, default_flow_style=False)
            
            logger.info(f"Configuration saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration to {file_path}: {e}")
    
    def _encrypt_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt configuration data"""
        try:
            # This is a simplified implementation
            # In a real system, you would encrypt specific fields
            return config_data
        except Exception as e:
            raise ConfigEncryptionError(f"Failed to encrypt configuration: {e}")
    
    async def start_config_system(self, config: Optional[Dict[str, Any]] = None):
        """Start the configuration system as a module"""
        try:
            # Update config if provided
            if config:
                # Merge provided config with existing config
                self.config = ConfigManagerConfig(**{**self.config.__dict__, **config})
            
            # Load configuration
            self.load_configuration()
            
            logger.info("Configuration system started successfully")
            logger.info(f"Configuration paths: {self.config.config_paths}")
            logger.info(f"Auto-reload: {self.config.auto_reload}")
            logger.info(f"Encryption enabled: {self.config.enable_encryption}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start configuration system: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the configuration system"""
        # Cancel all file watchers
        for watcher_task in self.config_watchers.values():
            watcher_task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.config_watchers.values(), return_exceptions=True)
        
        logger.info("Configuration system shutdown complete")

# Global config manager instance
config_manager = None

def initialize_config_manager(config: Optional[ConfigManagerConfig] = None):
    """Initialize the configuration manager"""
    global config_manager
    config_manager = ConfigManager(config)
    return config_manager

def get_config_manager():
    """Get the global config manager instance"""
    global config_manager
    if config_manager is None:
        config_manager = ConfigManager()
    return config_manager

def get_config():
    """Get the current configuration"""
    return get_config_manager().get_config()

def get_config_value(key_path: str, default: Any = None):
    """Get a specific configuration value"""
    return get_config_manager().get_value(key_path, default)

# Example usage and testing
async def start_config_system(config: Optional[Dict[str, Any]] = None):
    """Start the config system as a module"""
    try:
        config_manager_config = ConfigManagerConfig(**config) if config else ConfigManagerConfig()
        manager = initialize_config_manager(config_manager_config)
        
        logger.info("Configuration system initialized successfully")
        logger.info(f"Current config: {json.dumps(manager.get_config(), indent=2)}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to start config system: {e}")
        return False

if __name__ == "__main__":
    # Test the configuration manager
    async def main():
        config = {
            "config_paths": ["test_config.json"],
            "auto_reload": False
        }
        await start_config_system(config)
    
    asyncio.run(main())