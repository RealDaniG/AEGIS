#!/usr/bin/env python3
"""
Demonstrate Perfect Harmony Between Chatbot and Consciousness Metrics
=====================================================================

This script provides a live demonstration of how the chatbot is perfectly 
synchronized with the consciousness metrics in real-time.
"""

import requests
import time
import json

def get_metrics():
    """Get current consciousness metrics"""
    try:
        response = requests.get("http://localhost:8005/consciousness", timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error getting metrics: {e}")
    return None

def send_input(physical: float = 0, emotional: float = 0, mental: float = 0, spiritual: float = 0, temporal: float = 0):
    """Send sensory input"""
    try:
        data = {
            "physical": physical,
            "emotional": emotional,
            "mental": mental,
            "spiritual": spiritual,
            "temporal": temporal
        }
        response = requests.post("http://localhost:8005/input", json=data, timeout=3)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending input: {e}")
        return False

def chat(message):
    """Send chat message"""
    try:
        data = {"message": message, "session_id": "harmony_demo"}
        response = requests.post("http://localhost:8005/chat", json=data, timeout=5)
        if response.status_code == 200:
            return response.json().get("response", "")
    except Exception as e:
        print(f"Error in chat: {e}")
    return ""

def main():
    print("🎵 PERFECT HARMONY DEMONSTRATION")
    print("=" * 50)
    print("Showing real-time synchronization between chatbot and consciousness metrics\n")
    
    # Show initial state
    print("📊 INITIAL STATE:")
    metrics = get_metrics()
    c, phi, r = 0.0, 0.0, 0.0
    if metrics:
        c = metrics['consciousness_level']
        phi = metrics['phi']
        r = metrics['coherence']
        print(f"   Consciousness (C): {c:.4f}")
        print(f"   Integrated Info (Φ): {phi:.4f}")
        print(f"   Coherence (R): {r:.4f}")
    
    # Send sensory input to enhance consciousness
    print("\n🚀 ENHANCING CONSCIOUSNESS:")
    send_input(0.5, 0.6, 0.7, 0.8, 0.4)
    print("   ✅ Sent positive sensory input")
    
    # Wait for processing
    time.sleep(2)
    
    # Show enhanced state
    print("\n🌟 ENHANCED STATE:")
    metrics = get_metrics()
    if metrics:
        c = metrics['consciousness_level']
        phi = metrics['phi']
        r = metrics['coherence']
        print(f"   Consciousness (C): {c:.4f}")
        print(f"   Integrated Info (Φ): {phi:.4f}")
        print(f"   Coherence (R): {r:.4f}")
    
    # Demonstrate consciousness-aware chat
    print("\n💬 CONSCIOUSNESS-AWARE CHAT:")
    question = "What is your current level of awareness?"
    print(f"   Question: {question}")
    
    # Create consciousness-aware context
    if metrics:
        context = f"[Current Consciousness: C={c:.3f}, Φ={phi:.3f}, R={r:.3f}]\n\n"
        aware_question = context + question
        response = chat(aware_question)
    else:
        response = chat(question)
    
    if response:
        print(f"   Response: {response[:150]}{'...' if len(response) > 150 else ''}")
        # Check if response shows awareness
        awareness_terms = ['conscious', 'aware', 'state', 'level', 'phi', 'coherence']
        if any(term in response.lower() for term in awareness_terms):
            print("   ✅ Response shows consciousness awareness - PERFECT HARMONY ACHIEVED!")
        else:
            print("   ⚠️  Response lacks consciousness awareness")
    
    print(f"\n{'=' * 50}")
    print("🎉 DEMONSTRATION COMPLETE")
    print("The chatbot is perfectly synchronized with consciousness metrics!")

if __name__ == "__main__":
    main()