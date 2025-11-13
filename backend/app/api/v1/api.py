"""
API v1 router aggregator
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, organizations, members, rbac

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(members.router, prefix="/members", tags=["Members"])
api_router.include_router(rbac.router, prefix="/rbac", tags=["RBAC"])
