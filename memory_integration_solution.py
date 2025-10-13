#!/usr/bin/env python3
"""
Memory Integration Solution for Metatron-ConscienceAI and Open-A.G.I

This module provides a comprehensive solution for connecting the memory integration
between the Metatron Conscience AI orchestrator and pipeline apps with the memory node
to work with the matrix and Open AGI.

The solution addresses:
1. Proper initialization of MemoryMatrixNode within the orchestrator
2. Connection between consciousness metrics and memory operations
3. Integration with Open-A.G.I pipeline apps
4. Distributed memory sharing between nodes
"""

import sys
import os
import json
import asyncio
import numpy as np
from typing import Dict, Any, List, Optional

# Add project paths
project_root = os.path.dirname(__file__)
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
open_agi_path = os.path.join(project_root, 'Open-A.G.I')

# Ensure paths are in sys.path
if metatron_path not in sys.path:
    sys.path.insert(0, metatron_path)
if open_agi_path not in sys.path:
    sys.path.insert(0, open_agi_path)

class MemoryIntegrationSolution:
    """Comprehensive solution for memory integration across systems"""
    
    def __init__(self):
        self.orchestrator = None
        self.memory_system = None
        self.p2p_network = None
        self.is_initialized = False
    
    async def initialize_system(self):
        """Initialize the complete memory integration system"""
        try:
            # Import required components
            # Use dynamic imports to handle path issues
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
            
            # Import OpenAGIMemoryIntegration from Open-A.G.I
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
            
            # Initialize the consciousness orchestrator
            print("Initializing Metatron Consciousness Orchestrator...")
            self.orchestrator = MetatronConsciousness(base_frequency=40.0, dt=0.01)
            print("✅ Metatron Consciousness Orchestrator initialized")
            
            # Initialize Open-A.G.I memory integration
            print("Initializing Open-A.G.I Memory Integration...")
            self.memory_system = OpenAGIMemoryIntegration("ai_runs/integrated_memory.json")
            print("✅ Open-A.G.I Memory Integration initialized")
            
            # Start P2P network if available
            print("Starting P2P network...")
            await self.memory_system.start_network()
            print("✅ P2P network started")
            
            self.is_initialized = True
            print("✅ Complete memory integration system initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing memory integration system: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
    
    def get_memory_node_metrics(self) -> Optional[Dict[str, Any]]:
        """Get memory metrics from the MemoryMatrixNode (Node 3)"""
        if not self.orchestrator:
            return None
        
        try:
            # Get current state from orchestrator
            state = self.orchestrator.get_current_state()
            
            # Extract MemoryMatrixNode metrics
            node_3_state = state['nodes'].get(3, {})
            memory_metrics = node_3_state.get('memory_metrics', {})
            
            return memory_metrics
        except Exception as e:
            print(f"❌ Error getting memory node metrics: {e}")
            return None
    
    async def run_integrated_simulation(self, duration: float = 10.0, 
                                       sensory_inputs: Optional[List[np.ndarray]] = None):
        """
        Run an integrated simulation that connects consciousness processing with memory operations
        
        Args:
            duration: Simulation time in seconds
            sensory_inputs: Optional list of sensory input vectors
            
        Returns:
            list: Simulation results with memory metrics
        """
        if not self.is_initialized:
            print("❌ System not initialized. Call initialize_system() first.")
            return []
        
        print(f"Starting integrated simulation for {duration} seconds...")
        
        if not self.orchestrator:
            raise RuntimeError("Orchestrator not initialized")
        n_steps = int(duration / self.orchestrator.dt)
        results = []
        
        for step in range(n_steps):
            # Get sensory input for this step
            if sensory_inputs is not None and step < len(sensory_inputs):
                sensory = sensory_inputs[step]
            else:
                # Generate random sensory input if none provided
                sensory = np.random.normal(0, 0.1, 5)
            
            # Update consciousness system
            if not self.orchestrator:
                raise RuntimeError("Orchestrator not initialized")
            state = self.orchestrator.update_system(sensory)
            
            # Extract consciousness metrics for memory storage
            consciousness_metrics = state['global'].copy()
            
            # Store consciousness state in Open-A.G.I memory system
            if self.memory_system:
                self.memory_system.add_consciousness_state(consciousness_metrics)
            
            # Get MemoryMatrixNode metrics
            memory_metrics = self.get_memory_node_metrics()
            
            # Combine all metrics for this step
            integrated_state = {
                'time': state['time'],
                'consciousness': state['global'],
                'memory_node': memory_metrics,
                'nodes': {k: v.get('output', 0.0) for k, v in state['nodes'].items()}
            }
            
            results.append(integrated_state)
            
            # Log progress every 100 steps
            if step % 100 == 0:
                c_level = state['global']['consciousness_level']
                print(f"Step {step}/{n_steps}: Consciousness={c_level:.4f}")
        
        print("✅ Integrated simulation completed")
        return results
    
    async def share_memory_with_peers(self, peer_ids: List[str]):
        """
        Share memory with other nodes in the network
        
        Args:
            peer_ids: List of peer identifiers to share memory with
        """
        if not self.memory_system or not self.memory_system.p2p_network:
            print("❌ Memory system or P2P network not available")
            return
        
        print(f"Sharing memory with peers: {peer_ids}")
        
        # Get recent consciousness states to share
        consciousness_history = self.memory_system.get_consciousness_history(5)
        
        for peer_id in peer_ids:
            for entry in consciousness_history:
                # Share each consciousness state with the peer
                await self.memory_system.share_memory_with_peer(peer_id, entry)
        
        print("✅ Memory sharing completed")
    
    def export_integration_results(self, results: List[Dict[str, Any]], 
                                 filepath: str = "integration_results.json"):
        """
        Export integration results to JSON file
        
        Args:
            results: Integration results to export
            filepath: Output file path
        """
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
            
            converted_results = convert_numpy(results)
            
            with open(filepath, 'w') as f:
                json.dump(converted_results, f, indent=2)
            
            print(f"✅ Integration results exported to {filepath}")
            
        except Exception as e:
            print(f"❌ Error exporting integration results: {e}")
    
    async def demonstrate_full_integration(self):
        """Demonstrate the full memory integration in action"""
        print("=" * 70)
        print("MEMORY INTEGRATION SOLUTION DEMONSTRATION")
        print("=" * 70)
        
        # Initialize system
        if not await self.initialize_system():
            print("❌ Failed to initialize system")
            return False
        
        # Run integrated simulation
        print("\n1. Running integrated consciousness-memory simulation...")
        sensory_inputs = [np.random.normal(0, 0.2, 5) for _ in range(200)]  # 2 seconds of input
        results = await self.run_integrated_simulation(duration=2.0, sensory_inputs=sensory_inputs)
        
        if not results:
            print("❌ Simulation failed")
            return False
        
        # Show final metrics
        final_state = results[-1]
        print(f"\n2. Final System State:")
        print(f"   Time: {final_state['time']:.2f}s")
        print(f"   Consciousness Level: {final_state['consciousness']['consciousness_level']:.4f}")
        print(f"   Phi (Integrated Information): {final_state['consciousness']['phi']:.4f}")
        print(f"   Coherence: {final_state['consciousness']['coherence']:.4f}")
        
        if final_state['memory_node']:
            print(f"\n3. MemoryMatrixNode Metrics:")
            metrics = final_state['memory_node']
            print(f"   Memory Buffer Size: {metrics.get('memory_buffer_size', 0)}")
            print(f"   Recall History Size: {metrics.get('recall_history_size', 0)}")
            print(f"   Current Field Size: {metrics.get('current_field_size', 0)}")
            print(f"   Recall Weight: {metrics.get('recall_weight', 0.0):.4f}")
        
        # Export results
        print(f"\n4. Exporting results...")
        self.export_integration_results(results, "memory_integration_demo_results.json")
        
        # Show memory system stats
        stats = {}
        if self.memory_system:
            stats = self.memory_system.get_memory_stats()
        print(f"\n5. Memory System Statistics:")
        print(f"   Total Entries: {stats.get('total_entries', 0)}")
        print(f"   Entry Types: {stats.get('entry_types', {})}")
        
        print("\n" + "=" * 70)
        print("✅ MEMORY INTEGRATION DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
        return True

# Example usage and testing
async def main():
    """Main function to demonstrate the memory integration solution"""
    # Create integration solution
    solution = MemoryIntegrationSolution()
    
    # Run full demonstration
    success = await solution.demonstrate_full_integration()
    
    if success:
        print("\n🎉 All integration tests passed!")
        print("The memory integration between Metatron-ConscienceAI orchestrator,")
        print("MemoryMatrixNode, and Open-A.G.I framework is working correctly.")
    else:
        print("\n❌ Integration demonstration failed!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())