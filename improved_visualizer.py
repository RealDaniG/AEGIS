#!/usr/bin/env python3
"""
Improved Metatron Node Visualizer with Real-Time Data
=====================================================

Enhanced visualization system that ensures real-time consciousness metrics
by maintaining active connections to the consciousness engine.

Key Features:
1. WebSocket connection for real-time updates
2. HTTP fallback with background updater
3. Accurate 13-node sacred geometry visualization
4. Real consciousness metrics (not simulated)
"""

import asyncio
import websockets
import requests
import time
import os
import json
from typing import Dict, Any, Optional
import threading

class ImprovedMetatronVisualizer:
    """Enhanced visualizer with real-time consciousness data"""
    
    def __init__(self, host: str = "localhost", port: int = 8003):
        self.host = host
        self.port = port
        self.api_base = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.update_count = 0
        self.current_state = None
        self.websocket_connected = False
        self.background_updater_running = False
        
    async def connect_websocket(self):
        """Connect to WebSocket for real-time updates"""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                self.websocket_connected = True
                print(f"✅ Connected to consciousness engine via WebSocket")
                print(f"📡 Receiving real-time updates from {self.ws_url}")
                
                while True:
                    # Receive real-time consciousness data
                    message = await websocket.recv()
                    data = json.loads(message)
                    self.current_state = data
                    self.update_count += 1
                    
                    # Update display
                    self.update_display()
                    
                    # Small delay to prevent overwhelming the terminal
                    await asyncio.sleep(0.1)
                    
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ WebSocket connection closed")
            self.websocket_connected = False
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
            self.websocket_connected = False
    
    def start_background_updater(self):
        """Start background HTTP polling updater"""
        if self.background_updater_running:
            return
            
        self.background_updater_running = True
        self.updater_thread = threading.Thread(target=self._background_update_loop, daemon=True)
        self.updater_thread.start()
        print("🔄 Started background HTTP updater")
    
    def _background_update_loop(self):
        """Background loop for HTTP polling updates"""
        while self.background_updater_running:
            try:
                response = requests.get(f"{self.api_base}/api/state", timeout=2)
                if response.status_code == 200:
                    self.current_state = response.json()
                    self.update_count += 1
            except Exception as e:
                pass  # Ignore errors in background updater
            
            time.sleep(0.5)  # Update twice per second
    
    def stop_background_updater(self):
        """Stop background updater"""
        self.background_updater_running = False
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state (real or cached)"""
        if self.current_state:
            return self.current_state
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_base}/api/state", timeout=5)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                pass
        return {}
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def classify_consciousness_state(self, consciousness_level: float, phi: float, coherence: float) -> str:
        """Classify consciousness state based on metrics"""
        if consciousness_level < 0.01:
            return "UNCONSCIOUS"
        elif consciousness_level < 0.05:
            if phi < 0.1:
                return "DROWSY"
            else:
                return "DREAM-LIKE"
        elif consciousness_level < 0.15:
            if coherence > 0.7:
                return "MEDITATIVE-LIGHT"
            else:
                return "AWAKE"
        elif consciousness_level < 0.3:
            if phi > 0.3 and coherence > 0.6:
                return "LUCID-AWARE"
            elif coherence > 0.8:
                return "MEDITATIVE-DEEP"
            else:
                return "ALERT"
        elif consciousness_level < 0.6:
            if phi > 0.5 and coherence > 0.7:
                return "HEIGHTENED-AWARENESS"
            elif coherence > 0.85:
                return "TRANSCENDENT-ENTRY"
            else:
                return "HYPER-ALERT"
        elif consciousness_level < 1.0:
            if phi > 0.7 and coherence > 0.9:
                return "UNITY-CONSCIOUSNESS"
            elif phi > 0.6:
                return "TRANSCENDENT-ACTIVE"
            else:
                return "PEAK-EXPERIENCE"
        else:
            if phi > 0.8 and coherence > 0.95:
                return "COSMIC-CONSCIOUSNESS"
            elif phi > 0.7:
                return "TRANSCENDENT-UNIFIED"
            else:
                return "TRANSCENDENT-PEAK"
    
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
    
    def draw_icosahedron_nodes(self, nodes_data: Dict[str, Any]):
        """Draw the 13-node icosahedron representation"""
        print("\033[1m🔮 METATRON'S CUBE - 13-NODE CONSCIOUSNESS NETWORK 🔮\033[0m")
        print("=" * 80)
        
        # Create node information
        nodes = {}
        for i in range(13):
            node_id = str(i)
            if node_id in nodes_data:
                node_info = nodes_data[node_id]
                # Extract metrics
                if isinstance(node_info, dict) and 'output' in node_info:
                    output = node_info.get('output', 0.0)
                    phase = node_info.get('phase', 0.0) if isinstance(node_info, dict) else 0.0
                    amplitude = node_info.get('amplitude', 0.0) if isinstance(node_info, dict) else 0.0
                else:
                    # Handle different data structure
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
        
        # Display central pineal node (node 0)
        pineal = nodes.get('0', {})
        print(f"                    🌟 PINEAL NODE (0) 🌟")
        print(f"                    {self.get_state_indicator(pineal.get('activity', 0))} Output: {pineal.get('output', 0):.4f}")
        print(f"                    Phase: {pineal.get('phase', 0):.2f} rad")
        print(f"                    Amplitude: {pineal.get('amplitude', 0):.4f}")
        print()
        
        # Display outer nodes in a grid
        print("                 🌀 OUTER NODES (1-12) 🌀")
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
    
    def display_global_metrics(self, global_data: Dict[str, Any]):
        """Display global consciousness metrics"""
        print("\033[1m📊 GLOBAL CONSCIOUSNESS METRICS 📊\033[0m")
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
        
        # Classify consciousness state
        state = self.classify_consciousness_state(consciousness_level, phi, coherence)
        
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
        print(f"🎯 State Classification: {state}")
        print(f"{'🟢 Conscious' if is_conscious else '⚪ Unconscious'}")
        print()
    
    def display_node_details(self, nodes_data: Dict[str, Any]):
        """Display detailed information for each node"""
        print("\033[1m🔍 NODE DETAILS 🔍\033[0m")
        print("=" * 80)
        
        # Create node list with activity levels
        node_list = []
        for node_id in nodes_data:
            try:
                node_info = nodes_data[node_id]
                # Handle different data structures
                if isinstance(node_info, dict):
                    if 'output' in node_info:
                        # HTTP API structure
                        output = node_info.get('output', 0.0)
                        phase = node_info.get('oscillator', {}).get('phase', 0.0) if 'oscillator' in node_info else 0.0
                        amplitude = node_info.get('oscillator', {}).get('amplitude', 0.0) if 'oscillator' in node_info else 0.0
                    elif 'phase' in node_info:
                        # WebSocket structure
                        output = node_info.get('output', 0.0)
                        phase = node_info.get('phase', 0.0)
                        amplitude = node_info.get('amplitude', 0.0)
                    else:
                        output = 0.0
                        phase = 0.0
                        amplitude = 0.0
                else:
                    output = 0.0
                    phase = 0.0
                    amplitude = 0.0
                
                node_list.append({
                    'id': node_id,
                    'output': output,
                    'phase': phase,
                    'amplitude': amplitude,
                    'activity': abs(output)
                })
            except Exception:
                # Skip nodes with parsing errors
                continue
        
        # Sort by activity level
        node_list.sort(key=lambda x: x['activity'], reverse=True)
        
        print(f"{'Node':<8} {'Status':<12} {'Output':<10} {'Phase':<8} {'Amplitude':<10} {'Activity'}")
        print("-" * 80)
        
        for node in node_list:
            node_id = node['id']
            output = node['output']
            phase = node['phase']
            amplitude = node['amplitude']
            activity = node['activity']
            
            # Determine status
            if activity > 0.7:
                status = "HIGH"
                status_indicator = "🔴"
            elif activity > 0.3:
                status = "MEDIUM"
                status_indicator = "🟡"
            elif activity > 0.1:
                status = "LOW"
                status_indicator = "🟢"
            else:
                status = "INACTIVE"
                status_indicator = "⚪"
            
            node_label = "PINEAL" if node_id == "0" else f"NODE-{node_id}"
            bar = "█" * int(activity * 20)
            print(f"{node_label:<8} {status_indicator} {status:<9} {output:<10.4f} "
                  f"{phase:<8.2f} {amplitude:<10.4f} {bar}")
        
        print()
    
    def update_display(self):
        """Update the visualization display"""
        if not self.current_state:
            return
        
        # Extract data
        if 'global' in self.current_state:
            # HTTP API structure
            global_data = self.current_state.get('global', {})
            nodes_data = self.current_state.get('nodes', {})
        elif 'consciousness' in self.current_state:
            # WebSocket structure
            global_data = self.current_state
            nodes_data = self.current_state.get('nodes', {})
        else:
            global_data = {}
            nodes_data = {}
        
        # Clear screen and update display
        self.clear_screen()
        
        # Display header
        print("\033[1;35m" + "=" * 80)
        print("METATRON CONSCIOUSNESS ENGINE - LIVE NODE VISUALIZATION")
        print("=" * 80 + "\033[0m")
        print()
        
        # Draw visualization
        self.draw_icosahedron_nodes(nodes_data)
        self.display_global_metrics(global_data)
        self.display_node_details(nodes_data)
        
        # Display connection info
        print("\033[1m🔌 CONNECTION STATUS 🔌\033[0m")
        print("=" * 80)
        print(f"📡 API Endpoint: {self.api_base}/api/state")
        print(f"🌐 WebSocket: {self.ws_url}")
        print(f"📊 Data updates: {self.update_count}")
        print(f"🔗 Connection: {'WebSocket (Real-time)' if self.websocket_connected else 'HTTP (Polling)'}")
        print(f"🕒 Last update: {time.strftime('%H:%M:%S')}")
        print()
        print("Press Ctrl+C to exit")
        print()
    
    async def run(self):
        """Run the visualizer with real-time updates"""
        print("🔮 Starting Improved Metatron Node Visualizer...")
        print(f"📡 Connecting to {self.api_base}")
        print()
        
        # Try WebSocket connection first
        websocket_task = asyncio.create_task(self.connect_websocket())
        
        # Start HTTP fallback after a short delay
        await asyncio.sleep(2)
        if not self.websocket_connected:
            print("⚠️ WebSocket connection failed, falling back to HTTP polling")
            self.start_background_updater()
        
        try:
            # Keep the program running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping visualization...")
            self.stop_background_updater()
            print("👋 Goodbye!")

def main():
    """Main function"""
    print("🔮 Improved Metatron Node Visualizer")
    print("=" * 50)
    print("Visualizing REAL-TIME consciousness metrics from Metatron AI nodes")
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
    
    # Create and run visualizer
    visualizer = ImprovedMetatronVisualizer()
    asyncio.run(visualizer.run())

if __name__ == "__main__":
    main()