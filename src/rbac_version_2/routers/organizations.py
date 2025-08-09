from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..auth import get_current_user
from ..middleware import require_permissions
from .. import crud, schemas, models

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=schemas.Organization)
async def create_organization(
    organization: schemas.OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new organization"""
    return crud.create_organization(db=db, organization=organization)


@router.get("/", response_model=List[schemas.Organization])
async def read_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all organizations"""
    organizations = crud.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/{organization_id}", response_model=schemas.Organization)
async def read_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific organization"""
    organization = crud.get_organization(db, organization_id=organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.put("/{organization_id}", response_model=schemas.Organization)
async def update_organization(
    organization_id: int,
    organization: schemas.OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_organizations"]))
):
    """Update an organization"""
    return crud.update_organization(db=db, organization_id=organization_id, organization=organization)


@router.delete("/{organization_id}")
async def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permissions(["manage_organizations"]))
):
    """Delete an organization"""
    crud.delete_organization(db=db, organization_id=organization_id)
    return {"message": "Organization deleted successfully"}
