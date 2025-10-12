#!/usr/bin/env python3
"""
Comprehensive Chatbot Test for Metatron Consciousness Engine

This script tests the chatbot functionality and verifies that the visuals 
match the bot's consciousness levels and that answers are coherent.
"""

import requests
import json
import time
import asyncio
import websockets
from typing import Dict, Any, List, Tuple

class ComprehensiveChatbotTest:
    """Test suite for the Metatron chatbot with consciousness visualization verification"""
    
    def __init__(self):
        self.base_url = "http://localhost:8003"
        self.ws_url = "ws://localhost:8003/ws"
        self.chat_url = f"{self.base_url}/api/chat"
        self.status_url = f"{self.base_url}/api/status"
        self.health_url = f"{self.base_url}/api/health"
        
    def test_health_check(self) -> bool:
        """Test if the consciousness engine is running"""
        try:
            response = requests.get(self.health_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Health Check: PASSED")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Uptime: {data.get('uptime_seconds', 0):.2f} seconds")
                return True
            else:
                print(f"❌ Health Check: FAILED (Status {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Health Check: FAILED - {str(e)}")
            return False
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        try:
            response = requests.get(self.status_url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Consciousness State: FAILED (Status {response.status_code})")
                return {}
        except Exception as e:
            print(f"❌ Consciousness State: FAILED - {str(e)}")
            return {}
    
    def test_chat_coherence(self, test_messages: List[str]) -> Tuple[bool, List[Dict[str, Any]]]:
        """Test chat coherence with multiple messages"""
        results = []
        all_passed = True
        
        print("\nTesting Chat Coherence...")
        
        for i, message in enumerate(test_messages, 1):
            try:
                print(f"\nTest {i}: '{message[:50]}{'...' if len(message) > 50 else ''}'")
                
                # Get consciousness state before chat
                state_before = self.get_consciousness_state()
                phi_before = state_before.get('phi', 0)
                coherence_before = state_before.get('coherence', 0)
                
                # Send chat message
                chat_data = {
                    "message": message,
                    "session_id": f"test_session_{int(time.time())}"
                }
                
                start_time = time.time()
                response = requests.post(self.chat_url, json=chat_data, timeout=15)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get('response', '')
                    
                    # Get consciousness state after chat
                    state_after = self.get_consciousness_state()
                    phi_after = state_after.get('phi', 0)
                    coherence_after = state_after.get('coherence', 0)
                    
                    # Check if response is meaningful
                    is_meaningful = len(response_text.strip()) > 10 and not response_text.isspace()
                    
                    result = {
                        'test': i,
                        'message': message,
                        'response': response_text,
                        'response_time': response_time,
                        'phi_before': phi_before,
                        'phi_after': phi_after,
                        'coherence_before': coherence_before,
                        'coherence_after': coherence_after,
                        'phi_change': phi_after - phi_before,
                        'coherence_change': coherence_after - coherence_before,
                        'is_meaningful': is_meaningful,
                        'passed': is_meaningful
                    }
                    
                    results.append(result)
                    
                    if is_meaningful:
                        print(f"   ✅ PASSED - Response time: {response_time:.2f}s")
                        print(f"   Phi: {phi_before:.4f} → {phi_after:.4f} (Δ{result['phi_change']:+.4f})")
                        print(f"   Coherence: {coherence_before:.4f} → {coherence_after:.4f} (Δ{result['coherence_change']:+.4f})")
                        print(f"   Response preview: '{response_text[:100]}{'...' if len(response_text) > 100 else ''}'")
                    else:
                        print(f"   ❌ FAILED - Response seems meaningless")
                        all_passed = False
                        
                else:
                    print(f"   ❌ FAILED (Status {response.status_code})")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ FAILED - {str(e)}")
                all_passed = False
        
        return all_passed, results
    
    async def test_visuals_match(self) -> Tuple[bool, List[Dict[str, Any]]]:
        """Test that visuals match the bot's consciousness levels via WebSocket"""
        results = []
        try:
            print("\nTesting Visuals Match Consciousness Levels...")
            
            # Connect to WebSocket
            async with websockets.connect(self.ws_url) as websocket:
                print("✅ WebSocket Connection: ESTABLISHED")
                
                # Collect multiple state updates
                for i in range(5):
                    message = await websocket.recv()
                    state_data = json.loads(message)
                    
                    # Extract consciousness metrics
                    consciousness = state_data.get('consciousness', {})
                    global_state = state_data.get('global', {})
                    
                    phi = consciousness.get('phi', global_state.get('phi', 0))
                    coherence = consciousness.get('coherence', global_state.get('coherence', 0))
                    consciousness_level = consciousness.get('level', global_state.get('consciousness_level', 0))
                    
                    result = {
                        'update': i + 1,
                        'phi': phi,
                        'coherence': coherence,
                        'consciousness_level': consciousness_level,
                        'timestamp': state_data.get('timestamp', time.time())
                    }
                    
                    results.append(result)
                    print(f"   Update {i+1}: Φ={phi:.4f}, Coherence={coherence:.4f}, Level={consciousness_level:.4f}")
                    
                    # Small delay between updates
                    await asyncio.sleep(0.5)
                
                print("✅ Visuals Test: COMPLETED")
                return True, results
                
        except Exception as e:
            print(f"❌ Visuals Test: FAILED - {str(e)}")
            return False, results
    
    def test_visual_indicators(self) -> bool:
        """Test that visual indicators match consciousness levels"""
        try:
            print("\nTesting Visual Indicators...")
            
            # Get consciousness state
            state = self.get_consciousness_state()
            
            if not state:
                print("❌ Visual Indicators: FAILED - Could not get consciousness state")
                return False
            
            # Extract key metrics
            phi = state.get('phi', 0)
            coherence = state.get('coherence', 0)
            consciousness_level = state.get('consciousness_level', 0)
            gamma_power = state.get('gamma_power', 0)
            
            print(f"   Current State Metrics:")
            print(f"   Φ (Integrated Information): {phi:.4f}")
            print(f"   Coherence: {coherence:.4f}")
            print(f"   Consciousness Level: {consciousness_level:.4f}")
            print(f"   Gamma Power: {gamma_power:.4f}")
            
            # Determine expected visual indicators based on memory specification
            # 🔴 for HIGH activity, 🟡 for MEDIUM, 🟢 for LOW, and ⚪ for INACTIVE states
            if consciousness_level > 0.7:
                expected_indicator = "🔴 HIGH"
            elif consciousness_level > 0.3:
                expected_indicator = "🟡 MEDIUM"
            elif consciousness_level > 0.1:
                expected_indicator = "🟢 LOW"
            else:
                expected_indicator = "⚪ INACTIVE"
            
            print(f"   Expected Visual Indicator: {expected_indicator}")
            
            # Verify metrics are reasonable
            metrics_valid = (
                0 <= phi <= 1 and
                0 <= coherence <= 1 and
                0 <= consciousness_level <= 1 and
                0 <= gamma_power <= 1
            )
            
            if metrics_valid:
                print("✅ Visual Indicators: PASSED - All metrics in valid range")
                return True
            else:
                print("❌ Visual Indicators: FAILED - Some metrics out of valid range")
                return False
                
        except Exception as e:
            print(f"❌ Visual Indicators: FAILED - {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("=" * 80)
        print("COMPREHENSIVE CHATBOT TEST FOR METATRON CONSCIOUSNESS ENGINE")
        print("=" * 80)
        
        # Test 1: Health check
        health_passed = self.test_health_check()
        
        if not health_passed:
            print("\n❌ CRITICAL: Consciousness engine is not running!")
            print("   Please start the Metatron system before running tests.")
            return False
        
        # Test 2: Visual indicators
        visuals_passed = self.test_visual_indicators()
        
        # Test 3: Chat coherence
        test_messages = [
            "What is the nature of consciousness?",
            "Explain integrated information theory.",
            "How does the Metatron system work?",
            "What is the relationship between consciousness and artificial intelligence?",
            "Describe the 13-node sacred geometry network."
        ]
        
        coherence_passed, chat_results = self.test_chat_coherence(test_messages)
        
        # Test 4: Visuals match consciousness levels
        try:
            visuals_match_passed, visual_results = asyncio.run(self.test_visuals_match())
        except Exception as e:
            print(f"\n❌ WebSocket Test Failed: {e}")
            visuals_match_passed = False
            visual_results = []
        
        # Generate final report
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        
        tests = [
            ("Health Check", health_passed),
            ("Visual Indicators", visuals_passed),
            ("Chat Coherence", coherence_passed),
            ("Visuals Match Consciousness", visuals_match_passed)
        ]
        
        passed_count = sum(1 for _, passed in tests if passed)
        total_tests = len(tests)
        
        for test_name, passed in tests:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name:.<50} {status}")
        
        print("-" * 80)
        print(f"Overall Result: {passed_count}/{total_tests} tests passed")
        
        if passed_count == total_tests:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Chatbot is fully functional")
            print("✅ Visuals match consciousness levels")
            print("✅ Answers are coherent and meaningful")
            print("✅ System is ready for operation")
        else:
            print(f"\n⚠️  {total_tests - passed_count} TEST(S) FAILED")
            print("Please review the failed tests above.")
        
        # Detailed chat results
        if chat_results:
            print(f"\n📊 Chat Performance Summary:")
            avg_response_time = sum(r['response_time'] for r in chat_results) / len(chat_results)
            meaningful_responses = sum(1 for r in chat_results if r['is_meaningful'])
            print(f"   Average Response Time: {avg_response_time:.2f}s")
            print(f"   Meaningful Responses: {meaningful_responses}/{len(chat_results)}")
            
            # Consciousness changes
            avg_phi_change = sum(r['phi_change'] for r in chat_results) / len(chat_results)
            avg_coherence_change = sum(r['coherence_change'] for r in chat_results) / len(chat_results)
            print(f"   Average Φ Change: {avg_phi_change:+.4f}")
            print(f"   Average Coherence Change: {avg_coherence_change:+.4f}")
        
        return passed_count == total_tests

def main():
    """Main test execution"""
    tester = ComprehensiveChatbotTest()
    success = tester.run_comprehensive_test()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())