from pydantic import BaseModel
from typing import Optional

class LegionBase(BaseModel):
    name: str         # full name
    prefix: str       # short code
    area_id: int
    description: Optional[str] = None

class LegionCreate(LegionBase):
    pass

class LegionUpdate(BaseModel):
    name: Optional[str] = None
    prefix: Optional[str] = None
    area_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class LegionResponse(LegionBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
