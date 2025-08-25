from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict
from datetime import datetime
import uuid

from src.schemas.ioc_type import IOCTypeResponse
from src.schemas.organization import OrganizationResponse
from src.schemas.user import UserResponse

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
    created_by: uuid.UUID

class IOCUpdate(BaseModel):
    type_id: Optional[int] = None
    value: Optional[str] = None
    value_hash: Optional[str] = None
    tlp_level: Optional[str] = None
    metadata_: Optional[Dict] = None
    active: Optional[bool] = None
    source_org_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

class IOCResponse(BaseModel):
    id: uuid.UUID
    value: str
    value_hash: str
    tlp_level: str
    active: bool
    source_organization: Optional[str] = None
    creator: Optional[str] = None
    last_seen: datetime
    ioc_type: IOCTypeResponse

    model_config = ConfigDict(from_attributes=True)

class IOCDetailResponse(BaseModel):
    id: uuid.UUID
    value: str
    value_hash: str
    tlp_level: str
    metadata_: Optional[Dict] = None
    active: bool
    source_organization: Optional[str] = None
    creator: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_seen: datetime
    received_at: datetime
    ioc_type: IOCTypeResponse

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