from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class IOCType(Base):
    __tablename__ = "ioc_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    
    iocs = relationship("IOC", back_populates="ioc_type")