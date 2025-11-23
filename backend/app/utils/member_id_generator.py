from sqlalchemy.orm import Session
from app.models.member import Member
from datetime import datetime

def generate_member_id(db: Session, state_code: str, district_prefix: str) -> str:
    """
    Generate unique member ID in format: MEM-STATE-DISTRICT-YYYY-NNNN
    Example: MEM-MH-PUNE-2025-0001
    """
    current_year = datetime.now().year
    
    # Get count of members in this district for this year
    count = db.query(Member).filter(
        Member.member_id.like(f"MEM-{state_code}-{district_prefix}-{current_year}-%")
    ).count()
    
    # Generate sequential number
    sequence = str(count + 1).zfill(4)
    
    member_id = f"MEM-{state_code}-{district_prefix}-{current_year}-{sequence}"
    
    return member_id
