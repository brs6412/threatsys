from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

# Base schema
class IOCBase(BaseModel):
    type_id: int
    value: str
    value_hash: str
    tlp_level: str = "WHITE"
    active: bool = True
    metadata_: Optional[Dict[str, Any]] = Field(default_factory=dict)

# Creating an IOC
class IOCCreate(IOCBase):
    source_org_id: Optional[UUID] = None
    created_by: Optional[UUID] = None

# Updating an IOC
class IOCUpdate(BaseModel):
    type_id: Optional[int] = None
    value: Optional[str] = None
    value_hash: Optional[str] = None
    tlp_level: Optional[str] = None
    active: Optional[bool] = None
    metadata_: Optional[Dict[str, Any]] = None
    last_seen: Optional[datetime] = None

# Get IOC data
class IOCResponse(IOCBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    received_at: datetime
    last_seen: datetime
    source_org_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

# Schema for IOC with relationships
class IOCWithRelationships(IOCResponse):
    pass