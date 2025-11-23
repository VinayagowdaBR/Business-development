"""
Fix the roles table sequence
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_roles_sequence():
    db = SessionLocal()
    try:
        print("🔄 Fixing roles sequence...")
        
        # Get the maximum ID from roles table
        result = db.execute(text("SELECT MAX(id) FROM roles;"))
        max_id = result.scalar()
        
        if max_id is None:
            max_id = 0
        
        print(f"  Current max ID: {max_id}")
        
        # Reset the sequence to max_id + 1
        next_id = max_id + 1
        db.execute(text(f"ALTER SEQUENCE roles_id_seq RESTART WITH {next_id};"))
        db.commit()
        
        print(f"✅ Sequence reset to start at {next_id}")
        
        # Verify
        result = db.execute(text("SELECT nextval('roles_id_seq');"))
        next_val = result.scalar()
        print(f"✅ Next role ID will be: {next_val}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_roles_sequence()
