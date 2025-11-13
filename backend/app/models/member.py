"""
Member profile model - Extended user information
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal Information
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    date_of_birth = Column(Date)
    
    # Professional Information
    job_title = Column(String(100))
    department = Column(String(100))
    employee_id = Column(String(50), unique=True, index=True)
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    
    # Additional Info
    bio = Column(Text)
    profile_picture_url = Column(String(500))
    
    # Metadata
    joined_date = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="member_profile")
