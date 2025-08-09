#!/usr/bin/env python3
"""
Test script to test user registration functionality.
"""

import requests
import json

def test_registration():
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Test data
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "test123",
        "confirm_password": "test123",
        "organization_name": "Test Organization"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Testing user registration...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Registration successful!")
            print(f"User ID: {result.get('id')}")
            print(f"Email: {result.get('email')}")
            print(f"Organization: {result.get('organization', {}).get('name')}")
            return True
        else:
            print(f"❌ Registration failed!")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

if __name__ == "__main__":
    success = test_registration()
    if success:
        print("\n🎉 Registration test completed successfully!")
    else:
        print("\n💥 Registration test failed!")
