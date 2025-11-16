from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.member_type import MemberType
from app.schemas.member_type import MemberTypeCreate, MemberTypeUpdate, MemberTypeResponse
from app.database import get_db
from typing import List
from app.core.security import get_current_user

router = APIRouter(prefix="/member-types", tags=["Member Types"])

@router.get("/", response_model=List[MemberTypeResponse])
def list_member_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all member types"""
    return db.query(MemberType).offset(skip).limit(limit).all()

@router.get("/{member_type_id}", response_model=MemberTypeResponse)
def get_member_type(
    member_type_id: int,
    db: Session = Depends(get_db)
):
    """Get specific member type"""
    member_type = db.query(MemberType).filter(MemberType.id == member_type_id).first()
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    return member_type

@router.post("/", response_model=MemberTypeResponse)
def create_member_type(
    member_type: MemberTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new member type"""
    # Check if code already exists
    existing = db.query(MemberType).filter(MemberType.code == member_type.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member type code already exists")
    
    new_type = MemberType(**member_type.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

@router.put("/{member_type_id}", response_model=MemberTypeResponse)
def update_member_type(
    member_type_id: int,
    member_type: MemberTypeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update member type"""
    db_type = db.query(MemberType).filter(MemberType.id == member_type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    
    # Check if new code conflicts
    if member_type.code and member_type.code != db_type.code:
        existing = db.query(MemberType).filter(MemberType.code == member_type.code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Member type code already exists")
    
    for key, value in member_type.dict(exclude_unset=True).items():
        setattr(db_type, key, value)
    
    db.commit()
    db.refresh(db_type)
    return db_type

@router.delete("/{member_type_id}")
def delete_member_type(
    member_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete member type"""
    db_type = db.query(MemberType).filter(MemberType.id == member_type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    
    db.delete(db_type)
    db.commit()
    return {"message": "Member type deleted successfully"}
