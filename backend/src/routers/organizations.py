from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.organization import Organization
from ..schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all organizations with pagination"""
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    organizations = result.scalars().all()
    return organizations

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific organization by ID"""
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return organization

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    """Create a new organization"""
    # Check if organization already exists
    result = await db.execute(select(Organization).filter(Organization.name == org_data.name))
    existing_org = result.scalar_one_or_none()
    
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this name already exists"
        )
    
    db_org = Organization(
        name=org_data.name,
        tier=org_data.tier
    )
    
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: UUID,
    org_data: OrganizationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an organization"""
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    update_data = org_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)
    
    await db.commit()
    await db.refresh(organization)
    return organization

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an organization"""
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    await db.delete(organization)
    await db.commit()
    return None
