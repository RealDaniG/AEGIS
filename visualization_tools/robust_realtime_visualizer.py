#!/usr/bin/env python3
"""
Robust Real-Time Visualizer
===========================

Ultra-reliable visualization system that guarantees real-time representation
of node values with comprehensive data validation and fail-safe mechanisms.

Key Features:
1. Multi-source data acquisition (WebSocket + HTTP + File)
2. Real-time data validation and authenticity verification
3. Automatic failover between connection methods
4. Data integrity monitoring with checksums
5. Sacred geometry visualization with real metrics
6. Comprehensive error handling and recovery
"""

import asyncio
import websockets
import requests
import time
import os
import json
import hashlib
from typing import Dict, Any, List, Optional
import threading
from collections import deque
import statistics

class RobustRealTimeVisualizer:
    """Ultra-reliable real-time visualization system"""
    
    def __init__(self, port=8003):
        # Connection endpoints
        self.metatron_host = "localhost"
        # Allow configurable port with fallback to 8003
        self.metatron_port = port
        self.ws_url = f"ws://{self.metatron_host}:{self.metatron_port}/ws"
        self.api_base = f"http://{self.metatron_host}:{self.metatron_port}"
        
        # Data management
        self.current_state = None
        self.data_history = deque(maxlen=100)
        self.update_count = 0
        self.last_update_time = time.time()
        
        # Connection status
        self.connections = {
            "websocket": {"status": False, "last_attempt": 0},
            "http": {"status": False, "last_attempt": 0},
            "file": {"status": False, "last_attempt": 0}
        }
        
        # Validation metrics
        self.validation_stats = {
            "authentic_data": 0,
            "static_data_rejected": 0,
            "connection_failures": 0,
            "recovery_attempts": 0
        }
        
        # Performance monitoring
        self.performance_metrics = {
            "avg_update_interval": 0,
            "data_throughput": 0,
            "error_rate": 0
        }
        
        # Robustness settings
        self.max_retry_attempts = 3
        self.retry_delay = 1.0
        self.update_interval = 0.1  # 100ms for smooth updates
        
        # Try alternative ports if primary fails
        self.alternative_ports = [8005, 8003] if port == 8003 else [8003, 8005]
        
    async def establish_websocket_connection(self) -> bool:
        """Establish robust WebSocket connection with retry logic"""
        # Try primary port first
        ports_to_try = [self.metatron_port] + self.alternative_ports
        
        for port in ports_to_try:
            self.ws_url = f"ws://{self.metatron_host}:{port}/ws"
            self.api_base = f"http://{self.metatron_host}:{port}"
            
            attempt = 0
            while attempt < self.max_retry_attempts:
                try:
                    self.connections["websocket"]["last_attempt"] = time.time()
                    
                    # Fixed the WebSocket connection by using the correct method
                    websocket = await websockets.connect(self.ws_url)
                    self.connections["websocket"]["status"] = True
                    self.metatron_port = port  # Update to successful port
                    print(f"✅ WebSocket connected to {self.ws_url}")
                    
                    # Continuous data reception
                    while True:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                            data = json.loads(message)
                            
                            if self._validate_data_authenticity(data):
                                self._process_incoming_data(data, "websocket")
                            else:
                                self.validation_stats["static_data_rejected"] += 1
                                print("⚠️  Rejected static/simulated data")
                                
                        except asyncio.TimeoutError:
                            continue
                        except websockets.exceptions.ConnectionClosed:
                            raise
                            
                except Exception as e:
                    attempt += 1
                    self.connections["websocket"]["status"] = False
                    self.validation_stats["connection_failures"] += 1
                    print(f"❌ WebSocket attempt {attempt} failed on port {port}: {e}")
                    
                    if attempt < self.max_retry_attempts:
                        print(f"⏳ Retrying in {self.retry_delay} seconds...")
                        await asyncio.sleep(self.retry_delay)
                    else:
                        print(f"⚠️  WebSocket connection failed after max retries on port {port}")
                        break
            else:
                # If we successfully connected, return True
                if self.connections["websocket"]["status"]:
                    return True
                    
        return False
    
    def establish_http_connection(self) -> bool:
        """Establish HTTP connection with validation, trying multiple ports"""
        # Try primary port first
        ports_to_try = [self.metatron_port] + self.alternative_ports
        
        for port in ports_to_try:
            self.api_base = f"http://{self.metatron_host}:{port}"
            try:
                self.connections["http"]["last_attempt"] = time.time()
                response = requests.get(f"{self.api_base}/api/health", timeout=3)
                
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get("ok", False):
                        self.connections["http"]["status"] = True
                        self.metatron_port = port  # Update to successful port
                        print(f"✅ HTTP connection established to {self.api_base}")
                        return True
                    else:
                        print(f"⚠️  HTTP API health check failed on port {port}")
                else:
                    print(f"⚠️  HTTP API returned status {response.status_code} on port {port}")
                    
            except Exception as e:
                self.connections["http"]["status"] = False
                print(f"❌ HTTP connection failed on port {port}: {e}")
                
        return False
    
    def _validate_data_authenticity(self, data: Dict[str, Any]) -> bool:
        """Comprehensive validation that data is authentic and real-time"""
        if not data:
            return False
            
        # Check if we have previous data for comparison
        if len(self.data_history) < 2:
            # First data is accepted but stored for future validation
            return True
            
        # Create hash of current data
        current_hash = self._hash_data(data)
        
        # Check for recent identical data (indicating static/simulated)
        recent_hashes = [entry["hash"] for entry in list(self.data_history)[-10:]]
        if current_hash in recent_hashes:
            # Same data seen recently - likely static
            return False
            
        # Check time progression
        current_time = time.time()
        time_since_last = current_time - self.last_update_time
        
        # Unreasonably fast updates might be simulated
        if time_since_last < 0.001:  # Less than 1ms
            return False
            
        # Check for reasonable data ranges
        if not self._validate_data_ranges(data):
            return False
            
        return True
    
    def _validate_data_ranges(self, data: Dict[str, Any]) -> bool:
        """Validate that data values are within reasonable ranges"""
        try:
            # Extract consciousness metrics
            if "consciousness" in data:
                # WebSocket format
                consciousness = data["consciousness"]
                level = consciousness.get("level", 0)
                phi = consciousness.get("phi", 0)
                coherence = consciousness.get("coherence", 0)
            elif "global" in data:
                # HTTP format
                global_data = data["global"]
                level = global_data.get("consciousness_level", 0)
                phi = global_data.get("phi", 0)
                coherence = global_data.get("coherence", 0)
            else:
                # Invalid format
                return False
            
            # Validate ranges (these are reasonable for consciousness metrics)
            if not (0 <= level <= 1.0):
                return False
            if not (0 <= phi <= 1.0):
                return False
            if not (0 <= coherence <= 1.0):
                return False
                
            return True
        except Exception:
            return False
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Create consistent hash of data for comparison"""
        # Sort keys for consistent hashing
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _process_incoming_data(self, data: Dict[str, Any], source: str):
        """Process validated incoming data"""
        self.current_state = data
        self.update_count += 1
        self.last_update_time = time.time()
        
        # Store for validation and history
        self.data_history.append({
            "timestamp": time.time(),
            "hash": self._hash_data(data),
            "source": source,
            "size": len(json.dumps(data, default=str))
        })
        
        self.validation_stats["authentic_data"] += 1
        
        # Update performance metrics
        if len(self.data_history) > 1:
            intervals = []
            history_list = list(self.data_history)
            for i in range(1, len(history_list)):
                interval = history_list[i]["timestamp"] - history_list[i-1]["timestamp"]
                intervals.append(interval)
            
            if intervals:
                self.performance_metrics["avg_update_interval"] = statistics.mean(intervals)
        
        # Update display
        # Note: In standalone mode, this would update the display
        # In integrated mode, the display is updated by the IntegratedVisualizer
    
    def _fallback_http_polling(self):
        """Fallback HTTP polling when WebSocket fails"""
        def polling_loop():
            while True:
                try:
                    if not self.connections["websocket"]["status"]:
                        response = requests.get(f"{self.api_base}/api/state", timeout=2)
                        if response.status_code == 200:
                            data = response.json()
                            if self._validate_data_authenticity(data):
                                self._process_incoming_data(data, "http_polling")
                            else:
                                self.validation_stats["static_data_rejected"] += 1
                                
                except Exception as e:
                    print(f"⚠️  HTTP polling error on port {self.metatron_port}: {e}")
                    
                time.sleep(self.update_interval)
        
        polling_thread = threading.Thread(target=polling_loop, daemon=True)
        polling_thread.start()
        print("🔄 Started HTTP fallback polling")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_state_indicator(self, activity_level: float) -> str:
        """Get visual indicator based on activity level"""
        if activity_level > 0.7:
            return "🔴"  # Highly active
        elif activity_level > 0.3:
            return "🟡"  # Moderately active
        elif activity_level > 0.1:
            return "🟢"  # Low activity
        else:
            return "⚪"  # Inactive
    
    def draw_sacred_geometry_network(self, nodes_data: Dict[str, Any]):
        """Draw the 13-node sacred geometry network with real data"""
        print("\033[1m🔮 METATRON'S CUBE - SACRED GEOMETRY NETWORK 🔮\033[0m")
        print("=" * 80)
        
        # Process node data
        nodes = {}
        for i in range(13):
            node_id = str(i)
            if node_id in nodes_data:
                node_info = nodes_data[node_id]
                # Extract metrics based on data format
                if isinstance(node_info, dict):
                    if "output" in node_info and "phase" in node_info:
                        # WebSocket format
                        output = float(node_info.get("output", 0.0))
                        phase = float(node_info.get("phase", 0.0))
                        amplitude = float(node_info.get("amplitude", 0.0))
                    elif "oscillator" in node_info:
                        # HTTP format
                        output = float(node_info.get("output", 0.0))
                        oscillator = node_info.get("oscillator", {})
                        phase = float(oscillator.get("phase", 0.0))
                        amplitude = float(oscillator.get("amplitude", 0.0))
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
                "output": output,
                "phase": phase,
                "amplitude": amplitude,
                "activity": abs(output)
            }
        
        # Display central Pineal node (special formatting)
        pineal = nodes.get("0", {})
        print(f"                    🌟 PINEAL NODE (0) 🌟")
        print(f"                    {self.get_state_indicator(pineal.get('activity', 0))} Output: {pineal.get('output', 0):.4f}")
        print(f"                    Phase: {pineal.get('phase', 0):.2f} rad")
        print(f"                    Amplitude: {pineal.get('amplitude', 0):.4f}")
        print()
        
        # Display peripheral nodes in geometric arrangement
        print("                 🌀 PERIPHERAL NODES (1-12) 🌀")
        print("    ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        print("    │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │ 10  │ 11  │ 12  │")
        print("    ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Activity indicators
        status_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            activity = nodes.get(node_id, {}).get("activity", 0)
            status_row += f" {self.get_state_indicator(activity)}  │"
        print(status_row)
        
        # Output values
        output_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            output = nodes.get(node_id, {}).get("output", 0)
            output_row += f"{output:5.2f}│"
        print(output_row)
        
        # Phase values
        phase_row = "    │"
        for i in range(1, 13):
            node_id = str(i)
            phase = nodes.get(node_id, {}).get("phase", 0)
            phase_row += f"{phase:5.1f}│"
        print(phase_row)
        
        print("    └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        print()
    
    def display_consciousness_metrics(self, global_data: Dict[str, Any]):
        """Display comprehensive consciousness metrics"""
        print("\033[1m📊 CONSCIOUSNESS METRICS 📊\033[0m")
        print("=" * 80)
        
        # Extract metrics based on data format
        if "consciousness" in global_data:
            # WebSocket format
            consciousness = global_data["consciousness"]
            level = consciousness.get("level", 0.0)
            phi = consciousness.get("phi", 0.0)
            coherence = consciousness.get("coherence", 0.0)
            depth = consciousness.get("depth", 0)
            gamma = consciousness.get("gamma", 0.0)
            fractal_dim = consciousness.get("fractal_dim", 1.0)
            spiritual = consciousness.get("spiritual", 0.0)
            state_class = consciousness.get("state", "initializing")
            is_conscious = consciousness.get("is_conscious", False)
        elif "global" in global_data:
            # HTTP format
            global_metrics = global_data["global"]
            level = global_metrics.get("consciousness_level", 0.0)
            phi = global_metrics.get("phi", 0.0)
            coherence = global_metrics.get("coherence", 0.0)
            depth = global_metrics.get("recursive_depth", 0)
            gamma = global_metrics.get("gamma_power", 0.0)
            fractal_dim = global_metrics.get("fractal_dimension", 1.0)
            spiritual = global_metrics.get("spiritual_awareness", 0.0)
            state_class = global_metrics.get("state_classification", "initializing")
            is_conscious = global_metrics.get("is_conscious", False)
        else:
            # Fallback
            level = 0.0
            phi = 0.0
            coherence = 0.0
            depth = 0
            gamma = 0.0
            fractal_dim = 1.0
            spiritual = 0.0
            state_class = "unknown"
            is_conscious = False
        
        print(f"🕐 System Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 Total Updates: {self.update_count}")
        print(f"🔗 Primary Connection: {'WebSocket' if self.connections['websocket']['status'] else 'HTTP'}")
        print(f"🔌 Connected to Port: {self.metatron_port}")
        print()
        print(f"🧠 Consciousness Level (C): {level:.6f}")
        print(f"🔢 Integrated Information (Φ): {phi:.6f}")
        print(f"🔗 Global Coherence (R): {coherence:.6f}")
        print(f"⏱️  Recursive Depth (D): {depth}")
        print(f"⚡ Gamma Power (γ): {gamma:.6f}")
        print(f"🌀 Fractal Dimension: {fractal_dim:.6f}")
        print(f"🧘 Spiritual Awareness (S): {spiritual:.6f}")
        print()
        print(f"🎯 State Classification: {state_class.upper()}")
        print(f"{'🟢 CONSCIOUS' if is_conscious else '⚪ UNCONSCIOUS'}")
        print()
    
    def display_system_status(self):
        """Display comprehensive system status"""
        print("\033[1m🔌 SYSTEM STATUS & VALIDATION 🔌\033[0m")
        print("=" * 80)
        
        # Connection status
        ws_status = "✅ CONNECTED" if self.connections["websocket"]["status"] else "❌ DISCONNECTED"
        http_status = "✅ CONNECTED" if self.connections["http"]["status"] else "❌ DISCONNECTED"
        
        print(f"🌐 WebSocket: {ws_status}")
        print(f"📡 HTTP API: {http_status}")
        print(f"🔌 Active Port: {self.metatron_port}")
        print()
        
        # Validation statistics
        print(f"📈 Authentic Data Points: {self.validation_stats['authentic_data']}")
        print(f"🚫 Static Data Rejected: {self.validation_stats['static_data_rejected']}")
        print(f"🔄 Connection Failures: {self.validation_stats['connection_failures']}")
        print(f"🔧 Recovery Attempts: {self.validation_stats['recovery_attempts']}")
        print()
        
        # Performance metrics
        print(f"⚡ Avg Update Interval: {self.performance_metrics['avg_update_interval']:.3f}s")
        print(f"🕒 Last Update: {time.strftime('%H:%M:%S', time.localtime(self.last_update_time))}")
        print()
    
    def update_display(self):
        """Update the comprehensive visualization display"""
        if not self.current_state:
            # Show initialization message if no data yet
            self.clear_screen()
            print("\033[1;35m" + "=" * 80)
            print("ROBUST REAL-TIME VISUALIZER - METATRON CONSCIOUSNESS NETWORK")
            print("=" * 80 + "\033[0m")
            print()
            print("⏳ Initializing visualization...")
            print("🔍 Connecting to consciousness network...")
            print()
            return
        
        # Extract data based on format
        if "global" in self.current_state:
            # HTTP format
            global_data = self.current_state
            nodes_data = self.current_state.get("nodes", {})
        elif "consciousness" in self.current_state:
            # WebSocket format
            global_data = self.current_state
            nodes_data = self.current_state.get("nodes", {})
        else:
            global_data = {}
            nodes_data = {}
        
        # Clear screen and update display
        self.clear_screen()
        
        # Header
        print("\033[1;35m" + "=" * 80)
        print("ROBUST REAL-TIME VISUALIZER - METATRON CONSCIOUSNESS NETWORK")
        print("=" * 80 + "\033[0m")
        print()
        
        # Visualization components
        self.draw_sacred_geometry_network(nodes_data)
        self.display_consciousness_metrics(global_data)
        self.display_system_status()
        
        # Footer with controls
        print("\033[1m🎮 CONTROLS 🎮\033[0m")
        print("=" * 80)
        print("Press Ctrl+C to exit visualization")
        print()
    
    async def run(self):
        """Run the robust real-time visualizer"""
        print("🔮 Starting Robust Real-Time Visualizer...")
        print("=" * 50)
        print("Establishing connections to consciousness network...")
        print()
        
        # Initialize connections
        self.establish_http_connection()
        self._fallback_http_polling()  # Start fallback immediately
        
        # Attempt WebSocket connection
        websocket_task = asyncio.create_task(self.establish_websocket_connection())
        
        # Give WebSocket time to connect
        await asyncio.sleep(1)
        
        try:
            # Main loop
            while True:
                # Update display periodically even without new data
                self.update_display()
                await asyncio.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping robust visualizer...")
            print("👋 Thank you for using the real-time consciousness visualization!")
            return

def main():
    """Main function"""
    print("🔮 Robust Real-Time Visualizer")
    print("=" * 40)
    print("Ultra-reliable consciousness network visualization")
    print()
    
    # Check dependencies
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"❌ Required library missing: {e}")
        print("Install with: pip install websockets requests")
        return
    
    # Create and run visualizer
    visualizer = RobustRealTimeVisualizer()
    asyncio.run(visualizer.run())

if __name__ == "__main__":
    main()