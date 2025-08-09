#!/usr/bin/env python3
"""
Database initialization script for RBAC system.
This script creates sample organizations, roles, permissions, and users.
"""

import asyncio
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Organization, User, Role, Permission
from .auth import get_password_hash
from . import crud, schemas


def init_db():
    """Initialize the database with sample data"""
    db = SessionLocal()
    
    try:
        # Create sample permissions
        permissions_data = [
            {"name": "view_users", "description": "View users"},
            {"name": "manage_users", "description": "Manage users"},
            {"name": "view_roles", "description": "View roles"},
            {"name": "manage_roles", "description": "Manage roles"},
            {"name": "view_permissions", "description": "View permissions"},
            {"name": "manage_permissions", "description": "Manage permissions"},
            {"name": "manage_organizations", "description": "Manage organizations"},
            {"name": "view_organizations", "description": "View organizations"},
        ]
        
        permissions = []
        for perm_data in permissions_data:
            permission = crud.create_permission(db, schemas.PermissionCreate(**perm_data))
            permissions.append(permission)
            print(f"Created permission: {permission.name}")
        
        # Create sample organization
        org = crud.create_organization(db, schemas.OrganizationCreate(name="Sample Organization"))
        print(f"Created organization: {org.name}")
        
        # Create sample roles
        roles_data = [
            {"name": "admin", "organization_id": org.id},
            {"name": "manager", "organization_id": org.id},
            {"name": "user", "organization_id": org.id},
        ]
        
        roles = []
        for role_data in roles_data:
            role = crud.create_role(db, schemas.RoleCreate(**role_data))
            roles.append(role)
            print(f"Created role: {role.name}")
        
        # Assign permissions to roles
        admin_role = roles[0]  # admin
        manager_role = roles[1]  # manager
        user_role = roles[2]  # user
        
        # Admin gets all permissions
        for permission in permissions:
            crud.assign_permission_to_role(db, admin_role.id, permission.id)
        
        # Manager gets most permissions except manage_organizations
        manager_permissions = [p for p in permissions if p.name != "manage_organizations"]
        for permission in manager_permissions:
            crud.assign_permission_to_role(db, manager_role.id, permission.id)
        
        # User gets basic view permissions
        user_permissions = [p for p in permissions if p.name.startswith("view_")]
        for permission in user_permissions:
            crud.assign_permission_to_role(db, user_role.id, permission.id)
        
        print("Assigned permissions to roles")
        
        # Create sample users
        users_data = [
            {
                "name": "Admin User",
                "email": "admin@example.com",
                "password": "admin123",
                "organization_id": org.id,
                "role_id": admin_role.id
            },
            {
                "name": "Manager User",
                "email": "manager@example.com",
                "password": "manager123",
                "organization_id": org.id,
                "role_id": manager_role.id
            },
            {
                "name": "Regular User",
                "email": "user@example.com",
                "password": "user123",
                "organization_id": org.id,
                "role_id": user_role.id
            }
        ]
        
        for user_data in users_data:
            user = crud.create_user(db, schemas.UserCreate(**user_data))
            print(f"Created user: {user.name} ({user.email})")
        
        print("\nDatabase initialization completed successfully!")
        print("\nSample users created:")
        print("1. Admin User (admin@example.com) - password: admin123")
        print("2. Manager User (manager@example.com) - password: manager123")
        print("3. Regular User (user@example.com) - password: user123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
