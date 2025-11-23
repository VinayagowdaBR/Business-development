"""
Recreate permissions table to match the Permission model
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text

def fix_permissions_complete():
    db = SessionLocal()
    try:
        print("🔄 Recreating permissions table to match model...")
        
        # Drop existing tables
        db.execute(text("DROP TABLE IF EXISTS role_permissions CASCADE;"))
        db.execute(text("DROP TABLE IF EXISTS permissions CASCADE;"))
        print("  ✅ Dropped old tables")
        
        # Create permissions table with ALL fields
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT unique_resource_action UNIQUE (resource, action)
            );
        """))
        print("  ✅ Created permissions table with all fields")
        
        # Create indexes
        db.execute(text("CREATE INDEX idx_permissions_code ON permissions(code);"))
        db.execute(text("CREATE INDEX idx_permissions_resource ON permissions(resource);"))
        db.execute(text("CREATE INDEX idx_permissions_action ON permissions(action);"))
        print("  ✅ Created indexes")
        
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
        
        # Insert permissions with all fields
        print("\n🔄 Inserting permissions...")
        permissions = [
            # Users
            ("View Users", "users.read", "View user list and details", "User Management", "users", "read"),
            ("Create Users", "users.write", "Create and edit users", "User Management", "users", "write"),
            ("Delete Users", "users.delete", "Delete users", "User Management", "users", "delete"),
            
            # Organizations
            ("View Organizations", "organizations.read", "View organization details", "Organization Management", "organizations", "read"),
            ("Manage Organizations", "organizations.write", "Create and edit organizations", "Organization Management", "organizations", "write"),
            ("Delete Organizations", "organizations.delete", "Delete organizations", "Organization Management", "organizations", "delete"),
            
            # RBAC
            ("View Roles", "rbac.read", "View roles and permissions", "Access Control", "rbac", "read"),
            ("Manage Roles", "rbac.write", "Create and edit roles", "Access Control", "rbac", "write"),
            ("Delete Roles", "rbac.delete", "Delete roles", "Access Control", "rbac", "delete"),
            
            # Members
            ("View Members", "members.read", "View member list and details", "Member Management", "members", "read"),
            ("Manage Members", "members.write", "Create and edit members", "Member Management", "members", "write"),
            ("Delete Members", "members.delete", "Delete members", "Member Management", "members", "delete"),
            
            # States
            ("View States", "states.read", "View states", "Location Management", "states", "read"),
            ("Manage States", "states.write", "Create and edit states", "Location Management", "states", "write"),
            ("Delete States", "states.delete", "Delete states", "Location Management", "states", "delete"),
            
            # Districts
            ("View Districts", "districts.read", "View districts", "Location Management", "districts", "read"),
            ("Manage Districts", "districts.write", "Create and edit districts", "Location Management", "districts", "write"),
            ("Delete Districts", "districts.delete", "Delete districts", "Location Management", "districts", "delete"),
            
            # Dashboard
            ("View Dashboard", "dashboard.read", "Access dashboard", "General", "dashboard", "read"),
            
            # Reports
            ("View Reports", "reports.read", "View reports", "Reporting", "reports", "read"),
            ("Export Reports", "reports.export", "Export reports to files", "Reporting", "reports", "export"),
        ]
        
        for name, code, desc, category, resource, action in permissions:
            db.execute(text("""
                INSERT INTO permissions (name, code, description, category, resource, action, is_active, created_at, updated_at)
                VALUES (:name, :code, :desc, :category, :resource, :action, TRUE, NOW(), NOW());
            """), {
                "name": name,
                "code": code,
                "desc": desc,
                "category": category,
                "resource": resource,
                "action": action
            })
            print(f"  ✅ {code}")
        
        db.commit()
        
        # Verify count
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
        
        print("\n" + "="*60)
        print("✅ PERMISSIONS SETUP COMPLETE!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_permissions_complete()
