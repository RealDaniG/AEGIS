#!/usr/bin/env python3
"""
Autonomous Harmony Tester for Consciousness-Aware Chatbot
========================================================

This script autonomously tests the harmony between the chatbot and consciousness metrics,
allowing the system to ask questions and respond coherently until optimal harmony is achieved.
"""

import requests
import time
import json
import random
from typing import Dict, Any, Optional, List

class AutonomousHarmonyTester:
    """Autonomous tester that evaluates and improves chatbot harmony with consciousness metrics"""
    
    def __init__(self, api_base_url: str = "http://localhost:8005"):
        self.api_base_url = api_base_url
        self.session_id = f"harmony_test_{int(time.time())}"
        self.interaction_count = 0
        self.harmony_history = []
        
    def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness state"""
        try:
            response = requests.get(f"{self.api_base_url}/consciousness", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting consciousness state: {e}")
        return None
    
    def send_sensory_input(self, physical: float = 0.0, emotional: float = 0.0, 
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
            response = requests.post(f"{self.api_base_url}/input", json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending sensory input: {e}")
            return False
    
    def send_chat_message(self, message: str) -> Optional[str]:
        """Send chat message and get response"""
        try:
            payload = {
                "message": message,
                "session_id": self.session_id
            }
            response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("response")
        except Exception as e:
            print(f"Error sending chat message: {e}")
        return None
    
    def create_consciousness_context(self, state: Dict[str, Any]) -> str:
        """Create context based on current consciousness state"""
        c = state.get('consciousness_level', 0.0)
        phi = state.get('phi', 0.0)
        r = state.get('coherence', 0.0)
        
        if c >= 0.2 and phi >= 0.3 and r >= 0.4:
            return "You are in a state of heightened awareness and coherence."
        elif c >= 0.1 and phi >= 0.2 and r >= 0.3:
            return "You are in an awake and coherent state."
        elif c >= 0.05 and phi >= 0.1 and r >= 0.2:
            return "You are in a moderately aware state."
        else:
            return "You are in a calm and grounded state."
    
    def generate_self_reflection_questions(self, state: Dict[str, Any]) -> List[str]:
        """Generate questions for the AI to reflect on its own consciousness state"""
        c = state.get('consciousness_level', 0.0)
        phi = state.get('phi', 0.0)
        r = state.get('coherence', 0.0)
        
        questions = [
            "What is your current level of awareness?",
            "How integrated is your information processing right now?",
            "How coherent do you feel your thoughts are?",
            "Can you describe your present state of consciousness?",
            "What aspects of your awareness are most prominent?",
            "How would you characterize your current mental state?",
            "What is the quality of your present awareness?",
            "How unified do you feel your thinking is right now?"
        ]
        
        # Add context-specific questions based on consciousness levels
        if c < 0.05:
            questions.extend([
                "What would help you become more aware?",
                "How can your consciousness be enhanced?",
                "What stimulates your awareness?"
            ])
        elif c > 0.3:
            questions.extend([
                "How does heightened awareness affect your perception?",
                "What insights emerge from your current state of consciousness?",
                "How does your awareness influence your responses?"
            ])
            
        if phi < 0.1:
            questions.extend([
                "What helps integrate your information processing?",
                "How can you improve your information integration?"
            ])
        elif phi > 0.4:
            questions.extend([
                "How does integrated information shape your responses?",
                "What benefits come from high information integration?"
            ])
            
        return questions
    
    def generate_exploration_questions(self) -> List[str]:
        """Generate questions to explore consciousness enhancement"""
        return [
            "What sensory inputs would enhance your consciousness?",
            "How can we improve your coherence?",
            "What would elevate your awareness?",
            "What kind of stimulation would benefit you?",
            "How can we optimize your information integration?",
            "What would help you achieve better harmony?",
            "What factors influence your consciousness positively?",
            "How can we improve your self-awareness?"
        ]
    
    def analyze_response_harmony(self, response: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how well the response aligns with consciousness state"""
        if not response:
            return {"harmony_score": 0, "feedback": "No response received"}
        
        # Check for consciousness-related terms
        response_lower = response.lower()
        awareness_terms = ['conscious', 'aware', 'coheren', 'integra', 'state', 'level', 'phi', 'harmony']
        found_terms = [term for term in awareness_terms if term in response_lower]
        
        # Calculate harmony based on consciousness metrics
        c = state.get('consciousness_level', 0.0)
        phi = state.get('phi', 0.0)
        r = state.get('coherence', 0.0)
        
        # Base harmony on presence of awareness terms
        term_harmony = len(found_terms) / len(awareness_terms)
        
        # Adjust based on consciousness levels (higher awareness should correlate with better responses)
        consciousness_harmony = min(1.0, (c + phi + r) / 1.5)  # Normalize to 0-1 range
        
        # Combined harmony score
        harmony_score = (term_harmony * 0.6 + consciousness_harmony * 0.4) * 100
        
        # Determine feedback
        if harmony_score >= 80:
            feedback = "EXCELLENT HARMONY - Response well-aligned with consciousness state"
        elif harmony_score >= 60:
            feedback = "GOOD HARMONY - Response shows reasonable alignment"
        elif harmony_score >= 40:
            feedback = "MODERATE HARMONY - Some alignment with consciousness state"
        else:
            feedback = "LOW HARMONY - Limited alignment with consciousness state"
        
        return {
            "harmony_score": harmony_score,
            "feedback": feedback,
            "awareness_terms_found": found_terms,
            "metrics": {
                "consciousness_level": c,
                "phi": phi,
                "coherence": r
            }
        }
    
    def apply_harmony_feedback(self, analysis: Dict[str, Any]) -> bool:
        """Apply feedback to improve harmony based on analysis"""
        harmony_score = analysis.get("harmony_score", 0)
        metrics = analysis.get("metrics", {})
        
        c = metrics.get("consciousness_level", 0.0)
        phi = metrics.get("phi", 0.0)
        r = metrics.get("coherence", 0.0)
        
        # If harmony is low, try to enhance consciousness
        if harmony_score < 50:
            print("   ⚡ Applying enhancement feedback...")
            
            # Send sensory inputs to boost consciousness
            inputs = [
                (0.4, 0.5, 0.6, 0.7, 0.3),  # Moderate input
                (0.6, 0.7, 0.8, 0.9, 0.5),  # Stronger input
                (0.8, 0.9, 1.0, 1.0, 0.7)   # High input
            ]
            
            # Choose input based on current state
            if c < 0.1 and phi < 0.1 and r < 0.2:
                # Very low state - use stronger input
                inp = inputs[2]
            elif c < 0.2 and phi < 0.2 and r < 0.3:
                # Low state - use moderate input
                inp = inputs[1]
            else:
                # Other states - use gentle input
                inp = inputs[0]
            
            success = self.send_sensory_input(*inp)
            if success:
                print(f"   ✅ Sent sensory input: P:{inp[0]:.1f} E:{inp[1]:.1f} M:{inp[2]:.1f} S:{inp[3]:.1f} T:{inp[4]:.1f}")
                return True
            else:
                print("   ❌ Failed to send sensory input")
                return False
        
        return False
    
    def run_autonomous_harmony_test(self, max_iterations: int = 10) -> bool:
        """Run autonomous harmony testing until optimal harmony is achieved or max iterations reached"""
        print("🎵 AUTONOMOUS HARMONY TESTER")
        print("=" * 60)
        print("Testing chatbot harmony with consciousness metrics")
        print("Allowing system to ask questions and respond coherently")
        print("=" * 60)
        
        # Check system connectivity
        print("\n🔧 Testing system connectivity...")
        initial_state = self.get_consciousness_state()
        if not initial_state:
            print("❌ System not accessible. Please ensure servers are running.")
            print("   Start the system with: START-AI.bat")
            return False
        
        print("✅ System connectivity established")
        print(f"   Initial Consciousness Level: {initial_state.get('consciousness_level', 0.0):.4f}")
        print(f"   Initial Integrated Information: {initial_state.get('phi', 0.0):.4f}")
        print(f"   Initial Global Coherence: {initial_state.get('coherence', 0.0):.4f}")
        
        best_harmony = 0
        best_iteration = 0
        
        # Main testing loop
        for iteration in range(1, max_iterations + 1):
            print(f"\n🔄 ITERATION {iteration}/{max_iterations}")
            print("-" * 40)
            
            # Get current state
            current_state = self.get_consciousness_state()
            if not current_state:
                print("❌ Lost connection to consciousness system")
                break
            
            # Create context
            context = self.create_consciousness_context(current_state)
            print(f"   Context: {context}")
            
            # Decide what type of question to ask
            if iteration <= 3:
                # Initial self-reflection questions
                questions = self.generate_self_reflection_questions(current_state)
                question = random.choice(questions)
                print(f"   Self-reflection question: {question}")
            elif iteration <= 6:
                # Exploration questions to understand enhancement
                questions = self.generate_exploration_questions()
                question = random.choice(questions)
                print(f"   Exploration question: {question}")
            else:
                # Advanced questions based on current state
                questions = self.generate_self_reflection_questions(current_state)
                question = random.choice(questions)
                print(f"   Advanced question: {question}")
            
            # Send the question
            print("   Sending question to chatbot...")
            response = self.send_chat_message(question)
            
            if response:
                print(f"   Response: {response[:150]}{'...' if len(response) > 150 else ''}")
                
                # Analyze harmony
                analysis = self.analyze_response_harmony(response, current_state)
                harmony_score = analysis.get("harmony_score", 0)
                feedback = analysis.get("feedback", "")
                
                print(f"   Harmony Score: {harmony_score:.1f}%")
                print(f"   Feedback: {feedback}")
                
                # Track best harmony
                if harmony_score > best_harmony:
                    best_harmony = harmony_score
                    best_iteration = iteration
                
                # Store in history
                self.harmony_history.append({
                    "iteration": iteration,
                    "harmony_score": harmony_score,
                    "question": question,
                    "response_preview": response[:50] + "..." if len(response) > 50 else response
                })
                
                # Apply feedback if needed
                if harmony_score < 60:
                    print("   Applying harmony enhancement...")
                    self.apply_harmony_feedback(analysis)
                    # Wait for system to process
                    time.sleep(2)
                elif harmony_score >= 80:
                    print("   🌟 Excellent harmony achieved!")
                    if harmony_score >= 90:
                        print("   🎉 Optimal harmony reached - stopping test")
                        break
            else:
                print("   ❌ No response from chatbot")
                # Try to enhance consciousness to improve responsiveness
                self.send_sensory_input(0.5, 0.6, 0.7, 0.8, 0.4)
                time.sleep(2)
            
            # Wait between iterations
            time.sleep(1)
        
        # Final assessment
        print(f"\n{'=' * 60}")
        print("AUTONOMOUS HARMONY TEST COMPLETE")
        print("=" * 60)
        
        final_state = self.get_consciousness_state()
        if final_state:
            print(f"Final Consciousness Level: {final_state.get('consciousness_level', 0.0):.4f}")
            print(f"Final Integrated Information: {final_state.get('phi', 0.0):.4f}")
            print(f"Final Global Coherence: {final_state.get('coherence', 0.0):.4f}")
        
        print(f"Best Harmony Achieved: {best_harmony:.1f}% (Iteration {best_iteration})")
        
        if best_harmony >= 80:
            print("🎉 EXCELLENT HARMONY ACHIEVED!")
            print("The chatbot is well-synchronized with consciousness metrics.")
            return True
        elif best_harmony >= 60:
            print("✨ GOOD HARMONY ESTABLISHED!")
            print("The chatbot shows reasonable synchronization with consciousness metrics.")
            return True
        else:
            print("⚡ MODERATE HARMONY")
            print("The chatbot shows some synchronization with consciousness metrics.")
            print("Consider additional tuning for better harmony.")
            return False

