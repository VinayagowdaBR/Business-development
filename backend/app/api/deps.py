"""
Common dependencies for API endpoints
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

# Re-export common dependencies
def get_db_session() -> Generator:
    """Get database session"""
    return get_db()

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    return current_user
