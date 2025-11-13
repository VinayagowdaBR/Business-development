"""
Business logic for member management
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

from app.models.member import Member
from app.models.user import User
from app.schemas.member import MemberCreate, MemberUpdate

class MemberService:
    """Service class for member operations"""
    
    @staticmethod
    def create_member_profile(
        db: Session,
        user_id: int,
        member_data: MemberCreate
    ) -> Member:
        """Create member profile for user"""
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if profile already exists
        existing = db.query(Member).filter(Member.user_id == user_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member profile already exists"
            )
        
        # Generate employee ID
        employee_id = f"EMP{user_id:05d}"
        
        # Create member
        member = Member(
            user_id=user_id,
            employee_id=employee_id,
            **member_data.dict(exclude_none=True)
        )
        
        db.add(member)
        db.commit()
        db.refresh(member)
        
        return member
    
    @staticmethod
    def get_member_by_user_id(db: Session, user_id: int) -> Optional[Member]:
        """Get member profile by user ID"""
        return db.query(Member).filter(Member.user_id == user_id).first()
    
    @staticmethod
    def get_members_by_organization(
        db: Session,
        organization_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Member]:
        """Get all members in organization"""
        return db.query(Member).join(User).filter(
            User.organization_id == organization_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_member_profile(
        db: Session,
        member_id: int,
        member_data: MemberUpdate
    ) -> Member:
        """Update member profile"""
        member = db.query(Member).filter(Member.id == member_id).first()
        
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member profile not found"
            )
        
        # Update fields
        update_data = member_data.dict(exclude_none=True)
        for field, value in update_data.items():
            setattr(member, field, value)
        
        member.last_active = datetime.utcnow()
        
        db.commit()
        db.refresh(member)
        
        return member
    
    @staticmethod
    def delete_member_profile(db: Session, member_id: int) -> bool:
        """Delete member profile"""
        member = db.query(Member).filter(Member.id == member_id).first()
        
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member profile not found"
            )
        
        db.delete(member)
        db.commit()
        
        return True
    
    @staticmethod
    def search_members(
        db: Session,
        organization_id: int,
        search_term: str
    ) -> List[Member]:
        """Search members by name, email, or department"""
        return db.query(Member).join(User).filter(
            User.organization_id == organization_id,
            (Member.first_name.ilike(f"%{search_term}%") |
             Member.last_name.ilike(f"%{search_term}%") |
             Member.department.ilike(f"%{search_term}%") |
             User.email.ilike(f"%{search_term}%"))
        ).all()
