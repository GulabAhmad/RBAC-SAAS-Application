#!/usr/bin/env python3
"""
Test script to test email verification functionality.
"""

import requests
import json

def test_email_verification():
    url = "http://localhost:8000/api/v1/auth/verify-email"
    
    # Test data - using a user that was just registered
    data = {
        "email": "test@example.com",
        "verification_code": "123456"  # This will be the fallback code generated during registration
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Testing email verification...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email verification successful!")
            print(f"User ID: {result.get('id')}")
            print(f"Email: {result.get('email')}")
            print(f"Email Verified: {result.get('is_email_verified')}")
            return True
        else:
            print(f"❌ Email verification failed!")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing email verification: {e}")
        return False

if __name__ == "__main__":
    success = test_email_verification()
    if success:
        print("\n🎉 Email verification test completed successfully!")
    else:
        print("\n💥 Email verification test failed!")
