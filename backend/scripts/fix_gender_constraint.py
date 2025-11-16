"""
Fix gender check constraint in members table
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_gender_constraint():
    db = SessionLocal()
    
    try:
        print("🔄 Fixing gender check constraint...")
        
        # Drop old constraint
        db.execute(text("""
            ALTER TABLE members 
            DROP CONSTRAINT IF EXISTS members_gender_check;
        """))
        
        # Add new constraint that accepts both uppercase and proper case
        db.execute(text("""
            ALTER TABLE members 
            ADD CONSTRAINT members_gender_check 
            CHECK (gender IN ('Male', 'Female', 'MALE', 'FEMALE'));
        """))
        
        db.commit()
        print("✅ Gender constraint fixed! Now accepts: Male, Female, MALE, FEMALE")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_gender_constraint()
