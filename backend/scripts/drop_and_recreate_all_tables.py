"""
Drop ALL tables and recreate them fresh
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine, Base
from sqlalchemy import text

# Import ALL models so they register with Base
from app.models.organization import Organization
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.state import State
from app.models.district import District
from app.models.member import Member
from app.models.membership_fee import MembershipFee
from app.models.member_type import MemberType

def recreate_database():
    db = SessionLocal()
    try:
        print("🔄 Dropping ALL tables...")
        
        # Drop all tables in correct order
        db.execute(text("DROP TABLE IF EXISTS user_roles CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS role_permissions CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS districts CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS states CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS membership_fees CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS member_types CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS permissions CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS roles CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS organizations CASCADE;"))
        
        db.commit()
        print("✅ All tables dropped")
        
        print("🔄 Creating fresh tables...")
        # Create all tables fresh from models
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    response = input("⚠️  This will DELETE ALL DATA! Type 'YES' to continue: ")
    if response == "YES":
        recreate_database()
    else:
        print("Cancelled.")
