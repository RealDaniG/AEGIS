import requests
import json

# Test the Metatron consciousness API
url = "http://localhost:8003/api/input"
data = {
    "physical": 0.5,
    "emotional": 0.3,
    "mental": 0.7,
    "spiritual": 0.8,
    "temporal": 0.2,
    "session_id": "consciousness_test"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", str(e))

# Check the status after input
status_url = "http://localhost:8003/api/status"
try:
    status_response = requests.get(status_url)
    print("\nStatus after input:", status_response.json())
except Exception as e:
    print("Error getting status:", str(e))