from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import Optional, List, Dict
from datetime import datetime
import uuid

from src.models.ioc import IOC
from src.schemas.ioc import IOCCreate, IOCUpdate, IOCSearchParams
from src.exceptions import IOCNotFoundException
from src.utils.security import sha256_hash

class IOCService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_ioc(self, ioc_id: uuid.UUID, include_relationships: bool = False) -> Optional[IOC]:
        statement = (
            select(IOC)
            .options(
                joinedload(IOC.ioc_type),
                joinedload(IOC.source_organization),
                joinedload(IOC.creator)
            )
            .where(IOC.id == ioc_id)
        )
        result = await self.db.execute(statement)
        ioc = result.scalars().first()

        if not ioc:
            raise IOCNotFoundException('ID', str(ioc_id))

        return ioc
    
    async def get_iocs(
        self,
        skip: int = 0,
        limit: int = 100,
        active: Optional[bool] = None,
        tlp_level: Optional[str] = None,
        type_id: Optional[int] = None,
    ) -> List[IOC]:
        statement = (
            select(IOC)
            .options(
                joinedload(IOC.ioc_type),
                joinedload(IOC.source_organization),
                joinedload(IOC.creator)
            )
        )

        if active is not None:
            statement = statement.where(IOC.active == active)

        if tlp_level is not None:
            statement = statement.where(IOC.tlp_level == tlp_level)

        if type_id is not None:
            statement = statement.where(IOC.type_id == type_id)

        statement = statement.offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def get_by_value(self, value: str) -> Optional[IOC]:
        value_hash = sha256_hash(value)
        return await self.get_by_hash(value_hash)

    async def get_by_hash(self, value_hash: str) -> Optional[IOC]:
        statement = (
            select(IOC)
            .where(IOC.value_hash == value_hash)
        )
        result = await self.db.execute(statement)
        ioc = result.scalars().first()

        if not ioc:
            raise IOCNotFoundException('hash', str(value_hash))
        
        return ioc

    async def search_iocs(
        self,
        params: IOCSearchParams,
        skip: int = 0,
        limit: int = 100
    ) -> List[IOC]:
        statement = (
            select(IOC)
        )

        if params.value:
            value_hash = sha256_hash(params.value)
            statement = statement.where(IOC.value_hash == value_hash)
        if params.value_hash:
            statement = statement.where(IOC.value_hash == params.value_hash)
        if params.value_contains:
            statement = statement.where(IOC.value.ilike(f"%{params.value_contains}%"))
        if params.type_id:
            statement = statement.where(IOC.type_id == params.type_id)
        if params.tlp_level:
            statement = statement.where(IOC.tlp_level == params.tlp_level.value)
        if params.active is not None:
            statement = statement.where(IOC.active == params.active)
        if params.source_org_id:
            statement = statement.where(IOC.source_org_id == params.source_org_id)
        if params.created_by:
            statement = statement.where(IOC.created_by == params.created_by)
        if params.created_after:
            statement = statement.where(IOC.created_at >= params.created_after)
        if params.created_before:
            statement = statement.where(IOC.created_at < params.created_before)
        if params.last_seen_after:
            statement = statement.where(IOC.last_seen >= params.last_seen_after)
        if params.last_seen_before:
            statement = statement.where(IOC.last_seen < params.last_seen_before)
        
        statement = statement.options(
            joinedload(IOC.ioc_type),
            joinedload(IOC.source_organization),
            joinedload(IOC.creator)
        )
        statement = statement.offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()
    
    async def batch_lookup_by_values(self, values: List[str]) -> Dict[str, IOC]:
        if not values:
            return {}
        value_map = {value: sha256_hash(value) for value in values}
        results: Dict[str, IOC] = {}
        chunk_size = 1000
        items = list(value_map.items())
        for i in range(0, len(items), chunk_size):
            chunk = values[i:i + chunk_size]
            chunk_hashes = [v for _, v in chunk]

            statement = (
                select(IOC)
                .options(
                    joinedload(IOC.ioc_type),
                    joinedload(IOC.source_organization),
                    joinedload(IOC.creator)
                )
                .where(IOC.value_hash.in_(chunk_hashes))
            )
            result = await self.db.execute(statement)

            for ioc in result.scalars().all():
                for original_value, hash_ in chunk:
                    if ioc.value_hash == hash_:
                        results[original_value] = ioc
        return results
    
    async def batch_lookup_by_hashes(self, value_hashes: List[str]) -> List[IOC]:
        if not value_hashes:
            return []
        results: List[IOC] = []
        chunk_size = 1000
        for i in range(0, len(value_hashes), chunk_size):
            chunk = value_hashes[i:i + chunk_size]
            statement = (
                select(IOC)
                .options(
                    joinedload(IOC.ioc_type),
                    joinedload(IOC.source_organization),
                    joinedload(IOC.creator)
                )
                .where(IOC.value_hash.in_(chunk))
            )
            result = await self.db.execute(statement)
            results.extend(result.scalars().all())
        return results
    
    async def create_ioc(self, ioc_data: IOCCreate, created_by: uuid.UUID) -> IOC:
        value_hash = sha256_hash(ioc_data.value)
        existing = None
        try:
            existing = await self.get_by_hash(value_hash)
        except IOCNotFoundException:
            pass

        if existing:
            existing.last_seen = datetime.now()
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        db_ioc = IOC(
            type_id=ioc_data.type_id,
            value=ioc_data.value,
            value_hash=value_hash,
            tlp_level=ioc_data.tlp_level.value,
            active=ioc_data.active,
            metadata_=ioc_data.metadata_,
            source_org_id=ioc_data.source_org_id,
            created_by=created_by
        )
        
        self.db.add(db_ioc)
        await self.db.commit()
        await self.db.refresh(db_ioc)
        return db_ioc

    async def update_ioc(self, ioc_id: uuid.UUID, ioc_data: IOCUpdate) -> Optional[IOC]:
        ioc = await self.get_ioc(ioc_id)
        if not ioc: 
            raise IOCNotFoundException('ID', str(ioc_id))
        
        update_data = ioc_data.model_dump(exclude_unset=True, by_alias=True)

        if "value" in update_data:
            update_data["value_hash"] = sha256_hash(update_data["value"])

        for f, v in update_data.items():
            setattr(ioc, f, v)
        
        ioc.updated_at = datetime.now()
        
        await self.db.commit()
        await self.db.refresh(ioc)
        return ioc
    
    async def delete_ioc(self, ioc_id: uuid.UUID) -> None:
        ioc = await self.get_ioc(ioc_id)
        if not ioc:
            raise IOCNotFoundException(str(ioc_id))
        
        await self.db.delete(ioc)
        await self.db.commit()
        return
        
