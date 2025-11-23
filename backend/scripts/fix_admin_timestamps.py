"""
Fix admin user timestamps
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text
from datetime import datetime

def fix_timestamps():
    db = SessionLocal()
    try:
        print("🔄 Fixing admin user timestamps...")
        
        # Update admin user with current timestamp
        db.execute(text("""
            UPDATE users 
            SET created_at = NOW(), 
                updated_at = NOW() 
            WHERE id = 1;
        """))
        
        db.commit()
        print("✅ Timestamps fixed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_timestamps()
