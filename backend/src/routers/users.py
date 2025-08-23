from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from src.dependencies import get_database
from src.services.user_service import UserService
from src.schemas.user import UserCreate, UserUpdate, UserResponse, UserBase

router = APIRouter()

@router.get("/", response_model=List[UserBase])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    organization_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_database)
):
    """Get all users with filtering and pagination"""
    user_service = UserService(db)
    users = await user_service.get_users(
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Get a specific user by ID with role and organization details"""
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_database)):
    """Create a new user"""
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a user"""
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data)
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_database)):
    """Delete a user"""
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return
