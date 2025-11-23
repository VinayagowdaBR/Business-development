"""
Create members table with state and district
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def create_members_table():
    db = SessionLocal()
    try:
        print("🔄 Creating members table...")

        # Drop existing table if needed (be careful in production!)
        db.execute(text("DROP TABLE IF EXISTS members CASCADE;"))
        
        # Create members table
        db.execute(text("""
            CREATE TABLE members (
                id SERIAL PRIMARY KEY,
                member_id VARCHAR(50) UNIQUE NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                date_of_birth DATE NOT NULL,
                state_id INTEGER NOT NULL REFERENCES states(id) ON DELETE RESTRICT,
                district_id INTEGER NOT NULL REFERENCES districts(id) ON DELETE RESTRICT,
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        print("✅ Members table created")

        # Create indexes
        print("🔄 Creating indexes...")
        db.execute(text("CREATE INDEX idx_members_member_id ON members(member_id);"))
        db.execute(text("CREATE INDEX idx_members_email ON members(email);"))
        db.execute(text("CREATE INDEX idx_members_state ON members(state_id);"))
        db.execute(text("CREATE INDEX idx_members_district ON members(district_id);"))
        
        print("✅ Indexes created")

        db.commit()
        print("✅ Members table setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_members_table()
