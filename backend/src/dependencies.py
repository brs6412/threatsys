from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from fastapi import Depends

async def get_database() -> AsyncSession:
    async for db in get_db():
        yield db
