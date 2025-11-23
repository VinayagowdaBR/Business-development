"""
Organization model - Internal branches/offices
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Organization(Base):
    """Internal organization/branch offices"""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=True)
    
    # Contact Details
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    postal_code = Column(String(20), nullable=True)
    
    # Hierarchy (for branches under national office)
    parent_org_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    staff_users = relationship("User", back_populates="organization", cascade="all, delete-orphan", foreign_keys="[User.organization_id]")
    roles = relationship("Role", back_populates="organization", cascade="all, delete-orphan")
    
    # Self-referential relationship for hierarchy
    parent = relationship("Organization", remote_side=[id], backref="sub_branches")
