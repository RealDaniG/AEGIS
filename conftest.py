"""
Configuration file for pytest
"""

import pytest
import asyncio
import tempfile
import shutil
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