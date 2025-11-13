"""
Permission and Row-Level Policy models
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")

class RowLevelPolicy(Base):
    __tablename__ = "row_level_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete='CASCADE'))
    resource = Column(String, nullable=False)
    field = Column(String, nullable=False)
    operator = Column(String, nullable=False)  # equals, in, contains, not_equals
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    role = relationship("Role", back_populates="row_policies")
