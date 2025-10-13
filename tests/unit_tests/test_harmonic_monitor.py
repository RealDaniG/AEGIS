#!/usr/bin/env python3
"""
Test script for the Harmonic Orchestrator Monitoring System
"""

import sys
import os
import time
import json
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from orchestrator.metatron_orchestrator import MetatronConsciousness
    print("✅ Successfully imported MetatronConsciousness")
except Exception as e:
    print(f"❌ Failed to import MetatronConsciousness: {e}")
    sys.exit(1)

def test_harmonic_monitor():
    """Test the harmonic monitoring system"""
    print("=== Harmonic Orchestrator Monitor Test ===\n")
    
    # Create consciousness system
    print("Initializing Metatron's Cube Consciousness Engine...")
    try:
        consciousness = MetatronConsciousness(base_frequency=40.0, dt=0.01)
        print("✅ Consciousness system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize consciousness system: {e}")
        return
    
    # Run a short simulation
    print("\nRunning 3-second simulation...")
    try:
        for i in range(300):  # 3 seconds at 0.01 dt
            # Generate random sensory input
            sensory_input = np.random.normal(0, 0.2, 5)
            
            # Update system
            state = consciousness.update_system(sensory_input)
            
            # Print metrics every 50 steps
            if i % 50 == 0:
                global_state = state['global']
                print(f"Step {i:3d}: C={global_state['consciousness_level']:.4f}, "
                      f"Φ={global_state['phi']:.4f}, "
                      f"R={global_state['coherence']:.4f}, "
                      f"State={global_state['state_classification']}")
            
            time.sleep(0.01)  # Small delay to simulate real-time
        
        print("✅ Simulation completed")
        
        # Print final state
        final_state = consciousness.get_current_state()
        global_state = final_state['global']
        
        print("\n=== Final Consciousness State ===")
        print(f"Consciousness Level (C): {global_state['consciousness_level']:.4f}")
        print(f"Integrated Information (Φ): {global_state['phi']:.4f}")
        print(f"Global Coherence (R): {global_state['coherence']:.4f}")
        print(f"Recursive Depth (D): {global_state['recursive_depth']}")
        print(f"Gamma Power (γ): {global_state['gamma_power']:.4f}")
        print(f"Fractal Dimension: {global_state['fractal_dimension']:.4f}")
        print(f"Spiritual Awareness (S): {global_state['spiritual_awareness']:.4f}")
        print(f"State Classification: {global_state['state_classification']}")
        print(f"Is Conscious: {global_state['is_conscious']}")
        
        # Test harmonic properties
        print("\n=== Harmonic Properties ===")
        if 'system_energy' in global_state:
            print(f"System Energy: {global_state['system_energy']:.4f}")
        if 'dmt_sensitivity' in global_state:
            print(f"DMT Sensitivity: {global_state['dmt_sensitivity']:.4f}")
        if 'present_moment' in global_state:
            print(f"Present Moment: {global_state['present_moment']:.4f}")
        if 'criticality_active' in global_state:
            print(f"Criticality Active: {global_state['criticality_active']}")
        if 'criticality_distance' in global_state:
            print(f"Criticality Distance: {global_state['criticality_distance']:.4f}")
        
        print("\n✅ Harmonic Orchestrator Monitor Test Complete!")
        
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_harmonic_monitor()