"""
Initialize default permissions in database
"""
import sys
sys.path.append('..')

from app.database import SessionLocal
from app.models.permission import Permission

def initialize_permissions():
    """Create default permissions"""
    db = SessionLocal()
    
    default_permissions = [
        {"resource": "users", "action": "read", "description": "View users"},
        {"resource": "users", "action": "write", "description": "Create/edit users"},
        {"resource": "users", "action": "delete", "description": "Delete users"},
        {"resource": "rbac", "action": "read", "description": "View roles/permissions"},
        {"resource": "rbac", "action": "write", "description": "Create/edit roles"},
        {"resource": "rbac", "action": "delete", "description": "Delete roles"},
        {"resource": "members", "action": "read", "description": "View members"},
        {"resource": "members", "action": "write", "description": "Create/edit members"},
        {"resource": "members", "action": "delete", "description": "Delete members"},
        {"resource": "database", "action": "read", "description": "View database"},
        {"resource": "database", "action": "write", "description": "Edit database"},
        {"resource": "reports", "action": "read", "description": "View reports"},
        {"resource": "settings", "action": "read", "description": "View settings"},
        {"resource": "settings", "action": "write", "description": "Edit settings"},
    ]
    
    for perm_data in default_permissions:
        existing = db.query(Permission).filter(
            Permission.resource == perm_data["resource"],
            Permission.action == perm_data["action"]
        ).first()
        
        if not existing:
            permission = Permission(**perm_data)
            db.add(permission)
            print(f"✅ Created: {perm_data['resource']}:{perm_data['action']}")
    
    db.commit()
    db.close()
    print("\n🎉 Permissions initialized successfully!")

if __name__ == "__main__":
    initialize_permissions()
