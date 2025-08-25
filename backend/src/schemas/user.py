from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

from src.schemas.organization import OrganizationResponse
from src.schemas.role import RoleBase

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role_id: int = 3
    organization_id: Optional[uuid.UUID] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_id: Optional[uuid.UUID] = None
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    organization: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UserDetailResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleBase
    organization: Optional[OrganizationResponse]
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
