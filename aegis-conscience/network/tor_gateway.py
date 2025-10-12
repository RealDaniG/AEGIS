"""
TOR Gateway for AEGIS-Conscience Network
Integration with TOR v3 onion services
"""

import asyncio
import time
import secrets
import os
from typing import Optional, Dict, List
from dataclasses import asdict

# Conditional imports for TOR
try:
    from stem.control import Controller
    from stem import Signal
    HAS_STEM = True
except ImportError:
    HAS_STEM = False
    # Create dummy classes for type hints when stem is not available
    class Controller:
        pass
    class Signal:
        NEWNYM = "NEWNYM"

from schemas import NetworkMessage


class TORGateway:
    """TOR gateway for anonymous P2P communication"""
    
    def __init__(self, control_port: int = 9051, socks_port: int = 9050):
        self.control_port = control_port
        self.socks_port = socks_port
        self.controller: Optional[Controller] = None
        self.onion_services: Dict[str, str] = {}  # service_id -> private_key
        self.circuits: Dict[str, Dict] = {}  # circuit management
        self.initialized = False
        self.authorized_clients: Dict[str, str] = {}  # client_id -> auth_cookie
        
    async def initialize(self) -> bool:
        """Initialize TOR connection"""
        if not HAS_STEM:
            print("TOR integration disabled: stem library not available")
            return False
            
        try:
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            if not self.controller.is_alive():
                print("TOR controller is not alive")
                return False
                
            self.initialized = True
            print("TOR gateway initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing TOR gateway: {e}")
            return False
    
    async def create_onion_service(self, port: int, target_port: int = 0, 
                                 authorized_clients: Optional[List[str]] = None) -> Optional[str]:
        """
        Create a TOR v3 onion service with client authorization
        
        Args:
            port: Port to expose on the onion service
            target_port: Local port to forward to (defaults to port)
            authorized_clients: List of client IDs authorized to connect
            
        Returns:
            str: Onion service address or None if failed
        """
        if not self.initialized:
            print("TOR gateway not initialized")
            return None
            
        try:
            if target_port is None or target_port == 0:
                target_port = port
                
            # Generate authorization cookies for clients
            auth_cookies = {}
            if authorized_clients:
                for client_id in authorized_clients:
                    cookie = secrets.token_hex(16)
                    auth_cookies[client_id] = cookie
            
            # Prepare authorization parameters
            auth_params = {}
            if auth_cookies:
                # Create client authorization file content
                auth_content = ""
                for client_id, cookie in auth_cookies.items():
                    auth_content += f"client-auth-{client_id}:{cookie}\n"
                    self.authorized_clients[client_id] = cookie
                
                # For v3 onion services, we need to pass auth cookies directly
                auth_params = {"basic_auth": auth_cookies}
            
            # Create ephemeral hidden service with v3
            if HAS_STEM and self.controller:
                response = self.controller.create_ephemeral_hidden_service(
                    {port: target_port},
                    key_type='NEW',
                    key_content='ED25519-V3',
                    **auth_params
                )
                
                service_id = response.service_id
                self.onion_services[service_id] = "key_data"  # In practice, store the actual key
                
                print(f"v3 Onion service created: {service_id}.onion:{port}")
                if auth_cookies:
                    print(f"Authorized clients: {list(auth_cookies.keys())}")
                
                return f"{service_id}.onion"
            else:
                print("TOR not available, cannot create onion service")
                return None
            
        except Exception as e:
            print(f"Error creating onion service: {e}")
            return None
    
    async def add_authorized_client(self, client_id: str) -> str:
        """
        Add an authorized client for onion service access
        
        Args:
            client_id: Unique identifier for the client
            
        Returns:
            str: Authorization cookie for the client
        """
        cookie = secrets.token_hex(16)
        self.authorized_clients[client_id] = cookie
        return cookie
    
    async def rotate_circuit(self) -> bool:
        """Rotate TOR circuit for enhanced anonymity"""
        if not self.initialized or not HAS_STEM or not self.controller:
            return False
            
        try:
            self.controller.signal(Signal.NEWNYM)
            print("TOR circuit rotated")
            return True
        except Exception as e:
            print(f"Error rotating circuit: {e}")
            return False
    
    async def send_message_through_tor(self, target_onion: str, port: int, 
                                     message: NetworkMessage) -> bool:
        """Send a message through TOR network"""
        # This is a simplified implementation
        # In practice, you would use a SOCKS proxy to route through TOR
        try:
            # For demonstration, we'll just print the message
            print(f"Sending message through TOR to {target_onion}:{port}")
            print(f"Message: {message}")
            return True
        except Exception as e:
            print(f"Error sending message through TOR: {e}")
            return False
    
    def get_network_status(self) -> Dict:
        """Get TOR network status"""
        if not self.initialized or not HAS_STEM or not self.controller:
            return {"status": "not_initialized"}
            
        try:
            info = self.controller.get_info([
                'status/circuit-established',
                'status/enough-dir-info',
                'status/bootstrap-phase'
            ])
            
            return {
                'circuit_established': info.get('status/circuit-established') == '1',
                'enough_dir_info': info.get('status/enough-dir-info') == '1',
                'bootstrap_phase': info.get('status/bootstrap-phase', 'Unknown'),
            }
        except Exception as e:
            print(f"Error getting network status: {e}")
            return {"status": "error"}
    
    async def cleanup(self):
        """Clean up TOR resources"""
        if not self.initialized or not HAS_STEM or not self.controller:
            return
            
        try:
            # Remove all onion services
            for service_id in list(self.onion_services.keys()):
                try:
                    self.controller.remove_ephemeral_hidden_service(service_id)
                except:
                    pass
            
            # Close controller
            if self.controller:
                self.controller.close()
                
            print("TOR gateway cleaned up")
        except Exception as e:
            print(f"Error cleaning up TOR gateway: {e}")


# Example usage
if __name__ == "__main__":
    async def main():
        # Create TOR gateway
        tor = TORGateway()
        
        # Try to initialize
        if await tor.initialize():
            # Create an onion service with client authorization
            authorized_clients = ["client_1", "client_2"]
            onion_address = await tor.create_onion_service(8080, authorized_clients=authorized_clients)
            if onion_address:
                print(f"Created onion service: {onion_address}")
                print(f"Client authorizations: {tor.authorized_clients}")
            
            # Get network status
            status = tor.get_network_status()
            print(f"Network status: {status}")
            
            # Clean up
            await tor.cleanup()
        else:
            print("Failed to initialize TOR gateway")
    
    # Run the example
    asyncio.run(main())