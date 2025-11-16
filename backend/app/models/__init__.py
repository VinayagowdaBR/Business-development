"""
Models package - All models imported here
"""
from app.database import Base

# Core models
from app.models.organization import Organization
from app.models.user import User, user_roles
from app.models.role import Role, role_permissions
from app.models.permission import Permission

# Member-related models
from app.models.member_type import MemberType
from app.models.membership_fee import MembershipFee
from app.models.area import Area
from app.models.legion import Legion
from app.models.member import Member

__all__ = [
    "Base",
    # Core
    "Organization",
    "User",
    "Role",
    "Permission",
    # Members
    "Member",
    "MemberType",
    "MembershipFee",
    "Area",
    "Legion",
    # Many-to-Many tables
    "user_roles",
    "role_permissions"
]
