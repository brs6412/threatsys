from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

# Base schema
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    organization: Optional[str] = None
    role_id: int = 3

# Creating a user
class UserCreate(UserBase):
    pass

# Updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: str = None
    last_name: str = None
    organization_id: Optional[uuid.UUID] = None
    role_id: Optional[int] = None

# Get user data
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True