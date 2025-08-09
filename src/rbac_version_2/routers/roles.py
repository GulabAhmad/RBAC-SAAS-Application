from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..auth import get_current_user
from ..middleware import require_permissions
from .. import crud, schemas, models

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=schemas.Role)
async def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_roles"]))
):
    """Create a new role"""
    return crud.create_role(db=db, role=role)


@router.get("/", response_model=List[schemas.Role])
async def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_roles"]))
):
    """Get all roles"""
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles


@router.get("/{role_id}", response_model=schemas.Role)
async def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_roles"]))
):
    """Get a specific role"""
    role = crud.get_role(db, role_id=role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(
    role_id: int,
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_roles"]))
):
    """Update a role"""
    return crud.update_role(db=db, role_id=role_id, role=role)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_roles"]))
):
    """Delete a role"""
    crud.delete_role(db=db, role_id=role_id)
    return {"message": "Role deleted successfully"}


@router.get("/organization/{organization_id}", response_model=List[schemas.Role])
async def read_roles_by_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["view_roles"]))
):
    """Get all roles in a specific organization"""
    roles = crud.get_roles_by_organization(db, organization_id=organization_id)
    return roles


@router.post("/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_roles"]))
):
    """Assign a permission to a role"""
    role = crud.assign_permission_to_role(db=db, role_id=role_id, permission_id=permission_id)
    return {"message": "Permission assigned to role successfully", "role": role}


@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_roles"]))
):
    """Remove a permission from a role"""
    role = crud.remove_permission_from_role(db=db, role_id=role_id, permission_id=permission_id)
    return {"message": "Permission removed from role successfully", "role": role}
