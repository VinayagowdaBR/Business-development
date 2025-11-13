"""
Member profile schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date

class MemberBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None

class MemberCreate(MemberBase):
    """Schema for creating member profile"""
    pass

class MemberUpdate(MemberBase):
    """Schema for updating member profile"""
    pass

class MemberResponse(MemberBase):
    """Full member profile response"""
    id: int
    user_id: int
    employee_id: Optional[str]
    profile_picture_url: Optional[str]
    joined_date: datetime
    last_active: datetime
    is_verified: bool
    username: str
    email: str
    
    class Config:
        from_attributes = True

class MemberListItem(BaseModel):
    """Simplified member info for lists"""
    id: int
    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    username: str
    job_title: Optional[str]
    department: Optional[str]
    is_active: bool
    joined_date: datetime
    
    class Config:
        from_attributes = True
