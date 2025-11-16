"""
Run all migrations in correct order
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import SessionLocal

def run_all_migrations():
    """Run all database migrations"""
    
    print("\n" + "="*60)
    print("🚀 STARTING DATABASE MIGRATION")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # 1. Update permissions table
        print("1️⃣  Migrating permissions table...")
        db.execute(text("""
            DROP TABLE IF EXISTS role_permissions CASCADE;
            DROP TABLE IF EXISTS row_level_policies CASCADE;
            DROP TABLE IF EXISTS permissions CASCADE;
            
            CREATE TABLE permissions (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                category VARCHAR(50),
                resource VARCHAR(50) NOT NULL,
                action VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_permissions_code ON permissions(code);
            CREATE INDEX idx_permissions_resource ON permissions(resource);
            
            CREATE TABLE role_permissions (
                role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
                permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
                PRIMARY KEY (role_id, permission_id)
            );
        """))
        print("   ✅ Permissions table migrated\n")
        
        # 2. Update users table
        print("2️⃣  Updating users table...")
        db.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS first_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS last_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
            ADD COLUMN IF NOT EXISTS is_super_admin BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
        """))
        print("   ✅ Users table updated\n")
        
        # 3. Update members table
        print("3️⃣  Updating members table...")
        db.execute(text("DROP TABLE IF EXISTS member_profile CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
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
        """))
        print("   ✅ Members table updated\n")
        
        # 4. Update membership fees
        print("4️⃣  Updating membership_fees table...")
        db.execute(text("""
            ALTER TABLE membership_fees 
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE,
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """))
        print("   ✅ Membership fees table updated\n")
        
        db.commit()
        
        print("\n" + "="*60)
        print("🎉 ALL MIGRATIONS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}\n")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_all_migrations()
