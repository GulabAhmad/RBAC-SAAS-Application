from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from . import models, schemas
from .auth import get_password_hash, verify_password
from .email_service import email_service


# Organization CRUD operations
def create_organization(db: Session, organization: schemas.OrganizationCreate) -> models.Organization:
    db_organization = models.Organization(**organization.model_dump())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


def get_organization(db: Session, organization_id: int) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()


def get_organization_by_name(db: Session, name: str) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.name == name).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Organization]:
    return db.query(models.Organization).offset(skip).limit(limit).all()


def update_organization(db: Session, organization_id: int, organization: schemas.OrganizationCreate) -> models.Organization:
    db_organization = get_organization(db, organization_id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    for key, value in organization.model_dump().items():
        setattr(db_organization, key, value)
    
    db.commit()
    db.refresh(db_organization)
    return db_organization


def delete_organization(db: Session, organization_id: int) -> bool:
    db_organization = get_organization(db, organization_id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db.delete(db_organization)
    db.commit()
    return True


# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if organization exists, if not create it
    organization = get_organization_by_name(db, user.organization_name)
    if not organization:
        organization = create_organization(db, schemas.OrganizationCreate(name=user.organization_name))
    
    # Get or create default role for the organization
    default_role = db.query(models.Role).filter(
        models.Role.name == "user",
        models.Role.organization_id == organization.id
    ).first()
    
    if not default_role:
        default_role = models.Role(name="user", organization_id=organization.id)
        db.add(default_role)
        db.commit()
        db.refresh(default_role)
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Generate verification code (handle email service failures gracefully)
    verification_code = None
    try:
        verification_code = email_service.generate_and_send_verification_code(user.email)
    except Exception as e:
        print(f"Warning: Failed to send verification email: {e}")
        # Generate a verification code anyway for testing
        import random
        import string
        verification_code = ''.join(random.choices(string.digits, k=6))
    
    # Create user
    user_data = user.model_dump(exclude={'password', 'organization_name'})
    user_data['hashed_password'] = hashed_password
    user_data['organization_id'] = organization.id
    user_data['role_id'] = default_role.id
    user_data['email_verification_code'] = verification_code
    user_data['email_verification_expires'] = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user_email(db: Session, email: str, verification_code: str) -> models.User:
    """Verify user email with verification code"""
    try:
        print(f"🔍 Verifying email for: {email}")
        print(f"🔍 Verification code: {verification_code}")
        
        user = db.query(models.User).filter(models.User.email == email).first()
        print(f"🔍 User found: {user is not None}")
        
        if not user:
            print(f"❌ User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        
        print(f"🔍 User details: ID={user.id}, Email={user.email}, Verified={user.is_email_verified}")
        print(f"🔍 Stored verification code: {user.email_verification_code}")
        print(f"🔍 Verification expires: {user.email_verification_expires}")
        
        if user.is_email_verified:
            print(f"❌ Email already verified for: {email}")
            raise HTTPException(status_code=400, detail="Email already verified")
        
        if not user.email_verification_code:
            print(f"❌ No verification code found for: {email}")
            raise HTTPException(status_code=400, detail="No verification code found")
        
        if user.email_verification_expires < datetime.now(timezone.utc):
            print(f"❌ Verification code expired for: {email}")
            raise HTTPException(status_code=400, detail="Verification code expired")
        
        if user.email_verification_code != verification_code:
            print(f"❌ Invalid verification code for: {email}. Expected: {user.email_verification_code}, Got: {verification_code}")
            raise HTTPException(status_code=400, detail="Invalid verification code")
        
        # Mark email as verified
        user.is_email_verified = True
        user.email_verification_code = None
        user.email_verification_expires = None
        
        db.commit()
        db.refresh(user)
        
        print(f"✅ Email verified successfully for: {email}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in verify_user_email: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Email verification failed: {str(e)}")


def request_password_reset(db: Session, email: str) -> bool:
    """Request password reset for user"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # Don't reveal if user exists or not
        return True
    
    # Generate and send reset code
    reset_code = email_service.generate_and_send_reset_code(email)
    if not reset_code:
        raise HTTPException(status_code=500, detail="Failed to send password reset email")
    
    # Save reset code
    user.password_reset_code = reset_code
    user.password_reset_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    db.commit()
    return True


def verify_password_reset_code(db: Session, email: str, reset_code: str) -> bool:
    """Verify password reset code"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.password_reset_code:
        raise HTTPException(status_code=400, detail="No reset code found")
    
    if user.password_reset_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset code expired")
    
    if user.password_reset_code != reset_code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    
    return True


def reset_password(db: Session, email: str, reset_code: str, new_password: str) -> models.User:
    """Reset user password"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.password_reset_code:
        raise HTTPException(status_code=400, detail="No reset code found")
    
    if user.password_reset_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset code expired")
    
    if user.password_reset_code != reset_code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    user.password_reset_code = None
    user.password_reset_expires = None
    
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_users_by_organization(db: Session, organization_id: int) -> List[models.User]:
    return db.query(models.User).filter(models.User.organization_id == organization_id).all()


def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> models.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Hash password if provided
    user_data = user.model_dump()
    if 'password' in user_data:
        user_data['hashed_password'] = get_password_hash(user_data.pop('password'))
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return True


# Role CRUD operations
def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    db_role = models.Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Role]:
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_roles_by_organization(db: Session, organization_id: int) -> List[models.Role]:
    return db.query(models.Role).filter(models.Role.organization_id == organization_id).all()


def update_role(db: Session, role_id: int, role: schemas.RoleCreate) -> models.Role:
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    for key, value in role.model_dump().items():
        setattr(db_role, key, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int) -> bool:
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(db_role)
    db.commit()
    return True


# Permission CRUD operations
def create_permission(db: Session, permission: schemas.PermissionCreate) -> models.Permission:
    db_permission = models.Permission(**permission.model_dump())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_permission(db: Session, permission_id: int) -> Optional[models.Permission]:
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Permission]:
    return db.query(models.Permission).offset(skip).limit(limit).all()


def update_permission(db: Session, permission_id: int, permission: schemas.PermissionCreate) -> models.Permission:
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    for key, value in permission.model_dump().items():
        setattr(db_permission, key, value)
    
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_id: int) -> bool:
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    db.delete(db_permission)
    db.commit()
    return True


# Role-Permission CRUD operations
def assign_permission_to_role(db: Session, role_id: int, permission_id: int) -> models.Role:
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    if db_permission not in db_role.permissions:
        db_role.permissions.append(db_permission)
        db.commit()
        db.refresh(db_role)
    
    return db_role


def remove_permission_from_role(db: Session, role_id: int, permission_id: int) -> models.Role:
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    if db_permission in db_role.permissions:
        db_role.permissions.remove(db_permission)
        db.commit()
        db.refresh(db_role)
    
    return db_role
