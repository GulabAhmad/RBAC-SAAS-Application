from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .models import User, Permission
from .auth import get_current_user


def require_permissions(required_permissions: List[str]):
    """
    Middleware decorator to check if the current user has the required permissions
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Get user's role permissions
        user_permissions = [perm.name for perm in current_user.role.permissions]
        
        # Check if user has all required permissions
        for permission in required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' required"
                )
        
        return current_user
    
    return permission_checker


def require_any_permission(required_permissions: List[str]):
    """
    Middleware decorator to check if the current user has at least one of the required permissions
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Get user's role permissions
        user_permissions = [perm.name for perm in current_user.role.permissions]
        
        # Check if user has at least one required permission
        for permission in required_permissions:
            if permission in user_permissions:
                return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"At least one of these permissions required: {', '.join(required_permissions)}"
        )
    
    return permission_checker


def require_role(required_roles: List[str]):
    """
    Middleware decorator to check if the current user has one of the required roles
    """
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if current_user.role.name not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role.name}' not authorized. Required roles: {', '.join(required_roles)}"
            )
        
        return current_user
    
    return role_checker
