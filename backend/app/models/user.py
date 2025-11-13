"""
User model with authentication and authorization
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Many-to-Many relationship table
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    member_profile = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
