from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.member import Member  # Clean import
from app.models.member_type import MemberType
from app.models.state import State
from app.models.district import District
from app.schemas.member import MemberCreate, MemberResponse
from app.utils.member_id_generator import generate_member_id
from passlib.context import CryptContext

router = APIRouter(prefix="/members", tags=["Members"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    gender: str = Form(...),
    date_of_birth: date = Form(...),
    state_id: int = Form(...),
    district_id: int = Form(...),
    member_type_id: int = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Check if email exists
    if db.query(Member).filter(Member.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate state
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    
    # Validate district
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    
    # Check if district belongs to selected state
    if district.state_id != state_id:
        raise HTTPException(status_code=400, detail="District does not belong to selected state")
    
    # Validate member type
    member_type = db.query(MemberType).filter(MemberType.id == member_type_id).first()
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    
    # Generate unique member_id
    member_id = generate_member_id(db, state.code, district.prefix)
    
    # Hash password
    hashed_password = pwd_context.hash(password)
    
    # Create member
    db_member = Member(
        member_id=member_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        mobile=mobile,
        gender=gender,
        date_of_birth=date_of_birth,
        state_id=state_id,
        district_id=district_id,
        member_type_id=member_type_id,
        hashed_password=hashed_password
    )
    
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    return db_member


@router.get("/", response_model=List[MemberResponse])
def get_members(
    state_id: Optional[int] = None,
    district_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Member)
    
    if state_id:
        query = query.filter(Member.state_id == state_id)
    if district_id:
        query = query.filter(Member.district_id == district_id)
    
    members = query.offset(skip).limit(limit).all()
    return members


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/{member_id}")
def delete_member(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully", "member_id": member_id}
