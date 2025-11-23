from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Personal Info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mobile = Column(String(20), nullable=False)
    gender = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    # Location
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    
    # Password
    hashed_password = Column(String(255), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Membership
    member_type_id = Column(Integer, ForeignKey('member_types.id'), nullable=False)  
    
    
    # Relationships
    state = relationship("State", backref="members")
    district = relationship("District", backref="members")
    member_type = relationship("MemberType", back_populates="members")
