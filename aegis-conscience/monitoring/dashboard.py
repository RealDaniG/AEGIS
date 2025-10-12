"""
Monitoring Dashboard for AEGIS-Conscience Network
Flask + SocketIO web interface for real-time metrics
"""

import json
import time
from typing import Dict, List, Optional
from threading import Thread
from dataclasses import asdict

# Conditional imports for Flask
try:
    from flask import Flask, render_template, jsonify
    from flask_socketio import SocketIO, emit
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    # Create dummy classes for type hints when Flask is not available
    class Flask:
        def __init__(self, *args, **kwargs):
            pass
        def route(self, *args, **kwargs):
            return lambda x: x
    
    class SocketIO:
        def __init__(self, *args, **kwargs):
            pass
        def on_event(self, *args, **kwargs):
            pass
        def emit(self, *args, **kwargs):
            pass
        def run(self, *args, **kwargs):
            pass
    
    def jsonify(*args, **kwargs):
        pass
    
    def emit(*args, **kwargs):
        pass

from schemas import ConsciousnessState, PeerInfo


class MonitoringDashboard:
    """Real-time monitoring dashboard for the AEGIS network"""
    
    def __init__(self, node_id: str, port: int = 8080):
        self.node_id = node_id
        self.port = port
        self.app: Optional[Flask] = None
        self.socketio: Optional[SocketIO] = None
        self.metrics_history: List[Dict] = []
        self.peers: Dict[str, PeerInfo] = {}
        self.running = False
        
        if HAS_FLASK:
            self._setup_flask_app()
    
    def _setup_flask_app(self):
        """Set up Flask application and routes"""
        if not HAS_FLASK:
            return
            
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'aegis-conscience-secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Register routes
        if self.app:
            self.app.route('/')(self._index)
            self.app.route('/api/metrics')(self._api_metrics)
            self.app.route('/api/peers')(self._api_peers)
        
        # Register SocketIO events
        if self.socketio:
            self.socketio.on_event('connect', lambda: self._on_connect())
            self.socketio.on_event('disconnect', lambda: self._on_disconnect())
    
    def _index(self):
        """Serve the main dashboard page"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>AEGIS-Conscience Network Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .metric-card { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #3498db; }
        .chart-container { margin-top: 20px; height: 300px; }
        .peers-list { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-top: 20px; }
        .peer-item { padding: 10px; border-bottom: 1px solid #eee; }
        .peer-status { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 10px; }
        .status-connected { background: #2ecc71; }
        .status-disconnected { background: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AEGIS-Conscience Network Dashboard</h1>
            <p>Node ID: <span id="node-id">-</span></p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Global Coherence</h3>
                <div class="metric-value" id="coherence">0.00</div>
                <div class="chart-container">
                    <canvas id="coherence-chart"></canvas>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Network Entropy</h3>
                <div class="metric-value" id="entropy">0.00</div>
                <div class="chart-container">
                    <canvas id="entropy-chart"></canvas>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Active Peers</h3>
                <div class="metric-value" id="peers">0</div>
                <div class="chart-container">
                    <canvas id="peers-chart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="peers-list">
            <h3>Connected Peers</h3>
            <div id="peers-container"></div>
        </div>
    </div>
    
    <script>
        const socket = io();
        
        // Chart setup
        const coherenceCtx = document.getElementById('coherence-chart').getContext('2d');
        const entropyCtx = document.getElementById('entropy-chart').getContext('2d');
        const peersCtx = document.getElementById('peers-chart').getContext('2d');
        
        const coherenceChart = new Chart(coherenceCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Global Coherence',
                    data: [],
                    borderColor: 'rgb(52, 152, 219)',
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        const entropyChart = new Chart(entropyCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Network Entropy',
                    data: [],
                    borderColor: 'rgb(155, 89, 182)',
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        const peersChart = new Chart(peersCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Active Peers',
                    data: [],
                    borderColor: 'rgb(46, 204, 113)',
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        // Update metrics
        socket.on('metrics_update', function(data) {
            document.getElementById('node-id').textContent = data.node_id;
            document.getElementById('coherence').textContent = data.global_coherence.toFixed(3);
            document.getElementById('entropy').textContent = data.global_entropy.toFixed(3);
            document.getElementById('peers').textContent = data.active_peers;
            
            // Update charts
            const timestamp = new Date().toLocaleTimeString();
            
            coherenceChart.data.labels.push(timestamp);
            coherenceChart.data.datasets[0].data.push(data.global_coherence);
            coherenceChart.update();
            
            entropyChart.data.labels.push(timestamp);
            entropyChart.data.datasets[0].data.push(data.global_entropy);
            entropyChart.update();
            
            peersChart.data.labels.push(timestamp);
            peersChart.data.datasets[0].data.push(data.active_peers);
            peersChart.update();
            
            // Keep only last 20 data points
            if (coherenceChart.data.labels.length > 20) {
                coherenceChart.data.labels.shift();
                coherenceChart.data.datasets[0].data.shift();
            }
            
            if (entropyChart.data.labels.length > 20) {
                entropyChart.data.labels.shift();
                entropyChart.data.datasets[0].data.shift();
            }
            
            if (peersChart.data.labels.length > 20) {
                peersChart.data.labels.shift();
                peersChart.data.datasets[0].data.shift();
            }
        });
        
        // Update peers list
        socket.on('peers_update', function(data) {
            const container = document.getElementById('peers-container');
            container.innerHTML = '';
            
            data.peers.forEach(function(peer) {
                const peerDiv = document.createElement('div');
                peerDiv.className = 'peer-item';
                peerDiv.innerHTML = `
                    <span class="peer-status status-${peer.connection_status}"></span>
                    <strong>${peer.peer_id}</strong> - 
                    ${peer.ip_address}:${peer.port} - 
                    Reputation: ${peer.reputation_score.toFixed(2)}
                `;
                container.appendChild(peerDiv);
            });
        });
    </script>
</body>
</html>
        '''
    
    def _api_metrics(self):
        """API endpoint for metrics data"""
        if self.metrics_history:
            latest = self.metrics_history[-1]
            if HAS_FLASK:
                return jsonify(latest)
        if HAS_FLASK:
            return jsonify({})
    
    def _api_peers(self):
        """API endpoint for peers data"""
        if HAS_FLASK:
            return jsonify({
                'peers': [asdict(peer) for peer in self.peers.values()]
            })
        return {}
    
    def _on_connect(self):
        """Handle SocketIO client connection"""
        print("Dashboard client connected")
        if HAS_FLASK and self.socketio:
            self.socketio.emit('connected', {'node_id': self.node_id})
    
    def _on_disconnect(self):
        """Handle SocketIO client disconnection"""
        print("Dashboard client disconnected")
    
    def update_metrics(self, global_coherence: float, global_entropy: float, 
                      active_peers: int, timestamp: Optional[float] = None):
        """
        Update metrics data
        
        Args:
            global_coherence: Global coherence value
            global_entropy: Global entropy value
            active_peers: Number of active peers
            timestamp: Timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
            
        metrics = {
            'node_id': self.node_id,
            'global_coherence': global_coherence,
            'global_entropy': global_entropy,
            'active_peers': active_peers,
            'timestamp': timestamp
        }
        
        self.metrics_history.append(metrics)
        
        # Keep only last 100 metrics
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)
        
        # Broadcast to connected clients
        if HAS_FLASK and self.socketio:
            self.socketio.emit('metrics_update', metrics)
    
    def update_peers(self, peers: Dict[str, PeerInfo]):
        """
        Update peers data
        
        Args:
            peers: Dictionary of peer information
        """
        self.peers = peers
        
        # Broadcast to connected clients
        if HAS_FLASK and self.socketio:
            self.socketio.emit('peers_update', {
                'peers': [asdict(peer) for peer in peers.values()]
            })
    
    def start_dashboard(self, debug: bool = False):
        """
        Start the monitoring dashboard
        
        Args:
            debug: Enable Flask debug mode
        """
        if not HAS_FLASK:
            print("Cannot start dashboard: Flask not available")
            return
            
        if not self.app or not self.socketio:
            print("Dashboard not properly initialized")
            return
            
        self.running = True
        print(f"Starting dashboard on http://localhost:{self.port}")
        
        try:
            if self.socketio:
                self.socketio.run(self.app, host='0.0.0.0', port=self.port, debug=debug)
        except Exception as e:
            print(f"Error starting dashboard: {e}")
    
    def stop_dashboard(self):
        """Stop the monitoring dashboard"""
        self.running = False
        print("Dashboard stopped")


