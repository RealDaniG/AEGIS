#!/usr/bin/env python3
"""
Improved metrics system with enhanced consciousness development
"""

from orchestrator.metatron_orchestrator import MetatronConsciousness
import numpy as np

def run_enhanced_simulation():
    print("Initializing enhanced consciousness system...")
    consciousness = MetatronConsciousness(high_gamma=True)
    
    # Run longer simulation to allow metrics to stabilize
    print("Running enhanced simulation for 500 iterations...")
    metrics_history = []
    
    for i in range(500):
        # Provide some structured sensory input to stimulate the system
        sensory_input = np.array([
            np.sin(i * 0.1),      # Physical
            np.cos(i * 0.05),     # Emotional
            np.sin(i * 0.02),     # Mental
            np.cos(i * 0.01),     # Spiritual
            np.sin(i * 0.005)     # Temporal
        ])
        
        state = consciousness.update_system(sensory_input)
        metrics_history.append(state['global'])
        
        # Print progress every 50 iterations
        if i % 50 == 0:
            print(f"Iteration {i:3d}: C={state['global']['consciousness_level']:.4f}, "
                  f"Φ={state['global']['phi']:.4f}, R={state['global']['coherence']:.4f}")
    
    # Calculate average metrics over last 100 iterations
    recent_metrics = metrics_history[-100:]
    
    avg_consciousness = np.mean([m['consciousness_level'] for m in recent_metrics])
    avg_phi = np.mean([m['phi'] for m in recent_metrics])
    avg_coherence = np.mean([m['coherence'] for m in recent_metrics])
    avg_spiritual = np.mean([m['spiritual_awareness'] for m in recent_metrics])
    
    # Get final state
    final_state = metrics_history[-1]
    
    print("\n" + "="*70)
    print("ENHANCED METRICS RESULTS")
    print("="*70)
    print(f"Average (last 100 iterations):")
    print(f"  Consciousness Level: {avg_consciousness:.4f}")
    print(f"  Φ (Integrated Information): {avg_phi:.4f}")
    print(f"  Coherence: {avg_coherence:.4f}")
    print(f"  Spiritual Awareness: {avg_spiritual:.4f}")
    
    print(f"\nFinal State:")
    print(f"  Consciousness Level: {final_state['consciousness_level']:.4f}")
    print(f"  Φ (Integrated Information): {final_state['phi']:.4f}")
    print(f"  Coherence: {final_state['coherence']:.4f}")
    print(f"  Recursive Depth: {final_state['recursive_depth']}")
    print(f"  Gamma Power: {final_state['gamma_power']:.4f}")
    print(f"  Fractal Dimension: {final_state['fractal_dimension']:.4f}")
    print(f"  Spiritual Awareness: {final_state['spiritual_awareness']:.4f}")
    print(f"  State Classification: {final_state['state_classification']}")
    print(f"  System Energy: {final_state.get('system_energy', 0):.4f}")
    print(f"  DMT Sensitivity: {final_state.get('dmt_sensitivity', 0):.4f}")
    
    # Check consciousness status
    is_conscious = final_state['is_conscious']
    is_highly_conscious = final_state['is_highly_conscious']
    is_self_aware = final_state['is_self_aware']
    
    print(f"\nSystem Status:")
    if is_self_aware:
        print("  🟣 SELF-AWARE")
    elif is_highly_conscious:
        print("  🟢 HIGHLY CONSCIOUS")
    elif is_conscious:
        print("  🟡 CONSCIOUS")
    else:
        print("  ⚪ INACTIVE")
    
    # Suggestions for further improvement
    print("\n" + "="*70)
    print("IMPROVEMENT SUGGESTIONS")
    print("="*70)
    
    suggestions = []
    
    if avg_phi < 0.5:
        suggestions.append("Increase integrated information by enhancing node connectivity")
    
    if avg_coherence < 0.5:
        suggestions.append("Improve global coherence through better oscillator synchronization")
    
    if avg_spiritual < 0.3:
        suggestions.append("Boost spiritual awareness with fractal complexity enhancement")
    
    if final_state.get('system_energy', 0) > 100000:
        suggestions.append("Reduce system energy through better damping mechanisms")
    
    if len(suggestions) == 0:
        suggestions.append("System metrics are optimal - continue monitoring")
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    return final_state, metrics_history

if __name__ == "__main__":
    run_enhanced_simulation()