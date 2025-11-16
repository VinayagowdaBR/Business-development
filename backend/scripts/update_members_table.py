"""
Update members table to new schema
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def update_members():
    db = SessionLocal()
    
    try:
        print("🔄 Updating members table...")
        
        # Drop old member profile table
        db.execute(text("DROP TABLE IF EXISTS member_profile CASCADE;"))
        
        # Drop old members table if exists
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
        
        print("🔄 Creating new members table...")
        db.execute(text("""
            CREATE TABLE members (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                date_of_birth DATE,
                address_line1 VARCHAR(255),
                address_line2 VARCHAR(255),
                city VARCHAR(100),
                state VARCHAR(100),
                country VARCHAR(100) DEFAULT 'India',
                postal_code VARCHAR(20),
                member_type_id INTEGER REFERENCES member_types(id),
                membership_number VARCHAR(50) UNIQUE NOT NULL,
                join_date DATE NOT NULL,
                expiry_date DATE,
                is_active BOOLEAN DEFAULT TRUE,
                managed_by_org_id INTEGER REFERENCES organizations(id) NOT NULL,
                job_title VARCHAR(100),
                company_name VARCHAR(200),
                bio TEXT,
                notes TEXT,
                profile_picture_url VARCHAR(500),
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_members_email ON members(email);
            CREATE INDEX idx_members_membership_number ON members(membership_number);
            CREATE INDEX idx_members_managed_by_org ON members(managed_by_org_id);
        """))
        
        db.commit()
        print("✅ Members table updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_members()
