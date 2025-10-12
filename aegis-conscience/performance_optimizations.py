"""
Performance optimizations for AEGIS-Conscience Network
"""

import asyncio
import time
import functools
from typing import Dict, List, Any, Callable, Optional
from collections import OrderedDict


class LRUCache:
    """LRU Cache implementation for performance optimization"""
    
    def __init__(self, maxsize: int = 128):
        self.cache = OrderedDict()
        self.maxsize = maxsize
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.maxsize:
            # Remove least recently used item
            self.cache.popitem(last=False)
        self.cache[key] = value


class PerformanceOptimizer:
    """Performance optimization utilities for AEGIS system"""
    
    def __init__(self):
        self.cache = LRUCache(maxsize=1000)
        self.batch_queue: Dict[str, List[Any]] = {}
        self.batch_timers: Dict[str, float] = {}
        self.stats: Dict[str, int] = {
            'cache_hits': 0,
            'cache_misses': 0,
            'batched_operations': 0,
            'optimized_calls': 0
        }
    
    def cached(self, ttl: int = 300):
        """Decorator for caching function results"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Check cache
                cached_result = self.cache.get(key)
                if cached_result:
                    # Check if expired
                    result, timestamp = cached_result
                    if time.time() - timestamp < ttl:
                        self.stats['cache_hits'] += 1
                        return result
                
                # Cache miss - call function
                self.stats['cache_misses'] += 1
                result = func(*args, **kwargs)
                
                # Store in cache
                self.cache.put(key, (result, time.time()))
                return result
            
            return wrapper
        return decorator
    
    async def batch_operation(self, operation_type: str, items: List[Any], 
                            batch_size: int = 10, delay: float = 0.1):
        """Batch operations for better efficiency"""
        if operation_type not in self.batch_queue:
            self.batch_queue[operation_type] = []
        
        # Add items to queue
        self.batch_queue[operation_type].extend(items)
        
        # Process batches when queue is full or after delay
        while len(self.batch_queue[operation_type]) >= batch_size:
            batch = self.batch_queue[operation_type][:batch_size]
            self.batch_queue[operation_type] = self.batch_queue[operation_type][batch_size:]
            
            # Process batch
            await self._process_batch(operation_type, batch)
            self.stats['batched_operations'] += len(batch)
        
        # Set timer for remaining items
        if self.batch_queue[operation_type] and operation_type not in self.batch_timers:
            self.batch_timers[operation_type] = time.time() + delay
    
    async def _process_batch(self, operation_type: str, batch: List[Any]):
        """Process a batch of operations"""
        # This would be implemented based on specific operation types
        print(f"Processing batch of {len(batch)} {operation_type} operations")
        await asyncio.sleep(0.01)  # Simulate processing time
    
    def get_stats(self) -> Dict[str, int]:
        """Get performance statistics"""
        return self.stats.copy()


class OptimizedConsciousnessEngine:
    """Optimized consciousness engine with caching and batching"""
    
    def __init__(self, node_id: str, optimizer: PerformanceOptimizer):
        self.node_id = node_id
        self.optimizer = optimizer
        self.metrics_cache = {}
        self.last_calculation = 0
    
    def calculate_coherence(self, oscillator_phases: List[float]) -> float:
        """Calculate coherence with caching"""
        # Create cache key
        cache_key = f"coherence:{hash(str(oscillator_phases))}"
        
        # Check cache
        cached_result = self.optimizer.cache.get(cache_key)
        if cached_result:
            result, timestamp = cached_result
            if time.time() - timestamp < 60:  # 60 second TTL
                self.optimizer.stats['cache_hits'] += 1
                return result
        
        # Cache miss - calculate
        self.optimizer.stats['cache_misses'] += 1
        if len(oscillator_phases) == 0:
            result = 0.0
        else:
            # Calculate global phase coherence using Kuramoto order parameter approximation
            import math
            real_sum = sum(math.cos(phase) for phase in oscillator_phases)
            imag_sum = sum(math.sin(phase) for phase in oscillator_phases)
            
            # Calculate magnitude
            magnitude = math.sqrt(real_sum**2 + imag_sum**2) / len(oscillator_phases)
            result = max(0.0, min(1.0, magnitude))
        
        # Store in cache
        self.optimizer.cache.put(cache_key, (result, time.time()))
        return result
    
    def calculate_entropy(self, node_states: List[float]) -> float:
        """Calculate entropy with caching"""
        # Create cache key
        cache_key = f"entropy:{hash(str(node_states))}"
        
        # Check cache
        cached_result = self.optimizer.cache.get(cache_key)
        if cached_result:
            result, timestamp = cached_result
            if time.time() - timestamp < 30:  # 30 second TTL
                self.optimizer.stats['cache_hits'] += 1
                return result
        
        # Cache miss - calculate
        self.optimizer.stats['cache_misses'] += 1
        if len(node_states) == 0:
            result = 0.0
        else:
            # Convert to probability distribution
            abs_states = [abs(x) for x in node_states]
            total = sum(abs_states)
            
            if total < 1e-12:
                result = 0.0
            else:
                probs = [x / total for x in abs_states if x > 1e-12]  # Remove zeros
                
                if len(probs) == 0:
                    result = 0.0
                else:
                    # Shannon entropy
                    import math
                    entropy = -sum(p * math.log2(p + 1e-12) for p in probs)
                    
                    # Normalize by maximum entropy
                    max_entropy = math.log2(len(probs)) if len(probs) > 1 else 1.0
                    if max_entropy > 0:
                        normalized_entropy = entropy / max_entropy
                    else:
                        normalized_entropy = 0.0
                    
                    result = max(0.0, min(1.0, normalized_entropy))
        
        # Store in cache
        self.optimizer.cache.put(cache_key, (result, time.time()))
        return result
    
    async def batch_update_peers(self, peers: List[Dict[str, Any]]):
        """Batch update peer information"""
        await self.optimizer.batch_operation("peer_update", peers, batch_size=5)


class NetworkOptimizer:
    """Network optimization utilities"""
    
    def __init__(self):
        self.connection_pool = {}
        self.message_queue = asyncio.Queue(maxsize=1000)
        self.batch_size = 10
        self.send_interval = 0.05  # 50ms between sends
    
    async def batch_send_messages(self, messages: List[Dict[str, Any]]):
        """Batch send messages for efficiency"""
        for message in messages:
            try:
                await self.message_queue.put(message)
            except asyncio.QueueFull:
                print("Message queue full, dropping message")
    
    async def message_sender(self):
        """Background task to send batched messages"""
        while True:
            try:
                # Collect messages for batch
                batch = []
                try:
                    # Get first message
                    msg = await asyncio.wait_for(self.message_queue.get(), timeout=0.1)
                    batch.append(msg)
                    
                    # Try to get more messages for batch
                    while len(batch) < self.batch_size:
                        try:
                            msg = self.message_queue.get_nowait()
                            batch.append(msg)
                        except asyncio.QueueEmpty:
                            break
                except asyncio.TimeoutError:
                    # No messages available
                    continue
                
                if batch:
                    # Send batch
                    await self._send_batch(batch)
                
                # Wait before next send
                await asyncio.sleep(self.send_interval)
                
            except Exception as e:
                print(f"Error in message sender: {e}")
                await asyncio.sleep(1)
    
    async def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send a batch of messages"""
        print(f"Sending batch of {len(batch)} messages")
        # In a real implementation, this would send the actual network messages
        await asyncio.sleep(0.01)  # Simulate network delay


