"""
Configuration file for pytest
"""

import pytest
import asyncio
import tempfile
import shutil
import os
import sys
from pathlib import Path

# Configure asyncio mode for pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

def pytest_configure(config):
    """Configure pytest settings"""
    config.option.asyncio_mode = "strict"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Clean up after test
    try:
        shutil.rmtree(temp_path)
    except Exception:
        # On Windows, sometimes files are still locked
        pass

@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.resolve()

@pytest.fixture(scope="session")
def open_agi_path(project_root):
    """Return the Open-A.G.I directory path."""
    return project_root / "Open-A.G.I"

@pytest.fixture(scope="session")
def metatron_path(project_root):
    """Return the Metatron-ConscienceAI directory path."""
    return project_root / "Metatron-ConscienceAI"

@pytest.fixture(autouse=True)
def setup_test_environment(project_root, open_agi_path, metatron_path):
    """Automatically setup test environment for all tests."""
    # Add project directories to Python path
    paths_to_add = [
        str(project_root),
        str(open_agi_path),
        str(metatron_path),
        str(project_root / "tests" / "unit_tests"),
        str(project_root / "integrated_components")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Create test directories if they don't exist
    test_dirs = [
        project_root / "test_logs",
        project_root / "test_backups",
        project_root / "test_reports",
        project_root / "test_source"
    ]
    
    for test_dir in test_dirs:
        test_dir.mkdir(exist_ok=True)
    
    yield
    
    # Cleanup is handled by individual test fixtures

# Platform-specific configurations
def pytest_runtest_setup(item):
    """Setup before each test runs."""
    # Skip tests that require specific platforms
    if "windows_only" in item.keywords and sys.platform != "win32":
        pytest.skip("Test requires Windows platform")
    elif "unix_only" in item.keywords and sys.platform == "win32":
        pytest.skip("Test requires Unix-like platform")