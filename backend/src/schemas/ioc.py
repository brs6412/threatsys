from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, Dict
from datetime import datetime
import uuid

class IOCBase(BaseModel):
    type_id: int
    value: str
    value_hash: str
    tlp_level: Optional[str] = "WHITE"
    metadata_: Optional[Dict] = {}
    active: Optional[bool] = True
    source_org_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

class IOCCreate(IOCBase):
    created_by: uuid.UUID  # required when creating

class IOCUpdate(BaseModel):
    type_id: Optional[int] = None
    value: Optional[str] = None
    value_hash: Optional[str] = None
    tlp_level: Optional[str] = None
    metadata_: Optional[Dict] = None
    active: Optional[bool] = None
    source_org_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

class IOCResponse(IOCBase):
    id: uuid.UUID
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    last_seen: datetime
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)

class IOCSearchParams(BaseModel):
    value: Optional[str] = None
    value_hash: Optional[str] = None
    value_contains: Optional[str] = None
    type_id: Optional[int] = None
    tlp_level: Optional[str] = None
    active: Optional[bool] = None
    source_org_id: Optional[uuid.UUID] = None
    created_by: Optional[uuid.UUID] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    last_seen_after: Optional[datetime] = None
    last_seen_before: Optional[datetime] = None