"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.role import Role
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user and create/join organization
    """
    # Check if email exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Find or create organization
    org = db.query(Organization).filter(
        Organization.name == user.organization_name
    ).first()
    
    if not org:
        org = Organization(name=user.organization_name)
        db.add(org)
        db.commit()
        db.refresh(org)
    
    # Create user
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        organization_id=org.id,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create or get Admin role
    admin_role = db.query(Role).filter(
        Role.name == "Admin",
        Role.organization_id == org.id
    ).first()
    
    if not admin_role:
        admin_role = Role(
            name="Admin",
            description="Organization administrator",
            organization_id=org.id,
            is_system_role=True
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # Assign role
    new_user.roles = [admin_role]
    db.commit()
    
    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "organization": org.name,
        "role": "Admin"
    }

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"user_id": db_user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
