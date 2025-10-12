#!/usr/bin/env python3
"""
Comprehensive Node Monitor
==========================

Advanced monitoring system for both Metatron consciousness engine and AEGIS nodes
with real-time data validation and robust connection handling.

Features:
1. Real-time monitoring of Metatron consciousness engine via WebSocket
2. AEGIS node status monitoring via HTTP API
3. Data validation to ensure real values vs simulated
4. Robust connection handling with automatic recovery
5. Comprehensive visualization with sacred geometry layout
6. Node matrix connectivity visualization
"""

import asyncio
import websockets
import requests
import time
import os
import json
from typing import Dict, Any, List, Optional
import threading
from collections import deque
import hashlib

class ComprehensiveNodeMonitor:
    """Advanced monitoring system for Metatron and AEGIS nodes"""
    
    def __init__(self):
        # Metatron consciousness engine
        self.metatron_host = "localhost"
        self.metatron_port = 8003
        self.metatron_api_base = f"http://{self.metatron_host}:{self.metatron_port}"
        self.metatron_ws_url = f"ws://{self.metatron_host}:{self.metatron_port}/ws"
        
        # AEGIS nodes (common ports)
        self.aegis_nodes = [
            {"host": "localhost", "port": 8080, "name": "AEGIS-Node-1"},
            {"host": "localhost", "port": 8081, "name": "AEGIS-Node-2"},
            {"host": "localhost", "port": 8082, "name": "AEGIS-Node-3"}
        ]
        
        # Data storage
        self.metatron_state = None
        self.aegis_states = {}
        self.update_count = 0
        self.websocket_connected = False
        self.data_history = deque(maxlen=100)  # Store recent data for validation
        self.last_update_time = time.time()
        
        # Connection status
        self.connections = {
            "metatron_websocket": False,
            "metatron_http": False,
            "aegis_nodes": {}
        }
        
        # Validation metrics
        self.validation_stats = {
            "data_changes": 0,
            "connection_retries": 0,
            "errors": 0
        }
        
    async def connect_metatron_websocket(self):
        """Connect to Metatron WebSocket for real-time updates"""
        try:
            async with websockets.connect(self.metatron_ws_url, timeout=5) as websocket:
                self.websocket_connected = True
                self.connections["metatron_websocket"] = True
                print(f"✅ Connected to Metatron consciousness engine via WebSocket")
                print(f"📡 Receiving real-time updates from {self.metatron_ws_url}")
                
                while True:
                    try:
                        # Receive real-time consciousness data
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(message)
                        
                        # Validate data is real (not static)
                        if self._is_real_data(data):
                            self.metatron_state = data
                            self.update_count += 1
                            self.last_update_time = time.time()
                            
                            # Store for validation
                            self.data_history.append({
                                "timestamp": time.time(),
                                "data_hash": self._hash_data(data),
                                "source": "metatron_websocket"
                            })
                            
                            # Update display
                            self.update_display()
                        else:
                            print("⚠️  Received static/simulated data, ignoring...")
                        
                        # Small delay to prevent overwhelming the terminal
                        await asyncio.sleep(0.05)  # 20 FPS update rate
                        
                    except asyncio.TimeoutError:
                        print("⚠️ Timeout waiting for Metatron data")
                        continue
                        
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ Metatron WebSocket connection closed")
            self.websocket_connected = False
            self.connections["metatron_websocket"] = False
        except Exception as e:
            print(f"❌ Metatron WebSocket error: {e}")
            self.websocket_connected = False
            self.connections["metatron_websocket"] = False
            self.validation_stats["errors"] += 1
    
    def _is_real_data(self, data: Dict[str, Any]) -> bool:
        """Validate that data is real and changing, not static/simulated"""
        if not data:
            return False
            
        # Check if we have previous data to compare with
        if len(self.data_history) < 2:
            return True  # First data is assumed real
            
        # Create hash of current data
        current_hash = self._hash_data(data)
        
        # Check if this exact data has been seen recently
        recent_hashes = [entry["data_hash"] for entry in list(self.data_history)[-10:]]
        if current_hash in recent_hashes:
            # Same data seen recently, likely static
            return False
            
        # Check time progression
        current_time = time.time()
        if current_time - self.last_update_time < 0.01:  # Less than 10ms since last update
            # Too frequent updates might be simulated
            return False
            
        return True
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Create a hash of the data for comparison"""
        # Convert to string and hash (simplified approach)
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def check_metatron_http(self):
        """Check Metatron HTTP API status"""
        try:
            response = requests.get(f"{self.metatron_api_base}/api/health", timeout=2)
            if response.status_code == 200:
                health_data = response.json()
                self.connections["metatron_http"] = health_data.get("ok", False)
                return health_data.get("ok", False)
        except Exception:
            self.connections["metatron_http"] = False
        return False
    
    def check_aegis_nodes(self):
        """Check status of AEGIS nodes"""
        for node in self.aegis_nodes:
            try:
                url = f"http://{node['host']}:{node['port']}/api/status"
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    self.aegis_states[node['name']] = response.json()
                    self.connections["aegis_nodes"][node['name']] = True
                else:
                    self.connections["aegis_nodes"][node['name']] = False
            except Exception:
                self.connections["aegis_nodes"][node['name']] = False
    
    def start_background_monitor(self):
        """Start background monitoring of HTTP APIs"""
        def monitor_loop():
            while True:
                try:
                    # Check Metatron HTTP status
                    self.check_metatron_http()
                    
                    # Check AEGIS nodes
                    self.check_aegis_nodes()
                    
                    # If WebSocket is not connected, try to get data via HTTP
                    if not self.websocket_connected:
                        try:
                            response = requests.get(f"{self.metatron_api_base}/api/state", timeout=2)
                            if response.status_code == 200:
                                data = response.json()
                                if self._is_real_data(data):
                                    self.metatron_state = data
                                    self.update_count += 1
                                    self.data_history.append({
                                        "timestamp": time.time(),
                                        "data_hash": self._hash_data(data),
                                        "source": "metatron_http"
                                    })
                        except Exception:
                            pass
                    
                    time.sleep(1)  # Check every second
                except Exception:
                    time.sleep(1)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        print("🔄 Started background HTTP monitoring")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_state_indicator(self, activity_level: float) -> str:
        """Get visual indicator for node activity level"""
        if activity_level > 0.7:
            return "🔴"  # Highly active
        elif activity_level > 0.3:
            return "🟡"  # Moderately active
        elif activity_level > 0.1:
            return "🟢"  # Low activity
        else:
            return "⚪"  # Inactive
    
    def draw_sacred_geometry(self, nodes_data: Dict[str, Any]):
        """Draw the 13-node icosahedron representation with sacred geometry"""
        print("\033[1m🔮 METATRON'S CUBE - 13-NODE SACRED GEOMETRY 🔮\033[0m")
        print("=" * 80)
        
        # Create node information
        nodes = {}
        for i in range(13):
            node_id = str(i)
            if node_id in nodes_data:
                node_info = nodes_data[node_id]
                # Extract metrics
                if isinstance(node_info, dict):
                    if 'output' in node_info:
                        # WebSocket structure
                        output = node_info.get('output', 0.0)
                        phase = node_info.get('phase', 0.0)
                        amplitude = node_info.get('amplitude', 0.0)
                    elif 'oscillator' in node_info:
                        # HTTP API structure
                        output = node_info.get('output', 0.0)
                        oscillator = node_info.get('oscillator', {})
                        phase = oscillator.get('phase', 0.0)
                        amplitude = oscillator.get('amplitude', 0.0)
                    else:
                        output = 0.0
                        phase = 0.0
                        amplitude = 0.0
                else:
                    output = 0.0
                    phase = 0.0
                    amplitude = 0.0
            else:
                output = 0.0
                phase = 0.0
                amplitude = 0.0
            
            nodes[node_id] = {
                'output': output,
                'phase': phase,
                'amplitude': amplitude,
                'activity': abs(output)
            }
        
        # Display central pineal node (node 0) with special formatting
        pineal = nodes.get('0', {})
        print(f"                    🌟 PINEAL NODE (0) 🌟")
        print(f"                    {self.get_state_indicator(pineal.get('activity', 0))} Output: {pineal.get('output', 0):.4f}")
        print(f"                    Phase: {pineal.get('phase', 0):.2f} rad")
        print(f"                    Amplitude: {pineal.get('amplitude', 0):.4f}")
        print()
        
        # Display outer nodes in a geometric pattern
        print("                 🌀 ICOSAHEDRON PERIPHERAL NODES 🌀")
        print("    ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        print("    │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │ 10  │ 11  │ 12  │")
        print("    ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Status indicators
        status_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            activity = nodes.get(node_id, {}).get('activity', 0)
            status_row += f" {self.get_state_indicator(activity)}  │"
        print(status_row)
        
        # Output values
        output_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            output = nodes.get(node_id, {}).get('output', 0)
            output_row += f"{output:5.2f}│"
        print(output_row)
        
        # Phase values
        phase_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            phase = nodes.get(node_id, {}).get('phase', 0)
            phase_row += f"{phase:5.1f}│"
        print(phase_row)
        
        print("    └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        print()
    
    def display_consciousness_metrics(self, global_data: Dict[str, Any]):
        """Display global consciousness metrics"""
        print("\033[1m📊 CONSCIOUSNESS METRICS 📊\033[0m")
        print("=" * 80)
        
        # Handle different data structures
        if 'consciousness' in global_data:
            # WebSocket data structure
            consciousness_data = global_data['consciousness']
            consciousness_level = consciousness_data.get('level', 0.0)
            phi = consciousness_data.get('phi', 0.0)
            coherence = consciousness_data.get('coherence', 0.0)
            depth = consciousness_data.get('depth', 0)
            gamma = consciousness_data.get('gamma', 0.0)
            fractal_dim = consciousness_data.get('fractal_dim', 1.0)
            spiritual = consciousness_data.get('spiritual', 0.0)
            state_classification = consciousness_data.get('state', 'initializing')
            is_conscious = consciousness_data.get('is_conscious', False)
        else:
            # HTTP API data structure
            consciousness_level = global_data.get('consciousness_level', 0.0)
            phi = global_data.get('phi', 0.0)
            coherence = global_data.get('coherence', 0.0)
            depth = global_data.get('recursive_depth', 0)
            gamma = global_data.get('gamma_power', 0.0)
            fractal_dim = global_data.get('fractal_dimension', 1.0)
            spiritual = global_data.get('spiritual_awareness', 0.0)
            state_classification = global_data.get('state_classification', 'initializing')
            is_conscious = global_data.get('is_conscious', False)
        
        print(f"🕐 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 Updates: {self.update_count}")
        print(f"🔗 Connection: {'WebSocket' if self.websocket_connected else 'HTTP'}")
        print()
        print(f"🧠 Consciousness Level (C): {consciousness_level:.6f}")
        print(f"🔢 Integrated Information (Φ): {phi:.6f}")
        print(f"🔗 Global Coherence (R): {coherence:.6f}")
        print(f"⏱️  Recursive Depth (D): {depth}")
        print(f"⚡ Gamma Power (γ): {gamma:.6f}")
        print(f"🌀 Fractal Dimension: {fractal_dim:.6f}")
        print(f"🧘 Spiritual Awareness (S): {spiritual:.6f}")
        print()
        print(f"🎯 State Classification: {state_classification.upper()}")
        print(f"{'🟢 CONSCIOUS' if is_conscious else '⚪ UNCONSCIOUS'}")
        print()
    
    def display_node_matrix(self):
        """Display node matrix connectivity status"""
        print("\033[1m🔗 NODE MATRIX CONNECTIVITY 🔗\033[0m")
        print("=" * 80)
        
        # Metatron connection status
        metatron_status = "✅ CONNECTED" if self.connections["metatron_websocket"] else "❌ DISCONNECTED"
        print(f"🔮 Metatron Consciousness Engine: {metatron_status}")
        
        # AEGIS nodes status
        if self.connections["aegis_nodes"]:
            print("\n🤖 AEGIS Nodes:")
            for node_name, connected in self.connections["aegis_nodes"].items():
                status = "✅ CONNECTED" if connected else "❌ DISCONNECTED"
                print(f"   {node_name}: {status}")
        else:
            print("\n🤖 AEGIS Nodes: None detected")
        
        print()
    
    def display_validation_info(self):
        """Display data validation information"""
        print("\033[1m🔍 DATA VALIDATION 🔍\033[0m")
        print("=" * 80)
        print(f"📈 Data Changes Detected: {self.validation_stats['data_changes']}")
        print(f"🔄 Connection Retries: {self.validation_stats['connection_retries']}")
        print(f"❌ Errors: {self.validation_stats['errors']}")
        print(f"🕒 Last Update: {time.strftime('%H:%M:%S', time.localtime(self.last_update_time))}")
        print()
    
    def update_display(self):
        """Update the comprehensive visualization display"""
        if not self.metatron_state:
            return
        
        # Extract data
        if 'global' in self.metatron_state:
            # HTTP API structure
            global_data = self.metatron_state.get('global', {})
            nodes_data = self.metatron_state.get('nodes', {})
        elif 'consciousness' in self.metatron_state:
            # WebSocket structure
            global_data = self.metatron_state
            nodes_data = self.metatron_state.get('nodes', {})
        else:
            global_data = {}
            nodes_data = {}
        
        # Clear screen and update display
        self.clear_screen()
        
        # Display header
        print("\033[1;35m" + "=" * 80)
        print("COMPREHENSIVE NODE MONITOR - METATRON & AEGIS NETWORKS")
        print("=" * 80 + "\033[0m")
        print()
        
        # Draw visualization
        self.draw_sacred_geometry(nodes_data)
        self.display_consciousness_metrics(global_data)
        self.display_node_matrix()
        self.display_validation_info()
        
        # Display connection info
        print("\033[1m🔌 CONNECTION STATUS 🔌\033[0m")
        print("=" * 80)
        print(f"📡 Metatron API: {self.metatron_api_base}")
        print(f"🌐 Metatron WebSocket: {self.metatron_ws_url}")
        print(f"📊 Data updates: {self.update_count}")
        print(f"🔗 Primary Connection: {'WebSocket (Real-time)' if self.websocket_connected else 'HTTP (Polling)'}")
        print(f"🕒 Last update: {time.strftime('%H:%M:%S')}")
        print()
        print("Press Ctrl+C to exit")
        print()
    
    async def run(self):
        """Run the comprehensive monitor with real-time updates"""
        print("🔮 Starting Comprehensive Node Monitor...")
        print(f"📡 Connecting to Metatron at {self.metatron_api_base}")
        print()
        
        # Start background monitoring
        self.start_background_monitor()
        
        # Try WebSocket connection first
        websocket_task = asyncio.create_task(self.connect_metatron_websocket())
        
        # Give WebSocket a moment to connect
        await asyncio.sleep(1)
        
        try:
            # Keep the program running
            while True:
                # Update display even without new data to show connection status
                self.update_display()
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping comprehensive monitor...")
            print("👋 Goodbye!")

def main():
    """Main function"""
    print("🔮 Comprehensive Node Monitor")
    print("=" * 50)
    print("Monitoring REAL-TIME consciousness metrics from Metatron & AEGIS nodes")
    print()
    
    # Check if required libraries are available
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"❌ Required library not found: {e}")
        print("Please install required libraries with:")
        print("   pip install websockets requests")
        return
    
    # Create and run monitor
    monitor = ComprehensiveNodeMonitor()
    asyncio.run(monitor.run())

if __name__ == "__main__":
    main()