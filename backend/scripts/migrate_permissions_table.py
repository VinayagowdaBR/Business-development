"""
Update permissions table to new schema
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def migrate_permissions():
    db = SessionLocal()
    
    try:
        print("🔄 Migrating permissions table...")
        
        # Drop and recreate permissions table with new schema
        print("📝 Dropping old permissions table...")
        db.execute(text("""
            DROP TABLE IF EXISTS role_permissions CASCADE;
            DROP TABLE IF EXISTS row_level_policies CASCADE;
            DROP TABLE IF EXISTS permissions CASCADE;
        """))
        
        print("🔄 Creating new permissions table...")
        db.execute(text("""
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
            CREATE INDEX idx_permissions_action ON permissions(action);
        """))
        
        print("🔄 Creating role_permissions junction table...")
        db.execute(text("""
            CREATE TABLE role_permissions (
                role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
                permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
                PRIMARY KEY (role_id, permission_id)
            );
        """))
        
        db.commit()
        print("✅ Permissions table migrated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_permissions()

