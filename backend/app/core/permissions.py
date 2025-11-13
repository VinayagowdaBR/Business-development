"""
RBAC permission checking and enforcement
"""
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.database import get_db

def has_permission(user: User, resource: str, action: str) -> bool:
    """
    Check if user has permission to perform action on resource
    
    Args:
        user: User object
        resource: Resource name (e.g., "users", "roles")
        action: Action name (e.g., "read", "write", "delete")
        
    Returns:
        True if user has permission, False otherwise
    """
    if not user.roles:
        return False
    
    # System admins have all permissions
    for role in user.roles:
        if role.is_system_role and role.name == "Admin":
            return True
        
        # Check specific permissions
        for permission in role.permissions:
            if permission.resource == resource and permission.action == action:
                return True
    
    return False

def require_permission(resource: str, action: str):
    """
    Dependency to require specific permission
    
    Args:
        resource: Resource name
        action: Action name
        
    Returns:
        Dependency function
        
    Raises:
        HTTPException: If user doesn't have required permission
    """
    def permission_checker(user: User) -> User:
        if not has_permission(user, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {resource}:{action}"
            )
        return user
    
    return permission_checker

def require_admin(user: User) -> bool:
    """
    Check if user has admin role
    
    Args:
        user: User object
        
    Returns:
        True if user is admin
        
    Raises:
        HTTPException: If user is not admin
    """
    if not user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    for role in user.roles:
        if role.name.lower() in ["admin", "system admin"] or role.is_system_role:
            return True
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required"
    )

def check_same_organization(user: User, target_user: User) -> bool:
    """
    Verify users are in same organization
    
    Args:
        user: Current user
        target_user: Target user to check
        
    Returns:
        True if same organization
        
    Raises:
        HTTPException: If users are in different organizations
    """
    if user.organization_id != target_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access users from other organizations"
        )
    return True

def get_user_permissions(user: User) -> List[str]:
    """
    Get all permissions for a user as list of strings
    
    Args:
        user: User object
        
    Returns:
        List of permission strings in format "resource:action"
    """
    permissions = set()
    
    if not user.roles:
        return []
    
    for role in user.roles:
        if role.is_system_role and role.name == "Admin":
            permissions.add("*:*")
        
        if hasattr(role, 'permissions'):
            for permission in role.permissions:
                permissions.add(f"{permission.resource}:{permission.action}")
    
    return sorted(list(permissions))
