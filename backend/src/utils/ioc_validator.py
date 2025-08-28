from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.ioc_type import IOCType
from src.utils.ioc_utils import IOCUtils


class IOCValidator:
    """Validator for IOC types"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_ioc_type_by_id(self, type_id: int) -> Optional['IOCType']:
        """Get IOC type by ID"""
        result = await self.db.execute(
            select(IOCType).where(IOCType.id == type_id)
        )
        return result.scalar_one_or_none()
    
    async def validate_and_normalize_ioc(self, type_id: int, value: str) -> tuple[str, str]:
        """Validate IOC value and return (normalized_value, value_hash)"""
        ioc_type = await self.get_ioc_type_by_id(type_id)
        if not ioc_type:
            raise ValueError(f"Invalid IOC type ID: {type_id}")
        
        if not IOCUtils.validate_value(ioc_type.name, value):
            raise ValueError(f"Invalid format for {ioc_type.name}: {value}")
        
        normalized_value = IOCUtils.get_normalized_value(ioc_type.name, value) 

        value_hash = IOCUtils.compute_hash(ioc_type.name, normalized_value)
        
        return normalized_value, value_hash