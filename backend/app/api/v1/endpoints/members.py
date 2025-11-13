"""
Member profile endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberListItem
from app.services.member_service import MemberService
from app.core.security import get_current_user
from app.core.permissions import require_admin

router = APIRouter()

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member_profile(
    member_data: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create member profile for current user"""
    member = MemberService.create_member_profile(
        db=db,
        user_id=current_user.id,
        member_data=member_data
    )
    
    return {
        **member.__dict__,
        "username": current_user.username,
        "email": current_user.email
    }

@router.get("/me", response_model=MemberResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's member profile"""
    member = MemberService.get_member_by_user_id(db, current_user.id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member profile not found. Create one first."
        )
    
    return {
        **member.__dict__,
        "username": current_user.username,
        "email": current_user.email
    }

@router.put("/me", response_model=MemberResponse)
def update_my_profile(
    member_data: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's member profile"""
    member = MemberService.get_member_by_user_id(db, current_user.id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member profile not found"
        )
    
    updated_member = MemberService.update_member_profile(
        db=db,
        member_id=member.id,
        member_data=member_data
    )
    
    return {
        **updated_member.__dict__,
        "username": current_user.username,
        "email": current_user.email
    }

@router.get("/", response_model=List[MemberListItem])
def list_organization_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all members in organization (Admin only)"""
    require_admin(current_user)
    
    if search:
        members = MemberService.search_members(
            db=db,
            organization_id=current_user.organization_id,
            search_term=search
        )
    else:
        members = MemberService.get_members_by_organization(
            db=db,
            organization_id=current_user.organization_id,
            skip=skip,
            limit=limit
        )
    
    result = []
    for member in members:
        user = member.user
        result.append({
            "id": member.id,
            "user_id": member.user_id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": user.email,
            "username": user.username,
            "job_title": member.job_title,
            "department": member.department,
            "is_active": user.is_active,
            "joined_date": member.joined_date
        })
    
    return result

@router.get("/{member_id}", response_model=MemberResponse)
def get_member_by_id(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get member profile by ID (Admin only)"""
    require_admin(current_user)
    
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if member.user.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Cannot access members from other organizations")
    
    return {
        **member.__dict__,
        "username": member.user.username,
        "email": member.user.email
    }

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member_profile(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete member profile (Admin only)"""
    require_admin(current_user)
    
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if member.user.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Cannot delete members from other organizations")
    
    MemberService.delete_member_profile(db, member_id)
    
    return None
