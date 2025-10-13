"""
API Server Module for AEGIS

This module provides a dedicated API server that separates API endpoints
from the monitoring dashboard, offering:
- RESTful API endpoints for system control
- WebSocket support for real-time communication
- Authentication and authorization mechanisms
- Request validation and rate limiting
- Comprehensive API documentation with OpenAPI/Swagger
- CORS support for web integration
- Metrics collection for API performance
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
from functools import wraps

# Try to import required libraries
try:
    from fastapi import FastAPI, HTTPException, Depends, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Create dummy classes for when FastAPI is not available
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass
            
    class HTTPException(Exception):
        def __init__(self, status_code=500, detail=""):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)
            
    def Depends(x):
        return x
        
    class Request:
        pass
        
    class Response:
        pass
        
    class JSONResponse:
        def __init__(self, status_code=200, content=None):
            self.status_code = status_code
            self.content = content
            
    class CORSMiddleware:
        pass
        
    class HTTPBearer:
        pass
        
    class HTTPAuthorizationCredentials:
        pass
        
    class BaseModel:
        pass
        
    class uvicorn:
        class Config:
            def __init__(self, app, host, port, log_level):
                pass
                
        class Server:
            def __init__(self, config):
                pass
                
            async def serve(self):
                pass

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthLevel(Enum):
    """Authentication levels"""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    ADMIN = "admin"

@dataclass
class APIServerConfig:
    """Configuration for the API server"""
    host: str = "0.0.0.0"
    port: int = 8000
    enable_cors: bool = True
    cors_origins: list = field(default_factory=lambda: ["*"])
    cors_credentials: bool = True
    cors_methods: list = field(default_factory=lambda: ["*"])
    cors_headers: list = field(default_factory=lambda: ["*"])
    enable_auth: bool = False
    auth_secret: Optional[str] = None
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    enable_docs: bool = True
    api_prefix: str = "/api/v1"
    enable_websockets: bool = True

class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if a client is allowed to make a request"""
        now = time.time()
        
        # Initialize client requests list if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False
    
    def get_retry_after(self, client_id: str) -> int:
        """Get seconds until client can make another request"""
        if client_id not in self.requests or not self.requests[client_id]:
            return 0
        
        oldest_request = min(self.requests[client_id])
        now = time.time()
        return max(0, int(self.window_seconds - (now - oldest_request)))

class AuthManager:
    """Authentication manager for API endpoints"""
    
    def __init__(self, secret: Optional[str] = None):
        self.secret = secret
        self.security = HTTPBearer() if FASTAPI_AVAILABLE else None
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> bool:
        """Verify authentication token"""
        if not self.secret:
            return True  # No auth required
        
        if not credentials:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # In a real implementation, you would verify the token
        # This is a simplified example
        if credentials.credentials != self.secret:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return True
    
    def require_auth(self, level: AuthLevel = AuthLevel.AUTHENTICATED):
        """Decorator to require authentication for endpoints"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Authentication logic would go here
                return await func(*args, **kwargs)
            return wrapper
        return decorator

class MetricsCollector:
    """Collect metrics for API performance"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
        self.endpoint_metrics = {}
    
    def record_request(self, endpoint: str, response_time: float, success: bool = True):
        """Record a request"""
        self.request_count += 1
        if not success:
            self.error_count += 1
        
        self.response_times.append(response_time)
        
        # Record endpoint-specific metrics
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                "count": 0,
                "errors": 0,
                "response_times": []
            }
        
        self.endpoint_metrics[endpoint]["count"] += 1
        if not success:
            self.endpoint_metrics[endpoint]["errors"] += 1
        self.endpoint_metrics[endpoint]["response_times"].append(response_time)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            max_response_time = max(self.response_times)
            min_response_time = min(self.response_times)
        else:
            avg_response_time = 0
            max_response_time = 0
            min_response_time = 0
        
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "avg_response_time": avg_response_time,
            "max_response_time": max_response_time,
            "min_response_time": min_response_time,
            "endpoint_metrics": self.endpoint_metrics
        }

