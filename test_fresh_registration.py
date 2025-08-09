#!/usr/bin/env python3
"""
Test script to register a new user and then test email verification.
"""

import requests
import json
import time

def test_fresh_registration_and_verification():
    # Step 1: Register a new user
    register_url = "http://localhost:8000/api/v1/auth/register"
    
    register_data = {
        "first_name": "Fresh",
        "last_name": "User",
        "email": "fresh@example.com",
        "password": "fresh123",
        "confirm_password": "fresh123",
        "organization_name": "Fresh Organization"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Step 1: Registering new user...")
        print(f"URL: {register_url}")
        print(f"Data: {json.dumps(register_data, indent=2)}")
        
        register_response = requests.post(register_url, json=register_data, headers=headers)
        
        print(f"Status Code: {register_response.status_code}")
        
        if register_response.status_code == 200:
            register_result = register_response.json()
            print(f"✅ Registration successful!")
            print(f"User ID: {register_result.get('id')}")
            print(f"Email: {register_result.get('email')}")
            print(f"Email Verified: {register_result.get('is_email_verified')}")
            
            # Step 2: Get the verification code from the database
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
            
            from rbac_version_2.database import SessionLocal
            from rbac_version_2.models import User
            
            db = SessionLocal()
            user = db.query(User).filter(User.email == "fresh@example.com").first()
            db.close()
            
            if user and user.email_verification_code:
                verification_code = user.email_verification_code
                print(f"🔍 Verification code: {verification_code}")
                
                # Step 3: Verify email
                verify_url = "http://localhost:8000/api/v1/auth/verify-email"
                
                verify_data = {
                    "email": "fresh@example.com",
                    "verification_code": verification_code
                }
                
                print("\n🔍 Step 2: Verifying email...")
                print(f"URL: {verify_url}")
                print(f"Data: {json.dumps(verify_data, indent=2)}")
                
                verify_response = requests.post(verify_url, json=verify_data, headers=headers)
                
                print(f"Status Code: {verify_response.status_code}")
                
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    print(f"✅ Email verification successful!")
                    print(f"User ID: {verify_result.get('id')}")
                    print(f"Email: {verify_result.get('email')}")
                    print(f"Email Verified: {verify_result.get('is_email_verified')}")
                    return True
                else:
                    print(f"❌ Email verification failed!")
                    print(f"Response: {verify_response.text}")
                    return False
            else:
                print(f"❌ No verification code found for user!")
                return False
        else:
            print(f"❌ Registration failed!")
            print(f"Response: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing fresh registration and verification: {e}")
        return False

if __name__ == "__main__":
    success = test_fresh_registration_and_verification()
    if success:
        print("\n🎉 Fresh registration and verification test completed successfully!")
    else:
        print("\n💥 Fresh registration and verification test failed!")
