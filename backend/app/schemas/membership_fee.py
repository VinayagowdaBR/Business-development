from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MembershipFeeBase(BaseModel):
    package_name: str
    base_amount: float = Field(..., gt=0, description="Base amount before GST")
    gst_percentage: float = Field(default=18.0, ge=0, le=100)
    include_gst: bool = True
    start_date: date
    end_date: date
    package_image: Optional[str] = None

class MembershipFeeCreate(MembershipFeeBase):
    pass

class MembershipFeeUpdate(MembershipFeeBase):
    package_name: Optional[str] = None
    base_amount: Optional[float] = None
    gst_percentage: Optional[float] = None
    include_gst: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    package_image: Optional[str] = None

class MembershipFeeResponse(MembershipFeeBase):
    id: int
    gst_amount: float
    total_amount: float
    package_image: Optional[str] = None
    
    class Config:
        from_attributes = True
