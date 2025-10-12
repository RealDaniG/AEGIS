"""
NAT Traversal Module for AEGIS-Conscience Network
Implementation of STUN/TURN client for peer discovery behind firewalls
"""

import asyncio
import socket
import struct
import random
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from enum import Enum


class STUNMessageType(Enum):
    """STUN message types"""
    BINDING_REQUEST = 0x0001
    BINDING_RESPONSE = 0x0101
    BINDING_ERROR_RESPONSE = 0x0111


class STUNAttributeType(Enum):
    """STUN attribute types"""
    MAPPED_ADDRESS = 0x0001
    USERNAME = 0x0006
    MESSAGE_INTEGRITY = 0x0008
    ERROR_CODE = 0x0009
    UNKNOWN_ATTRIBUTES = 0x000A
    REALM = 0x0014
    NONCE = 0x0015
    XOR_MAPPED_ADDRESS = 0x0020


@dataclass
class STUNBinding:
    """STUN binding information"""
    public_ip: str
    public_port: int
    local_ip: str
    local_port: int
    server_ip: str
    server_port: int


class STUNClient:
    """STUN client for NAT traversal"""
    
    def __init__(self):
        self.stun_servers = [
            ("stun.l.google.com", 19302),
            ("stun1.l.google.com", 19302),
            ("stun.stunprotocol.org", 3478),
            ("stun.voiparound.com", 3478),
        ]
        self.bindings: Dict[str, STUNBinding] = {}
    
    async def discover_public_address(self) -> Optional[STUNBinding]:
        """
        Discover public IP and port using STUN
        
        Returns:
            STUNBinding: Public address information or None if failed
        """
        for server_ip, server_port in self.stun_servers:
            try:
                binding = await self._send_binding_request(server_ip, server_port)
                if binding:
                    self.bindings[f"{server_ip}:{server_port}"] = binding
                    return binding
            except Exception as e:
                print(f"STUN request to {server_ip}:{server_port} failed: {e}")
                continue
        
        return None
    
    async def _send_binding_request(self, server_ip: str, server_port: int) -> Optional[STUNBinding]:
        """
        Send STUN binding request to server
        
        Args:
            server_ip: STUN server IP
            server_port: STUN server port
            
        Returns:
            STUNBinding: Binding information or None if failed
        """
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)  # 5 second timeout
        
        try:
            # Get local address
            local_ip = self._get_local_ip()
            local_port = random.randint(10000, 60000)
            
            # Bind to local address
            sock.bind((local_ip, local_port))
            
            # Create STUN binding request
            transaction_id = self._generate_transaction_id()
            message = self._create_binding_request(transaction_id)
            
            # Send request
            sock.sendto(message, (server_ip, server_port))
            
            # Receive response
            data, addr = sock.recvfrom(1024)
            
            # Parse response
            public_ip, public_port = self._parse_binding_response(data, transaction_id)
            
            if public_ip and public_port:
                return STUNBinding(
                    public_ip=public_ip,
                    public_port=public_port,
                    local_ip=local_ip,
                    local_port=local_port,
                    server_ip=server_ip,
                    server_port=server_port
                )
            
        except Exception as e:
            print(f"STUN binding request failed: {e}")
        finally:
            sock.close()
        
        return None
    
    def _create_binding_request(self, transaction_id: bytes) -> bytes:
        """
        Create STUN binding request message
        
        Args:
            transaction_id: 12-byte transaction ID
            
        Returns:
            bytes: STUN message
        """
        # STUN header: 20 bytes
        # - Message Type (2 bytes): BINDING_REQUEST
        # - Message Length (2 bytes): 0 (no attributes)
        # - Magic Cookie (4 bytes): 0x2112A442
        # - Transaction ID (12 bytes)
        
        message_type = struct.pack('!H', STUNMessageType.BINDING_REQUEST.value)
        message_length = struct.pack('!H', 0)  # No attributes
        magic_cookie = struct.pack('!I', 0x2112A442)
        
        return message_type + message_length + magic_cookie + transaction_id
    
    def _parse_binding_response(self, data: bytes, expected_transaction_id: bytes) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse STUN binding response
        
        Args:
            data: Response data
            expected_transaction_id: Expected transaction ID
            
        Returns:
            Tuple[str, int]: Public IP and port, or (None, None) if failed
        """
        if len(data) < 20:
            return None, None
        
        # Parse header
        message_type, message_length, magic_cookie = struct.unpack('!HHI', data[:8])
        transaction_id = data[8:20]
        
        # Check if it's a binding response
        if message_type != STUNMessageType.BINDING_RESPONSE.value:
            return None, None
        
        # Check transaction ID
        if transaction_id != expected_transaction_id:
            return None, None
        
        # Parse attributes
        offset = 20
        public_ip = None
        public_port = None
        
        while offset < len(data):
            if offset + 4 > len(data):
                break
                
            attr_type, attr_length = struct.unpack('!HH', data[offset:offset+4])
            offset += 4
            
            if offset + attr_length > len(data):
                break
            
            attr_value = data[offset:offset+attr_length]
            offset += attr_length
            
            # Pad to 4-byte boundary
            offset += (4 - (attr_length % 4)) % 4
            
            if attr_type == STUNAttributeType.MAPPED_ADDRESS.value:
                # Parse MAPPED-ADDRESS attribute
                if len(attr_value) >= 8:
                    family = struct.unpack('!H', attr_value[2:4])[0]
                    port = struct.unpack('!H', attr_value[4:6])[0]
                    if family == 1:  # IPv4
                        ip_bytes = attr_value[6:10]
                        public_ip = socket.inet_ntoa(ip_bytes)
                        public_port = port
                        break
        
        return public_ip, public_port
    
    def _generate_transaction_id(self) -> bytes:
        """Generate random 12-byte transaction ID"""
        return bytes([random.randint(0, 255) for _ in range(12)])
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            # Connect to external server to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"


class TURNClient:
    """TURN client for relay-based NAT traversal"""
    
    def __init__(self, turn_server: str, turn_port: int, username: str, password: str):
        self.turn_server = turn_server
        self.turn_port = turn_port
        self.username = username
        self.password = password
        self.allocation = None
    
    async def allocate_relay_address(self) -> Optional[Tuple[str, int]]:
        """
        Allocate a relay address on TURN server
        
        Returns:
            Tuple[str, int]: Relay IP and port, or None if failed
        """
        # This is a simplified implementation
        # In practice, you would need to implement the full TURN protocol
        print(f"Allocating relay address on {self.turn_server}:{self.turn_port}")
        
        # For demonstration, return a mock relay address
        return ("192.0.2.1", 50000)
    
    async def create_permission(self, peer_ip: str, peer_port: int) -> bool:
        """
        Create permission for peer to send data through relay
        
        Args:
            peer_ip: Peer IP address
            peer_port: Peer port
            
        Returns:
            bool: True if successful
        """
        # This is a simplified implementation
        print(f"Creating permission for {peer_ip}:{peer_port}")
        return True
    
    async def send_data_through_relay(self, data: bytes, peer_ip: str, peer_port: int) -> bool:
        """
        Send data through TURN relay to peer
        
        Args:
            data: Data to send
            peer_ip: Peer IP address
            peer_port: Peer port
            
        Returns:
            bool: True if successful
        """
        # This is a simplified implementation
        print(f"Sending {len(data)} bytes through relay to {peer_ip}:{peer_port}")
        return True


class NATTraversalManager:
    """Manager for NAT traversal using STUN/TURN"""
    
    def __init__(self):
        self.stun_client = STUNClient()
        self.turn_clients: Dict[str, TURNClient] = {}
        self.public_binding: Optional[STUNBinding] = None
    
    async def discover_public_address(self) -> bool:
        """
        Discover public address using STUN
        
        Returns:
            bool: True if successful
        """
        print("Discovering public address using STUN...")
        self.public_binding = await self.stun_client.discover_public_address()
        
        if self.public_binding:
            print(f"Public address discovered: {self.public_binding.public_ip}:{self.public_binding.public_port}")
            return True
        else:
            print("Failed to discover public address using STUN")
            return False
    
    def add_turn_server(self, server_id: str, turn_server: str, turn_port: int, 
                       username: str, password: str):
        """
        Add TURN server for relay-based NAT traversal
        
        Args:
            server_id: Unique identifier for the TURN server
            turn_server: TURN server address
            turn_port: TURN server port
            username: TURN username
            password: TURN password
        """
        self.turn_clients[server_id] = TURNClient(turn_server, turn_port, username, password)
    
    async def get_relay_address(self, server_id: str) -> Optional[Tuple[str, int]]:
        """
        Get relay address from TURN server
        
        Args:
            server_id: TURN server identifier
            
        Returns:
            Tuple[str, int]: Relay IP and port, or None if failed
        """
        if server_id in self.turn_clients:
            return await self.turn_clients[server_id].allocate_relay_address()
        return None
    
    def get_public_binding(self) -> Optional[STUNBinding]:
        """
        Get current public binding
        
        Returns:
            STUNBinding: Current public binding or None
        """
        return self.public_binding


# Example usage
async def main():
    """Example usage of NAT traversal components"""
    print("=== NAT Traversal Demo ===")
    
    # Create NAT traversal manager
    nat_manager = NATTraversalManager()
    
    # Discover public address
    success = await nat_manager.discover_public_address()
    
    if success:
        binding = nat_manager.get_public_binding()
        if binding:
            print(f"Local address: {binding.local_ip}:{binding.local_port}")
            print(f"Public address: {binding.public_ip}:{binding.public_port}")
    else:
        print("STUN discovery failed, adding TURN server as fallback")
        
        # Add TURN server
        nat_manager.add_turn_server(
            "fallback", 
            "turn.example.com", 
            3478, 
            "username", 
            "password"
        )
        
        # Get relay address
        relay_addr = await nat_manager.get_relay_address("fallback")
        if relay_addr:
            print(f"Relay address: {relay_addr[0]}:{relay_addr[1]}")
        else:
            print("Failed to get relay address")


if __name__ == "__main__":
    asyncio.run(main())