"""
Create permissions with detailed logging
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def create_permissions():
    db = SessionLocal()
    try:
        print("🔄 Creating permissions...")
        
        # Check if permissions table exists
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'permissions'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            print("❌ Permissions table doesn't exist!")
            print("   Creating it now...")
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id SERIAL PRIMARY KEY,
                    resource VARCHAR(100) NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    description VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(resource, action)
                );
            """))
            db.commit()
            print("✅ Permissions table created!")
        
        # Insert permissions
        permissions = [
            ("users", "read", "View users"),
            ("users", "write", "Create/Edit users"),
            ("users", "delete", "Delete users"),
            ("organizations", "read", "View organizations"),
            ("organizations", "write", "Create/Edit organizations"),
            ("organizations", "delete", "Delete organizations"),
            ("rbac", "read", "View roles and permissions"),
            ("rbac", "write", "Create/Edit roles"),
            ("rbac", "delete", "Delete roles"),
            ("members", "read", "View members"),
            ("members", "write", "Create/Edit members"),
            ("members", "delete", "Delete members"),
            ("states", "read", "View states"),
            ("states", "write", "Create/Edit states"),
            ("states", "delete", "Delete states"),
            ("districts", "read", "View districts"),
            ("districts", "write", "Create/Edit districts"),
            ("districts", "delete", "Delete districts"),
            ("dashboard", "read", "View dashboard"),
        ]
        
        for resource, action, desc in permissions:
            try:
                db.execute(text("""
                    INSERT INTO permissions (resource, action, description, created_at)
                    VALUES (:resource, :action, :desc, NOW())
                    ON CONFLICT (resource, action) DO NOTHING;
                """), {"resource": resource, "action": action, "desc": desc})
                print(f"  ✅ {resource}:{action}")
            except Exception as e:
                print(f"  ❌ Failed {resource}:{action} - {e}")
        
        db.commit()
        
        # Verify
        result = db.execute(text("SELECT COUNT(*) FROM permissions;"))
        count = result.scalar()
        print(f"\n✅ Total permissions created: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_permissions()
