"""
Recreate membership_fees table with new schema
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def recreate_table():
    """Drop and recreate membership_fees table"""
    db = SessionLocal()
    
    try:
        print("🔄 Dropping old table...")
        db.execute(text("DROP TABLE IF EXISTS membership_fees CASCADE;"))
        
        print("🔄 Creating new table...")
        db.execute(text("""
            CREATE TABLE membership_fees (
                id SERIAL PRIMARY KEY,
                package_name VARCHAR NOT NULL,
                base_amount FLOAT NOT NULL,
                gst_percentage FLOAT DEFAULT 18.0,
                gst_amount FLOAT NOT NULL,
                total_amount FLOAT NOT NULL,
                include_gst BOOLEAN DEFAULT TRUE,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                package_image VARCHAR
            );
        """))
        
        db.commit()
        print("\n✅ Table recreated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    recreate_table()
