"""
Organization management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.role import Role
from app.schemas.user import UserCreateByAdmin
from app.schemas.organization import OrganizationUpdate
from app.core.security import get_current_user, hash_password
from app.core.permissions import require_admin, check_same_organization

router = APIRouter()

@router.get("/me")
def get_my_organization(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's organization information"""
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    user_count = db.query(User).filter(
        User.organization_id == org.id
    ).count()
    
    # Get user roles
    user_roles = [role.name for role in current_user.roles] if current_user.roles else []
    primary_role = user_roles[0] if user_roles else "No Role"
    
    return {
        "organization_id": org.id,
        "organization_name": org.name,
        "created_at": org.created_at,
        "user_role": primary_role,
        "user_roles": user_roles,
        "user_count": user_count
    }

@router.get("/users")
def list_org_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users in organization (Admin only)"""
    require_admin(current_user)
    
    users = db.query(User).filter(
        User.organization_id == current_user.organization_id
    ).all()
    
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "roles": [r.name for r in u.roles] if u.roles else [],
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

@router.post("/users", status_code=201)
def create_user_in_organization(
    user_data: UserCreateByAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new user (Admin only)"""
    require_admin(current_user)
    
    # Check duplicates
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Find role
    role = db.query(Role).filter(
        Role.name == user_data.role,
        Role.organization_id == current_user.organization_id
    ).first()
    
    if not role:
        raise HTTPException(status_code=400, detail=f"Role '{user_data.role}' not found")
    
    # Create user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        organization_id=current_user.organization_id,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Assign role
    new_user.roles = [role]
    db.commit()
    
    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "roles": [role.name]
    }

@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user (Admin only)"""
    require_admin(current_user)
    
    target_user = db.query(User).filter(User.id == user_id).first()
    
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    check_same_organization(current_user, target_user)
    
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    db.delete(target_user)
    db.commit()
    
    return {"message": "User deleted successfully"}

@router.put("/me")
def update_organization(
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update organization name (Admin only)"""
    require_admin(current_user)
    
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if name taken
    if db.query(Organization).filter(
        Organization.name == org_update.name,
        Organization.id != org.id
    ).first():
        raise HTTPException(status_code=400, detail="Organization name already taken")
    
    org.name = org_update.name
    db.commit()
    
    return {"message": "Organization updated", "organization_name": org.name}
