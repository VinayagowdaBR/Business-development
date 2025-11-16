from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.legion import Legion
from app.models.area import Area
from app.schemas.legion import LegionCreate, LegionResponse, LegionUpdate

router = APIRouter(prefix="/legions", tags=["legions"])


@router.post("/", response_model=LegionResponse, status_code=status.HTTP_201_CREATED)
def create_legion(legion: LegionCreate, db: Session = Depends(get_db)):
    # Check area exists
    if not db.query(Area).filter(Area.id == legion.area_id).first():
        raise HTTPException(status_code=404, detail="Area not found")

    # Check prefix unique
    if db.query(Legion).filter(Legion.prefix == legion.prefix).first():
        raise HTTPException(status_code=400, detail="Legion prefix already exists")

    db_legion = Legion(
        name=legion.name,
        prefix=legion.prefix,
        area_id=legion.area_id,
        description=legion.description,
    )
    db.add(db_legion)
    db.commit()
    db.refresh(db_legion)
    return db_legion
