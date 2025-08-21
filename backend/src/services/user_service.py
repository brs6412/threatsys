from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import Optional, List
import uuid

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.exceptions import UserNotFoundException, UserExistsException

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user(self, user_id: uuid.UUID) -> Optional[User]:
        statement = (
            select(User)
            .options(
                joinedload(User.role),
                joinedload(User.organization)
            )
            .where(User.id == user_id)
        )
        result = await self.db.execute(statement)
        user = result.scalars().first()

        if not user:
            raise UserNotFoundException(str(user_id))
        
        return user

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        organization_id: Optional[uuid.UUID] = None
    ) -> List[User]:
        statement = (
            select(User)
            .options(
                joinedload(User.role),
                joinedload(User.organization)
            )
        )

        if organization_id:
            statement = statement.where(User.organization_id == organization_id)

        statement = statement.offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()
    
    async def create_user(self, user_data: UserCreate) -> User:
        statement = select(User).where(User.email == user_data.email)
        result = await self.db.execute(statement)
        user = result.scalars().first()

        if user:
            raise UserExistsException(str(user_data.email))
        user = User(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        result = await self.db.get(User, user_id)
        user = result.scalars().first()

        if not user:
            raise UserNotFoundException(str(user_id))
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.db.get(User, user_id)

        if not user:
            raise UserNotFoundException(str(user_id))
        
        await self.db.delete(user)
        await self.db.commit()
        return