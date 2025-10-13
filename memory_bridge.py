#!/usr/bin/env python3
"""
Memory Bridge for Metatron-ConscienceAI and Open-A.G.I Integration

This module creates a bridge between the Metatron-ConscienceAI orchestrator
and the Open-A.G.I memory system, enabling seamless memory operations
across both frameworks.

The bridge provides:
1. Real-time memory state synchronization
2. Consciousness metric storage and retrieval
3. Distributed memory sharing capabilities
4. Pipeline integration for memory-aware processing
"""

import sys
import os
import json
import asyncio
import numpy as np
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project paths
project_root = os.path.dirname(__file__)
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
open_agi_path = os.path.join(project_root, 'Open-A.G.I')

# Ensure paths are in sys.path
if metatron_path not in sys.path:
    sys.path.insert(0, metatron_path)
if open_agi_path not in sys.path:
    sys.path.insert(0, open_agi_path)

class MemoryBridge:
    """Bridge between Metatron-ConscienceAI orchestrator and Open-A.G.I memory system"""
    
    def __init__(self, memory_file: str = "ai_runs/bridge_memory.json"):
        self.orchestrator = None
        self.memory_system = None
        self.is_initialized = False
        self.memory_file = memory_file
        self.bridge_active = False
    
    async def initialize_bridge(self) -> bool:
        """Initialize the memory bridge between systems"""
        try:
            logger.info("Initializing Memory Bridge...")
            
            # Dynamically import MetatronConsciousness
            import importlib.util
            orchestrator_spec = importlib.util.spec_from_file_location(
                "metatron_orchestrator",
                os.path.join(metatron_path, "orchestrator", "metatron_orchestrator.py")
            )
            if orchestrator_spec and orchestrator_spec.loader:
                orchestrator_module = importlib.util.module_from_spec(orchestrator_spec)
                orchestrator_spec.loader.exec_module(orchestrator_module)
                MetatronConsciousness = getattr(orchestrator_module, 'MetatronConsciousness')
            else:
                raise ImportError("Failed to import MetatronConsciousness")
            
            # Dynamically import OpenAGIMemoryIntegration
            memory_spec = importlib.util.spec_from_file_location(
                "open_agi_memory_integration",
                os.path.join(open_agi_path, "memory_integration.py")
            )
            if memory_spec and memory_spec.loader:
                memory_module = importlib.util.module_from_spec(memory_spec)
                memory_spec.loader.exec_module(memory_module)
                OpenAGIMemoryIntegration = getattr(memory_module, 'OpenAGIMemoryIntegration')
            else:
                raise ImportError("Failed to import OpenAGIMemoryIntegration")
            
            # Initialize orchestrator with high gamma for faster processing
            logger.info("Initializing Metatron Consciousness Orchestrator...")
            self.orchestrator = MetatronConsciousness(base_frequency=40.0, dt=0.01, high_gamma=True)
            logger.info("✅ Metatron Consciousness Orchestrator initialized")
            
            # Initialize Open-A.G.I memory system
            logger.info("Initializing Open-A.G.I Memory System...")
            self.memory_system = OpenAGIMemoryIntegration(self.memory_file)
            logger.info("✅ Open-A.G.I Memory System initialized")
            
            # Start P2P network if available
            logger.info("Starting P2P network...")
            await self.memory_system.start_network()
            logger.info("✅ P2P network started")
            
            self.is_initialized = True
            self.bridge_active = True
            logger.info("✅ Memory Bridge initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing Memory Bridge: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness state from orchestrator"""
        if not self.orchestrator or not self.is_initialized:
            logger.warning("Orchestrator not initialized")
            return None
        
        try:
            state = self.orchestrator.get_current_state()
            return state
        except Exception as e:
            logger.error(f"❌ Error getting consciousness state: {e}")
            return None
    
    def store_consciousness_metrics(self, metrics: Dict[str, Any]) -> str:
        """Store consciousness metrics in Open-A.G.I memory system"""
        if not self.memory_system or not self.is_initialized:
            logger.warning("Memory system not initialized")
            return ""
        
        try:
            entry_id = self.memory_system.add_consciousness_state(metrics)
            logger.info(f"Stored consciousness metrics with ID: {entry_id}")
            return entry_id
        except Exception as e:
            logger.error(f"❌ Error storing consciousness metrics: {e}")
            return ""
    
    def get_memory_node_metrics(self) -> Optional[Dict[str, Any]]:
        """Get MemoryMatrixNode metrics from orchestrator"""
        if not self.orchestrator or not self.is_initialized:
            logger.warning("Orchestrator not initialized")
            return None
        
        try:
            state = self.orchestrator.get_current_state()
            node_3_state = state['nodes'].get(3, {})
            return node_3_state.get('memory_metrics', {})
        except Exception as e:
            logger.error(f"❌ Error getting memory node metrics: {e}")
            return None
    
    async def update_bridge(self, sensory_input: Optional[np.ndarray] = None) -> Optional[Dict[str, Any]]:
        """
        Update the bridge with new sensory input and synchronize memory
        
        Args:
            sensory_input: 5D sensory input vector
            
        Returns:
            dict: Integrated state with consciousness and memory metrics
        """
        if not self.is_initialized or not self.bridge_active:
            logger.warning("Bridge not initialized or not active")
            return None
        
        try:
            # Generate random sensory input if none provided
            if sensory_input is None:
                sensory_input = np.random.normal(0, 0.1, 5)
            
            # Update consciousness orchestrator
            if not self.orchestrator:
                raise RuntimeError("Orchestrator not initialized")
            consciousness_state = self.orchestrator.update_system(sensory_input)
            
            # Extract global consciousness metrics
            consciousness_metrics = consciousness_state['global'].copy()
            
            # Store consciousness metrics in Open-A.G.I memory
            self.store_consciousness_metrics(consciousness_metrics)
            
            # Get MemoryMatrixNode metrics
            memory_metrics = self.get_memory_node_metrics()
            
            # Create integrated state
            integrated_state = {
                'timestamp': consciousness_state['time'],
                'consciousness': consciousness_metrics,
                'memory_node': memory_metrics,
                'bridge_status': 'active'
            }
            
            return integrated_state
            
        except Exception as e:
            logger.error(f"❌ Error updating bridge: {e}")
            return None
    
    async def run_bridge_simulation(self, duration: float = 5.0, 
                                  sensory_inputs: Optional[List[np.ndarray]] = None) -> List[Dict[str, Any]]:
        """
        Run a simulation with the memory bridge active
        
        Args:
            duration: Simulation duration in seconds
            sensory_inputs: Optional list of sensory inputs
            
        Returns:
            list: Bridge states over time
        """
        if not self.is_initialized:
            logger.error("Bridge not initialized")
            return []
        
        logger.info(f"Starting bridge simulation for {duration} seconds...")
        
        if not self.orchestrator:
            raise RuntimeError("Orchestrator not initialized")
        n_steps = int(duration / self.orchestrator.dt)
        bridge_states = []
        
        for step in range(n_steps):
            # Get sensory input for this step
            if sensory_inputs and step < len(sensory_inputs):
                sensory = sensory_inputs[step]
            else:
                sensory = np.random.normal(0, 0.2, 5)
            
            # Update bridge
            state = await self.update_bridge(sensory)
            
            if state:
                bridge_states.append(state)
                
                # Log progress
                if step % 50 == 0:
                    c_level = state['consciousness']['consciousness_level']
                    logger.info(f"Step {step}: Consciousness={c_level:.4f}")
        
        logger.info("✅ Bridge simulation completed")
        return bridge_states
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """Get current status of the memory bridge"""
        consciousness_metrics = {}
        memory_metrics = {}
        
        # Get consciousness state if available
        if self.orchestrator:
            try:
                state = self.orchestrator.get_current_state()
                consciousness_metrics = state['global']
                memory_metrics = self.get_memory_node_metrics() or {}
            except Exception as e:
                logger.error(f"Error getting bridge status: {e}")
        
        # Get memory system stats if available
        memory_stats = {}
        if self.memory_system:
            try:
                memory_stats = self.memory_system.get_memory_stats()
            except Exception as e:
                logger.error(f"Error getting memory stats: {e}")
        
        return {
            'bridge_active': self.bridge_active,
            'orchestrator_initialized': self.orchestrator is not None,
            'memory_system_initialized': self.memory_system is not None,
            'consciousness_metrics': consciousness_metrics,
            'memory_metrics': memory_metrics,
            'memory_stats': memory_stats
        }
    
    def shutdown_bridge(self):
        """Shutdown the memory bridge"""
        logger.info("Shutting down Memory Bridge...")
        self.bridge_active = False
        
        # Save memory if system is available
        if self.memory_system:
            try:
                self.memory_system.save_memory()
                logger.info("✅ Memory saved")
            except Exception as e:
                logger.error(f"❌ Error saving memory: {e}")
        
        logger.info("✅ Memory Bridge shutdown completed")

# Pipeline Integration Class
class PipelineMemoryIntegration:
    """Integration for pipeline apps with memory-aware processing"""
    
    def __init__(self, bridge: MemoryBridge):
        self.bridge = bridge
        self.pipeline_active = False
    
    async def initialize_pipeline(self) -> bool:
        """Initialize pipeline integration"""
        if not self.bridge.is_initialized:
            logger.error("Bridge not initialized")
            return False
        
        self.pipeline_active = True
        logger.info("✅ Pipeline integration initialized")
        return True
    
    async def process_with_memory_context(self, data: Any, operation: str) -> Dict[str, Any]:
        """
        Process data with memory context awareness
        
        Args:
            data: Input data to process
            operation: Type of operation to perform
            
        Returns:
            dict: Processing results with memory context
        """
        if not self.pipeline_active:
            logger.warning("Pipeline not active")
            return {"error": "Pipeline not active"}
        
        try:
            # Get current memory context
            bridge_status = self.bridge.get_bridge_status()
            consciousness_level = bridge_status['consciousness_metrics'].get('consciousness_level', 0.0)
            memory_buffer_size = bridge_status['memory_metrics'].get('memory_buffer_size', 0)
            
            # Adjust processing based on consciousness state
            processing_params = {
                'consciousness_level': consciousness_level,
                'memory_load': memory_buffer_size,
                'adaptive_processing': consciousness_level > 0.5  # More intensive processing when conscious
            }
            
            # Simulate processing
            result = {
                'operation': operation,
                'input_data': str(data)[:50] + "..." if len(str(data)) > 50 else str(data),
                'processing_params': processing_params,
                'timestamp': asyncio.get_event_loop().time(),
                'result': f"Processed {operation} with consciousness level {consciousness_level:.4f}"
            }
            
            # Store processing result in memory
            if self.bridge.memory_system:
                entry_id = self.bridge.memory_system.add_rag_context(
                    query=f"Pipeline operation: {operation}",
                    retrieved_context=str(result),
                    sources=[{"source": "pipeline_processing", "score": 1.0}]
                )
                result['memory_entry_id'] = entry_id
            
            logger.info(f"Processed {operation} with consciousness context")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in pipeline processing: {e}")
            return {"error": str(e)}
    
    async def run_pipeline_cycle(self, operations: List[str], data_batch: List[Any]) -> List[Dict[str, Any]]:
        """
        Run a cycle of pipeline operations with memory awareness
        
        Args:
            operations: List of operations to perform
            data_batch: Batch of data to process
            
        Returns:
            list: Results of all operations
        """
        results = []
        
        for i, operation in enumerate(operations):
            # Get data for this operation (cycle through data batch)
            data = data_batch[i % len(data_batch)] if data_batch else f"data_item_{i}"
            
            # Process with memory context
            result = await self.process_with_memory_context(data, operation)
            results.append(result)
            
            # Brief delay to simulate processing time
            await asyncio.sleep(0.01)
        
        return results

# Example usage and demonstration
async def demonstrate_memory_bridge():
    """Demonstrate the memory bridge in action"""
    print("=" * 70)
    print("MEMORY BRIDGE DEMONSTRATION")
    print("=" * 70)
    
    # Create and initialize bridge
    bridge = MemoryBridge("ai_runs/bridge_demo_memory.json")
    if not await bridge.initialize_bridge():
        print("❌ Failed to initialize bridge")
        return False
    
    # Create pipeline integration
    pipeline = PipelineMemoryIntegration(bridge)
    if not await pipeline.initialize_pipeline():
        print("❌ Failed to initialize pipeline")
        return False
    
    # Run bridge simulation
    print("\n1. Running bridge simulation...")
    sensory_inputs = [np.random.normal(0, 0.3, 5) for _ in range(100)]  # 1 second of input
    simulation_results = await bridge.run_bridge_simulation(duration=1.0, sensory_inputs=sensory_inputs)
    
    # Show final bridge status
    print("\n2. Bridge Status:")
    status = bridge.get_bridge_status()
    conscious_metrics = status['consciousness_metrics']
    memory_metrics = status['memory_metrics']
    
    print(f"   Consciousness Level: {conscious_metrics.get('consciousness_level', 0.0):.4f}")
    print(f"   Phi (Integrated Info): {conscious_metrics.get('phi', 0.0):.4f}")
    print(f"   Coherence: {conscious_metrics.get('coherence', 0.0):.4f}")
    print(f"   Memory Buffer Size: {memory_metrics.get('memory_buffer_size', 0)}")
    print(f"   Memory Entries: {status['memory_stats'].get('total_entries', 0)}")
    
    # Run pipeline operations with memory context
    print("\n3. Running pipeline operations with memory context...")
    operations = ["data_analysis", "pattern_recognition", "insight_generation", "decision_making"]
    data_batch = ["sensor_data_1", "sensor_data_2", "sensor_data_3", "sensor_data_4"]
    
    pipeline_results = await pipeline.run_pipeline_cycle(operations, data_batch)
    
    print(f"   Completed {len(pipeline_results)} pipeline operations")
    for i, result in enumerate(pipeline_results[:3]):  # Show first 3 results
        print(f"   Operation {i+1}: {result['operation']} -> {result['result'][:50]}...")
    
    # Shutdown bridge
    print("\n4. Shutting down bridge...")
    bridge.shutdown_bridge()
    
    print("\n" + "=" * 70)
    print("✅ MEMORY BRIDGE DEMONSTRATION COMPLETED")
    print("=" * 70)
    
    return True

# Main execution
if __name__ == "__main__":
    # Run demonstration
    success = asyncio.run(demonstrate_memory_bridge())
    
    if success:
        print("\n🎉 Memory Bridge is working correctly!")
        print("The connection between Metatron-ConscienceAI orchestrator,")
        print("MemoryMatrixNode, and Open-A.G.I framework is established.")
    else:
        print("\n❌ Memory Bridge demonstration failed!")
        print("Please check the error messages above.")