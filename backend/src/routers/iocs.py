from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict
import uuid

from src.dependencies import get_database
from src.services.ioc_service import IOCService
from src.schemas.ioc import (
    IOCCreate, IOCUpdate, IOCSearchParams, IOCResponse, IOCDetailResponse, IOCLookupByValue
)

router = APIRouter()

@router.get("/", response_model=List[IOCResponse])
async def get_iocs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active: Optional[bool] = Query(None),
    tlp_level: Optional[str] = Query(None),
    type_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_database)
):
    """Get all IOCs with pagination and filtering"""
    ioc_service = IOCService(db)
    iocs = await ioc_service.get_iocs(skip=skip, limit=limit, active=active, tlp_level=tlp_level, type_id=type_id)
    return [
        IOCResponse(
            id=ioc.id,
            value=ioc.value,
            value_hash=ioc.value_hash,
            tlp_level=ioc.tlp_level,
            active=ioc.active,
            source_organization=ioc.source_organization.name if ioc.source_organization else None,
            creator=ioc.creator.email if ioc.creator else None,
            last_seen=ioc.last_seen,
            ioc_type=ioc.ioc_type
        )
        for ioc in iocs
    ]

@router.get("/{ioc_id}", response_model=IOCDetailResponse)
async def get_ioc(ioc_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get a specific IOC by ID"""
    ioc_service = IOCService(db)
    ioc = await ioc_service.get_ioc(ioc_id)
    return IOCDetailResponse(
            id=ioc.id,
            value=ioc.value,
            value_hash=ioc.value_hash,
            tlp_level=ioc.tlp_level,
            active=ioc.active,
            source_organization=ioc.source_organization.name if ioc.source_organization else None,
            creator=ioc.creator.email if ioc.creator else None,
            created_at=ioc.created_at,
            updated_at=ioc.updated_at,
            last_seen=ioc.last_seen,
            received_at=ioc.received_at,
            ioc_type=ioc.ioc_type
        )

@router.post("/", response_model=IOCResponse, status_code=201)
async def create_ioc(ioc_data: IOCCreate, db: AsyncSession = Depends(get_database)):
    """Create a new IOC"""
    ioc_service = IOCService(db)
    return await ioc_service.create_ioc(ioc_data)

@router.put("/{ioc_id}", response_model=IOCResponse)
async def update_ioc(
    ioc_id: uuid.UUID,
    ioc_data: IOCUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update an IOC"""
    ioc_service = IOCService(db)
    return await ioc_service.update_ioc(ioc_id, ioc_data)

@router.delete("/{ioc_id}", status_code=204)
async def delete_ioc(ioc_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Delete an IOC"""
    ioc_service = IOCService(db)
    return await ioc_service.delete_ioc(ioc_id)

@router.get("/search/", response_model=List[IOCResponse])
async def search_iocs(
    search: IOCSearchParams = Depends(),
    skip: int = Query(100, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_database)
):
    """Search IOCs by value"""
    ioc_service = IOCService(db)
    return await ioc_service.search_iocs(params=search, skip=skip, limit=limit)

@router.get("/by-typed-value/{type_id}/{value}") # , response_model=IOCResponse
async def get_ioc_by_typed_value(
    type_id: int,
    value: str,
    db: AsyncSession = Depends(get_database)
):
    """Get IOC by value with type-aware hash computation"""
    service = IOCService(db)
    return await service.get_by_value(type_id, value)

@router.post("/batch-lookup-typed", response_model=Dict[str, IOCResponse])
async def batch_lookup_by_typed_values(
    lookups: List[IOCLookupByValue],
    db: AsyncSession = Depends(get_database)
):
    """Batch lookup IOCs by values with type-aware hash computation"""
    service = IOCService(db)
    results = await service.batch_lookup_by_typed_values(lookups)
    return results