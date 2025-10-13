"""
Metrics Bridge for integrating Open-A.G.I monitoring with AEGIS visualization tools

This module provides a bridge that allows AEGIS to use Open-A.G.I's monitoring and metrics
collection while maintaining compatibility with AEGIS's existing visualization systems.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta

# Try to import Open-A.G.I monitoring components
try:
    from Open_A_G_I.monitoring_dashboard import MonitoringDashboard
    from Open_A_G_I.metrics_collector import MetricsCollector, Metric, MetricConfig, MetricType, MetricCategory
    OPEN_AGI_MONITORING_AVAILABLE = True
except ImportError:
    OPEN_AGI_MONITORING_AVAILABLE = False
    # Create placeholder classes for when Open-A.G.I monitoring is not available
    class MetricType(Enum):
        COUNTER = "counter"
        GAUGE = "gauge"
        HISTOGRAM = "histogram"
        SUMMARY = "summary"
    
    class MetricCategory(Enum):
        SYSTEM = "system"
        NETWORK = "network"
        PERFORMANCE = "performance"
        SECURITY = "security"
        CONSCIOUSNESS = "consciousness"
        CUSTOM = "custom"
    
    @dataclass
    class MetricConfig:
        name: str
        type: MetricType
        category: MetricCategory
        description: str = ""
        labels: List[str] = field(default_factory=list)
    
    class Metric:
        def __init__(self, config: MetricConfig):
            self.config = config
            self.history = deque(maxlen=1000)
            self.current_value = None
            self.last_updated = None
        
        def set_value(self, value: Any, labels: Dict[str, str] = None):
            self.current_value = value
            self.last_updated = time.time()
            self.history.append({
                "value": value,
                "timestamp": self.last_updated,
                "labels": labels or {}
            })
        
        def get_value(self) -> Any:
            return self.current_value
        
        def get_history(self, limit: int = None) -> List[Dict]:
            if limit:
                return list(self.history)[-limit:]
            return list(self.history)
    
    class MetricsCollector:
        def __init__(self, config: Dict[str, Any] = None):
            self.config = config or {}
            self.metrics: Dict[str, Metric] = {}
            self.collectors: List[Callable] = []
        
        def register_metric(self, config: MetricConfig) -> Metric:
            metric = Metric(config)
            self.metrics[config.name] = metric
            return metric
        
        def set_metric_value(self, name: str, value: Any, labels: Dict[str, str] = None):
            if name in self.metrics:
                self.metrics[name].set_value(value, labels)
        
        def get_metric(self, name: str) -> Optional[Metric]:
            return self.metrics.get(name)
        
        def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
            result = {}
            for name, metric in self.metrics.items():
                result[name] = {
                    "value": metric.get_value(),
                    "config": {
                        "type": metric.config.type.value,
                        "category": metric.config.category.value,
                        "description": metric.config.description
                    }
                }
            return result

# Try to import AEGIS visualization components
try:
    # Assuming AEGIS has websocket visualization tools
    from visualization_tools.websocket_visuals import WebSocketBroadcaster
    AEGIS_VISUALIZATION_AVAILABLE = True
except ImportError:
    AEGIS_VISUALIZATION_AVAILABLE = False
    # Create placeholder for when AEGIS visualization is not available
    class WebSocketBroadcaster:
        def __init__(self):
            pass
        
        async def broadcast(self, channel: str, data: Dict[str, Any]):
            # Simulate broadcasting
            pass

# Configure logging
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

@dataclass
class AEGISMetricsConfig:
    """Configuration for AEGIS metrics collection"""
    collection_interval: int = 10  # seconds
    history_size: int = 1000
    enable_system_metrics: bool = True
    enable_network_metrics: bool = True
    enable_performance_metrics: bool = True
    enable_consciousness_metrics: bool = True
    enable_custom_metrics: bool = True
    websocket_broadcast: bool = True
    prometheus_export: bool = False

class MetricsBridge:
    """Bridge that integrates Open-A.G.I monitoring with AEGIS visualization tools"""
    
    def __init__(self, config: AEGISMetricsConfig = None):
        self.config = config or AEGISMetricsConfig()
        self.metrics_collector = None
        self.websocket_broadcaster = None
        self.running = False
        self.collection_task = None
        self.metatron_metrics = {}  # Special metrics for Metatron 13-node network
        
        # Initialize metrics collector
        if OPEN_AGI_MONITORING_AVAILABLE:
            # Use Open-A.G.I metrics collector
            self.metrics_collector = MetricsCollector({
                "collection_interval": self.config.collection_interval,
                "history_size": self.config.history_size
            })
        else:
            # Fallback to our own implementation
            self.metrics_collector = MetricsCollector()
        
        # Initialize websocket broadcaster if available
        if AEGIS_VISUALIZATION_AVAILABLE:
            self.websocket_broadcaster = WebSocketBroadcaster()
        
        # Register default metrics
        self._register_default_metrics()
        
        logger.info("MetricsBridge initialized")
    
    def _register_default_metrics(self):
        """Register default metrics for the AEGIS system"""
        if not self.metrics_collector:
            return
        
        # System metrics
        if self.config.enable_system_metrics:
            self.metrics_collector.register_metric(MetricConfig(
                name="cpu_usage_percent",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="CPU usage percentage"
            ))
            
            self.metrics_collector.register_metric(MetricConfig(
                name="memory_usage_bytes",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="Memory usage in bytes"
            ))
            
            self.metrics_collector.register_metric(MetricConfig(
                name="disk_usage_percent",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="Disk usage percentage"
            ))
        
        # Network metrics
        if self.config.enable_network_metrics:
            self.metrics_collector.register_metric(MetricConfig(
                name="network_bytes_sent",
                type=MetricType.COUNTER,
                category=MetricCategory.NETWORK,
                description="Total network bytes sent"
            ))
            
            self.metrics_collector.register_metric(MetricConfig(
                name="network_bytes_received",
                type=MetricType.COUNTER,
                category=MetricCategory.NETWORK,
                description="Total network bytes received"
            ))
        
        # Performance metrics
        if self.config.enable_performance_metrics:
            self.metrics_collector.register_metric(MetricConfig(
                name="request_latency_seconds",
                type=MetricType.HISTOGRAM,
                category=MetricCategory.PERFORMANCE,
                description="Request latency in seconds"
            ))
        
        # Consciousness metrics (specific to AEGIS/Metatron)
        if self.config.enable_consciousness_metrics:
            self.metrics_collector.register_metric(MetricConfig(
                name="consciousness_phi",
                type=MetricType.GAUGE,
                category=MetricCategory.CONSCIOUSNESS,
                description="Integrated information (Phi) of the consciousness engine"
            ))
            
            self.metrics_collector.register_metric(MetricConfig(
                name="recursive_depth",
                type=MetricType.GAUGE,
                category=MetricCategory.CONSCIOUSNESS,
                description="Recursive depth of consciousness processing"
            ))
            
            self.metrics_collector.register_metric(MetricConfig(
                name="coherence_level",
                type=MetricType.GAUGE,
                category=MetricCategory.CONSCIOUSNESS,
                description="Coherence level of the consciousness network"
            ))
    
    def register_metatron_metric(self, node_id: str, metric_name: str, value: Any, 
                                labels: Dict[str, str] = None):
        """Register a metric specific to a Metatron node"""
        if node_id not in self.metatron_metrics:
            self.metatron_metrics[node_id] = {}
        
        metric_key = f"{node_id}_{metric_name}"
        self.metatron_metrics[node_id][metric_name] = {
            "value": value,
            "timestamp": time.time(),
            "labels": labels or {}
        }
        
        # Also register in the main metrics collector
        if self.metrics_collector:
            full_metric_name = f"metatron_{node_id}_{metric_name}"
            self.metrics_collector.set_metric_value(full_metric_name, value, labels)
    
    def set_metric_value(self, name: str, value: Any, labels: Dict[str, str] = None):
        """Set the value of a metric"""
        if self.metrics_collector:
            self.metrics_collector.set_metric_value(name, value, labels)
    
    def get_metric_value(self, name: str) -> Any:
        """Get the current value of a metric"""
        if self.metrics_collector:
            metric = self.metrics_collector.get_metric(name)
            if metric:
                return metric.get_value()
        return None
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        if self.metrics_collector:
            return self.metrics_collector.get_all_metrics()
        return {}
    
    def get_metatron_network_metrics(self) -> Dict[str, Any]:
        """Get metrics for the entire Metatron network"""
        return {
            "nodes": self.metatron_metrics,
            "timestamp": time.time(),
            "total_nodes": len(self.metatron_metrics)
        }
    
    async def start_collection(self):
        """Start periodic metrics collection"""
        if self.running:
            return
        
        self.running = True
        
        async def collection_loop():
            while self.running:
                try:
                    # Collect metrics
                    await self._collect_metrics()
                    
                    # Broadcast to websocket if enabled
                    if self.config.websocket_broadcast:
                        await self._broadcast_metrics()
                    
                    # Wait for next collection interval
                    await asyncio.sleep(self.config.collection_interval)
                except Exception as e:
                    logger.error(f"Error in metrics collection loop: {e}")
                    await asyncio.sleep(self.config.collection_interval)
        
        self.collection_task = asyncio.create_task(collection_loop())
        logger.info("Metrics collection started")
    
    async def stop_collection(self):
        """Stop periodic metrics collection"""
        self.running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        logger.info("Metrics collection stopped")
    
    async def _collect_metrics(self):
        """Collect system metrics"""
        # This would integrate with actual system monitoring
        # For now, we'll simulate some metrics
        import random
        import psutil  # Optional dependency
        
        try:
            # System metrics (if psutil is available)
            if self.config.enable_system_metrics:
                try:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    self.set_metric_value("cpu_usage_percent", cpu_percent)
                    
                    memory = psutil.virtual_memory()
                    self.set_metric_value("memory_usage_bytes", memory.used)
                    
                    disk = psutil.disk_usage("/")
                    disk_percent = (disk.used / disk.total) * 100
                    self.set_metric_value("disk_usage_percent", disk_percent)
                except Exception:
                    # Fallback to simulated metrics
                    self.set_metric_value("cpu_usage_percent", random.uniform(10, 90))
                    self.set_metric_value("memory_usage_bytes", random.uniform(1e9, 8e9))
                    self.set_metric_value("disk_usage_percent", random.uniform(20, 80))
            
            # Network metrics (simulated)
            if self.config.enable_network_metrics:
                self.set_metric_value("network_bytes_sent", random.uniform(1000, 10000))
                self.set_metric_value("network_bytes_received", random.uniform(1000, 10000))
            
            # Performance metrics (simulated)
            if self.config.enable_performance_metrics:
                self.set_metric_value("request_latency_seconds", random.uniform(0.01, 1.0))
                
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    async def _broadcast_metrics(self):
        """Broadcast metrics to websocket"""
        if not self.websocket_broadcaster:
            return
        
        try:
            # Get all metrics
            metrics = self.get_all_metrics()
            metatron_metrics = self.get_metatron_network_metrics()
            
            # Broadcast system metrics
            await self.websocket_broadcaster.broadcast("metrics.update", {
                "type": "system_metrics",
                "data": metrics,
                "timestamp": time.time()
            })
            
            # Broadcast Metatron network metrics
            await self.websocket_broadcaster.broadcast("metrics.update", {
                "type": "metatron_network",
                "data": metatron_metrics,
                "timestamp": time.time()
            })
            
        except Exception as e:
            logger.error(f"Failed to broadcast metrics: {e}")
    
    def export_metrics_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        if not self.config.prometheus_export:
            return ""
        
        metrics = self.get_all_metrics()
        prometheus_output = []
        
        for name, metric in metrics.items():
            value = metric.get("value", 0)
            description = metric.get("config", {}).get("description", "")
            
            if description:
                prometheus_output.append(f"# HELP {name} {description}")
            
            metric_type = metric.get("config", {}).get("type", "gauge")
            prometheus_output.append(f"# TYPE {name} {metric_type}")
            prometheus_output.append(f"{name} {value}")
            prometheus_output.append("")  # Empty line between metrics
        
        return "\n".join(prometheus_output)
    
    async def add_custom_collector(self, collector_func: Callable):
        """Add a custom metrics collector function"""
        if self.metrics_collector and hasattr(self.metrics_collector, 'collectors'):
            self.metrics_collector.collectors.append(collector_func)
            logger.info("Custom collector added")

# Global instance
metrics_bridge = None

def get_metrics_bridge(config: AEGISMetricsConfig = None) -> MetricsBridge:
    """Get the global metrics bridge instance"""
    global metrics_bridge
    if metrics_bridge is None:
        metrics_bridge = MetricsBridge(config)
    return metrics_bridge

def initialize_metrics_bridge(config: AEGISMetricsConfig = None) -> MetricsBridge:
    """Initialize and return the metrics bridge"""
    global metrics_bridge
    metrics_bridge = MetricsBridge(config)
    return metrics_bridge

# Example usage
async def main():
    """Example usage of the metrics bridge"""
    # Initialize the bridge
    config = AEGISMetricsConfig(
        collection_interval=5,
        enable_consciousness_metrics=True,
        websocket_broadcast=True
    )
    
    bridge = initialize_metrics_bridge(config)
    
    # Start metrics collection
    await bridge.start_collection()
    
    # Simulate setting some metrics
    bridge.set_metric_value("cpu_usage_percent", 45.5)
    bridge.set_metric_value("memory_usage_bytes", 2048000000)
    
    # Register Metatron node metrics
    bridge.register_metatron_metric("metatron-main", "consciousness_phi", 0.75)
    bridge.register_metatron_metric("metatron-main", "recursive_depth", 5)
    bridge.register_metatron_metric("metatron-node-1", "consciousness_phi", 0.68)
    bridge.register_metatron_metric("metatron-node-1", "recursive_depth", 3)
    
    # Wait a bit to see collection in action
    await asyncio.sleep(15)
    
    # Get all metrics
    all_metrics = bridge.get_all_metrics()
    print(f"All metrics: {json.dumps(all_metrics, indent=2, default=str)}")
    
    # Get Metatron network metrics
    network_metrics = bridge.get_metatron_network_metrics()
    print(f"Metatron network metrics: {json.dumps(network_metrics, indent=2, default=str)}")
    
    # Stop collection
    await bridge.stop_collection()

if __name__ == "__main__":
    asyncio.run(main())