from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from src.database import Base

class IOCRelationship(Base):
    __tablename__ = "ioc_relationships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("iocs.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("iocs.id"), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    confidence_score = Column(Integer, default=50)
    first_observed = Column(DateTime(timezone=True), server_default=func.now())
    last_observed = Column(DateTime(timezone=True), server_default=func.now())
    metadata_ = Column("metadata", JSONB, default={})
    
    source_ioc = relationship("IOC", foreign_keys=[source_id], back_populates="source_relationships")
    target_ioc = relationship("IOC", foreign_keys=[target_id], back_populates="target_relationships")