# Example usage and performance test
async def performance_test():
    """Test performance optimizations"""
    print("=== AEGIS Performance Optimization Test ===\n")
    
    # Create optimizer
    optimizer = PerformanceOptimizer()
    engine = OptimizedConsciousnessEngine("test_node", optimizer)
    network_optimizer = NetworkOptimizer()
    
    # Start network sender
    sender_task = asyncio.create_task(network_optimizer.message_sender())
    
    # Test caching
    print("1. Testing caching optimization...")
    oscillator_phases = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    # First call (cache miss)
    start_time = time.time()
    coherence1 = engine.calculate_coherence(oscillator_phases)
    time1 = time.time() - start_time
    
    # Second call (cache hit)
    start_time = time.time()
    coherence2 = engine.calculate_coherence(oscillator_phases)
    time2 = time.time() - start_time
    
    print(f"   First call: {coherence1:.6f} (took {time1*1000:.2f}ms)")
    print(f"   Second call: {coherence2:.6f} (took {time2*1000:.2f}ms)")
    print(f"   Speedup: {time1/time2:.2f}x" if time2 > 0 else "   Speedup: ∞x")
    
    # Test batching
    print("\n2. Testing batch operations...")
    peers = [{"id": f"peer_{i}", "status": "connected"} for i in range(20)]
    
    start_time = time.time()
    await engine.batch_update_peers(peers)
    batch_time = time.time() - start_time
    
    print(f"   Batched {len(peers)} peer updates in {batch_time*1000:.2f}ms")
    
    # Test network batching
    print("\n3. Testing network message batching...")
    messages = [{"type": "state", "data": f"message_{i}"} for i in range(50)]
    
    start_time = time.time()
    await network_optimizer.batch_send_messages(messages)
    network_time = time.time() - start_time
    
    print(f"   Batched {len(messages)} messages in {network_time*1000:.2f}ms")
    
    # Show statistics
    print("\n4. Performance statistics:")
    stats = optimizer.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Cancel sender task
    sender_task.cancel()
    try:
        await sender_task
    except asyncio.CancelledError:
        pass
    
    print("\n✅ Performance optimization test completed!")


if __name__ == "__main__":
    asyncio.run(performance_test())