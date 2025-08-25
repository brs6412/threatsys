from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from src.dependencies import get_database
from src.services.organization_service import OrganizationService
from src.schemas.organization import (
    OrganizationCreate, 
    OrganizationUpdate, 
    OrganizationResponse, 
    OrganizationDetailResponse
)

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_database)
):
    """Get all organizations with pagination"""
    org_service = OrganizationService(db)
    orgs = await org_service.get_organizations(
        skip=skip,
        limit=limit
    )
    return orgs

@router.get("/{org_id}", response_model=OrganizationDetailResponse)
async def get_organization(org_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get a specific organization by ID"""
    org_service = OrganizationService(db)
    org = await org_service.get_organization(org_id)
    return org

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate, db: AsyncSession = Depends(get_database)):
    """Create a new organization"""
    org_service = OrganizationService(db)
    org = await org_service.create_organization(org_data)
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: uuid.UUID,
    org_data: OrganizationUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update an organization"""
    org_service = OrganizationService(db)
    org = await org_service.update_organization(org_id, org_data)
    return org

@router.delete("/{org_id}", status_code=204)
async def delete_organization(org_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Delete an organization"""
    org_service = OrganizationService(db)
    await org_service.delete_organization(org_id)
    return
