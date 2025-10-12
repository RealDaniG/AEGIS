# Netifaces Installation Issue Resolution

## Problem
The `netifaces` package is failing to build on Windows with the error:
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
```

## Solutions (in order of preference)

### Solution 1: Install Microsoft C++ Build Tools (Recommended)
1. Download Microsoft C++ Build Tools from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install the "C++ build tools" workload
3. After installation, try installing netifaces again:
   ```bash
   pip install netifaces
   ```

### Solution 2: Use Alternative IP Detection Method
The code already has fallbacks for when netifaces is not available. The system will:
- Show a warning message: "netifaces no disponible; detección de IP local puede ser limitada en este entorno."
- Use socket-based IP detection as fallback

This approach will work but may be less accurate in complex network environments.

### Solution 3: Skip Netifaces Installation
Since the code has graceful fallbacks, you can continue without netifaces:
1. The system will use alternative methods for IP detection
2. All core functionality should still work
3. Some advanced network interface detection features may be limited

## Code Fallback Mechanism
The P2P network module already implements graceful handling:

```python
try:
    import netifaces
    HAS_NETIFACES = True
except Exception:
    netifaces = None
    HAS_NETIFACES = False
    logger.warning("netifaces no disponible; detección de IP local puede ser limitada en este entorno.")

def _get_local_ip(self) -> str:
    """Obtiene la IP local del nodo"""
    try:
        if HAS_NETIFACES:
            # Intentar obtener IP de interfaces de red
            interfaces = netifaces.interfaces()
            # ... netifaces-based IP detection ...
    
    # Fallback: usar socket para conectar a servidor externo
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
```

## Recommendation
1. For development: Install Microsoft C++ Build Tools for full functionality
2. For quick testing: Continue without netifaces - the fallbacks will work for basic operation
3. For production: Install the build tools to ensure optimal network interface detection

The system is designed to work even without netifaces, so you can proceed with testing while considering the long-term installation of the build tools.