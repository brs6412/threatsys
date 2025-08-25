from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

class OrganizationBase(BaseModel):
    name: str
    tier: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[str] = None

class OrganizationDetailResponse(OrganizationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str