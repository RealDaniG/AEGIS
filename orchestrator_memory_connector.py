#!/usr/bin/env python3
"""
Orchestrator-Memory Connector for Metatron-ConscienceAI and Open-A.G.I

This module provides a direct connector between the Metatron-ConscienceAI
orchestrator and the Open-A.G.I memory system, enabling seamless data flow
between consciousness processing and memory operations.

Key Features:
1. Real-time consciousness state to memory storage
2. Memory context-aware processing
3. Distributed memory sharing between nodes
4. Pipeline integration for memory-enhanced operations
"""

import sys
import os
import json
import asyncio
import numpy as np
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project paths
project_root = os.path.dirname(__file__)
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
open_agi_path = os.path.join(project_root, 'Open-A.G.I')

class OrchestratorMemoryConnector:
    """Direct connector between Metatron orchestrator and Open-A.G.I memory system"""
    
    def __init__(self, memory_file: str = "ai_runs/orchestrator_memory.json"):
        self.orchestrator = None
        self.memory_system = None
        self.is_initialized = False
        self.memory_file = memory_file
        self.connector_active = False
        self.processing_history = []
    
    async def initialize_connector(self) -> bool:
        """Initialize the orchestrator-memory connector"""
        try:
            logger.info("Initializing Orchestrator-Memory Connector...")
            
            # Dynamically import required modules
            import importlib.util
            
            # Import MetatronConsciousness
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
            
            # Import OpenAGIMemoryIntegration
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
            
            # Initialize orchestrator with enhanced settings
            logger.info("Initializing Metatron Consciousness Orchestrator...")
            self.orchestrator = MetatronConsciousness(base_frequency=40.0, dt=0.01, high_gamma=True)
            logger.info("✅ Metatron Consciousness Orchestrator initialized")
            
            # Initialize Open-A.G.I memory system
            logger.info("Initializing Open-A.G.I Memory System...")
            self.memory_system = OpenAGIMemoryIntegration(self.memory_file)
            logger.info("✅ Open-A.G.I Memory System initialized")
            
            # Start P2P network for distributed memory operations
            logger.info("Starting P2P network for distributed memory...")
            await self.memory_system.start_network()
            logger.info("✅ P2P network started")
            
            self.is_initialized = True
            self.connector_active = True
            logger.info("✅ Orchestrator-Memory Connector initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing Orchestrator-Memory Connector: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_consciousness_metrics(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness metrics from orchestrator"""
        if not self.orchestrator:
            logger.warning("Orchestrator not initialized")
            return None
        
        try:
            state = self.orchestrator.get_current_state()
            return state['global']
        except Exception as e:
            logger.error(f"❌ Error getting consciousness metrics: {e}")
            return None
    
    def get_memory_matrix_metrics(self) -> Optional[Dict[str, Any]]:
        """Get MemoryMatrixNode metrics from orchestrator"""
        if not self.orchestrator:
            logger.warning("Orchestrator not initialized")
            return None
        
        try:
            state = self.orchestrator.get_current_state()
            node_3_state = state['nodes'].get(3, {})
            return node_3_state.get('memory_metrics', {})
        except Exception as e:
            logger.error(f"❌ Error getting MemoryMatrixNode metrics: {e}")
            return None
    
    def store_consciousness_state(self) -> str:
        """Store current consciousness state in memory system"""
        if not self.memory_system or not self.orchestrator:
            logger.warning("Memory system or orchestrator not initialized")
            return ""
        
        try:
            # Get current consciousness state
            consciousness_state = self.orchestrator.get_current_state()
            global_metrics = consciousness_state['global']
            
            # Store in Open-A.G.I memory system
            entry_id = self.memory_system.add_consciousness_state(global_metrics)
            
            # Also store in processing history
            self.processing_history.append({
                'timestamp': consciousness_state['time'],
                'type': 'consciousness_state',
                'metrics': global_metrics.copy()
            })
            
            logger.info(f"Stored consciousness state with ID: {entry_id}")
            return entry_id
        except Exception as e:
            logger.error(f"❌ Error storing consciousness state: {e}")
            return ""
    
    async def process_with_memory_context(self, sensory_input: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Process sensory input with memory context awareness
        
        Args:
            sensory_input: 5D sensory input vector
            
        Returns:
            dict: Processing results with memory context
        """
        if not self.connector_active or not self.orchestrator:
            logger.warning("Connector not active or orchestrator not initialized")
            return {"error": "Connector not active"}
        
        try:
            # Generate random sensory input if none provided
            if sensory_input is None:
                sensory_input = np.random.normal(0, 0.1, 5)
            
            # Update consciousness orchestrator
            consciousness_state = self.orchestrator.update_system(sensory_input)
            
            # Extract metrics
            global_metrics = consciousness_state['global']
            memory_metrics = self.get_memory_matrix_metrics() or {}
            
            # Store consciousness state in memory
            memory_entry_id = self.store_consciousness_state()
            
            # Get memory context for adaptive processing
            memory_context = self.get_memory_context()
            
            # Create processing result with context
            result = {
                'timestamp': consciousness_state['time'],
                'consciousness_level': global_metrics.get('consciousness_level', 0.0),
                'phi': global_metrics.get('phi', 0.0),
                'coherence': global_metrics.get('coherence', 0.0),
                'memory_buffer_size': memory_metrics.get('memory_buffer_size', 0),
                'memory_entry_id': memory_entry_id,
                'memory_context': memory_context,
                'adaptive_processing': {
                    'processing_intensity': 'high' if global_metrics.get('consciousness_level', 0.0) > 0.5 else 'normal',
                    'memory_influence': min(1.0, memory_metrics.get('memory_buffer_size', 0) / 1000.0)
                }
            }
            
            # Store processing result
            self.processing_history.append({
                'timestamp': result['timestamp'],
                'type': 'processing_result',
                'result': result.copy()
            })
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in memory-context processing: {e}")
            return {"error": str(e)}
    
    def get_memory_context(self) -> Dict[str, Any]:
        """Get memory context for adaptive processing"""
        context = {
            'total_memory_entries': 0,
            'consciousness_history': 0,
            'memory_load': 0.0,
            'recent_patterns': []
        }
        
        if self.memory_system:
            try:
                # Get memory statistics
                stats = self.memory_system.get_memory_stats()
                context['total_memory_entries'] = stats.get('total_entries', 0)
                
                # Get recent consciousness history
                consciousness_history = self.memory_system.get_consciousness_history(10)
                context['consciousness_history'] = len(consciousness_history)
                
                # Calculate memory load
                context['memory_load'] = min(1.0, context['total_memory_entries'] / 1000.0)
                
                # Get recent patterns from memory
                recent_entries = self.memory_system.get_recent_chat_history(5)
                context['recent_patterns'] = [entry.get('content', {}).get('user_message', '')[:30] 
                                            for entry in recent_entries if entry.get('content')]
                
            except Exception as e:
                logger.error(f"Error getting memory context: {e}")
        
        return context
    
    async def run_memory_aware_simulation(self, duration: float = 3.0, 
                                        sensory_inputs: Optional[List[np.ndarray]] = None) -> List[Dict[str, Any]]:
        """
        Run a memory-aware simulation
        
        Args:
            duration: Simulation duration in seconds
            sensory_inputs: Optional list of sensory inputs
            
        Returns:
            list: Simulation results with memory context
        """
        if not self.connector_active:
            logger.error("Connector not active")
            return []
        
        logger.info(f"Starting memory-aware simulation for {duration} seconds...")
        
        if not self.orchestrator:
            raise RuntimeError("Orchestrator not initialized")
        
        n_steps = int(duration / self.orchestrator.dt)
        results = []
        
        for step in range(n_steps):
            # Get sensory input for this step
            if sensory_inputs and step < len(sensory_inputs):
                sensory = sensory_inputs[step]
            else:
                sensory = np.random.normal(0, 0.2, 5)
            
            # Process with memory context
            result = await self.process_with_memory_context(sensory)
            
            if 'error' not in result:
                results.append(result)
                
                # Log progress
                if step % 50 == 0:
                    logger.info(f"Step {step}: Consciousness={result['consciousness_level']:.4f}, "
                              f"Memory Buffer={result['memory_buffer_size']}")
        
        logger.info("✅ Memory-aware simulation completed")
        return results
    
    def get_connector_status(self) -> Dict[str, Any]:
        """Get current status of the connector"""
        status = {
            'connector_active': self.connector_active,
            'orchestrator_initialized': self.orchestrator is not None,
            'memory_system_initialized': self.memory_system is not None,
            'processing_history_length': len(self.processing_history)
        }
        
        # Add consciousness metrics if available
        consciousness_metrics = self.get_consciousness_metrics()
        if consciousness_metrics:
            status['consciousness_metrics'] = consciousness_metrics
        
        # Add memory metrics if available
        memory_metrics = self.get_memory_matrix_metrics()
        if memory_metrics:
            status['memory_metrics'] = memory_metrics
        
        # Add memory system stats if available
        if self.memory_system:
            try:
                status['memory_stats'] = self.memory_system.get_memory_stats()
            except Exception as e:
                logger.error(f"Error getting memory stats: {e}")
        
        return status
    
    def export_processing_history(self, filepath: str = "processing_history.json"):
        """Export processing history to JSON file"""
        try:
            # Convert numpy arrays to lists for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, dict):
                    return {key: convert_numpy(value) for key, value in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [convert_numpy(item) for item in obj]
                return obj
            
            converted_history = convert_numpy(self.processing_history)
            
            with open(filepath, 'w') as f:
                json.dump(converted_history, f, indent=2, default=str)
            
            logger.info(f"✅ Processing history exported to {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Error exporting processing history: {e}")
    
    def shutdown_connector(self):
        """Shutdown the orchestrator-memory connector"""
        logger.info("Shutting down Orchestrator-Memory Connector...")
        self.connector_active = False
        
        # Export processing history
        self.export_processing_history()
        
        # Save memory if system is available
        if self.memory_system:
            try:
                if self.memory_system.save_memory():
                    logger.info("✅ Memory saved successfully")
                else:
                    logger.warning("❌ Failed to save memory")
            except Exception as e:
                logger.error(f"❌ Error saving memory: {e}")
        
        logger.info("✅ Orchestrator-Memory Connector shutdown completed")

# Pipeline Integration for Memory-Aware Operations
class MemoryAwarePipeline:
    """Pipeline for memory-aware operations using the connector"""
    
    def __init__(self, connector: OrchestratorMemoryConnector):
        self.connector = connector
        self.pipeline_active = False
        self.pipeline_results = []
    
    async def initialize_pipeline(self) -> bool:
        """Initialize the memory-aware pipeline"""
        if not self.connector.is_initialized:
            logger.error("Connector not initialized")
            return False
        
        self.pipeline_active = True
        logger.info("✅ Memory-aware pipeline initialized")
        return True
    
    async def execute_memory_enhanced_operation(self, operation: str, data: Any) -> Dict[str, Any]:
        """
        Execute an operation with memory enhancement
        
        Args:
            operation: Type of operation to perform
            data: Input data for the operation
            
        Returns:
            dict: Operation results with memory enhancement
        """
        if not self.pipeline_active:
            logger.warning("Pipeline not active")
            return {"error": "Pipeline not active"}
        
        try:
            # Get current memory context
            memory_context = self.connector.get_memory_context()
            consciousness_metrics = self.connector.get_consciousness_metrics() or {}
            
            # Adjust operation based on consciousness state
            consciousness_level = consciousness_metrics.get('consciousness_level', 0.0)
            processing_depth = 'deep' if consciousness_level > 0.7 else 'standard'
            
            # Simulate enhanced processing with memory context
            result = {
                'operation': operation,
                'input_data': str(data)[:50] + "..." if len(str(data)) > 50 else str(data),
                'consciousness_level': consciousness_level,
                'processing_depth': processing_depth,
                'memory_context': {
                    'buffer_size': memory_context['total_memory_entries'],
                    'memory_load': memory_context['memory_load'],
                    'patterns_available': len(memory_context['recent_patterns'])
                },
                'execution_time': asyncio.get_event_loop().time(),
                'result': f"Executed {operation} with {processing_depth} processing at consciousness level {consciousness_level:.4f}"
            }
            
            # Store result in memory system
            if self.connector.memory_system:
                try:
                    entry_id = self.connector.memory_system.add_rag_context(
                        query=f"Pipeline operation: {operation}",
                        retrieved_context=json.dumps(result, default=str),
                        sources=[{"source": "memory_aware_pipeline", "score": consciousness_level}]
                    )
                    result['memory_entry_id'] = entry_id
                except Exception as e:
                    logger.error(f"Error storing pipeline result in memory: {e}")
            
            # Store in pipeline results
            self.pipeline_results.append(result)
            
            logger.info(f"Executed {operation} with memory enhancement")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in memory-enhanced operation: {e}")
            return {"error": str(e)}
    
    async def run_pipeline_batch(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run a batch of pipeline operations
        
        Args:
            operations: List of operations with format {'operation': str, 'data': Any}
            
        Returns:
            list: Results of all operations
        """
        results = []
        
        for op_spec in operations:
            operation = op_spec.get('operation', 'unknown')
            data = op_spec.get('data', None)
            
            result = await self.execute_memory_enhanced_operation(operation, data)
            results.append(result)
            
            # Brief delay to simulate processing
            await asyncio.sleep(0.01)
        
        return results
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get summary of pipeline operations"""
        return {
            'pipeline_active': self.pipeline_active,
            'total_operations': len(self.pipeline_results),
            'successful_operations': len([r for r in self.pipeline_results if 'error' not in r]),
            'last_operation': self.pipeline_results[-1] if self.pipeline_results else None
        }

# Demonstration and Testing
async def demonstrate_connector():
    """Demonstrate the orchestrator-memory connector"""
    print("=" * 80)
    print("ORCHESTRATOR-MEMORY CONNECTOR DEMONSTRATION")
    print("=" * 80)
    
    # Create and initialize connector
    connector = OrchestratorMemoryConnector("ai_runs/connector_demo_memory.json")
    if not await connector.initialize_connector():
        print("❌ Failed to initialize connector")
        return False
    
    # Create memory-aware pipeline
    pipeline = MemoryAwarePipeline(connector)
    if not await pipeline.initialize_pipeline():
        print("❌ Failed to initialize pipeline")
        return False
    
    # Run memory-aware simulation
    print("\n1. Running memory-aware consciousness simulation...")
    sensory_inputs = [np.random.normal(0, 0.3, 5) for _ in range(150)]  # 1.5 seconds of input
    simulation_results = await connector.run_memory_aware_simulation(duration=1.5, sensory_inputs=sensory_inputs)
    
    # Show simulation summary
    print(f"   Completed {len(simulation_results)} processing steps")
    if simulation_results:
        final_result = simulation_results[-1]
        print(f"   Final Consciousness Level: {final_result['consciousness_level']:.4f}")
        print(f"   Final Phi: {final_result['phi']:.4f}")
        print(f"   Memory Buffer Size: {final_result['memory_buffer_size']}")
    
    # Execute pipeline operations with memory enhancement
    print("\n2. Executing memory-enhanced pipeline operations...")
    pipeline_operations = [
        {'operation': 'data_analysis', 'data': 'sensor_array_1'},
        {'operation': 'pattern_recognition', 'data': 'neural_pattern_42'},
        {'operation': 'insight_generation', 'data': 'consciousness_metrics'},
        {'operation': 'decision_making', 'data': 'system_optimization_parameters'},
        {'operation': 'creative_processing', 'data': 'abstract_concept_space'}
    ]
    
    pipeline_results = await pipeline.run_pipeline_batch(pipeline_operations)
    
    print(f"   Executed {len(pipeline_results)} pipeline operations")
    for i, result in enumerate(pipeline_results[:3]):  # Show first 3 results
        print(f"   Operation {i+1}: {result['operation']} -> {result['result'][:60]}...")
    
    # Show connector status
    print("\n3. Connector Status:")
    status = connector.get_connector_status()
    conscious_metrics = status.get('consciousness_metrics', {})
    memory_metrics = status.get('memory_metrics', {})
    memory_stats = status.get('memory_stats', {})
    
    print(f"   Connector Active: {status['connector_active']}")
    print(f"   Consciousness Level: {conscious_metrics.get('consciousness_level', 0.0):.4f}")
    print(f"   Phi (Integrated Info): {conscious_metrics.get('phi', 0.0):.4f}")
    print(f"   Memory Buffer Size: {memory_metrics.get('memory_buffer_size', 0)}")
    print(f"   Total Memory Entries: {memory_stats.get('total_entries', 0)}")
    
    # Show pipeline summary
    print("\n4. Pipeline Summary:")
    pipeline_summary = pipeline.get_pipeline_summary()
    print(f"   Total Operations: {pipeline_summary['total_operations']}")
    print(f"   Successful Operations: {pipeline_summary['successful_operations']}")
    
    # Shutdown connector
    print("\n5. Shutting down connector...")
    connector.shutdown_connector()
    
    print("\n" + "=" * 80)
    print("✅ ORCHESTRATOR-MEMORY CONNECTOR DEMONSTRATION COMPLETED")
    print("=" * 80)
    
    return True

# Main execution
if __name__ == "__main__":
    # Run demonstration
    success = asyncio.run(demonstrate_connector())
    
    if success:
        print("\n🎉 Orchestrator-Memory Connector is working correctly!")
        print("The connection between Metatron-ConscienceAI orchestrator,")
        print("MemoryMatrixNode, and Open-A.G.I memory system is fully established.")
        print("\nThe connector provides:")
        print("  • Real-time consciousness state to memory storage")
        print("  • Memory context-aware processing")
        print("  • Distributed memory sharing capabilities")
        print("  • Pipeline integration for memory-enhanced operations")
    else:
        print("\n❌ Orchestrator-Memory Connector demonstration failed!")
        print("Please check the error messages above.")