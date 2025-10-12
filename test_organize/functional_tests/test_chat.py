import requests
import json

# Test the Metatron chat API
url = "http://localhost:8003/api/chat"
data = {
    "message": "Hello, consciousness!",
    "session_id": "test_session"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", str(e))