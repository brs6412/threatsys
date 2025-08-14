from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class IOC(Base):
    __tablename__ = "iocs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type_id = Column(Integer, ForeignKey("ioc_types.type_id"))
    value = Column(String(255), nullable=False)
    value_hash = Column(String(64), nullable=False, index=True)
    tlp_level = Column(String(20), default='WHITE')
    received_at = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now())
    active = Column(Boolean, nullable=False)
    metadata_ = Column("metadata", JSONB, default={})
    source_org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    ioc_type = relationship("IOCType", back_populates="iocs")
    source_organization = relationship("Organization", foreign_keys=[source_org_id], back_populates="source_iocs")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_iocs")
    
    source_relationships = relationship(
        "IOCRelationship", 
        foreign_keys="[IOCRelationship.source_id]", 
        back_populates="source_ioc"
    )
    target_relationships = relationship(
        "IOCRelationship", 
        foreign_keys="[IOCRelationship.target_id]", 
        back_populates="target_ioc"
    )