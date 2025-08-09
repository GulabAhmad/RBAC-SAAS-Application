#!/usr/bin/env python3
"""
Test script to check database connection with URL encoding.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.database import engine, get_database_url
from rbac_version_2.config import settings

def test_connection():
    try:
        print(f"Testing database connection...")
        print(f"Original URL: {settings.database_url}")
        print(f"Encoded URL: {get_database_url()}")
        
        # Test the connection
        with engine.connect() as connection:
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 Database connection test completed successfully!")
    else:
        print("\n💥 Database connection test failed!")
        sys.exit(1)
