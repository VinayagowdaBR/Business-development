"""
Membership Fee model
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
from datetime import datetime
from app.database import Base


class MembershipFee(Base):
    """Membership fee packages"""
    __tablename__ = "membership_fees"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Package details
    package_name = Column(String(255), nullable=False)
    package_image = Column(String(500), nullable=True)  # Image URL/path
    
    # Pricing
    base_amount = Column(Float, nullable=False)  # Amount before GST
    gst_percentage = Column(Float, default=18.0)  # GST % (default 18%)
    gst_amount = Column(Float, nullable=False)  # Calculated GST amount
    total_amount = Column(Float, nullable=False)  # Base + GST
    include_gst = Column(Boolean, default=True)  # Whether to include GST
    
    # Validity period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
