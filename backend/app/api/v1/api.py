"""
API v1 router aggregator
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, organizations, rbac, membership_fees, member_types
from app.api.v1.endpoints import state, district, member

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(rbac.router, prefix="/rbac", tags=["RBAC"])
api_router.include_router(state.router, tags=["States"])
api_router.include_router(district.router, tags=["Districts"])
api_router.include_router(member.router, tags=["Members"])
api_router.include_router(membership_fees.router, prefix="/membership-fees", tags=["Membership Fees"])
api_router.include_router(member_types.router)