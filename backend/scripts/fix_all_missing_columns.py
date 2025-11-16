"""
Add all missing columns to tables
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_all_tables():
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("🔧 FIXING ALL MISSING COLUMNS")
        print("="*60 + "\n")
        
        # 1. Fix organizations table
        print("1️⃣  Adding columns to organizations table...")
        db.execute(text("""
            ALTER TABLE organizations 
            ADD COLUMN IF NOT EXISTS code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS email VARCHAR(255),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
            ADD COLUMN IF NOT EXISTS address TEXT,
            ADD COLUMN IF NOT EXISTS city VARCHAR(100),
            ADD COLUMN IF NOT EXISTS state VARCHAR(100),
            ADD COLUMN IF NOT EXISTS country VARCHAR(100) DEFAULT 'India',
            ADD COLUMN IF NOT EXISTS postal_code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS parent_org_id INTEGER REFERENCES organizations(id),
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
            
            -- Add unique constraint on code
            CREATE UNIQUE INDEX IF NOT EXISTS idx_organizations_code ON organizations(code);
        """))
        print("   ✅ Organizations table fixed\n")
        
        # 2. Fix roles table
        print("2️⃣  Adding columns to roles table...")
        db.execute(text("""
            ALTER TABLE roles 
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
        """))
        print("   ✅ Roles table fixed\n")
        
        # 3. Update existing organizations with code if NULL
        print("3️⃣  Updating existing organizations...")
        db.execute(text("""
            UPDATE organizations 
            SET code = 'ORG' || id 
            WHERE code IS NULL;
        """))
        print("   ✅ Organizations updated\n")
        
        db.commit()
        
        print("\n" + "="*60)
        print("🎉 ALL TABLES FIXED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_all_tables()
