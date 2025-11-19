"""
Member service - Business logic for managing external clients/members
"""
from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.member_type import MemberType
from app.models.organization import Organization
from app.models.membership_fee import MembershipFee
from datetime import date
from passlib.context import CryptContext
import random

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MemberService:
    """Service class for member operations"""
    
    @staticmethod
    def generate_membership_number() -> str:
        """Generate unique membership number"""
        return f"MEM{random.randint(100000, 999999)}"
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_member(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        mobile: str,
        gender: str,
        date_of_birth: date,
        password: str,
        member_type_id: int,
        membership_fee_id: int,
        managed_by_org_id: int,
        **kwargs
    ) -> Member:
        """Create a new member (external client)"""
        
        # Check if email already exists
        existing = db.query(Member).filter(Member.email == email).first()
        if existing:
            raise ValueError("Email already registered")
        
        # Verify member type exists
        member_type = db.query(MemberType).filter(MemberType.id == member_type_id).first()
        if not member_type:
            raise ValueError("Member type not found")
        
        # Verify organization exists
        org = db.query(Organization).filter(Organization.id == managed_by_org_id).first()
        if not org:
            raise ValueError("Organization not found")
        
        # Verify membership fee exists
        fee = db.query(MembershipFee).filter(MembershipFee.id == membership_fee_id).first()
        if not fee:
            raise ValueError("Membership fee plan not found")
        
        
        # Validate gender
        if gender not in ['Male', 'Female']:
            raise ValueError("Gender must be 'Male' or 'Female'")
        
        # Generate unique membership number
        membership_number = MemberService.generate_membership_number()
        while db.query(Member).filter(Member.membership_number == membership_number).first():
            membership_number = MemberService.generate_membership_number()
        
        # Hash password
        hashed_password = MemberService.hash_password(password)
        
        # Create member
        member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            gender=gender,
            date_of_birth=date_of_birth,
            hashed_password=hashed_password,
            member_type_id=member_type_id,
            membership_fee_id=membership_fee_id,
            managed_by_org_id=managed_by_org_id,
            membership_number=membership_number,
            join_date=date.today(),
            **kwargs
        )
        
        db.add(member)
        db.commit()
        db.refresh(member)
        
        return member
    
    @staticmethod
    def get_member_by_id(db: Session, member_id: int) -> Member:
        """Get member by ID"""
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError("Member not found")
        return member
    
    @staticmethod
    def get_member_by_email(db: Session, email: str) -> Member:
        """Get member by email"""
        return db.query(Member).filter(Member.email == email).first()
    
    @staticmethod
    def authenticate_member(db: Session, email: str, password: str) -> Member:
        """Authenticate member by email and password"""
        member = MemberService.get_member_by_email(db, email)
        if not member:
            return None
        if not MemberService.verify_password(password, member.hashed_password):
            return None
        if not member.is_active:
            raise ValueError("Member account is inactive")
        return member
    
    @staticmethod
    def update_member(db: Session, member_id: int, **kwargs) -> Member:
        """Update member details"""
        member = MemberService.get_member_by_id(db, member_id)
        
        # If password is being updated, hash it
        if 'password' in kwargs:
            kwargs['hashed_password'] = MemberService.hash_password(kwargs.pop('password'))
        
        for key, value in kwargs.items():
            if hasattr(member, key) and key != 'hashed_password':
                setattr(member, key, value)
            elif key == 'hashed_password':
                setattr(member, key, value)
        
        db.commit()
        db.refresh(member)
        
        return member
    
    @staticmethod
    def delete_member(db: Session, member_id: int) -> bool:
        """Delete a member"""
        member = MemberService.get_member_by_id(db, member_id)
        db.delete(member)
        db.commit()
        return True
    
    @staticmethod
    def get_members_by_organization(db: Session, org_id: int, skip: int = 0, limit: int = 100):
        """Get all members managed by a specific organization"""
        return db.query(Member).filter(
            Member.managed_by_org_id == org_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_members_by_type(db: Session, member_type_id: int, skip: int = 0, limit: int = 100):
        """Get all members of a specific type"""
        return db.query(Member).filter(
            Member.member_type_id == member_type_id
        ).offset(skip).limit(limit).all()
    

    
    @staticmethod
    def search_members(db: Session, org_id: int, search_term: str):
        """Search members by name, email, or mobile"""
        return db.query(Member).filter(
            Member.managed_by_org_id == org_id,
            (Member.first_name.ilike(f"%{search_term}%") |
             Member.last_name.ilike(f"%{search_term}%") |
             Member.email.ilike(f"%{search_term}%") |
             Member.mobile.ilike(f"%{search_term}%") |
             Member.membership_number.ilike(f"%{search_term}%"))
        ).all()
    
