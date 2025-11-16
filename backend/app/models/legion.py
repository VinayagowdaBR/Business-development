from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Legion(Base):
    __tablename__ = "legions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)                 # full name
    prefix = Column(String(20), unique=True, nullable=False)   # short code

    area_id = Column(Integer, ForeignKey("areas.id"), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    area = relationship("Area", backref="legions")