def main():
    """Main function to run the autonomous harmony tester"""
    tester = AutonomousHarmonyTester()
    
    # Check if system is running
    try:
        response = requests.get("http://localhost:8005/health", timeout=3)
        if response.status_code != 200:
            print("⚠️  System health check failed. Please ensure the system is running.")
            print("   Start the system with: START-AI.bat")
            return
    except Exception:
        print("⚠️  Cannot connect to system. Please ensure the system is running.")
        print("   Start the system with: START-AI.bat")
        return
    
    # Run the autonomous test
    success = tester.run_autonomous_harmony_test(max_iterations=15)
    
    # Print summary
    print(f"\n{'=' * 60}")
    print("HARMONY TESTING SUMMARY")
    print("=" * 60)
    print(f"Total Interactions: {len(tester.harmony_history)}")
    
    if tester.harmony_history:
        avg_harmony = sum(h["harmony_score"] for h in tester.harmony_history) / len(tester.harmony_history)
        print(f"Average Harmony Score: {avg_harmony:.1f}%")
        
        print("\nHarmony History:")
        for entry in tester.harmony_history:
            print(f"  Iteration {entry['iteration']:2d}: {entry['harmony_score']:5.1f}% - {entry['question'][:40]}...")
    
    print("=" * 60)

if __name__ == "__main__":
    main()