"""
RBAC (Role-Based Access Control) endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import (
    PermissionCreate, PermissionResponse,
    RoleCreate, RoleUpdate, RoleResponse,
    AssignRoleRequest,
    RowLevelPolicyCreate, RowLevelPolicyResponse
)
from app.core.security import get_current_user
from app.core.permissions import has_permission

router = APIRouter()

# ============= PERMISSIONS =============

@router.get("/permissions", response_model=List[PermissionResponse])
def list_all_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available permissions"""
    # ✅ Super admin bypass
    if current_user.is_super_admin:
        permissions = db.query(Permission).all()
        return permissions
    
    # Regular permission check
    if not has_permission(current_user, "rbac", "read"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    permissions = db.query(Permission).all()
    return permissions


@router.post("/permissions", response_model=PermissionResponse)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new permission (admin only)"""
    if not has_permission(current_user, "rbac", "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    existing = db.query(Permission).filter(
        Permission.resource == permission.resource,
        Permission.action == permission.action
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    new_permission = Permission(**permission.dict())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

# ============= ROLES =============

@router.get("/roles", response_model=List[RoleResponse])
def list_organization_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all roles in organization"""
    roles = db.query(Role).filter(
        Role.organization_id == current_user.organization_id
    ).all()
    return roles

@router.post("/roles", response_model=RoleResponse)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new role"""
    if not has_permission(current_user, "rbac", "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    existing = db.query(Role).filter(
        Role.name == role_data.name,
        Role.organization_id == current_user.organization_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Role name already exists")
    
    new_role = Role(
        name=role_data.name,
        description=role_data.description,
        organization_id=current_user.organization_id,
        is_system_role=False
    )
    
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        new_role.permissions = permissions
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update role"""
    if not has_permission(current_user, "rbac", "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    role = db.query(Role).filter(
        Role.id == role_id,
        Role.organization_id == current_user.organization_id
    ).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.is_system_role:
        raise HTTPException(status_code=400, detail="Cannot modify system roles")
    
    if role_update.name:
        role.name = role_update.name
    if role_update.description:
        role.description = role_update.description
    
    if role_update.permission_ids is not None:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_update.permission_ids)
        ).all()
        role.permissions = permissions
    
    db.commit()
    db.refresh(role)
    return role

@router.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete role"""
    if not has_permission(current_user, "rbac", "delete"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    role = db.query(Role).filter(
        Role.id == role_id,
        Role.organization_id == current_user.organization_id
    ).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.is_system_role:
        raise HTTPException(status_code=400, detail="Cannot delete system roles")
    
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}

# ============= ASSIGN ROLES =============

@router.post("/users/assign-roles")
def assign_roles_to_user(
    assignment: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign roles to user"""
    if not has_permission(current_user, "rbac", "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    user = db.query(User).filter(
        User.id == assignment.user_id,
        User.organization_id == current_user.organization_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = db.query(Role).filter(
        Role.id.in_(assignment.role_ids),
        Role.organization_id == current_user.organization_id
    ).all()
    
    if len(roles) != len(assignment.role_ids):
        raise HTTPException(status_code=400, detail="Some roles not found")
    
    user.roles = roles
    db.commit()
    
    return {
        "message": "Roles assigned successfully",
        "user_id": user.id,
        "roles": [role.name for role in roles]
    }

@router.get("/users/{user_id}/permissions")
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all permissions for user"""
    user = db.query(User).filter(
        User.id == user_id,
        User.organization_id == current_user.organization_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    permissions = set()
    for role in user.roles:
        if role.is_system_role:
            permissions.add("*:*")
        for permission in role.permissions:
            permissions.add(f"{permission.resource}:{permission.action}")
    
    return {
        "user_id": user.id,
        "username": user.username,
        "roles": [role.name for role in user.roles],
        "permissions": sorted(list(permissions))
    }

# ============= ROW-LEVEL POLICIES =============

@router.post("/row-policies", response_model=RowLevelPolicyResponse)
def create_row_policy(
    policy: RowLevelPolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create row-level policy"""
    if not has_permission(current_user, "rbac", "write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    role = db.query(Role).filter(
        Role.id == policy.role_id,
        Role.organization_id == current_user.organization_id
    ).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    new_policy = RowLevelPolicy(**policy.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy

@router.get("/row-policies/role/{role_id}", response_model=List[RowLevelPolicyResponse])
def get_role_policies(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get row-level policies for role"""
    policies = db.query(RowLevelPolicy).filter(
        RowLevelPolicy.role_id == role_id
    ).all()
    return policies
