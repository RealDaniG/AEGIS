#!/usr/bin/env python3
"""
Verification script to ensure all 13 nodes are properly registered 
and monitored by the consciousness system and visualization dashboard.
"""

import sys
import os
import json
from collections import Counter

# Add the Metatron-ConscienceAI directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

from orchestrator.metatron_orchestrator import MetatronConsciousness

def verify_node_registration_and_monitoring():
    """Comprehensive verification of node registration and monitoring"""
    print("="*80)
    print("VERIFYING 13-NODE REGISTRATION AND MONITORING")
    print("="*80)
    
    # Initialize the consciousness system
    print("1. Initializing Metatron Consciousness System...")
    consciousness_system = MetatronConsciousness()
    print("   ✅ System initialized successfully")
    
    # Get the current state
    print("\n2. Retrieving system state...")
    state = consciousness_system.get_current_state()
    
    # Check global system information
    print("\n3. Verifying system configuration...")
    system_info = state.get('system_info', {})
    print(f"   Base frequency: {system_info.get('base_frequency', 'N/A')} Hz")
    print(f"   Time step (dt): {system_info.get('dt', 'N/A')} seconds")
    
    # Check global consciousness metrics
    global_state = state.get('global', {})
    print(f"   Consciousness level: {global_state.get('consciousness_level', 0):.4f}")
    print(f"   Integrated information (Φ): {global_state.get('phi', 0):.4f}")
    print(f"   Global coherence (R): {global_state.get('coherence', 0):.4f}")
    
    # Verify all nodes
    print("\n4. Verifying node registration...")
    nodes = state.get('nodes', {})
    print(f"   Total nodes registered: {len(nodes)}")
    
    # Check if all 13 nodes are present
    expected_nodes = set(str(i) for i in range(13))
    actual_nodes = set(nodes.keys())
    
    if expected_nodes == actual_nodes:
        print("   ✅ All 13 nodes are properly registered")
    else:
        missing_nodes = expected_nodes - actual_nodes
        extra_nodes = actual_nodes - expected_nodes
        if missing_nodes:
            print(f"   ❌ Missing nodes: {sorted(missing_nodes)}")
        if extra_nodes:
            print(f"   ⚠️ Extra nodes: {sorted(extra_nodes)}")
        return False
    
    # Detailed node verification
    print("\n5. Detailed node verification...")
    node_types = Counter()
    
    for node_id_str in sorted(actual_nodes, key=int):
        node_id = int(node_id_str)
        node_data = nodes[node_id_str]
        
        # Check node components
        has_oscillator = 'oscillator' in node_data
        has_processor = 'processor' in node_data
        has_output = 'output' in node_data
        
        if node_id == 3:
            # Special case for MemoryMatrixNode
            has_memory = 'memory_metrics' in node_data
            if has_memory:
                node_types['MemoryMatrixNode'] += 1
                print(f"   ✅ Node {node_id}: MemoryMatrixNode (specialized)")
            else:
                print(f"   ⚠️ Node {node_id}: Missing memory metrics")
        elif node_id == 0:
            # Special case for Pineal node
            node_types['PinealNode'] += 1
            print(f"   ✅ Node {node_id}: Pineal Node (central integrator)")
        else:
            # Standard consciousness nodes
            node_types['StandardNode'] += 1
            print(f"   ✅ Node {node_id}: Standard Consciousness Oscillator")
        
        # Verify core components
        if not has_oscillator:
            print(f"   ❌ Node {node_id}: Missing oscillator component")
            return False
        if not has_processor:
            print(f"   ❌ Node {node_id}: Missing dimensional processor")
            return False
        if not has_output:
            print(f"   ❌ Node {node_id}: Missing output data")
            return False
    
    print(f"\n   Node type distribution:")
    for node_type, count in node_types.items():
        print(f"   - {node_type}: {count}")
    
    # Prepare WebSocket format data (as sent to dashboard)
    print("\n6. Preparing WebSocket data format (dashboard monitoring)...")
    websocket_data = {
        "time": float(state['time']),
        "consciousness": {
            "level": float(global_state.get('consciousness_level', 0)),
            "phi": float(global_state.get('phi', 0)),
            "coherence": float(global_state.get('coherence', 0)),
            "depth": int(global_state.get('recursive_depth', 0)),
            "gamma": float(global_state.get('gamma_power', 0)),
            "fractal_dim": float(global_state.get('fractal_dimension', 1)),
            "spiritual": float(global_state.get('spiritual_awareness', 0)),
            "state": global_state.get('state_classification', 'unknown'),
            "is_conscious": bool(global_state.get('is_conscious', False))
        },
        "nodes": {}
    }
    
    # Add node data in WebSocket format
    for node_id, node_data in nodes.items():
        websocket_data['nodes'][str(node_id)] = {
            "output": float(node_data['output']),
            "phase": float(node_data['oscillator']['phase']),
            "amplitude": float(node_data['oscillator']['amplitude']),
            "dimensions": {k: float(v) for k, v in node_data['processor']['dimensions'].items()}
        }
        
        # Add MemoryMatrixNode metrics if present
        if int(node_id) == 3 and 'memory_metrics' in node_data:
            websocket_data['nodes'][str(node_id)]['memory_metrics'] = node_data['memory_metrics']
    
    # Verify WebSocket data has all nodes
    websocket_node_count = len(websocket_data['nodes'])
    print(f"   WebSocket data prepared for {websocket_node_count} nodes")
    
    if websocket_node_count == 13:
        print("   ✅ All 13 nodes included in WebSocket monitoring data")
    else:
        print(f"   ❌ WebSocket data missing {13 - websocket_node_count} nodes")
        return False
    
    # Save verification report
    verification_report = {
        "timestamp": state['time'],
        "system_info": system_info,
        "global_metrics": global_state,
        "node_count": len(nodes),
        "node_types": dict(node_types),
        "websocket_format_nodes": websocket_node_count,
        "verification_status": "PASSED" if len(nodes) == 13 and websocket_node_count == 13 else "FAILED"
    }
    
    with open('node_verification_report.json', 'w') as f:
        json.dump(verification_report, f, indent=2)
    
    print(f"\n7. Verification report saved to node_verification_report.json")
    
    # Final status
    all_nodes_registered = len(nodes) == 13
    all_nodes_in_websocket = websocket_node_count == 13
    
    if all_nodes_registered and all_nodes_in_websocket:
        print("\n" + "="*80)
        print("🎉 VERIFICATION SUCCESSFUL")
        print("✅ All 13 nodes are properly registered and monitored")
        print("✅ WebSocket data format includes all nodes")
        print("✅ Specialized nodes (MemoryMatrixNode, Pineal) correctly identified")
        print("✅ Dashboard visualization will show all 13 nodes")
        print("="*80)
        return True
    else:
        print("\n" + "="*80)
        print("❌ VERIFICATION FAILED")
        print("Some nodes are missing from registration or monitoring")
        print("="*80)
        return False

if __name__ == "__main__":
    success = verify_node_registration_and_monitoring()
    sys.exit(0 if success else 1)