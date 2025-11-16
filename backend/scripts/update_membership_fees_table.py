"""
Add GST columns to membership_fees table
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from sqlalchemy import text

def update_table():
    """Add new columns to membership_fees table"""
    db = SessionLocal()
    
    try:
        print("🔄 Updating membership_fees table...")
        
        # Check if table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'membership_fees'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            print("❌ Table membership_fees does not exist. Creating it...")
            # Create the table
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
            print("✅ Table created successfully!")
        else:
            # Check if old column 'amount' exists
            result = db.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'membership_fees' AND column_name = 'amount';
            """))
            has_old_amount = result.scalar()
            
            if has_old_amount:
                print("🔄 Migrating from old schema (amount) to new schema (base_amount + GST)...")
                
                # Add new columns
                db.execute(text("""
                    ALTER TABLE membership_fees 
                    ADD COLUMN IF NOT EXISTS base_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS gst_percentage FLOAT DEFAULT 18.0,
                    ADD COLUMN IF NOT EXISTS gst_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS total_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS include_gst BOOLEAN DEFAULT TRUE;
                """))
                
                # Migrate data: copy amount to base_amount and calculate GST
                db.execute(text("""
                    UPDATE membership_fees 
                    SET 
                        base_amount = amount,
                        gst_amount = CASE WHEN gst THEN (amount * 18.0 / 100) ELSE 0 END,
                        total_amount = CASE WHEN gst THEN (amount + (amount * 18.0 / 100)) ELSE amount END,
                        include_gst = gst,
                        gst_percentage = 18.0
                    WHERE base_amount IS NULL;
                """))
                
                # Drop old columns
                db.execute(text("""
                    ALTER TABLE membership_fees 
                    DROP COLUMN IF EXISTS amount,
                    DROP COLUMN IF EXISTS gst;
                """))
                
                print("✅ Migration completed!")
            else:
                # Just add missing columns if needed
                db.execute(text("""
                    ALTER TABLE membership_fees 
                    ADD COLUMN IF NOT EXISTS base_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS gst_percentage FLOAT DEFAULT 18.0,
                    ADD COLUMN IF NOT EXISTS gst_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS total_amount FLOAT,
                    ADD COLUMN IF NOT EXISTS include_gst BOOLEAN DEFAULT TRUE;
                """))
                print("✅ Columns added!")
        
        db.commit()
        print("\n" + "="*60)
        print("🎉 SUCCESS! Database updated successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_table()
