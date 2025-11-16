"""
Create member_types table with initial data
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def create_table():
    """Create member_types table with initial data"""
    db = SessionLocal()
    
    try:
        print("🔄 Creating member_types table...")
        
        # Create table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS member_types (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                code VARCHAR NOT NULL UNIQUE,
                description VARCHAR,
                is_active BOOLEAN DEFAULT TRUE
            );
        """))
        
        print("✅ Table created!")
        
        # Insert default member types
        print("🔄 Inserting default member types...")
        
        db.execute(text("""
            INSERT INTO member_types (name, code, description, is_active)
            VALUES 
                ('Visitors', 'VIS', 'Temporary visitors or guests', true),
                ('Legion Members', 'LEG', 'Members affiliated with a specific legion', true),
                ('National Members', 'NAT', 'Members at the national level', true),
                ('Guests', 'GST', 'Guest members with limited access', true)
            ON CONFLICT (code) DO NOTHING;
        """))
        
        db.commit()
        print("✅ Default member types inserted!")
        print("\n" + "="*60)
        print("🎉 SUCCESS! Member types table created with initial data!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_table()
