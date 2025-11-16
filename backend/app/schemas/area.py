from pydantic import BaseModel
from typing import Optional

class AreaBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class AreaResponse(AreaBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
