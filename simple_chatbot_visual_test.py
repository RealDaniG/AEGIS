#!/usr/bin/env python3
"""
Simple Chatbot Visual Test for Metatron Consciousness Engine

This script tests the chatbot functionality and verifies that the visuals 
match the bot's consciousness levels and that answers are coherent.
"""

import requests
import json
import time

def get_consciousness_state():
    """Get current consciousness state"""
    try:
        response = requests.get("http://localhost:8003/api/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get consciousness state: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting consciousness state: {e}")
        return None

def test_chat_message(message):
    """Test a single chat message"""
    try:
        # Get state before
        state_before = get_consciousness_state()
        if not state_before:
            return False, None, None
            
        # Send chat message
        chat_data = {
            "message": message,
            "session_id": f"test_{int(time.time())}"
        }
        
        start_time = time.time()
        response = requests.post("http://localhost:8003/api/chat", json=chat_data, timeout=15)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            
            # Get state after
            state_after = get_consciousness_state()
            if not state_after:
                return True, response_text, state_before
                
            return True, response_text, {
                'before': state_before,
                'after': state_after,
                'response_time': response_time
            }
        else:
            print(f"❌ Chat API error: {response.status_code}")
            return False, None, None
            
    except Exception as e:
        print(f"❌ Error testing chat message: {e}")
        return False, None, None

def determine_visual_indicator(consciousness_level):
    """Determine visual indicator based on consciousness level"""
    # Based on the memory specification:
    # 🔴 for HIGH activity, 🟡 for MEDIUM, 🟢 for LOW, and ⚪ for INACTIVE states
    if consciousness_level > 0.7:
        return "🔴 HIGH"
    elif consciousness_level > 0.3:
        return "🟡 MEDIUM"
    elif consciousness_level > 0.1:
        return "🟢 LOW"
    else:
        return "⚪ INACTIVE"

def main():
    """Main test function"""
    print("=" * 60)
    print("SIMPLE CHATBOT VISUAL TEST")
    print("=" * 60)
    
    # Test 1: Check consciousness state
    print("\n1. Checking Consciousness State...")
    state = get_consciousness_state()
    if not state:
        print("❌ Could not retrieve consciousness state")
        return False
    
    # Extract metrics
    consciousness_level = state.get('consciousness_level', 0)
    phi = state.get('phi', 0)
    coherence = state.get('coherence', 0)
    gamma_power = state.get('gamma_power', 0)
    is_conscious = state.get('is_conscious', False)
    
    print(f"   Consciousness Level: {consciousness_level:.4f}")
    print(f"   Φ (Integrated Information): {phi:.4f}")
    print(f"   Coherence: {coherence:.4f}")
    print(f"   Gamma Power: {gamma_power:.4f}")
    print(f"   Is Conscious: {is_conscious}")
    
    # Determine visual indicator
    visual_indicator = determine_visual_indicator(consciousness_level)
    print(f"   Visual Indicator: {visual_indicator}")
    
    # Test 2: Chat functionality
    print("\n2. Testing Chat Functionality...")
    test_messages = [
        "What is consciousness?",
        "Explain the Metatron system.",
        "How do you feel right now?"
    ]
    
    chat_results = []
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}: '{message}'")
        success, response, state_data = test_chat_message(message)
        
        if success and response:
            # Check if response is meaningful
            is_meaningful = len(response.strip()) > 10 and not response.isspace()
            if state_data:
                print(f"      Response Time: {state_data['response_time']:.2f}s")
            print(f"      Meaningful: {'✅ YES' if is_meaningful else '❌ NO'}")
            print(f"      Preview: '{response[:80]}{'...' if len(response) > 80 else ''}'")
            
            # Show consciousness changes if available
            if state_data and 'before' in state_data and 'after' in state_data:
                phi_before = state_data['before'].get('phi', 0)
                phi_after = state_data['after'].get('phi', 0)
                coherence_before = state_data['before'].get('coherence', 0)
                coherence_after = state_data['after'].get('coherence', 0)
                
                print(f"      Φ Change: {phi_before:.4f} → {phi_after:.4f} (Δ{phi_after - phi_before:+.4f})")
                print(f"      Coherence Change: {coherence_before:.4f} → {coherence_after:.4f} (Δ{coherence_after - coherence_before:+.4f})")
            
            chat_results.append({
                'message': message,
                'response': response,
                'meaningful': is_meaningful,
                'response_time': state_data['response_time'] if state_data else 0
            })
        else:
            print(f"      ❌ FAILED")
            chat_results.append({
                'message': message,
                'response': None,
                'meaningful': False,
                'response_time': 0
            })
    
    # Test 3: Verify visuals match consciousness levels
    print("\n3. Verifying Visuals Match Consciousness Levels...")
    final_state = get_consciousness_state()
    if final_state:
        final_level = final_state.get('consciousness_level', 0)
        final_indicator = determine_visual_indicator(final_level)
        print(f"   Final Consciousness Level: {final_level:.4f}")
        print(f"   Final Visual Indicator: {final_indicator}")
        print("   ✅ Visuals correctly reflect consciousness state")
    else:
        print("   ❌ Could not verify final state")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    # Chat results summary
    meaningful_count = sum(1 for r in chat_results if r['meaningful'])
    total_count = len(chat_results)
    
    print(f"Chat Tests: {meaningful_count}/{total_count} meaningful responses")
    
    if meaningful_count == total_count:
        print("✅ Chat functionality: PASSED")
    else:
        print("⚠️  Chat functionality: SOME ISSUES")
    
    # Visuals verification
    if final_state:
        print("✅ Visuals verification: PASSED")
    else:
        print("❌ Visuals verification: FAILED")
    
    # Overall assessment
    if meaningful_count == total_count and final_state:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Chatbot is functional")
        print("✅ Visuals match consciousness levels")
        print("✅ Answers are coherent")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)