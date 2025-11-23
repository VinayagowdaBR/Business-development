"""
Create default permissions for the system
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.permission import Permission
from sqlalchemy import text

def create_permissions():
    db = SessionLocal()
    try:
        print("🔄 Creating default permissions...")

        # Define all permissions
        permissions = [
            # User Management
            {"resource": "users", "action": "read", "description": "View users"},
            {"resource": "users", "action": "write", "description": "Create/Edit users"},
            {"resource": "users", "action": "delete", "description": "Delete users"},
            
            # Organization Management
            {"resource": "organizations", "action": "read", "description": "View organizations"},
            {"resource": "organizations", "action": "write", "description": "Create/Edit organizations"},
            {"resource": "organizations", "action": "delete", "description": "Delete organizations"},
            
            # RBAC Management
            {"resource": "rbac", "action": "read", "description": "View roles and permissions"},
            {"resource": "rbac", "action": "write", "description": "Create/Edit roles and permissions"},
            {"resource": "rbac", "action": "delete", "description": "Delete roles and permissions"},
            
            # Member Management
            {"resource": "members", "action": "read", "description": "View members"},
            {"resource": "members", "action": "write", "description": "Create/Edit members"},
            {"resource": "members", "action": "delete", "description": "Delete members"},
            
            # State Management
            {"resource": "states", "action": "read", "description": "View states"},
            {"resource": "states", "action": "write", "description": "Create/Edit states"},
            {"resource": "states", "action": "delete", "description": "Delete states"},
            
            # District Management
            {"resource": "districts", "action": "read", "description": "View districts"},
            {"resource": "districts", "action": "write", "description": "Create/Edit districts"},
            {"resource": "districts", "action": "delete", "description": "Delete districts"},
            
            # Dashboard
            {"resource": "dashboard", "action": "read", "description": "View dashboard"},
            
            # Reports
            {"resource": "reports", "action": "read", "description": "View reports"},
            {"resource": "reports", "action": "export", "description": "Export reports"},
        ]

        # Insert permissions
        for perm in permissions:
            existing = db.query(Permission).filter(
                Permission.resource == perm["resource"],
                Permission.action == perm["action"]
            ).first()
            
            if not existing:
                new_perm = Permission(**perm)
                db.add(new_perm)
                print(f"  ✅ Created: {perm['resource']}:{perm['action']}")
            else:
                print(f"  ⏭️  Exists: {perm['resource']}:{perm['action']}")

        db.commit()
        
        # Count total permissions
        total = db.query(Permission).count()
        print(f"\n✅ Total permissions in database: {total}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_permissions()
