"""
Create areas and legions tables with sample data (DROP and recreate)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def create_tables():
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("🔄 CREATING AREAS & LEGIONS TABLES")
        print("="*60 + "\n")
        
        # Drop existing tables
        print("1️⃣  Dropping old tables...")
        db.execute(text("DROP TABLE IF EXISTS legions CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS areas CASCADE;"))
        print("   ✅ Old tables dropped\n")
        
        # Create areas table
        print("2️⃣  Creating areas table...")
        db.execute(text("""
            CREATE TABLE areas (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                description VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_areas_code ON areas(code);
        """))
        print("   ✅ Areas table created\n")
        
        # Create legions table
        print("3️⃣  Creating legions table...")
        db.execute(text("""
            CREATE TABLE legions (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                area_id INTEGER REFERENCES areas(id) NOT NULL,
                description VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_legions_code ON legions(code);
            CREATE INDEX idx_legions_area ON legions(area_id);
        """))
        print("   ✅ Legions table created\n")
        
        # Insert sample areas (A to F)
        print("4️⃣  Inserting sample areas...")
        db.execute(text("""
            INSERT INTO areas (name, code, description) VALUES
            ('Area A', 'AREA_A', 'Region A'),
            ('Area B', 'AREA_B', 'Region B'),
            ('Area C', 'AREA_C', 'Region C'),
            ('Area D', 'AREA_D', 'Region D'),
            ('Area E', 'AREA_E', 'Region E'),
            ('Area F', 'AREA_F', 'Region F');
        """))
        print("   ✅ 6 areas inserted\n")
        
        # Insert sample legions for each area (3 legions per area)
        print("5️⃣  Inserting sample legions...")
        
        areas = ['AREA_A', 'AREA_B', 'AREA_C', 'AREA_D', 'AREA_E', 'AREA_F']
        for area_code in areas:
            for i in range(1, 4):  # 3 legions per area
                db.execute(text(f"""
                    INSERT INTO legions (name, code, area_id, description)
                    SELECT 
                        '{area_code} - Legion {i}',
                        'LEG_{area_code}_{i}',
                        id,
                        'Legion {i} in {area_code}'
                    FROM areas WHERE code = '{area_code}';
                """))
        
        print("   ✅ 18 legions inserted (3 per area)\n")
        
        db.commit()
        
        # Show summary
        print("="*60)
        print("🎉 AREAS & LEGIONS CREATED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        print("📊 Summary:")
        print("  • 6 Areas: Area A, B, C, D, E, F")
        print("  • 18 Legions: 3 legions per area")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
