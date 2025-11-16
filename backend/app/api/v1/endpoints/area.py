from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.area import Area
from app.schemas.area import AreaCreate, AreaUpdate, AreaResponse

router = APIRouter(prefix="/areas", tags=["areas"])


@router.post("/", response_model=AreaResponse, status_code=status.HTTP_201_CREATED)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    # Unique checks
    if db.query(Area).filter(Area.code == area.code).first():
        raise HTTPException(status_code=400, detail="Area code already exists")
    if db.query(Area).filter(Area.name == area.name).first():
        raise HTTPException(status_code=400, detail="Area name already exists")

    db_area = Area(
        name=area.name,
        code=area.code,
        description=area.description,
    )
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


@router.get("/", response_model=List[AreaResponse])
def get_areas(db: Session = Depends(get_db)):
    return db.query(Area).all()


@router.get("/{area_id}", response_model=AreaResponse)
def get_area(area_id: int, db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area


@router.put("/{area_id}", response_model=AreaResponse)
def update_area(area_id: int, area: AreaUpdate, db: Session = Depends(get_db)):
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")

    if area.name is not None:
        if db.query(Area).filter(Area.name == area.name, Area.id != area_id).first():
            raise HTTPException(status_code=400, detail="Area name already exists")
        db_area.name = area.name

    if area.code is not None:
        if db.query(Area).filter(Area.code == area.code, Area.id != area_id).first():
            raise HTTPException(status_code=400, detail="Area code already exists")
        db_area.code = area.code

    if area.description is not None:
        db_area.description = area.description

    if area.is_active is not None:
        db_area.is_active = area.is_active

    db.commit()
    db.refresh(db_area)
    return db_area


@router.delete("/{area_id}")
def delete_area(area_id: int, db: Session = Depends(get_db)):
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")

    from app.models.legion import Legion
    if db.query(Legion).filter(Legion.area_id == area_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete area with legions")

    db.delete(db_area)
    db.commit()
    return {"message": "Area deleted"}
