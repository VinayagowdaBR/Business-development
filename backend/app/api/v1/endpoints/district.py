from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.district import District
from app.models.state import State
from app.schemas.district import DistrictResponse

router = APIRouter(prefix="/districts", tags=["Districts"])


@router.post("/", response_model=DistrictResponse, status_code=status.HTTP_201_CREATED)
def create_district(
    name: str = Form(...),
    prefix: str = Form(...),
    state_id: int = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Check state exists
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")

    # Check prefix unique
    if db.query(District).filter(District.prefix == prefix).first():
        raise HTTPException(status_code=400, detail="District prefix already exists")

    db_district = District(name=name, prefix=prefix, state_id=state_id, description=description)
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district


@router.get("/", response_model=List[DistrictResponse])
def get_districts(
    state_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(District).filter(District.is_active == True)
    
    if state_id is not None:
        query = query.filter(District.state_id == state_id)
    
    districts = query.offset(skip).limit(limit).all()
    return districts


@router.get("/{district_id}", response_model=DistrictResponse)
def get_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district


@router.put("/{district_id}", response_model=DistrictResponse)
def update_district(
    district_id: int,
    name: Optional[str] = Form(None),
    prefix: Optional[str] = Form(None),
    state_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    db_district = db.query(District).filter(District.id == district_id).first()
    if not db_district:
        raise HTTPException(status_code=404, detail="District not found")

    if name:
        db_district.name = name

    if prefix:
        existing = db.query(District).filter(District.prefix == prefix, District.id != district_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="District prefix already exists")
        db_district.prefix = prefix

    if state_id:
        state = db.query(State).filter(State.id == state_id).first()
        if not state:
            raise HTTPException(status_code=404, detail="State not found")
        db_district.state_id = state_id

    if description is not None:
        db_district.description = description

    if is_active is not None:
        db_district.is_active = is_active

    db.commit()
    db.refresh(db_district)
    return db_district


@router.delete("/{district_id}")
def delete_district(district_id: int, db: Session = Depends(get_db)):
    db_district = db.query(District).filter(District.id == district_id).first()
    if not db_district:
        raise HTTPException(status_code=404, detail="District not found")

    db.delete(db_district)
    db.commit()
    return {"message": "District deleted successfully"}
