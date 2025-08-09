#!/usr/bin/env python3
"""
Test script to check database connection and create tables.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.database import engine, Base
from rbac_version_2.models import Organization, User, Role, Permission, role_permissions
from rbac_version_2.config import settings

def test_database():
    try:
        print(f"Testing database connection to: {settings.database_url}")
        
        # Test the connection
        with engine.connect() as connection:
            print("✅ Database connection successful!")
        
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
