"""
Create State and District tables
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def create_tables():
    db = SessionLocal()
    try:
        print("🔄 Creating State and District tables...")

        # Create states table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS states (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                description VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Create districts table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS districts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                prefix VARCHAR(20) UNIQUE NOT NULL,
                state_id INTEGER NOT NULL REFERENCES states(id) ON DELETE CASCADE,
                description VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Create indexes
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_states_code ON states(code);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_districts_prefix ON districts(prefix);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_districts_state_id ON districts(state_id);"))

        db.commit()
        print("✅ Tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
