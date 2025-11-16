"""
Add missing is_active column to roles table
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_roles_table():
    db = SessionLocal()
    
    try:
        print("🔄 Adding is_active column to roles table...")
        
        db.execute(text("""
            ALTER TABLE roles 
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
        """))
        
        db.commit()
        print("✅ Roles table fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_roles_table()
