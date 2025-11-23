"""
RBAC schemas for roles, permissions, and policies
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Permission Schemas
class PermissionBase(BaseModel):
    resource: str
    action: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
    created_at: Optional[datetime] = None  # ✅ Make optional

    class Config:
        from_attributes = True


# Role Schemas
class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    permission_ids: List[int] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None


class RoleResponse(RoleBase):
    id: int
    organization_id: int
    is_system_role: Optional[bool] = False  # ✅ Make optional with default
    created_at: Optional[datetime] = None    # ✅ Make optional
    updated_at: Optional[datetime] = None    # ✅ Add this field as optional
    is_active: Optional[bool] = True         # ✅ Add this field
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True


class AssignRoleRequest(BaseModel):
    user_id: int
    role_ids: List[int]


# Row-Level Policy Schemas
class RowLevelPolicyBase(BaseModel):
    resource: str
    field: str
    operator: str = Field(..., pattern="^(equals|in|contains|not_equals)$")
    value: str


class RowLevelPolicyCreate(RowLevelPolicyBase):
    role_id: int


class RowLevelPolicyResponse(RowLevelPolicyBase):
    id: int
    role_id: int
    created_at: Optional[datetime] = None  # ✅ Make optional

    class Config:
        from_attributes = True
