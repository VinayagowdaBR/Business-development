"""
Permission model - Simplified for cleaner RBAC
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Permission(Base):
    """System permissions for role-based access control"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Permission details
    name = Column(String(100), nullable=False)
    code = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "member.create"
    description = Column(Text, nullable=True)
    
    # Categorization
    category = Column(String(50), nullable=True)  # e.g., "Member Management", "User Management"
    resource = Column(String(50), nullable=False, index=True)  # e.g., "member", "user", "organization"
    action = Column(String(50), nullable=False, index=True)  # e.g., "create", "read", "update", "delete"
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
