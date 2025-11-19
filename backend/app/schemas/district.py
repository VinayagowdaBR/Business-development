from pydantic import BaseModel
from typing import Optional

class DistrictBase(BaseModel):
    name: str
    prefix: str
    state_id: int
    description: Optional[str] = None

class DistrictCreate(DistrictBase):
    pass

class DistrictUpdate(BaseModel):
    name: Optional[str] = None
    prefix: Optional[str] = None
    state_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DistrictResponse(BaseModel):
    id: int
    name: str
    prefix: str
    state_id: int
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
