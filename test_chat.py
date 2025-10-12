#!/usr/bin/env python3
"""
Simple test script to verify chat functionality
"""

import requests
import json

def test_chat():
    """Test the chat API"""
    url = "http://localhost:8003/api/chat"
    
    # Test data
    data = {
        "message": "What is consciousness?",
        "session_id": "test_session"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat API is working!")
            print(f"Response: {result.get('response', 'No response')}")
            return True
        else:
            print("❌ Chat API returned error")
            return False
            
    except Exception as e:
        print(f"❌ Error testing chat API: {e}")
        return False

if __name__ == "__main__":
    test_chat()