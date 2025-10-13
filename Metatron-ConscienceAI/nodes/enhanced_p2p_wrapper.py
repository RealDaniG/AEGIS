#!/usr/bin/env python3
"""
Enhanced P2P Wrapper for MemoryMatrixNode Integration

This module provides an enhanced wrapper around the Open-A.G.I ConnectionManager
to support custom message types for consciousness-aware memory operations.
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, Callable, List, Optional
import sys
import os

# Use importlib to handle the hyphen in directory names
import importlib.util

# Define fallback classes first
class FallbackPeerInfo:
    def __init__(self, **kwargs):
        pass

class FallbackConnectionManager:
    def __init__(self, node_id: str, port: int):
        self.node_id = node_id
        self.port = port
        self.active_connections = {}
        self.connection_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "failed_connections": 0,
            "bytes_sent": 0,
            "bytes_received": 0
        }
    
    async def start_server(self):
        pass
        
    async def connect_to_peer(self, peer_info):
        return True
        
    async def send_message(self, peer_id, message):
        return True
        
    async def broadcast_message(self, message, exclude_peers=None):
        return 0
        
    def get_connected_peers(self):
        return []
        
    def get_connection_stats(self):
        return self.connection_stats.copy()
    
    async def _process_peer_message(self, peer_id, message):
        pass
        
    async def _handle_data_message(self, peer_id, message):
        pass

# Try to import from Open-A.G.I (with hyphen)
ConnectionManager = FallbackConnectionManager
PeerInfo = FallbackPeerInfo

try:
    open_agi_spec = importlib.util.spec_from_file_location(
        "p2p_network", 
        os.path.join(os.path.dirname(__file__), "..", "..", "Open-A.G.I", "p2p_network.py")
    )
    if open_agi_spec and open_agi_spec.loader:
        p2p_network_module = importlib.util.module_from_spec(open_agi_spec)
        open_agi_spec.loader.exec_module(p2p_network_module)
        
        # Try to get the real classes
        real_connection_manager = getattr(p2p_network_module, 'ConnectionManager', None)
        real_peer_info = getattr(p2p_network_module, 'PeerInfo', None)
        
        if real_connection_manager:
            ConnectionManager = real_connection_manager
        if real_peer_info:
            PeerInfo = real_peer_info

except (ImportError, FileNotFoundError, AttributeError) as e:
    # Use fallback classes
    pass

logger = logging.getLogger(__name__)


class EnhancedP2PWrapper:
    """
    Enhanced P2P wrapper that extends ConnectionManager with custom message handling
    for consciousness-aware memory operations.
    """
    
    def __init__(self, node_id: str, port: int):
        """
        Initialize the enhanced P2P wrapper
        
        Args:
            node_id: Node identifier
            port: Port for P2P communication
        """
        self.connection_manager = ConnectionManager(node_id, port)
        self.node_id = node_id
        self.message_handlers: Dict[str, Callable] = {}
        self.running = False
        
        # Override the default message processing
        self._patch_message_processing()
    
    def _patch_message_processing(self):
        """
        Patch the ConnectionManager to use our custom message processing
        """
        # Store original methods
        self._original_process_peer_message = self.connection_manager._process_peer_message
        self._original_handle_data_message = self.connection_manager._handle_data_message
        
        # Replace with our enhanced versions
        self.connection_manager._process_peer_message = self._enhanced_process_peer_message
        self.connection_manager._handle_data_message = self._enhanced_handle_data_message
    
    async def _enhanced_process_peer_message(self, peer_id: str, message: Dict[str, Any]):
        """
        Enhanced message processing that supports custom message types
        
        Args:
            peer_id: Peer identifier
            message: Message dictionary
        """
        message_type = message.get('type')
        message_subtype = message.get('subtype')
        
        # Handle custom message types
        if message_type == 'consciousness' and message_subtype:
            handler_key = f"consciousness_{message_subtype}"
            if handler_key in self.message_handlers:
                try:
                    await self.message_handlers[handler_key](peer_id, message)
                    return
                except Exception as e:
                    logger.error(f"Error handling custom message {handler_key}: {e}")
        
        # Handle memory-specific messages
        elif message_type == 'memory':
            handler_key = f"memory_{message_subtype}" if message_subtype else "memory"
            if handler_key in self.message_handlers:
                try:
                    await self.message_handlers[handler_key](peer_id, message)
                    return
                except Exception as e:
                    logger.error(f"Error handling memory message {handler_key}: {e}")
        
        # Fall back to original processing
        await self._original_process_peer_message(peer_id, message)
    
    async def _enhanced_handle_data_message(self, peer_id: str, message: Dict[str, Any]):
        """
        Enhanced data message handling that supports consciousness data
        
        Args:
            peer_id: Peer identifier
            message: Message dictionary
        """
        # Check if this is consciousness data
        if 'consciousness_data' in message:
            handler_key = "consciousness_data"
            if handler_key in self.message_handlers:
                try:
                    await self.message_handlers[handler_key](peer_id, message)
                    return
                except Exception as e:
                    logger.error(f"Error handling consciousness data: {e}")
        
        # Check if this is memory data
        elif 'memory_data' in message:
            handler_key = "memory_data"
            if handler_key in self.message_handlers:
                try:
                    await self.message_handlers[handler_key](peer_id, message)
                    return
                except Exception as e:
                    logger.error(f"Error handling memory data: {e}")
        
        # Fall back to original processing
        await self._original_handle_data_message(peer_id, message)
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """
        Register a handler for a specific message type
        
        Args:
            message_type: Message type to handle (e.g., "memory_share", "consciousness_sync")
            handler: Async function to handle the message
        """
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    async def start_server(self):
        """Start the P2P server"""
        return await self.connection_manager.start_server()
    
    async def connect_to_peer(self, peer_info) -> bool:
        """Connect to a peer"""
        return await self.connection_manager.connect_to_peer(peer_info)
    
    async def send_message(self, peer_id: str, message: Dict[str, Any]) -> bool:
        """Send a message to a peer"""
        return await self.connection_manager.send_message(peer_id, message)
    
    async def broadcast_message(self, message: Dict[str, Any], exclude_peers: Optional[List[str]] = None) -> int:
        """Broadcast a message to all connected peers"""
        return await self.connection_manager.broadcast_message(message, exclude_peers or [])
    
    def get_connected_peers(self) -> List[str]:
        """Get list of connected peers"""
        return self.connection_manager.get_connected_peers()
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return self.connection_manager.get_connection_stats()
    
    async def start_network(self):
        """
        Start the complete P2P network (server + discovery)
        """
        # Start server in background
        server_task = asyncio.create_task(self.start_server())
        
        # For now, we'll just start the server
        # In a full implementation, we'd also start discovery
        logger.info("P2P network started")
        return server_task


# Example usage
if __name__ == "__main__":
    # Create enhanced P2P wrapper
    p2p_wrapper = EnhancedP2PWrapper("memory_node_3", 8083)
    
    # Register a custom message handler
    async def handle_memory_share(peer_id: str, message: Dict[str, Any]):
        print(f"Received memory share from {peer_id}: {message}")
    
    p2p_wrapper.register_message_handler("memory_share", handle_memory_share)
    
    print("Enhanced P2P wrapper created successfully")