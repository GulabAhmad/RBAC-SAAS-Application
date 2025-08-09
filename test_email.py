#!/usr/bin/env python3
"""
Test script to verify email functionality.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.email_service import email_service

def test_email_service():
    try:
        print("Testing email service...")
        
        # Test email generation
        test_email = "test@example.com"
        verification_code = email_service.generate_and_send_verification_code(test_email)
        
        if verification_code:
            print(f"✅ Verification code generated: {verification_code}")
            print("✅ Email service is working!")
            return True
        else:
            print("❌ Failed to generate verification code")
            return False
            
    except Exception as e:
        print(f"❌ Error testing email service: {e}")
        return False

if __name__ == "__main__":
    success = test_email_service()
    if success:
        print("\n🎉 Email service test completed successfully!")
    else:
        print("\n💥 Email service test failed!")
        sys.exit(1)
