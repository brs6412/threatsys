from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

# Base schema
class UserBase(BaseModel):
    email: EmailStr

# Creating a user
class UserCreate(UserBase):
    organization_id: Optional[UUID] = None
    role_id: int = 3

# Updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    organization_id: Optional[UUID] = None
    role_id: Optional[int] = None

# Get user data
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    organization_id: Optional[UUID] = None
    role_id: int
    created_at: datetime
    last_login: Optional[datetime] = None