# Example usage
if __name__ == "__main__":
    if HAS_FLASK:
        # Create dashboard
        dashboard = MonitoringDashboard("test_node_1", 8080)
        
        # Simulate metrics updates
        def simulate_metrics():
            import random
            for i in range(100):
                if not dashboard.running:
                    break
                    
                dashboard.update_metrics(
                    global_coherence=random.uniform(0.5, 0.9),
                    global_entropy=random.uniform(0.1, 0.4),
                    active_peers=random.randint(3, 8)
                )
                
                # Simulate peer updates
                peers = {}
                for j in range(5):
                    peer_id = f"peer_{j+1}"
                    peers[peer_id] = PeerInfo(
                        peer_id=peer_id,
                        ip_address=f"192.168.1.{100+j}",
                        port=8080+j,
                        public_key=f"key_{j}",
                        last_seen=time.time(),
                        connection_status="connected" if j < 3 else "disconnected",
                        reputation_score=random.uniform(0.6, 1.0),
                        latency=random.uniform(0.05, 0.3)
                    )
                
                dashboard.update_peers(peers)
                time.sleep(2)
        
        # Start metrics simulation in background
        metrics_thread = Thread(target=simulate_metrics)
        metrics_thread.daemon = True
        metrics_thread.start()
        
        # Start dashboard
        try:
            dashboard.start_dashboard(debug=True)
        except KeyboardInterrupt:
            dashboard.stop_dashboard()
    else:
        print("Flask not available, cannot start dashboard")