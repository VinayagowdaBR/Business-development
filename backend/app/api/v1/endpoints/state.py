from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.state import State
from app.schemas.state import StateResponse

router = APIRouter(prefix="/states", tags=["States"])


@router.post("/", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
def create_state(
    name: str = Form(...),
    code: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Check duplicates
    if db.query(State).filter(State.code == code).first():
        raise HTTPException(status_code=400, detail="State code already exists")
    
    if db.query(State).filter(State.name == name).first():
        raise HTTPException(status_code=400, detail="State name already exists")

    db_state = State(name=name, code=code, description=description)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


@router.get("/", response_model=List[StateResponse])
def get_states(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    states = db.query(State).filter(State.is_active == True).offset(skip).limit(limit).all()
    return states


@router.get("/{state_id}", response_model=StateResponse)
def get_state(state_id: int, db: Session = Depends(get_db)):
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return state


@router.put("/{state_id}", response_model=StateResponse)
def update_state(
    state_id: int,
    name: Optional[str] = Form(None),
    code: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    db_state = db.query(State).filter(State.id == state_id).first()
    if not db_state:
        raise HTTPException(status_code=404, detail="State not found")

    if name:
        existing = db.query(State).filter(State.name == name, State.id != state_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="State name already exists")
        db_state.name = name

    if code:
        existing = db.query(State).filter(State.code == code, State.id != state_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="State code already exists")
        db_state.code = code

    if description is not None:
        db_state.description = description

    if is_active is not None:
        db_state.is_active = is_active

    db.commit()
    db.refresh(db_state)
    return db_state


@router.delete("/{state_id}")
def delete_state(state_id: int, db: Session = Depends(get_db)):
    db_state = db.query(State).filter(State.id == state_id).first()
    if not db_state:
        raise HTTPException(status_code=404, detail="State not found")

    from app.models.district import District
    district_count = db.query(District).filter(District.state_id == state_id).count()
    if district_count > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete state with {district_count} districts")

    db.delete(db_state)
    db.commit()
    return {"message": "State deleted successfully"}
