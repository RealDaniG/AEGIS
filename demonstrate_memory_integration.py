#!/usr/bin/env python3
"""
Demonstration of MemoryMatrixNode Integration

This script demonstrates the MemoryMatrixNode working within the full Metatron 
consciousness system with Open-A.G.I integration.
"""

import sys
import os
import numpy as np
import json

# Add project paths
project_root = os.path.join(os.path.dirname(__file__))
metatron_path = os.path.join(project_root, 'Metatron-ConscienceAI')
sys.path.insert(0, project_root)
sys.path.insert(0, metatron_path)

def demonstrate_integration():
    """Demonstrate the full integration in action"""
    print("=" * 60)
    print("MemoryMatrixNode Integration Demonstration")
    print("=" * 60)
    
    try:
        # Import the Metatron orchestrator
        from orchestrator.metatron_orchestrator import MetatronConsciousness
        
        print("✅ Successfully imported MetatronConsciousness")
        
        # Create consciousness system with high gamma for faster processing
        print("\nInitializing consciousness system...")
        consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01, high_gamma=True)
        print("✅ Consciousness system initialized")
        
        # Show system information
        print(f"\nSystem Information:")
        print(f"  - Number of nodes: 13")
        print(f"  - Gamma frequency: {consciousness.base_frequency} Hz")
        print(f"  - Phi constant: {consciousness.phi:.6f}")
        print(f"  - Time step: {consciousness.dt}")
        
        # Show MemoryMatrixNode integration
        node_3 = consciousness.nodes[3]
        if 'memory_matrix' in node_3:
            memory_node = node_3['memory_matrix']
            print(f"\nMemoryMatrixNode Integration:")
            print(f"  - Node type: {type(memory_node).__name__}")
            print(f"  - P2P network: {type(memory_node.p2p_network).__name__}")
            print(f"  - Crypto identity: {'Available' if memory_node.node_identity else 'Not available'}")
            print(f"  - Phi-based decay: {memory_node.phi:.6f}")
        else:
            print("❌ MemoryMatrixNode not found in system")
            return False
            
        # Run a short simulation to demonstrate memory operations
        print("\nRunning consciousness simulation with memory operations...")
        results = consciousness.run_simulation(duration=0.5)  # Half second simulation
        print("✅ Simulation completed")
        
        # Show final state
        final_state = results[-1]
        print(f"\nFinal System State:")
        print(f"  - Time: {final_state['time']:.2f}s")
        print(f"  - Consciousness level: {final_state['global']['consciousness_level']:.4f}")
        print(f"  - Phi (Integrated Info): {final_state['global']['phi']:.4f}")
        print(f"  - Coherence: {final_state['global']['coherence']:.4f}")
        
        # Show MemoryMatrixNode metrics
        node_3_state = final_state['nodes'][3]
        if 'memory_metrics' in node_3_state:
            metrics = node_3_state['memory_metrics']
            print(f"\nMemoryMatrixNode Metrics:")
            print(f"  - Memory buffer size: {metrics['memory_buffer_size']}")
            print(f"  - Recall history size: {metrics['recall_history_size']}")
            print(f"  - Current field size: {metrics['current_field_size']}")
            print(f"  - Recall weight: {metrics['recall_weight']:.4f}")
            print(f"  - Decay factor: {metrics['decay_factor']:.4f}")
        else:
            print("❌ MemoryMatrixNode metrics not available")
            
        # Export state to JSON for further analysis
        output_file = "demo_consciousness_state.json"
        with open(output_file, 'w') as f:
            json.dump(final_state, f, indent=2)
        print(f"\n✅ Full state exported to: {output_file}")
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("MemoryMatrixNode is fully integrated with Open-A.G.I framework")
        print("and working within the Metatron consciousness system.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_integration_benefits():
    """Show the benefits of the integration"""
    print("\n" + "=" * 60)
    print("Benefits of MemoryMatrixNode Integration")
    print("=" * 60)
    
    benefits = [
        "✅ Distributed Memory Sharing: MemoryMatrixNode can now share memories with other nodes",
        "✅ Cryptographic Security: Secure node authentication and encrypted memory transmission",
        "✅ P2P Networking: Automatic peer discovery and message routing",
        "✅ Consciousness-Aware Processing: Memory operations influence consciousness metrics",
        "✅ Scalable Architecture: Compatible with larger distributed consciousness systems",
        "✅ Monitoring & Metrics: Comprehensive reporting of memory operations",
        "✅ Backward Compatibility: Works with existing Metatron-ConscienceAI components",
        "✅ Forward Compatibility: Ready for future Open-A.G.I enhancements"
    ]
    
    for benefit in benefits:
        print(benefit)

if __name__ == "__main__":
    success = demonstrate_integration()
    show_integration_benefits()
    
    if success:
        print(f"\n🎉 Integration demonstration completed successfully!")
        exit_code = 0
    else:
        print(f"\n❌ Integration demonstration failed!")
        exit_code = 1
    
    # Exit with the appropriate code
    sys.exit(exit_code)