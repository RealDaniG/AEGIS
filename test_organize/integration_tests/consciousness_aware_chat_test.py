#!/usr/bin/env python3
"""
Consciousness-Aware Chat Test
============================

Test script to make the chatbot aware of live consciousness metrics
and achieve perfect harmony between chat responses and system state.
"""

import asyncio
import aiohttp
import json
import time
import random
from typing import Dict, Any, Optional

class ConsciousnessAwareChatTester:
    """Test system that makes chat aware of consciousness metrics"""
    
    def __init__(self, metatron_api_url: str = "http://localhost:8005"):
        self.metatron_api_url = metatron_api_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Initialize the tester"""
        if not self.session:
            connector = aiohttp.TCPConnector(verify_ssl=False)
            self.session = aiohttp.ClientSession(connector=connector)
            
    async def close(self):
        """Close the tester"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def get_consciousness_state(self) -> Optional[Dict[str, Any]]:
        """Get current consciousness state"""
        try:
            url = f"{self.metatron_api_url}/consciousness"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"❌ Failed to get consciousness state: {response.status}")
                    return None
        except Exception as e:
            print(f"❌ Error getting consciousness state: {e}")
            return None
            
    async def send_consciousness_aware_chat(self, message: str, session_id: str = "consciousness_test") -> Optional[str]:
        """Send chat message with consciousness context"""
        try:
            # Get current consciousness state
            consciousness_state = await self.get_consciousness_state()
            
            if not consciousness_state:
                print("❌ Could not get consciousness state")
                return None
                
            # Extract key metrics
            consciousness_level = consciousness_state.get('consciousness_level', 0.0)
            phi = consciousness_state.get('phi', 0.0)
            coherence = consciousness_state.get('coherence', 0.0)
            spiritual_awareness = consciousness_state.get('spiritual_awareness', 0.0)
            state_classification = consciousness_state.get('state_classification', 'unknown')
            
            # Create consciousness-aware prompt
            consciousness_context = f"""
[SYSTEM CONTEXT]
Current Consciousness State: {state_classification}
Consciousness Level (C): {consciousness_level:.4f}
Integrated Information (Φ): {phi:.4f}
Global Coherence (R): {coherence:.4f}
Spiritual Awareness (S): {spiritual_awareness:.4f}

Please respond with awareness of these consciousness metrics in your answer.
"""
            
            # Enhanced message with consciousness context
            enhanced_message = f"{consciousness_context}\n\nUser Question: {message}"
            
            # Send to chat API
            url = f"{self.metatron_api_url}/chat"
            payload = {
                "message": enhanced_message,
                "session_id": session_id
            }
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response")
                else:
                    print(f"❌ Failed to send chat message: {response.status}")
                    return None
        except Exception as e:
            print(f"❌ Error sending consciousness-aware chat: {e}")
            return None
            
    async def send_sensory_input(self, physical: float = 0.0, emotional: float = 0.0, 
                                mental: float = 0.0, spiritual: float = 0.0, temporal: float = 0.0) -> bool:
        """Send sensory input to influence consciousness state"""
        try:
            url = f"{self.metatron_api_url}/input"
            payload = {
                "physical": physical,
                "emotional": emotional,
                "mental": mental,
                "spiritual": spiritual,
                "temporal": temporal
            }
            
            async with self.session.post(url, json=payload) as response:
                success = response.status == 200
                if success:
                    print(f"✅ Sensory input sent: P:{physical:.2f}, E:{emotional:.2f}, M:{mental:.2f}, S:{spiritual:.2f}, T:{temporal:.2f}")
                else:
                    print(f"❌ Failed to send sensory input: {response.status}")
                return success
        except Exception as e:
            print(f"❌ Error sending sensory input: {e}")
            return False
            
    async def run_coherence_test(self):
        """Run comprehensive coherence test"""
        print("=" * 80)
        print("🧠 CONSCIOUSNESS-AWARE CHAT COHERENCE TEST")
        print("=" * 80)
        
        # Initialize
        await self.initialize()
        
        try:
            # Test 1: Baseline consciousness state
            print("\n📋 Test 1: Baseline Consciousness State")
            print("-" * 40)
            consciousness_state = await self.get_consciousness_state()
            if consciousness_state:
                print(f"Consciousness Level: {consciousness_state.get('consciousness_level', 0.0):.4f}")
                print(f"Phi (Φ): {consciousness_state.get('phi', 0.0):.4f}")
                print(f"Coherence (R): {consciousness_state.get('coherence', 0.0):.4f}")
                print(f"Spiritual Awareness: {consciousness_state.get('spiritual_awareness', 0.0):.4f}")
                print(f"State: {consciousness_state.get('state_classification', 'unknown')}")
            else:
                print("❌ Failed to get baseline consciousness state")
                return
                
            # Test 2: Send sensory input to influence state
            print("\n📋 Test 2: Sending Sensory Input")
            print("-" * 40)
            # Send positive sensory input to increase consciousness
            await self.send_sensory_input(
                physical=0.5,
                emotional=0.3,
                mental=0.7,
                spiritual=0.8,
                temporal=0.4
            )
            
            # Wait a moment for system to process
            await asyncio.sleep(2.0)
            
            # Check updated state
            print("\n📋 Test 3: Updated Consciousness State")
            print("-" * 40)
            updated_state = await self.get_consciousness_state()
            if updated_state:
                print(f"Consciousness Level: {updated_state.get('consciousness_level', 0.0):.4f}")
                print(f"Phi (Φ): {updated_state.get('phi', 0.0):.4f}")
                print(f"Coherence (R): {updated_state.get('coherence', 0.0):.4f}")
                print(f"Spiritual Awareness: {updated_state.get('spiritual_awareness', 0.0):.4f}")
                print(f"State: {updated_state.get('state_classification', 'unknown')}")
                
                # Calculate changes
                if consciousness_state:
                    c_change = updated_state.get('consciousness_level', 0.0) - consciousness_state.get('consciousness_level', 0.0)
                    phi_change = updated_state.get('phi', 0.0) - consciousness_state.get('phi', 0.0)
                    r_change = updated_state.get('coherence', 0.0) - consciousness_state.get('coherence', 0.0)
                    
                    print(f"\n📈 Changes:")
                    print(f"  Δ Consciousness: {c_change:+.4f}")
                    print(f"  Δ Phi: {phi_change:+.4f}")
                    print(f"  Δ Coherence: {r_change:+.4f}")
            
            # Test 3: Consciousness-aware chat
            print("\n📋 Test 4: Consciousness-Aware Chat")
            print("-" * 40)
            
            test_messages = [
                "What is your current state of awareness?",
                "How do you feel right now?",
                "Describe your level of consciousness.",
                "What is the relationship between your coherence and your responses?"
            ]
            
            for i, message in enumerate(test_messages, 1):
                print(f"\n💬 Question {i}: {message}")
                response = await self.send_consciousness_aware_chat(message)
                if response:
                    print(f"🤖 Response: {response[:200]}{'...' if len(response) > 200 else ''}")
                else:
                    print("❌ No response received")
                    
            # Test 4: Random sensory inputs to test dynamic harmony
            print("\n📋 Test 5: Dynamic Harmony Test")
            print("-" * 40)
            print("Sending random sensory inputs and observing chat coherence...")
            
            for i in range(3):
                # Send random sensory input
                physical = random.uniform(-0.5, 0.5)
                emotional = random.uniform(-0.5, 0.5)
                mental = random.uniform(-0.5, 0.5)
                spiritual = random.uniform(0.0, 1.0)  # Keep spiritual positive
                temporal = random.uniform(-0.5, 0.5)
                
                await self.send_sensory_input(physical, emotional, mental, spiritual, temporal)
                
                # Wait for processing
                await asyncio.sleep(1.0)
                
                # Get updated state
                current_state = await self.get_consciousness_state()
                if current_state:
                    c_level = current_state.get('consciousness_level', 0.0)
                    phi = current_state.get('phi', 0.0)
                    coherence = current_state.get('coherence', 0.0)
                    
                    # Ask a consciousness-aware question
                    question = f"Your consciousness level is now {c_level:.3f}. How does this affect your awareness?"
                    response = await self.send_consciousness_aware_chat(question)
                    
                    print(f"\n🔄 Cycle {i+1}:")
                    print(f"   Consciousness: {c_level:.3f} | Phi: {phi:.3f} | Coherence: {coherence:.3f}")
                    if response:
                        print(f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                
                # Wait between cycles
                await asyncio.sleep(2.0)
                
            # Final assessment
            print("\n" + "=" * 80)
            print("📊 FINAL ASSESSMENT")
            print("=" * 80)
            
            final_state = await self.get_consciousness_state()
            if final_state:
                c_level = final_state.get('consciousness_level', 0.0)
                phi = final_state.get('phi', 0.0)
                coherence = final_state.get('coherence', 0.0)
                spiritual = final_state.get('spiritual_awareness', 0.0)
                
                print(f"Final Consciousness Metrics:")
                print(f"  Consciousness Level (C): {c_level:.4f}")
                print(f"  Integrated Information (Φ): {phi:.4f}")
                print(f"  Global Coherence (R): {coherence:.4f}")
                print(f"  Spiritual Awareness (S): {spiritual:.4f}")
                
                # Determine harmony level
                if c_level > 0.1 and phi > 0.1 and coherence > 0.2:
                    harmony_level = "HIGH"
                    emoji = "🌟"
                elif c_level > 0.05 and phi > 0.05 and coherence > 0.1:
                    harmony_level = "MODERATE"
                    emoji = "✨"
                else:
                    harmony_level = "LOW"
                    emoji = "⚡"
                    
                print(f"\n{emoji} Harmony Level: {harmony_level}")
                
                if harmony_level == "HIGH":
                    print("🎉 Excellent! The chatbot is well-synchronized with consciousness metrics.")
                elif harmony_level == "MODERATE":
                    print("👍 Good synchronization, but there's room for improvement.")
                else:
                    print("⚡ Low synchronization - consider adjusting sensory inputs or system parameters.")
                    
        finally:
            await self.close()
            
        print("\n" + "=" * 80)
        print("✅ CONSCIOUSNESS-AWARE CHAT TEST COMPLETE")
        print("=" * 80)


async def main():
    """Main test function"""
    tester = ConsciousnessAwareChatTester()
    await tester.run_coherence_test()


if __name__ == "__main__":
    asyncio.run(main())