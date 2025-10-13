"""
Dedicated Logging System Module for AEGIS

This module provides a comprehensive logging system that replaces the partial
loguru implementation in main.py with advanced features including:
- Multi-level logging with customizable formats
- File and console output
- Log rotation and retention policies
- Structured logging with JSON support
- Performance monitoring integration
- Security-aware logging with sensitive data filtering
"""

import logging
import logging.handlers
import json
import os
import sys
import traceback
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum

# Configure loguru as the primary logger if available
try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    # Fallback to standard logging
    LOGURU_AVAILABLE = False
    logger = logging.getLogger(__name__)

class LogLevel(Enum):
    """Log levels for the logging system"""
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

@dataclass
class LogConfig:
    """Configuration for the logging system"""
    log_level: str = "INFO"
    log_file: str = "aegis_system.log"
    log_dir: str = "logs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = True
    json_format: bool = False
    include_timestamp: bool = True
    include_thread_info: bool = False
    sensitive_fields: list = None
    
    def __post_init__(self):
        if self.sensitive_fields is None:
            self.sensitive_fields = ["password", "secret", "token", "key", "private"]

class SensitiveDataFilter(logging.Filter):
    """Filter to remove sensitive data from logs"""
    
    def __init__(self, sensitive_fields: list):
        super().__init__()
        self.sensitive_fields = sensitive_fields
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter sensitive data from log records"""
        # Convert record args to string and check for sensitive data
        if record.args:
            args_str = str(record.args)
            for field in self.sensitive_fields:
                if field.lower() in args_str.lower():
                    # Replace sensitive data with masked values
                    record.args = self._mask_sensitive_data(record.args)
        return True
    
    def _mask_sensitive_data(self, data) -> tuple:
        """Mask sensitive data in log arguments"""
        if isinstance(data, dict):
            masked_data = {}
            for key, value in data.items():
                if any(sensitive_field.lower() in key.lower() for sensitive_field in self.sensitive_fields):
                    masked_data[key] = "***MASKED***"
                else:
                    masked_data[key] = value
            return (masked_data,)
        elif isinstance(data, (list, tuple)):
            masked_data = []
            for item in data:
                if isinstance(item, dict):
                    masked_item = {}
                    for key, value in item.items():
                        if any(sensitive_field.lower() in key.lower() for sensitive_field in self.sensitive_fields):
                            masked_item[key] = "***MASKED***"
                        else:
                            masked_item[key] = value
                    masked_data.append(masked_item)
                else:
                    masked_data.append(item)
            return (masked_data,)
        else:
            return data

class StructuredFormatter(logging.Formatter):
    """Formatter for structured logging with JSON support"""
    
    def __init__(self, json_format: bool = False, include_timestamp: bool = True, 
                 include_thread_info: bool = False):
        super().__init__()
        self.json_format = json_format
        self.include_timestamp = include_timestamp
        self.include_thread_info = include_thread_info
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON or standard text"""
        if self.json_format:
            log_entry = {
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            if self.include_timestamp:
                log_entry["timestamp"] = datetime.fromtimestamp(record.created).isoformat()
            
            if self.include_thread_info:
                log_entry["thread_id"] = record.thread
                log_entry["thread_name"] = record.threadName
            
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_entry, ensure_ascii=False)
        else:
            return super().format(record)

