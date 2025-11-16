from pydantic import BaseModel
from typing import Optional

class MemberTypeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: bool = True

class MemberTypeCreate(MemberTypeBase):
    pass

class MemberTypeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class MemberTypeResponse(MemberTypeBase):
    id: int
    
    class Config:
        from_attributes = True
