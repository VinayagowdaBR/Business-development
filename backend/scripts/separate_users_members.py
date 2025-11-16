"""
Separate Users and Members into distinct tables
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    
    try:
        print("🔄 Separating Users and Members...")
        
        # Drop old member profile table if exists
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
        
        # Create new members table (external clients)
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS members (
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
        """))
        
        # Add staff fields to users table
        db.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS first_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS last_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
            ADD COLUMN IF NOT EXISTS is_super_admin BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
        """))
        
        db.commit()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
