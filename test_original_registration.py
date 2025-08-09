#!/usr/bin/env python3
"""
Test script to test the original registration request that was failing.
"""

import requests
import json

def test_original_registration():
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Original test data that was failing
    data = {
        "first_name": "alpha",
        "last_name": "beta",
        "email": "dobafof815@cronack.com",
        "password": "alpha123",
        "confirm_password": "alpha123",
        "organization_name": "Alpha Enterprise"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Testing original registration request...")
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
            print(f"First Name: {result.get('first_name')}")
            print(f"Last Name: {result.get('last_name')}")
            print(f"Organization: {result.get('organization', {}).get('name')}")
            print(f"Email Verified: {result.get('is_email_verified')}")
            return True
        else:
            print(f"❌ Registration failed!")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

if __name__ == "__main__":
    success = test_original_registration()
    if success:
        print("\n🎉 Original registration test completed successfully!")
    else:
        print("\n💥 Original registration test failed!")
