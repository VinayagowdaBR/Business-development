from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date

class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    gender: str
    date_of_birth: date
    state_id: int
    district_id: int
    member_type_id: int
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('mobile')
    def validate_mobile(cls, v):
        if not v.isdigit() or len(v) < 10:
            raise ValueError('Invalid mobile number')
        return v

class MemberResponse(BaseModel):
    id: int
    member_id: str
    first_name: str
    last_name: str
    email: str
    mobile: str
    gender: str
    date_of_birth: date
    state_id: int
    district_id: int
    member_type_id: int
    is_active: bool

    class Config:
        from_attributes = True

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    is_active: Optional[bool] = None
