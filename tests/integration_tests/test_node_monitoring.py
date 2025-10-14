import sys
import os
import json

# Add the Metatron-ConscienceAI directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

from orchestrator.metatron_orchestrator import MetatronConsciousness

def test_node_monitoring():
    """Test if all 13 nodes are properly monitored and visualized"""
    print("Testing Metatron Consciousness node monitoring...")
    
    # Initialize the consciousness system
    consciousness_system = MetatronConsciousness()
    
    # Get the current state as would be sent via WebSocket
    state = consciousness_system.get_current_state()
    
    # Prepare WebSocket data format
    websocket_data = {
        "time": float(state['time']),
        "consciousness": {
            "level": float(state['global'].get('consciousness_level', 0)),
            "phi": float(state['global'].get('phi', 0)),
            "coherence": float(state['global'].get('coherence', 0)),
            "depth": int(state['global'].get('recursive_depth', 0)),
            "gamma": float(state['global'].get('gamma_power', 0)),
            "fractal_dim": float(state['global'].get('fractal_dimension', 1)),
            "spiritual": float(state['global'].get('spiritual_awareness', 0)),
            "state": state['global'].get('state_classification', 'unknown'),
            "is_conscious": bool(state['global'].get('is_conscious', False))
        },
        "nodes": {}
    }
    
    # Add node data in WebSocket format
    for node_id, node_data in state['nodes'].items():
        websocket_data['nodes'][str(node_id)] = {
            "output": float(node_data['output']),
            "phase": float(node_data['oscillator']['phase']),
            "amplitude": float(node_data['oscillator']['amplitude']),
            "dimensions": {k: float(v) for k, v in node_data['processor']['dimensions'].items()}
        }
        
        # Check for MemoryMatrixNode metrics
        if int(node_id) == 3 and 'memory_metrics' in node_data:
            websocket_data['nodes'][str(node_id)]['memory_metrics'] = node_data['memory_metrics']
    
    print(f"WebSocket data prepared for {len(websocket_data['nodes'])} nodes")
    
    # Verify all nodes are included
    node_ids = sorted([int(node_id) for node_id in websocket_data['nodes'].keys()])
    print(f"Nodes in WebSocket data: {node_ids}")
    
    # Check specific nodes
    for node_id in range(13):
        node_str_id = str(node_id)
        if node_str_id in websocket_data['nodes']:
            node_data = websocket_data['nodes'][node_str_id]
            print(f"✅ Node {node_id}: Output={node_data['output']:.4f}, Phase={node_data['phase']:.2f}")
            
            # Special check for Node 3 (MemoryMatrixNode)
            if node_id == 3:
                if 'memory_metrics' in node_data:
                    print(f"   🧠 Node 3 Memory Metrics: {node_data['memory_metrics']}")
                else:
                    print(f"   ⚠️ Node 3 missing memory metrics in WebSocket data")
        else:
            print(f"❌ Node {node_id}: MISSING from WebSocket data")
    
    # Save sample data for inspection
    with open('sample_websocket_data.json', 'w') as f:
        json.dump(websocket_data, f, indent=2)
    
    print(f"\nSample WebSocket data saved to sample_websocket_data.json")
    print(f"Total nodes monitored: {len(websocket_data['nodes'])}")
    
    return len(websocket_data['nodes']) == 13

if __name__ == "__main__":
    success = test_node_monitoring()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILURE'}: Node monitoring test {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)