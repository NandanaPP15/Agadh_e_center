import requests
import json
import time

print("Testing Rasa Chatbot...")
print("=" * 50)

# Wait for services
time.sleep(5)

test_messages = [
    "hello",
    "What documents for ration card?",
    "What documents for passport?",
    "What documents for aadhaar?",
    "What services do you provide?",
    "thank you",
    "bye"
]

for msg in test_messages:
    print(f"\nYou: {msg}")
    
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "test_user", "message": msg},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                bot_reply = data[0]['text']
                print(f"Bot: {bot_reply[:100]}..." if len(bot_reply) > 100 else f"Bot: {bot_reply}")
            else:
                print("Bot: (No response)")
        else:
            print(f"Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(1)

print("\n" + "=" * 50)
print("Test completed!")