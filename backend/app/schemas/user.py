"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    organization_name: str = Field(..., min_length=2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    organization_id: int
    is_active: bool
    created_at: datetime
    roles: List[str] = []

    class Config:
        from_attributes = True

class UserCreateByAdmin(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., description="Role name to assign")
