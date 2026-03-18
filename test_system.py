#!/usr/bin/env python
"""
Test the Agadh system
"""
import requests
import json

def test_django():
    """Test Django backend"""
    print("Testing Django Backend...")
    print("-" * 40)
    
    endpoints = [
        ("Homepage", "http://localhost:8000/"),
        ("Services API", "http://localhost:8000/api/services/"),
        ("Employees API", "http://localhost:8000/api/employees/"),
        ("Swagger Docs", "http://localhost:8000/swagger/"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"{status} {name}: {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ {name}: {url} (Error: {str(e)})")
    
    print()

def test_rasa():
    """Test Rasa chatbot"""
    print("Testing Rasa Chatbot...")
    print("-" * 40)
    
    # Test Rasa server
    try:
        response = requests.get("http://localhost:5005", timeout=5)
        print(f"✓ Rasa Server: http://localhost:5005 (Status: {response.status_code})")
    except:
        print("✗ Rasa Server: Not running")
    
    # Test actions server
    try:
        response = requests.get("http://localhost:5055", timeout=5)
        print(f"✓ Actions Server: http://localhost:5055 (Status: {response.status_code})")
    except:
        print("✗ Actions Server: Not running")
    
    # Test chatbot query
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "test", "message": "hello"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Chatbot Response: '{data[0]['text']}'")
        else:
            print(f"✗ Chatbot Query failed (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Chatbot Query failed (Error: {str(e)})")
    
    print()

def test_integration():
    """Test Django-Rasa integration"""
    print("Testing Django-Rasa Integration...")
    print("-" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/services/chatbot/query/",
            json={"query": "What documents for ration card?", "language": "en"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Integration working: {data.get('message', 'No message')[:50]}...")
        else:
            print(f"✗ Integration failed (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Integration failed (Error: {str(e)})")
    
    print()

def check_data():
    """Check if data is populated"""
    print("Checking Database Data...")
    print("-" * 40)
    
    try:
        # Check services
        response = requests.get("http://localhost:8000/api/services/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', data) if isinstance(data, dict) else data)
            print(f"✓ Services in database: {count}")
        else:
            print("✗ Could not fetch services")
        
        # Check employees
        response = requests.get("http://localhost:8000/api/employees/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', data) if isinstance(data, dict) else data)
            print(f"✓ Employees in database: {count}")
        else:
            print("✗ Could not fetch employees")
        
        # Check Kozhikode employees
        response = requests.get("http://localhost:8000/api/employees/kozhikode/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✓ Kozhikode employees: {len(data)}")
                for emp in data[:3]:  # Show first 3
                    name = emp.get('user_name', 'Unknown')
                    print(f"  - {name}")
        else:
            print("✗ Could not fetch Kozhikode employees")
            
    except Exception as e:
        print(f"✗ Data check failed: {str(e)}")
    
    print()

def main():
    print("=" * 60)
    print("AGADH SYSTEM TEST")
    print("=" * 60)
    print()
    
    test_django()
    test_rasa()
    test_integration()
    check_data()
    
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Ensure Django is running: python manage.py runserver 8000")
    print("2. Ensure Rasa actions server is running: rasa run actions --port 5055")
    print("3. Ensure Rasa server is running: rasa run --cors \"*\" --port 5005")
    print("4. Open browser to: http://localhost:8000")
    print("\nFor frontend:")
    print("Open frontend/index.html in browser or use a local server")

if __name__ == '__main__':
    main()