#!/usr/bin/env python3
"""
Script to check database tables.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.database import engine
from sqlalchemy import text

def check_database():
    try:
        print("🔍 Checking database tables...")
        
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check if users table exists
            if 'users' in tables:
                print("✅ Users table exists!")
                
                # Check users table structure
                result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"))
                columns = [(row[0], row[1]) for row in result]
                
                print("Users table columns:")
                for column_name, data_type in columns:
                    print(f"  - {column_name}: {data_type}")
            else:
                print("❌ Users table does not exist!")
                
            return True
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    success = check_database()
    if success:
        print("\n🎉 Database check completed successfully!")
    else:
        print("\n💥 Database check failed!")
