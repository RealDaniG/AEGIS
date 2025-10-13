"""
Integration test for the Open A.G.I system
Tests all components working together
"""

import asyncio
import sys
import os
import time
import json
from pathlib import Path
import pytest

# Add the necessary directories to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Open-A.G.I'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'integrated_components'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tests', 'unit_tests'))

def test_module_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    modules_to_test = [
        'logging_system',
        'config_manager', 
        'api_server',
        'metrics_collector',
        'alert_system',
        'web_dashboard',
        'backup_system',
        'test_framework'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} imported successfully")
        except ImportError as e:
            print(f"  ✗ {module_name} failed to import: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"Failed to import modules: {failed_imports}")
        return False
    
    print("All modules imported successfully!")
    return True

@pytest.mark.asyncio
async def test_logging_system():
    """Test the logging system"""
    print("Testing logging system...")
    
    try:
        from logging_system import start_logging_system
        
        # Test with a simple configuration
        config = {
            "log_level": "INFO",
            "log_file": "integration_test.log",
            "log_dir": "test_logs",
            "enable_console": False,  # Disable console to avoid output
            "enable_file": True
        }
        
        result = await start_logging_system(config)
        if result:
            print("  ✓ Logging system started successfully")
            return True
        else:
            print("  ✗ Logging system failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Logging system test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_config_manager():
    """Test the configuration manager"""
    print("Testing configuration manager...")
    
    try:
        from config_manager import start_config_system
        
        # Test with a simple configuration
        config = {
            "config_paths": ["test_config.json"],
            "auto_reload": False
        }
        
        result = await start_config_system(config)
        if result:
            print("  ✓ Configuration manager started successfully")
            return True
        else:
            print("  ✗ Configuration manager failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Configuration manager test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_api_server():
    """Test the API server"""
    print("Testing API server...")
    
    try:
        from api_server import start_api_server
        
        # Test with a simple configuration
        config = {
            "host": "127.0.0.1",
            "port": 8001,
            "enable_docs": False,
            "enable_cors": False
        }
        
        result = await start_api_server(config)
        if result:
            print("  ✓ API server started successfully")
            return True
        else:
            print("  ✗ API server failed to start")
            return False
    except Exception as e:
        print(f"  ✗ API server test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_metrics_collector():
    """Test the metrics collector"""
    print("Testing metrics collector...")
    
    try:
        from metrics_collector import start_metrics_collector
        
        # Test with a simple configuration
        config = {
            "enable_prometheus": False,
            "collection_interval": 1,  # Fast interval for testing
            "enable_system_metrics": False  # Disable system metrics for faster test
        }
        
        result = await start_metrics_collector(config)
        if result:
            print("  ✓ Metrics collector started successfully")
            return True
        else:
            print("  ✗ Metrics collector failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Metrics collector test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_alert_system():
    """Test the alert system"""
    print("Testing alert system...")
    
    try:
        from alert_system import start_alert_system
        
        # Test with a simple configuration
        config = {
            "enable_email_notifications": False,
            "enable_webhook_notifications": False,
            "notification_interval": 30
        }
        
        result = await start_alert_system(config)
        if result:
            print("  ✓ Alert system started successfully")
            return True
        else:
            print("  ✗ Alert system failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Alert system test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_web_dashboard():
    """Test the web dashboard"""
    print("Testing web dashboard...")
    
    try:
        from web_dashboard import start_web_dashboard
        
        # Test with a simple configuration
        config = {
            "host": "127.0.0.1",
            "port": 8081,
            "debug": False
        }
        
        result = await start_web_dashboard(config)
        if result:
            print("  ✓ Web dashboard started successfully")
            return True
        else:
            print("  ✗ Web dashboard failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Web dashboard test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_backup_system():
    """Test the backup system"""
    print("Testing backup system...")
    
    try:
        from backup_system import start_backup_system
        
        # Test with a simple configuration
        config = {
            "enabled": False,  # Disable for testing
            "interval_hours": 1,
            "retention_days": 7,
            "enable_encryption": False,
            "source_directories": ["test_source"],
            "backup_directory": "test_backups"
        }
        
        result = await start_backup_system(config)
        if result:
            print("  ✓ Backup system started successfully")
            return True
        else:
            print("  ✗ Backup system failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Backup system test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_test_framework():
    """Test the test framework"""
    print("Testing test framework...")
    
    try:
        from test_framework import start_test_framework
        
        # Test with a simple configuration
        config = {
            "parallel_tests": False,
            "max_concurrent_tests": 1,
            "report_directory": "test_reports"
        }
        
        result = await start_test_framework(config)
        if result:
            print("  ✓ Test framework started successfully")
            return True
        else:
            print("  ✗ Test framework failed to start")
            return False
    except Exception as e:
        print(f"  ✗ Test framework test failed: {e}")
        return False

async def run_integration_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("Open A.G.I Integration Tests")
    print("=" * 60)
    
    start_time = time.time()
    
    # Test module imports first
    if not test_module_imports():
        print("Module import tests failed. Aborting integration tests.")
        return False
    
    # Run async tests
    tests = [
        test_logging_system,
        test_config_manager,
        test_api_server,
        test_metrics_collector,
        test_alert_system,
        test_web_dashboard,
        test_backup_system,
        test_test_framework
    ]
    
    passed_tests = 0
    failed_tests = 0
    
    for test_func in tests:
        try:
            result = await test_func()
            if result:
                passed_tests += 1
            else:
                failed_tests += 1
        except Exception as e:
            print(f"  ✗ {test_func.__name__} failed with exception: {e}")
            failed_tests += 1
        
        # Small delay between tests
        await asyncio.sleep(0.1)
    
    end_time = time.time()
    
    print("=" * 60)
    print("Integration Test Results")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if failed_tests == 0:
        print("🎉 All integration tests passed!")
        return True
    else:
        print(f"❌ {failed_tests} integration test(s) failed.")
        return False

if __name__ == "__main__":
    # Create test directories
    Path("test_logs").mkdir(exist_ok=True)
    Path("test_backups").mkdir(exist_ok=True)
    Path("test_reports").mkdir(exist_ok=True)
    Path("test_source").mkdir(exist_ok=True)
    
    # Run integration tests
    result = asyncio.run(run_integration_tests())
    
    # Clean up test directories
    import shutil
    try:
        if Path("test_logs").exists():
            shutil.rmtree("test_logs")
        if Path("test_backups").exists():
            shutil.rmtree("test_backups")
        if Path("test_reports").exists():
            shutil.rmtree("test_reports")
        if Path("test_source").exists():
            shutil.rmtree("test_source")
    except Exception as e:
        print(f"Warning: Failed to clean up test directories: {e}")
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)