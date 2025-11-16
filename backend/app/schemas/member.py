"""
Member schemas
"""
from pydantic import BaseModel, EmailStr, validator
from datetime import date, datetime
from typing import Optional

class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    gender: str  # "Male" or "Female"
    date_of_birth: date
    password: str
    confirm_password: str
    member_type_id: int
    membership_fee_id: int
    area_id: int
    legion_id: int
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v

class MemberResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    mobile: str
    gender: str
    date_of_birth: date
    membership_number: str
    member_type_id: int
    membership_fee_id: int
    area_id: int
    legion_id: int
    is_active: bool
    join_date: date
    
    # Additional info
    area_name: Optional[str] = None
    legion_name: Optional[str] = None
    member_type_name: Optional[str] = None
    
    class Config:
        from_attributes = True
