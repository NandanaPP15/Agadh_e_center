"""
Test script for Agadh platform
"""
import requests
import json

def test_apis():
    """Test all API endpoints"""
    base_url = "http://localhost:8000/api"
    
    endpoints = [
        "/services/",
        "/documents/",
        "/employees/",
        "/auth/login/",
        "/auth/register/"
    ]
    
    print("Testing Agadh APIs...")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"{endpoint}: {'✓' if response.status_code == 200 else '✗'} ({response.status_code})")
        except:
            print(f"{endpoint}: ✗ (Connection failed)")

def test_chatbot():
    """Test chatbot integration"""
    print("\nTesting Chatbot Integration...")
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "test_user", "message": "hello"},
            timeout=5
        )
        print(f"Chatbot: {'✓' if response.status_code == 200 else '✗'}")
    except:
        print("Chatbot: ✗ (Connection failed)")

if __name__ == "__main__":
    test_apis()
    test_chatbot()
    print("\nTest completed!")