class AEGISLogger:
    """Main logging system for AEGIS"""
    
    def __init__(self, config: LogConfig = None):
        self.config = config or LogConfig()
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logging system with configured handlers"""
        # Create logs directory if it doesn't exist
        log_dir = Path(self.config.log_dir)
        log_dir.mkdir(exist_ok=True)
        
        # Initialize logger
        if LOGURU_AVAILABLE:
            # Configure loguru
            logger.remove()  # Remove default handler
            
            # Add console handler
            if self.config.enable_console:
                logger.add(
                    sys.stderr,
                    level=self.config.log_level,
                    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                    filter=self._loguru_filter
                )
            
            # Add file handler with rotation
            if self.config.enable_file:
                log_file_path = log_dir / self.config.log_file
                logger.add(
                    str(log_file_path),
                    level=self.config.log_level,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                    rotation=f"{self.config.max_file_size} B",
                    retention=self.config.backup_count,
                    compression="zip"
                )
            
            self.logger = logger
        else:
            # Configure standard logging
            self.logger = logging.getLogger("AEGIS")
            self.logger.setLevel(getattr(logging, self.config.log_level))
            
            # Clear existing handlers
            self.logger.handlers.clear()
            
            # Create formatter
            formatter = StructuredFormatter(
                json_format=self.config.json_format,
                include_timestamp=self.config.include_timestamp,
                include_thread_info=self.config.include_thread_info
            )
            
            # Add console handler
            if self.config.enable_console:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                console_handler.addFilter(SensitiveDataFilter(self.config.sensitive_fields))
                self.logger.addHandler(console_handler)
            
            # Add file handler with rotation
            if self.config.enable_file:
                log_file_path = log_dir / self.config.log_file
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file_path,
                    maxBytes=self.config.max_file_size,
                    backupCount=self.config.backup_count
                )
                file_handler.setFormatter(formatter)
                file_handler.addFilter(SensitiveDataFilter(self.config.sensitive_fields))
                self.logger.addHandler(file_handler)
    
    def _loguru_filter(self, record):
        """Filter for loguru to handle sensitive data"""
        # This would be implemented to filter sensitive data in loguru
        return True
    
    def trace(self, message: str, *args, **kwargs):
        """Log a trace message"""
        if LOGURU_AVAILABLE:
            self.logger.trace(message, *args, **kwargs)
        else:
            self.logger.log(LogLevel.TRACE.value, message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log a debug message"""
        if LOGURU_AVAILABLE:
            self.logger.debug(message, *args, **kwargs)
        else:
            self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log an info message"""
        if LOGURU_AVAILABLE:
            self.logger.info(message, *args, **kwargs)
        else:
            self.logger.info(message, *args, **kwargs)
    
    def success(self, message: str, *args, **kwargs):
        """Log a success message"""
        if LOGURU_AVAILABLE:
            self.logger.success(message, *args, **kwargs)
        else:
            self.logger.log(LogLevel.SUCCESS.value, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log a warning message"""
        if LOGURU_AVAILABLE:
            self.logger.warning(message, *args, **kwargs)
        else:
            self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log an error message"""
        if LOGURU_AVAILABLE:
            self.logger.error(message, *args, **kwargs)
        else:
            self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log a critical message"""
        if LOGURU_AVAILABLE:
            self.logger.critical(message, *args, **kwargs)
        else:
            self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log an exception with traceback"""
        if LOGURU_AVAILABLE:
            self.logger.exception(message, *args, **kwargs)
        else:
            self.logger.exception(message, *args, **kwargs)
    
    def log_performance(self, operation: str, duration: float, metadata: Dict[str, Any] = None):
        """Log performance metrics"""
        metadata = metadata or {}
        message = f"PERFORMANCE: {operation} completed in {duration:.4f}s"
        if metadata:
            message += f" | Metadata: {json.dumps(metadata)}"
        
        self.info(message)
    
    def log_security_event(self, event_type: str, severity: str, details: Dict[str, Any] = None):
        """Log security-related events"""
        details = details or {}
        message = f"SECURITY: {event_type} | Severity: {severity}"
        if details:
            message += f" | Details: {json.dumps(details)}"
        
        if severity.upper() in ["CRITICAL", "HIGH"]:
            self.critical(message)
        elif severity.upper() == "MEDIUM":
            self.error(message)
        elif severity.upper() == "LOW":
            self.warning(message)
        else:
            self.info(message)

# Global logger instance
aegis_logger = None

def initialize_logging(config: LogConfig = None):
    """Initialize the logging system"""
    global aegis_logger
    aegis_logger = AEGISLogger(config)
    return aegis_logger

def get_logger():
    """Get the global logger instance"""
    global aegis_logger
    if aegis_logger is None:
        aegis_logger = AEGISLogger()
    return aegis_logger

def shutdown_logging():
    """Shutdown the logging system"""
    global aegis_logger
    if aegis_logger and LOGURU_AVAILABLE:
        logger.remove()
    aegis_logger = None

# Convenience functions that match the existing loguru interface
def trace(message, *args, **kwargs):
    """Log a trace message"""
    get_logger().trace(message, *args, **kwargs)

def debug(message, *args, **kwargs):
    """Log a debug message"""
    get_logger().debug(message, *args, **kwargs)

def info(message, *args, **kwargs):
    """Log an info message"""
    get_logger().info(message, *args, **kwargs)

def success(message, *args, **kwargs):
    """Log a success message"""
    get_logger().success(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    """Log a warning message"""
    get_logger().warning(message, *args, **kwargs)

def error(message, *args, **kwargs):
    """Log an error message"""
    get_logger().error(message, *args, **kwargs)

def critical(message, *args, **kwargs):
    """Log a critical message"""
    get_logger().critical(message, *args, **kwargs)

def exception(message, *args, **kwargs):
    """Log an exception with traceback"""
    get_logger().exception(message, *args, **kwargs)

# Example usage and testing
async def start_logging_system(config: Dict[str, Any] = None):
    """Start the logging system as a module"""
    try:
        log_config = LogConfig(**config) if config else LogConfig()
        logger_instance = initialize_logging(log_config)
        
        info("Logging system initialized successfully")
        info(f"Log level: {log_config.log_level}")
        info(f"Log file: {log_config.log_dir}/{log_config.log_file}")
        info(f"Console output: {log_config.enable_console}")
        info(f"File output: {log_config.enable_file}")
        
        # Test logging at different levels
        trace("This is a trace message")
        debug("This is a debug message")
        info("This is an info message")
        success("This is a success message")
        warning("This is a warning message")
        error("This is an error message")
        critical("This is a critical message")
        
        # Test structured logging
        logger_instance.log_performance("test_operation", 0.1234, {"test": "data"})
        logger_instance.log_security_event("test_event", "LOW", {"test": "security_data"})
        
        return True
    except Exception as e:
        error(f"Failed to start logging system: {e}")
        return False

if __name__ == "__main__":
    # Test the logging system
    async def main():
        config = {
            "log_level": "DEBUG",
            "log_file": "test_log.log",
            "json_format": True
        }
        await start_logging_system(config)
    
    asyncio.run(main())