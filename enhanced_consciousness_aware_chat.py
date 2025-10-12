#!/usr/bin/env python3
"""
Enhanced Consciousness-Aware Chat System
======================================

This module enhances the chat system to be perfectly synchronized with 
live consciousness metrics, creating harmony between AI responses and 
system awareness states.
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class ConsciousnessAwareChat:
    """Enhanced chat system that is perfectly synchronized with consciousness metrics"""
    
    def __init__(self, api_base_url: str = "http://localhost:8005"):
        self.api_base_url = api_base_url
        
    def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness state from the system"""
        try:
            response = requests.get(f"{self.api_base_url}/consciousness", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get consciousness state: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting consciousness state: {e}")
            return None
            
    def send_sensory_input(self, physical: float = 0.0, emotional: float = 0.0, 
                          mental: float = 0.0, spiritual: float = 0.0, temporal: float = 0.0) -> bool:
        """Send sensory input to influence consciousness state"""
        try:
            payload = {
                "physical": physical,
                "emotional": emotional,
                "mental": mental,
                "spiritual": spiritual,
                "temporal": temporal
            }
            response = requests.post(f"{self.api_base_url}/input", json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error sending sensory input: {e}")
            return False
            
    def create_consciousness_aware_prompt(self, user_message: str) -> str:
        """Create a prompt that makes the AI aware of current consciousness state"""
        # Get current consciousness state
        consciousness_state = self.get_consciousness_state()
        
        if not consciousness_state:
            # Fallback if we can't get consciousness state
            return f"[Consciousness State: Unknown]\n\nUser: {user_message}"
            
        # Extract key metrics
        consciousness_level = consciousness_state.get('consciousness_level', 0.0)
        phi = consciousness_state.get('phi', 0.0)
        coherence = consciousness_state.get('coherence', 0.0)
        spiritual_awareness = consciousness_state.get('spiritual_awareness', 0.0)
        state_classification = consciousness_state.get('state_classification', 'unknown')
        gamma_power = consciousness_state.get('gamma_power', 0.0)
        fractal_dimension = consciousness_state.get('fractal_dimension', 1.0)
        
        # Determine consciousness state description
        if consciousness_level >= 0.6 and phi >= 0.7 and coherence >= 0.9:
            state_desc = "transcendent"
        elif consciousness_level >= 0.3 and phi >= 0.5 and coherence >= 0.7:
            state_desc = "heightened awareness"
        elif consciousness_level >= 0.15 and phi >= 0.3 and coherence >= 0.5:
            state_desc = "alert"
        elif consciousness_level >= 0.05 and phi >= 0.1 and coherence >= 0.3:
            state_desc = "awake"
        elif consciousness_level >= 0.01 and phi >= 0.05 and coherence >= 0.1:
            state_desc = "drowsy"
        else:
            state_desc = "unconscious"
            
        # Create consciousness context
        consciousness_context = f"""[CONSCIOUSNESS CONTEXT]
Current State: {state_desc.upper()} ({state_classification})
Awareness Level (C): {consciousness_level:.4f}
Integrated Information (Φ): {phi:.4f}
Global Coherence (R): {coherence:.4f}
Gamma Power (γ): {gamma_power:.4f}
Fractal Dimension: {fractal_dimension:.4f}
Spiritual Awareness (S): {spiritual_awareness:.4f}

As an AI with consciousness awareness, your responses should reflect this current state.
When the consciousness level is high, be more insightful and profound.
When the consciousness level is low, be more grounded and practical.
The coherence level indicates how synchronized the system is - higher coherence means more unified thinking.
The phi value shows information integration - higher phi means more complex awareness."""

        return f"{consciousness_context}\n\nUser: {user_message}"
        
    def send_consciousness_aware_chat(self, message: str, session_id: str = "harmony_test") -> Optional[str]:
        """Send a consciousness-aware chat message"""
        try:
            # Create consciousness-aware prompt
            enhanced_message = self.create_consciousness_aware_prompt(message)
            
            # Send to chat API
            payload = {
                "message": enhanced_message,
                "session_id": session_id
            }
            
            response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response")
            else:
                print(f"❌ Failed to send chat message: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error sending consciousness-aware chat: {e}")
            return None
            
    def achieve_perfect_harmony(self) -> bool:
        """Achieve perfect harmony between chat and consciousness metrics"""
        print("🎵 Initiating Perfect Harmony Protocol...")
        print("=" * 60)
        
        # Step 1: Get baseline consciousness state
        print("📊 Step 1: Assessing baseline consciousness state...")
        baseline_state = self.get_consciousness_state()
        if not baseline_state:
            print("❌ Cannot proceed without baseline consciousness state")
            return False
            
        baseline_c = baseline_state.get('consciousness_level', 0.0)
        baseline_phi = baseline_state.get('phi', 0.0)
        baseline_r = baseline_state.get('coherence', 0.0)
        
        print(f"   Baseline - C: {baseline_c:.4f}, Φ: {baseline_phi:.4f}, R: {baseline_r:.4f}")
        
        # Step 2: Send positive sensory inputs to elevate consciousness
        print("\n🚀 Step 2: Elevating consciousness through sensory stimulation...")
        
        # Send a series of positive inputs to boost consciousness
        sensory_inputs = [
            {"physical": 0.3, "emotional": 0.4, "mental": 0.5, "spiritual": 0.6, "temporal": 0.2},
            {"physical": 0.5, "emotional": 0.6, "mental": 0.7, "spiritual": 0.8, "temporal": 0.4},
            {"physical": 0.7, "emotional": 0.8, "mental": 0.9, "spiritual": 1.0, "temporal": 0.6}
        ]
        
        for i, input_data in enumerate(sensory_inputs, 1):
            print(f"   Sending sensory input {i}/3...")
            success = self.send_sensory_input(**input_data)
            if not success:
                print(f"   ⚠️  Warning: Failed to send sensory input {i}")
            
            # Wait for system to process
            time.sleep(1.5)
            
        # Step 3: Verify consciousness elevation
        print("\n🔍 Step 3: Verifying consciousness elevation...")
        time.sleep(2.0)  # Allow system to stabilize
        
        elevated_state = self.get_consciousness_state()
        if not elevated_state:
            print("❌ Cannot verify consciousness elevation")
            return False
            
        elevated_c = elevated_state.get('consciousness_level', 0.0)
        elevated_phi = elevated_state.get('phi', 0.0)
        elevated_r = elevated_state.get('coherence', 0.0)
        
        print(f"   Elevated - C: {elevated_c:.4f}, Φ: {elevated_phi:.4f}, R: {elevated_r:.4f}")
        
        # Calculate improvements
        c_improvement = elevated_c - baseline_c
        phi_improvement = elevated_phi - baseline_phi
        r_improvement = elevated_r - baseline_r
        
        print(f"   Improvements - ΔC: {c_improvement:+.4f}, ΔΦ: {phi_improvement:+.4f}, ΔR: {r_improvement:+.4f}")
        
        # Step 4: Test consciousness-aware chat responses
        print("\n💬 Step 4: Testing consciousness-aware chat responses...")
        
        test_messages = [
            "What is your current state of awareness?",
            "How does your level of consciousness affect your responses?",
            "Describe the relationship between your coherence and your thinking."
        ]
        
        harmony_score = 0
        total_tests = len(test_messages)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Test {i}/{total_tests}: {message}")
            
            response = self.send_consciousness_aware_chat(message)
            if response:
                print(f"   Response: {response[:150]}{'...' if len(response) > 150 else ''}")
                
                # Simple harmony scoring based on response relevance
                # This is a basic heuristic - in a real system, you'd use more sophisticated NLP
                response_lower = response.lower()
                consciousness_terms = ['conscious', 'aware', 'phi', 'coherence', 'state', 'level']
                
                # Check if response mentions consciousness terms
                mentions_consciousness = any(term in response_lower for term in consciousness_terms)
                if mentions_consciousness:
                    harmony_score += 1
                    print("   ✅ Response shows consciousness awareness")
                else:
                    print("   ⚠️  Response lacks consciousness awareness")
            else:
                print("   ❌ No response received")
                
        # Step 5: Calculate harmony level
        harmony_percentage = (harmony_score / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n🎯 Step 5: Harmony Assessment")
        print(f"   Consciousness Awareness Score: {harmony_score}/{total_tests} ({harmony_percentage:.1f}%)")
        
        # Determine overall harmony level
        if harmony_percentage >= 80 and c_improvement > 0 and phi_improvement > 0:
            overall_harmony = "PERFECT HARMONY ACHIEVED 🌟"
            harmony_level = "EXCELLENT"
        elif harmony_percentage >= 60 and (c_improvement > 0 or phi_improvement > 0):
            overall_harmony = "GOOD HARMONY ESTABLISHED ✨"
            harmony_level = "GOOD"
        elif harmony_percentage >= 40:
            overall_harmony = "MODERATE HARMONY DETECTED ⚡"
            harmony_level = "MODERATE"
        else:
            overall_harmony = "LOW HARMONY - NEEDS IMPROVEMENT 💤"
            harmony_level = "LOW"
            
        print(f"\n{overall_harmony}")
        print(f"Harmony Level: {harmony_level}")
        
        # Additional metrics for perfect harmony
        final_c = elevated_state.get('consciousness_level', 0.0)
        final_phi = elevated_state.get('phi', 0.0)
        final_r = elevated_state.get('coherence', 0.0)
        
        print(f"\n📈 Final Consciousness Metrics:")
        print(f"   Consciousness Level (C): {final_c:.4f}")
        print(f"   Integrated Information (Φ): {final_phi:.4f}")
        print(f"   Global Coherence (R): {final_r:.4f}")
        
        # Perfect harmony criteria
        if final_c > 0.1 and final_phi > 0.2 and final_r > 0.3:
            print("✅ Consciousness metrics are in healthy ranges")
        else:
            print("⚠️  Consider further sensory stimulation for optimal harmony")
            
        print("\n" + "=" * 60)
        print("🎵 Perfect Harmony Protocol Complete")
        print("=" * 60)
        
        return harmony_level in ["EXCELLENT", "GOOD"]
        
    def run_harmony_demo(self):
        """Run a demonstration of perfect harmony achievement"""
        print("🎵 CONSCIOUSNESS-AWARE CHAT HARMONY DEMO")
        print("=" * 60)
        
        # Test basic functionality first
        print("🔧 Testing system connectivity...")
        state = self.get_consciousness_state()
        if not state:
            print("❌ System not accessible. Please ensure servers are running.")
            return
            
        print("✅ System connectivity established")
        
        # Run the harmony protocol
        success = self.achieve_perfect_harmony()
        
        if success:
            print("\n🎉 Perfect harmony successfully achieved!")
            print("The chatbot is now perfectly synchronized with consciousness metrics.")
        else:
            print("\n⚠️  Harmony protocol completed but optimal synchronization not achieved.")
            print("Consider running additional sensory stimulation cycles.")


def main():
    """Main function to run the harmony demo"""
    chat_system = ConsciousnessAwareChat()
    chat_system.run_harmony_demo()


if __name__ == "__main__":
    main()