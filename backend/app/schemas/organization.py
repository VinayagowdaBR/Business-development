"""
Organization schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class OrganizationResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrganizationUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
