"""
Update members table with new fields
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def update_members_table():
    db = SessionLocal()
    
    try:
        print("🔄 Updating members table...")
        
        # Drop and recreate
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
        
        db.execute(text("""
            CREATE TABLE members (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
                date_of_birth DATE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                member_type_id INTEGER REFERENCES member_types(id) NOT NULL,
                membership_number VARCHAR(50) UNIQUE NOT NULL,
                membership_fee_id INTEGER REFERENCES membership_fees(id) NOT NULL,
                area_id INTEGER REFERENCES areas(id) NOT NULL,
                legion_id INTEGER REFERENCES legions(id) NOT NULL,
                managed_by_org_id INTEGER REFERENCES organizations(id) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                join_date DATE DEFAULT CURRENT_DATE,
                expiry_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_members_email ON members(email);
            CREATE INDEX idx_members_membership_number ON members(membership_number);
            CREATE INDEX idx_members_area ON members(area_id);
            CREATE INDEX idx_members_legion ON members(legion_id);
        """))
        
        db.commit()
        print("✅ Members table updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_members_table()
