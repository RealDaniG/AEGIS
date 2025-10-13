#!/usr/bin/env python3
"""
Final system verification for MemoryMatrixNode integration.
"""

import sys
import os
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from orchestrator.metatron_orchestrator import MetatronConsciousness


def main():
    print("=== FINAL SYSTEM VERIFICATION ===")
    
    # Initialize consciousness system
    consciousness = MetatronConsciousness()
    
    # Check total nodes
    print(f"Total nodes: {len(consciousness.nodes)}")
    
    # Check Node 3 specifically
    node_3 = consciousness.nodes[3]
    print(f"Node 3 has memory_matrix: {'memory_matrix' in node_3}")
    print(f"Node 3 type: {type(node_3['memory_matrix']).__name__}")
    
    # Run a system update
    state = consciousness.update_system(np.random.randn(5))
    
    # Check memory metrics
    node_3_metrics = state['nodes'][3].get('memory_metrics', {})
    print(f"Memory metrics available: {len(node_3_metrics) > 0}")
    
    if node_3_metrics:
        print(f"Memory buffer size: {node_3_metrics.get('memory_buffer_size', 0)}")
    
    print("✅ SYSTEM VERIFICATION COMPLETE")


if __name__ == "__main__":
    main()