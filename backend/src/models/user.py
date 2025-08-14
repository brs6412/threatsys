from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=3)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    organization = relationship("Organization", back_populates="users")
    role = relationship("Role", back_populates="users")
    created_iocs = relationship("IOC", foreign_keys="[IOC.created_by]", back_populates="creator")