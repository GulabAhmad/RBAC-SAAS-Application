from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..auth import get_current_user
from ..middleware import require_permissions
from .. import crud, schemas, models

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("/", response_model=schemas.Permission)
async def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_permissions"]))
):
    """Create a new permission"""
    return crud.create_permission(db=db, permission=permission)


@router.get("/", response_model=List[schemas.Permission])
async def read_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_permissions"]))
):
    """Get all permissions"""
    permissions = crud.get_permissions(db, skip=skip, limit=limit)
    return permissions


@router.get("/{permission_id}", response_model=schemas.Permission)
async def read_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_permissions"]))
):
    """Get a specific permission"""
    permission = crud.get_permission(db, permission_id=permission_id)
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.put("/{permission_id}", response_model=schemas.Permission)
async def update_permission(
    permission_id: int,
    permission: schemas.PermissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_permissions"]))
):
    """Update a permission"""
    return crud.update_permission(db=db, permission_id=permission_id, permission=permission)


@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_permissions"]))
):
    """Delete a permission"""
    crud.delete_permission(db=db, permission_id=permission_id)
    return {"message": "Permission deleted successfully"}
