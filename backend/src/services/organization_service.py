from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import Optional, List
import uuid 

from src.models.organization import Organization
from src.schemas.organization import OrganizationCreate, OrganizationUpdate
from src.exceptions import OrganizationNotFoundException, OrganizationExistsException

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_organization(self, org_id: uuid.UUID) -> Organization:
        statement = select(Organization).where(Organization.id == org_id)
        result = await self.db.execute(statement)
        org = result.scalars().first()

        if not org:
            raise OrganizationNotFoundException(str(org_id))
        
        return org

    async def get_organizations(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        statement = select(Organization).offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def create_organization(self, org_data: OrganizationCreate) -> Organization:
        statement = select(Organization).where(Organization.name == org_data.name)
        result = await self.db.execute(statement)
        org = result.scalars().first()

        if org:
            raise OrganizationExistsException(str(org_data.name))

        org = Organization(**org_data.dict())
        self.db.add(org)
        await self.db.commit()
        await self.db.refresh(org)
        return org

    async def update_organization(self, org_id: uuid.UUID, org_data: OrganizationUpdate) -> Organization:
        result = await self.db.get(Organization, org_id)
        org = result.scalars().first()

        if not org:
            raise OrganizationNotFoundException(str(org_id))
        
        update_data = org_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(org, field, value)
        
        await self.db.commit()
        await self.db.refresh(org)
        return org
    
    async def delete_organization(self, org_id: uuid.UUID, org_data: OrganizationUpdate) -> Organization:
        org = await self.db.get(Organization, org_id)

        if not org:
            raise OrganizationNotFoundException(str(org_id))
        
        await self.db.delete(org)
        await self.db.commit()
        return