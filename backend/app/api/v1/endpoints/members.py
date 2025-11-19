"""
Members API endpoints - For external clients/members
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.member_service import MemberService
from app.schemas.member import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_member(
    member_data: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new member with all required fields:
    - Personal: first_name, last_name, email, mobile, gender, date_of_birth
    - Auth: password, confirm_password
    - Membership: member_type_id, membership_fee_id

    """
    try:
        member = MemberService.create_member(
            db=db,
            first_name=member_data.first_name,
            last_name=member_data.last_name,
            email=member_data.email,
            mobile=member_data.mobile,
            gender=member_data.gender,
            date_of_birth=member_data.date_of_birth,
            password=member_data.password,
            member_type_id=member_data.member_type_id,
            membership_fee_id=member_data.membership_fee_id,
            managed_by_org_id=current_user.organization_id
        )
        
        return {
            "id": member.id,
            "membership_number": member.membership_number,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "message": "Member created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
def list_members(
    skip: int = 0,
    limit: int = 100,
    member_type_id: int = None,
    area_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all members managed by current user's organization"""
    
    if member_type_id:
        members = MemberService.get_members_by_type(db, member_type_id, skip, limit)
    elif area_id:
        members = MemberService.get_members_by_area(db, area_id, skip, limit)
    else:
        members = MemberService.get_members_by_organization(
            db, 
            current_user.organization_id, 
            skip, 
            limit
        )
    
    return [
        {
            "id": m.id,
            "membership_number": m.membership_number,
            "first_name": m.first_name,
            "last_name": m.last_name,
            "email": m.email,
            "mobile": m.mobile,
            "gender": m.gender,
            "member_type_id": m.member_type_id,
            "is_active": m.is_active,
            "join_date": str(m.join_date)
        }
        for m in members
    ]


@router.get("/{member_id}", response_model=dict)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get member details"""
    try:
        member = MemberService.get_member_by_id(db, member_id)
        
        # Check access
        if member.managed_by_org_id != current_user.organization_id and not current_user.is_super_admin:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {
            "id": member.id,
            "membership_number": member.membership_number,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "mobile": member.mobile,
            "gender": member.gender,
            "date_of_birth": str(member.date_of_birth),
            "member_type_id": member.member_type_id,
            "membership_fee_id": member.membership_fee_id,
            "is_active": member.is_active,
            "is_verified": member.is_verified,
            "join_date": str(member.join_date),
            "expiry_date": str(member.expiry_date) if member.expiry_date else None
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{member_id}", response_model=dict)
def update_member(
    member_id: int,
    first_name: str = None,
    last_name: str = None,
    mobile: str = None,
    gender: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update member details"""
    try:
        member = MemberService.get_member_by_id(db, member_id)
        
        # Check access
        if member.managed_by_org_id != current_user.organization_id and not current_user.is_super_admin:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Prepare update data
        update_data = {}
        if first_name: update_data['first_name'] = first_name
        if last_name: update_data['last_name'] = last_name
        if mobile: update_data['mobile'] = mobile
        if gender: update_data['gender'] = gender
        if is_active is not None: update_data['is_active'] = is_active
        
        updated_member = MemberService.update_member(db, member_id, **update_data)
        
        return {
            "id": updated_member.id,
            "message": "Member updated successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a member"""
    try:
        member = MemberService.get_member_by_id(db, member_id)
        
        # Check access
        if member.managed_by_org_id != current_user.organization_id and not current_user.is_super_admin:
            raise HTTPException(status_code=403, detail="Access denied")
        
        MemberService.delete_member(db, member_id)
        
        return {"message": "Member deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

