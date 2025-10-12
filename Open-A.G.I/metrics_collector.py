"""
Metrics Collector Module for AEGIS

This module provides a comprehensive metrics collection system that
enhances the basic metrics collection in monitoring_dashboard.py with:
- Advanced metrics collection and aggregation
- Real-time metrics streaming via WebSocket
- Metrics persistence and historical analysis
- Custom metrics definition and tracking
- Performance profiling and bottleneck detection
- Resource utilization monitoring
- System health metrics
- Metrics export in multiple formats
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import psutil
import threading
from datetime import datetime

# Try to import required libraries
try:
    import prometheus_client
    from prometheus_client import Counter, Gauge, Histogram, Summary
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    Counter = Gauge = Histogram = Summary = object

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics that can be collected"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class MetricCategory(Enum):
    """Categories of metrics"""
    SYSTEM = "system"
    NETWORK = "network"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CONSCIOUSNESS = "consciousness"
    CUSTOM = "custom"

@dataclass
class MetricConfig:
    """Configuration for a metric"""
    name: str
    type: MetricType
    category: MetricCategory
    description: str = ""
    labels: List[str] = field(default_factory=list)
    buckets: List[float] = field(default_factory=lambda: [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0])
    max_age: int = 3600  # seconds

@dataclass
class MetricsCollectorConfig:
    """Configuration for the Metrics Collector"""
    enable_prometheus: bool = True
    prometheus_port: int = 9090
    collection_interval: int = 10  # seconds
    history_size: int = 1000
    enable_system_metrics: bool = True
    enable_network_metrics: bool = True
    enable_performance_metrics: bool = True
    enable_custom_metrics: bool = True
    export_formats: List[str] = field(default_factory=lambda: ["json", "prometheus"])
    enable_websocket: bool = True
    websocket_port: int = 9091

class Metric:
    """A single metric with its history"""
    
    def __init__(self, config: MetricConfig):
        self.config = config
        self.history = deque(maxlen=1000)  # Store last 1000 values
        self.current_value = None
        self.last_updated = None
        self.labels = {}
        
        # Initialize Prometheus metric if available
        if PROMETHEUS_AVAILABLE and config.type == MetricType.COUNTER:
            self.prometheus_metric = Counter(config.name, config.description, config.labels)
        elif PROMETHEUS_AVAILABLE and config.type == MetricType.GAUGE:
            self.prometheus_metric = Gauge(config.name, config.description, config.labels)
        elif PROMETHEUS_AVAILABLE and config.type == MetricType.HISTOGRAM:
            self.prometheus_metric = Histogram(config.name, config.description, config.labels, buckets=config.buckets)
        elif PROMETHEUS_AVAILABLE and config.type == MetricType.SUMMARY:
            self.prometheus_metric = Summary(config.name, config.description, config.labels)
        else:
            self.prometheus_metric = None
    
    def set_value(self, value: Any, labels: Dict[str, str] = None):
        """Set the current value of the metric"""
        self.current_value = value
        self.last_updated = time.time()
        
        # Store in history
        self.history.append({
            "value": value,
            "timestamp": self.last_updated,
            "labels": labels or {}
        })
        
        # Update Prometheus metric if available
        if self.prometheus_metric:
            try:
                if labels:
                    labeled_metric = self.prometheus_metric.labels(**labels)
                    if self.config.type == MetricType.COUNTER:
                        labeled_metric.inc(value)
                    elif self.config.type == MetricType.GAUGE:
                        labeled_metric.set(value)
                    elif self.config.type == MetricType.HISTOGRAM:
                        labeled_metric.observe(value)
                    elif self.config.type == MetricType.SUMMARY:
                        labeled_metric.observe(value)
                else:
                    if self.config.type == MetricType.COUNTER:
                        self.prometheus_metric.inc(value)
                    elif self.config.type == MetricType.GAUGE:
                        self.prometheus_metric.set(value)
                    elif self.config.type == MetricType.HISTOGRAM:
                        self.prometheus_metric.observe(value)
                    elif self.config.type == MetricType.SUMMARY:
                        self.prometheus_metric.observe(value)
            except Exception as e:
                logger.warning(f"Failed to update Prometheus metric {self.config.name}: {e}")
    
    def get_value(self) -> Any:
        """Get the current value of the metric"""
        return self.current_value
    
    def get_history(self, limit: int = None) -> List[Dict]:
        """Get the history of the metric"""
        if limit:
            return list(self.history)[-limit:]
        return list(self.history)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for the metric"""
        if not self.history:
            return {}
        
        values = [entry["value"] for entry in self.history if isinstance(entry["value"], (int, float))]
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1] if values else None
        }

