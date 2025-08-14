from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..models.ioc import IOC
from ..schemas.ioc import IOCCreate, IOCUpdate, IOCResponse

router = APIRouter()

@router.get("/", response_model=List[IOCResponse])
async def get_iocs(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = Query(None, description="Filter by active status"),
    tlp_level: Optional[str] = Query(None, description="Filter by TLP level"),
    type_id: Optional[int] = Query(None, description="Filter by IOC type"),
    db: AsyncSession = Depends(get_db)
):
    """Get all IOCs with pagination and filtering"""
    query = select(IOC)
    
    if active is not None:
        query = query.filter(IOC.active == active)
    if tlp_level:
        query = query.filter(IOC.tlp_level == tlp_level)
    if type_id:
        query = query.filter(IOC.type_id == type_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    iocs = result.scalars().all()
    return iocs

@router.get("/{ioc_id}", response_model=IOCResponse)
async def get_ioc(ioc_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific IOC by ID"""
    result = await db.execute(select(IOC).filter(IOC.id == ioc_id))
    ioc = result.scalar_one_or_none()
    if not ioc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IOC not found"
        )
    return ioc

@router.post("/", response_model=IOCResponse, status_code=status.HTTP_201_CREATED)
async def create_ioc(ioc_data: IOCCreate, db: AsyncSession = Depends(get_db)):
    """Create a new IOC"""
    result = await db.execute(select(IOC).filter(IOC.value_hash == ioc_data.value_hash))
    existing_ioc = result.scalar_one_or_none()
    
    if existing_ioc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IOC with this value hash already exists"
        )
    
    db_ioc = IOC(
        type_id=ioc_data.type_id,
        value=ioc_data.value,
        value_hash=ioc_data.value_hash,
        tlp_level=ioc_data.tlp_level,
        active=ioc_data.active,
        metadata=ioc_data.metadata_,
        source_org_id=ioc_data.source_org_id,
        created_by=ioc_data.created_by
    )
    
    db.add(db_ioc)
    await db.commit()
    await db.refresh(db_ioc)
    return db_ioc

@router.put("/{ioc_id}", response_model=IOCResponse)
async def update_ioc(
    ioc_id: UUID,
    ioc_data: IOCUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an IOC"""
    result = await db.execute(select(IOC).filter(IOC.id == ioc_id))
    ioc = result.scalar_one_or_none()
    if not ioc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IOC not found"
        )
    
    update_data = ioc_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ioc, field, value)
    
    await db.commit()
    await db.refresh(ioc)
    return ioc

@router.delete("/{ioc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ioc(ioc_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an IOC"""
    result = await db.execute(select(IOC).filter(IOC.id == ioc_id))
    ioc = result.scalar_one_or_none()
    if not ioc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IOC not found"
        )
    
    await db.delete(ioc)
    await db.commit()
    return None

@router.get("/search/", response_model=List[IOCResponse])
async def search_iocs(
    q: str = Query(..., description="Search query for IOC values"),
    limit: int = Query(50, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search IOCs by value"""
    result = await db.execute(select(IOC).filter(IOC.value.ilike(f"%{q}%")).limit(limit))
    iocs = result.scalars().all()
    return iocs
