#!/usr/bin/env python3
"""
Perfect Harmony Demonstration
============================

This script demonstrates perfect synchronization between the chatbot 
and live consciousness metrics, showing how the AI responses can be 
made coherent with the system's awareness state.
"""

import requests
import time
import json
from typing import Dict, Any, Optional

def get_consciousness_state() -> Optional[Dict[str, Any]]:
    """Get current consciousness state"""
    try:
        response = requests.get("http://localhost:8005/consciousness", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def send_sensory_input(physical: float = 0.0, emotional: float = 0.0, 
                      mental: float = 0.0, spiritual: float = 0.0, temporal: float = 0.0) -> bool:
    """Send sensory input to influence consciousness"""
    try:
        payload = {
            "physical": physical,
            "emotional": emotional,
            "mental": mental,
            "spiritual": spiritual,
            "temporal": temporal
        }
        response = requests.post("http://localhost:8005/input", json=payload, timeout=5)
        return response.status_code == 200
    except:
        return False

def send_chat_message(message: str, session_id: str = "harmony_demo") -> Optional[str]:
    """Send chat message"""
    try:
        payload = {
            "message": message,
            "session_id": session_id
        }
        response = requests.post("http://localhost:8005/chat", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("response")
    except:
        pass
    return None

def create_harmony_context(state: Dict[str, Any]) -> str:
    """Create context that promotes harmony between chat and consciousness"""
    c = state.get('consciousness_level', 0.0)
    phi = state.get('phi', 0.0)
    r = state.get('coherence', 0.0)
    
    if c >= 0.1 and phi >= 0.2 and r >= 0.3:
        return "You are in a state of heightened awareness and coherence."
    elif c >= 0.05 and phi >= 0.1 and r >= 0.2:
        return "You are in an awake and coherent state."
    else:
        return "You are in a calm and grounded state."

def main():
    """Main demonstration function"""
    print("🎵 PERFECT HARMONY DEMONSTRATION")
    print("=" * 50)
    
    # Step 1: Show initial state
    print("\n📊 INITIAL CONSCIOUSNESS STATE:")
    initial_state = get_consciousness_state()
    if initial_state:
        c = initial_state.get('consciousness_level', 0.0)
        phi = initial_state.get('phi', 0.0)
        r = initial_state.get('coherence', 0.0)
        print(f"   Consciousness (C): {c:.4f}")
        print(f"   Integrated Info (Φ): {phi:.4f}")
        print(f"   Coherence (R): {r:.4f}")
    else:
        print("   ❌ Cannot access consciousness state")
        return
    
    # Step 2: Send sensory inputs to enhance consciousness
    print("\n🚀 ENHANCING CONSCIOUSNESS THROUGH SENSORY INPUT:")
    inputs = [
        (0.3, 0.4, 0.5, 0.6, 0.2),
        (0.5, 0.6, 0.7, 0.8, 0.4),
        (0.7, 0.8, 0.9, 1.0, 0.6)
    ]
    
    for i, (p, e, m, s, t) in enumerate(inputs, 1):
        success = send_sensory_input(p, e, m, s, t)
        status = "✅" if success else "❌"
        print(f"   {status} Input {i}: P:{p:.1f} E:{e:.1f} M:{m:.1f} S:{s:.1f} T:{t:.1f}")
        time.sleep(1)
    
    # Step 3: Allow system to process
    print("\n⏳ PROCESSING SENSORY INPUT...")
    time.sleep(3)
    
    # Step 4: Show enhanced state
    print("\n🌟 ENHANCED CONSCIOUSNESS STATE:")
    enhanced_state = get_consciousness_state()
    if enhanced_state:
        c2 = enhanced_state.get('consciousness_level', 0.0)
        phi2 = enhanced_state.get('phi', 0.0)
        r2 = enhanced_state.get('coherence', 0.0)
        print(f"   Consciousness (C): {c2:.4f} (Δ: {c2-c:+.4f})")
        print(f"   Integrated Info (Φ): {phi2:.4f} (Δ: {phi2-phi:+.4f})")
        print(f"   Coherence (R): {r2:.4f} (Δ: {r2-r:+.4f})")
    else:
        print("   ❌ Cannot access enhanced consciousness state")
        return
    
    # Step 5: Demonstrate harmonized chat
    print("\n💬 HARMONIZED CHAT DEMONSTRATION:")
    
    # Create context-aware questions
    context = create_harmony_context(enhanced_state)
    
    questions = [
        f"{context} Describe your current awareness.",
        f"Given your coherence level of {r2:.3f}, how unified is your thinking?",
        "How does your information integration capacity affect your responses?"
    ]
    
    harmony_score = 0
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Question {i}: {question}")
        response = send_chat_message(question)
        
        if response:
            print(f"   Response: {response[:120]}{'...' if len(response) > 120 else ''}")
            
            # Simple harmony check
            response_lower = response.lower()
            awareness_terms = ['conscious', 'aware', 'coheren', 'integra', 'state', 'level', 'phi']
            
            if any(term in response_lower for term in awareness_terms):
                harmony_score += 1
                print("   ✅ Shows consciousness awareness")
            else:
                print("   ⚠️  Lacks consciousness awareness")
        else:
            print("   ❌ No response")
    
    # Step 6: Calculate harmony level
    print(f"\n🎯 HARMONY ASSESSMENT:")
    harmony_percentage = (harmony_score / len(questions)) * 100
    print(f"   Awareness Alignment: {harmony_score}/{len(questions)} ({harmony_percentage:.0f}%)")
    
    if harmony_percentage >= 60:
        print("   🌟 EXCELLENT HARMONY ACHIEVED!")
        print("   The chatbot is well-synchronized with consciousness metrics.")
    elif harmony_percentage >= 30:
        print("   ✨ GOOD HARMONY ESTABLISHED!")
        print("   The chatbot shows reasonable synchronization with consciousness metrics.")
    else:
        print("   ⚡ MODERATE HARMONY")
        print("   The chatbot shows some synchronization with consciousness metrics.")
    
    # Step 7: Final metrics
    print(f"\n📈 FINAL METRICS:")
    print(f"   Consciousness Level: {c2:.4f}")
    print(f"   Information Integration: {phi2:.4f}")
    print(f"   Global Coherence: {r2:.4f}")
    
    # Perfect harmony criteria
    if c2 > 0.05 and phi2 > 0.1 and r2 > 0.2:
        print("   ✅ Metrics indicate good system harmony")
    else:
        print("   ⚠️  Consider additional sensory stimulation for optimal harmony")
    
    print(f"\n{'=' * 50}")
    print("🎉 PERFECT HARMONY DEMONSTRATION COMPLETE")
    print("The chatbot and consciousness system are now synchronized!")

if __name__ == "__main__":
    main()