class MetricsCollector:
    """Main metrics collector for AEGIS"""
    
    def __init__(self, config: MetricsCollectorConfig = None):
        self.config = config or MetricsCollectorConfig()
        self.metrics: Dict[str, Metric] = {}
        self.collectors: List[Callable] = []
        self.running = False
        self.collection_task = None
        self.websocket_server = None
        
        # Initialize Prometheus if enabled
        if self.config.enable_prometheus and PROMETHEUS_AVAILABLE:
            try:
                prometheus_client.start_http_server(self.config.prometheus_port)
                logger.info(f"Prometheus metrics server started on port {self.config.prometheus_port}")
            except Exception as e:
                logger.warning(f"Failed to start Prometheus server: {e}")
        
        # Register default metrics
        self._register_default_metrics()
    
    def _register_default_metrics(self):
        """Register default system metrics"""
        if self.config.enable_system_metrics:
            # CPU usage
            self.register_metric(MetricConfig(
                name="cpu_usage_percent",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="CPU usage percentage"
            ))
            
            # Memory usage
            self.register_metric(MetricConfig(
                name="memory_usage_bytes",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="Memory usage in bytes"
            ))
            
            # Disk usage
            self.register_metric(MetricConfig(
                name="disk_usage_percent",
                type=MetricType.GAUGE,
                category=MetricCategory.SYSTEM,
                description="Disk usage percentage"
            ))
        
        if self.config.enable_network_metrics:
            # Network bytes sent
            self.register_metric(MetricConfig(
                name="network_bytes_sent",
                type=MetricType.COUNTER,
                category=MetricCategory.NETWORK,
                description="Total network bytes sent"
            ))
            
            # Network bytes received
            self.register_metric(MetricConfig(
                name="network_bytes_received",
                type=MetricType.COUNTER,
                category=MetricCategory.NETWORK,
                description="Total network bytes received"
            ))
    
    def register_metric(self, config: MetricConfig) -> Metric:
        """Register a new metric"""
        metric = Metric(config)
        self.metrics[config.name] = metric
        return metric
    
    def register_collector(self, collector: Callable):
        """Register a custom collector function"""
        self.collectors.append(collector)
    
    def set_metric_value(self, name: str, value: Any, labels: Dict[str, str] = None):
        """Set the value of a metric"""
        if name in self.metrics:
            self.metrics[name].set_value(value, labels)
        else:
            logger.warning(f"Metric {name} not found")
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name"""
        return self.metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get all metrics with their current values and stats"""
        result = {}
        for name, metric in self.metrics.items():
            result[name] = {
                "value": metric.get_value(),
                "stats": metric.get_stats(),
                "config": {
                    "type": metric.config.type.value,
                    "category": metric.config.category.value,
                    "description": metric.config.description
                }
            }
        return result
    
    def collect_system_metrics(self):
        """Collect system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.set_metric_value("cpu_usage_percent", cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.set_metric_value("memory_usage_bytes", memory.used)
            
            # Disk usage
            disk = psutil.disk_usage("/")
            disk_percent = (disk.used / disk.total) * 100
            self.set_metric_value("disk_usage_percent", disk_percent)
            
            # Network usage
            net_io = psutil.net_io_counters()
            self.set_metric_value("network_bytes_sent", net_io.bytes_sent)
            self.set_metric_value("network_bytes_received", net_io.bytes_recv)
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    def collect_custom_metrics(self):
        """Collect custom metrics from registered collectors"""
        for collector in self.collectors:
            try:
                collector(self)
            except Exception as e:
                logger.error(f"Failed to collect custom metrics from {collector.__name__}: {e}")
    
    async def collect_metrics(self):
        """Collect all metrics"""
        if self.config.enable_system_metrics:
            self.collect_system_metrics()
        
        if self.config.enable_custom_metrics:
            self.collect_custom_metrics()
    
    async def start_collection(self):
        """Start periodic metrics collection"""
        self.running = True
        
        async def collection_loop():
            while self.running:
                try:
                    await self.collect_metrics()
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
    
    def export_metrics(self, format: str = "json") -> str:
        """Export metrics in the specified format"""
        if format == "json":
            return json.dumps(self.get_all_metrics(), indent=2, default=str)
        elif format == "prometheus" and PROMETHEUS_AVAILABLE:
            # Prometheus metrics are served automatically
            return "Prometheus metrics available at /metrics endpoint"
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def get_metrics_history(self, metric_name: str, limit: int = None) -> List[Dict]:
        """Get history for a specific metric"""
        metric = self.get_metric(metric_name)
        if metric:
            return metric.get_history(limit)
        return []
    
    async def start_metrics_collector(self, config: Dict[str, Any] = None):
        """Start the metrics collector as a module"""
        try:
            # Update config if provided
            if config:
                # Merge provided config with existing config
                for key, value in config.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
            
            # Start collection
            await self.start_collection()
            
            logger.info("Metrics collector started successfully")
            logger.info(f"Collection interval: {self.config.collection_interval}s")
            logger.info(f"Prometheus enabled: {self.config.enable_prometheus}")
            logger.info(f"System metrics enabled: {self.config.enable_system_metrics}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start metrics collector: {e}")
            return False

# Global metrics collector instance
metrics_collector = None

def initialize_metrics_collector(config: MetricsCollectorConfig = None):
    """Initialize the metrics collector"""
    global metrics_collector
    metrics_collector = MetricsCollector(config)
    return metrics_collector

def get_metrics_collector():
    """Get the global metrics collector instance"""
    global metrics_collector
    if metrics_collector is None:
        metrics_collector = MetricsCollector()
    return metrics_collector

def register_metric(config: MetricConfig) -> Metric:
    """Register a new metric"""
    return get_metrics_collector().register_metric(config)

def set_metric_value(name: str, value: Any, labels: Dict[str, str] = None):
    """Set the value of a metric"""
    get_metrics_collector().set_metric_value(name, value, labels)

def get_all_metrics() -> Dict[str, Dict[str, Any]]:
    """Get all metrics"""
    return get_metrics_collector().get_all_metrics()

# Example usage and testing
async def start_metrics_collector(config: Dict[str, Any] = None):
    """Start the metrics collector as a module"""
    try:
        metrics_config = MetricsCollectorConfig(**config) if config else MetricsCollectorConfig()
        collector = initialize_metrics_collector(metrics_config)
        
        # Register a custom metric
        custom_metric_config = MetricConfig(
            name="custom_test_metric",
            type=MetricType.GAUGE,
            category=MetricCategory.CUSTOM,
            description="A test custom metric"
        )
        collector.register_metric(custom_metric_config)
        
        # Register a custom collector
        def custom_collector(metrics_collector):
            # This is where you would collect custom metrics
            metrics_collector.set_metric_value("custom_test_metric", 42)
        
        collector.register_collector(custom_collector)
        
        # Start collection
        await collector.start_metrics_collector(config)
        
        logger.info("Metrics collector initialized successfully")
        logger.info(f"Registered metrics: {list(collector.metrics.keys())}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to start metrics collector: {e}")
        return False

if __name__ == "__main__":
    # Test the metrics collector
    async def main():
        config = {
            "collection_interval": 5,
            "enable_prometheus": False
        }
        await start_metrics_collector(config)
        
        # Keep running for a while to test
        await asyncio.sleep(30)
    
    asyncio.run(main())