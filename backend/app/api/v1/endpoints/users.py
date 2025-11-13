"""
User management endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "organization_id": current_user.organization_id,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "roles": [role.name for role in current_user.roles] if current_user.roles else []
    }

@router.get("/all")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users (DEV ONLY)"""
    users = db.query(User).all()
    return {
        "count": len(users),
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "roles": [role.name for role in u.roles] if u.roles else []
            } for u in users
        ]
    }
