import pytest

def test_safe_import():
    """Test that safe_import function works correctly."""
    from main import safe_import
    
    # Test importing a standard library module
    mod, err = safe_import("os")
    assert mod is not None
    assert err is None
    
    # Test importing a non-existent module
    mod, err = safe_import("non_existent_module_12345")
    assert mod is None
    assert err is not None

def test_module_call():
    """Test that module_call function works correctly."""
    import asyncio
    from main import safe_import, module_call
    
    # Import a module with a simple function
    mod, err = safe_import("os")
    assert mod is not None
    
    # Test calling a synchronous function
    result = asyncio.run(module_call(mod, "getcwd"))
    assert result is not None