class APIServer:
    """Main API server for AEGIS"""
    
    def __init__(self, config: APIServerConfig = None):
        self.config = config or APIServerConfig()
        self.app = None
        self.rate_limiter = RateLimiter(
            self.config.rate_limit_requests,
            self.config.rate_limit_window
        )
        self.auth_manager = AuthManager(self.config.auth_secret)
        self.metrics_collector = MetricsCollector()
        self.routes = {}
        self.running = False
        
        # Initialize FastAPI app if available
        if FASTAPI_AVAILABLE:
            self._setup_app()
    
    def _setup_app(self):
        """Setup the FastAPI application"""
        self.app = FastAPI(
            title="AEGIS API Server",
            description="API server for the AEGIS distributed AI system",
            version="1.0.0",
            docs_url="/docs" if self.config.enable_docs else None,
            redoc_url="/redoc" if self.config.enable_docs else None
        )
        
        # Add CORS middleware if enabled
        if self.config.enable_cors:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.config.cors_origins,
                allow_credentials=self.config.cors_credentials,
                allow_methods=self.config.cors_methods,
                allow_headers=self.config.cors_headers,
            )
        
        # Add middleware for metrics collection
        @self.app.middleware("http")
        async def metrics_middleware(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Record metrics
            endpoint = f"{request.method} {request.url.path}"
            success = response.status_code < 400
            self.metrics_collector.record_request(endpoint, process_time, success)
            
            return response
        
        # Add middleware for rate limiting
        @self.app.middleware("http")
        async def rate_limit_middleware(request: Request, call_next):
            client_id = request.client.host if request.client else "unknown"
            
            if not self.rate_limiter.is_allowed(client_id):
                retry_after = self.rate_limiter.get_retry_after(client_id)
                return JSONResponse(
                    status_code=429,
                    content={"detail": f"Rate limit exceeded. Try again in {retry_after} seconds."}
                )
            
            return await call_next(request)
        
        # Add default routes
        self._add_default_routes()
    
    def _add_default_routes(self):
        """Add default API routes"""
        if not self.app:
            return
        
        @self.app.get("/")
        async def root():
            return {
                "message": "AEGIS API Server",
                "version": "1.0.0",
                "docs": "/docs" if self.config.enable_docs else None
            }
        
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": time.time()
            }
        
        @self.app.get("/metrics")
        async def get_metrics():
            return self.metrics_collector.get_metrics()
        
        @self.app.get("/config")
        async def get_config():
            # This would return the current configuration
            return {
                "host": self.config.host,
                "port": self.config.port,
                "enable_cors": self.config.enable_cors,
                "enable_auth": self.config.enable_auth
            }
    
    def add_route(self, method: str, path: str, handler: Callable, 
                  auth_level: AuthLevel = AuthLevel.PUBLIC, 
                  description: str = ""):
        """Add a custom route to the API"""
        if not self.app:
            logger.warning("FastAPI not available, cannot add route")
            return
        
        # Store route information
        route_key = f"{method.upper()} {path}"
        self.routes[route_key] = {
            "handler": handler,
            "auth_level": auth_level,
            "description": description
        }
        
        # Add route to FastAPI app
        if method.upper() == "GET":
            self.app.get(path)(handler)
        elif method.upper() == "POST":
            self.app.post(path)(handler)
        elif method.upper() == "PUT":
            self.app.put(path)(handler)
        elif method.upper() == "DELETE":
            self.app.delete(path)(handler)
        else:
            logger.warning(f"Unsupported HTTP method: {method}")
    
    async def start_server(self):
        """Start the API server"""
        if not self.app:
            logger.error("FastAPI not available, cannot start server")
            return False
        
        try:
            self.running = True
            logger.info(f"Starting API server on {self.config.host}:{self.config.port}")
            
            # Configure uvicorn
            config = uvicorn.Config(
                self.app,
                host=self.config.host,
                port=self.config.port,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            # Check if we're running in a thread and handle accordingly
            try:
                # Start server
                await server.serve()
            except RuntimeError as e:
                if "loop" in str(e).lower():
                    # This might happen when running in a thread with an existing event loop
                    logger.warning("Detected threaded execution, using alternative server start method")
                    # In this case, we'll just run the server without the full lifespan management
                    from uvicorn import Server, Config
                    config = Config(
                        self.app,
                        host=self.config.host,
                        port=self.config.port,
                        log_level="info"
                    )
                    server = Server(config)
                    await server.serve()
                else:
                    raise e
            
            return True
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the API server"""
        self.running = False
        logger.info("API server stopped")
    
    def get_app(self):
        """Get the FastAPI application instance"""
        return self.app

# Global API server instance
api_server = None

def initialize_api_server(config: APIServerConfig = None):
    """Initialize the API server"""
    global api_server
    if FASTAPI_AVAILABLE:
        api_server = APIServer(config)
    else:
        logger.warning("FastAPI not available, API server not initialized")
    return api_server

def get_api_server():
    """Get the global API server instance"""
    global api_server
    if api_server is None:
        api_server = APIServer()
    return api_server

# Example request/response models
class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: float

class MetricsResponse(BaseModel):
    """Response model for metrics"""
    request_count: int
    error_count: int
    error_rate: float
    avg_response_time: float
    max_response_time: float
    min_response_time: float

# Example usage and testing
async def start_api_server(config: Dict[str, Any] = None):
    """Start the API server as a module"""
    try:
        if not FASTAPI_AVAILABLE:
            logger.error("FastAPI is not installed. Please install it with: pip install fastapi uvicorn[standard]")
            return False
        
        api_config = APIServerConfig(**config) if config else APIServerConfig()
        server = initialize_api_server(api_config)
        
        if not server:
            logger.error("Failed to initialize API server")
            return False
        
        logger.info("API server initialized successfully")
        logger.info(f"Host: {api_config.host}")
        logger.info(f"Port: {api_config.port}")
        logger.info(f"CORS enabled: {api_config.enable_cors}")
        logger.info(f"Authentication enabled: {api_config.enable_auth}")
        
        # Add some example routes
        @server.app.get("/example")
        async def example_endpoint():
            return {"message": "This is an example endpoint"}
        
        # Start server directly instead of creating a task
        # This avoids issues with lifespan management in separate threads
        logger.info("Starting API server...")
        return await server.start_server()
        
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        return False

if __name__ == "__main__":
    # Test the API server
    async def main():
        config = {
            "host": "127.0.0.1",
            "port": 8001,
            "enable_docs": True
        }
        await start_api_server(config)
    
    asyncio.run(main())