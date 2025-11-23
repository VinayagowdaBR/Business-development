"""
Models package - All models imported here
"""
from app.database import Base

# Core models
from app.models.organization import Organization
from app.models.user import User, user_roles
from app.models.role import Role, role_permissions
from app.models.permission import Permission

# Location models
from app.models.state import State
from app.models.district import District

# Member models (NEW - without relationships to old structure)
from app.models.member import Member
from app.models.member_type import MemberType
from app.models.membership_fee import MembershipFee

__all__ = [
    "Base",
    # Core
    "Organization",
    "User",
    "Role",
    "Permission",
    # Location
    "State",
    "District",
    # Members
    "Member",
    "MemberType",
    "MembershipFee",
    # Many-to-Many tables
    "user_roles",
    "role_permissions"
]
