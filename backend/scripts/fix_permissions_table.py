"""
Fix permissions table with proper constraint
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_permissions_table():
    db = SessionLocal()
    try:
        print("🔄 Fixing permissions table...")
        
        # Drop and recreate with proper constraint
        db.execute(text("DROP TABLE IF EXISTS role_permissions CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS permissions CASCADE;"))
        
        print("  ✅ Dropped old tables")
        
        # Create permissions table with unique constraint
        db.execute(text("""
            CREATE TABLE permissions (
                id SERIAL PRIMARY KEY,
                resource VARCHAR(100) NOT NULL,
                action VARCHAR(50) NOT NULL,
                description VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT unique_resource_action UNIQUE (resource, action)
            );
        """))
        
        print("  ✅ Created permissions table")
        
        # Create role_permissions junction table
        db.execute(text("""
            CREATE TABLE role_permissions (
                role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                permission_id INTEGER NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
                PRIMARY KEY (role_id, permission_id)
            );
        """))
        
        print("  ✅ Created role_permissions table")
        
        db.commit()
        
        # Now insert permissions
        print("\n🔄 Inserting permissions...")
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
            ("reports", "read", "View reports"),
            ("reports", "export", "Export reports"),
        ]
        
        for resource, action, desc in permissions:
            db.execute(text("""
                INSERT INTO permissions (resource, action, description, created_at)
                VALUES (:resource, :action, :desc, NOW());
            """), {"resource": resource, "action": action, "desc": desc})
            print(f"  ✅ {resource}:{action}")
        
        db.commit()
        
        # Verify
        result = db.execute(text("SELECT COUNT(*) FROM permissions;"))
        count = result.scalar()
        print(f"\n✅ Total permissions created: {count}")
        
        # Assign ALL to Super Admin
        print("\n🔄 Assigning to Super Admin...")
        result = db.execute(text("SELECT id FROM permissions;"))
        perm_ids = [row[0] for row in result]
        
        for perm_id in perm_ids:
            db.execute(text("""
                INSERT INTO role_permissions (role_id, permission_id)
                VALUES (1, :perm_id);
            """), {"perm_id": perm_id})
        
        db.commit()
        print(f"✅ Assigned {len(perm_ids)} permissions to Super Admin!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_permissions_table()
