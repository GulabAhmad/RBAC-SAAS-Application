from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..auth import get_current_user
from ..middleware import require_permissions, require_any_permission
from .. import crud, schemas, models

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_users"]))
):
    """Create a new user"""
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_users"]))
):
    """Get all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_users"]))
):
    """Get a specific user"""
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_users"]))
):
    """Update a user"""
    return crud.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_users"]))
):
    """Delete a user"""
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}


@router.get("/organization/{organization_id}", response_model=List[schemas.User])
async def read_users_by_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_users"]))
):
    """Get all users in a specific organization"""
    users = crud.get_users_by_organization(db, organization_id=organization_id)
    return users
