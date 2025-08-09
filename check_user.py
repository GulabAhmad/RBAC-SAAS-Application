#!/usr/bin/env python3
"""
Script to check if a user exists in the database.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.database import SessionLocal
from rbac_version_2.models import User
from datetime import datetime, timezone

def check_user(email: str):
    try:
        print(f"🔍 Checking user: {email}")
        
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"✅ User found!")
            print(f"  - ID: {user.id}")
            print(f"  - Email: {user.email}")
            print(f"  - First Name: {user.first_name}")
            print(f"  - Last Name: {user.last_name}")
            print(f"  - Email Verified: {user.is_email_verified}")
            print(f"  - Verification Code: {user.email_verification_code}")
            print(f"  - Verification Expires: {user.email_verification_expires}")
            
            if user.email_verification_expires:
                now = datetime.now(timezone.utc)
                print(f"  - Current Time: {now}")
                print(f"  - Expired: {user.email_verification_expires < now}")
            
            return user
        else:
            print(f"❌ User not found!")
            return None
            
    except Exception as e:
        print(f"❌ Error checking user: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    email = "test@example.com"
    user = check_user(email)
    if user:
        print(f"\n🎉 User check completed successfully!")
    else:
        print(f"\n💥 User check failed!")
