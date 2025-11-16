"""
Member model - External clients/members with login capability
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"

class Member(Base):
    """External clients/members who can login"""
    __tablename__ = "members"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mobile = Column(String(20), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    
    # Membership Details
    member_type_id = Column(Integer, ForeignKey("member_types.id"), nullable=False)
    membership_number = Column(String(50), unique=True, nullable=False, index=True)
    membership_fee_id = Column(Integer, ForeignKey("membership_fees.id"), nullable=False)
    
    # Location
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=False)
    legion_id = Column(Integer, ForeignKey("legions.id"), nullable=False)
    
    # Which organization manages this member
    managed_by_org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Dates
    join_date = Column(Date, default=datetime.utcnow)
    expiry_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - Use string references for foreign_keys
    managing_organization = relationship(
        "Organization", 
        foreign_keys="[Member.managed_by_org_id]",  # ✅ Fixed: Use string reference
        overlaps="managed_members"
    )
    member_type = relationship("MemberType")
    membership_fee = relationship("MembershipFee")
    area = relationship("Area")
    legion = relationship("Legion")
