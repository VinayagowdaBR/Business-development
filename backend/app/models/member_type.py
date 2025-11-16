"""
Member Type model - Categories of members
"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class MemberType(Base):
    """Types/categories of members"""
    __tablename__ = "member_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # Visitors, Legion Members, etc.
    code = Column(String(20), unique=True, nullable=False)  # VIS, LEG, NAT, GST
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    members = relationship("Member", back_populates="member_type")
