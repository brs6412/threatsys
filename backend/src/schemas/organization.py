from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

# Base schema
class OrganizationBase(BaseModel):
    name: str
    tier: str

# Creating an organization
class OrganizationCreate(OrganizationBase):
    pass

# Updating an organization
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[str] = None

# Get organization data
class OrganizationResponse(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime