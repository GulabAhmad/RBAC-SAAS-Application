#!/usr/bin/env python3
"""
Script to initialize the database with sample data.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rbac_version_2.init_db import init_db

if __name__ == "__main__":
    print("🚀 Initializing database with sample data...")
    init_db()
    print("✅ Database initialization completed!")
