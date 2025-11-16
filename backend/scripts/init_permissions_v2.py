"""
Initialize system permissions - Updated version
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.permission import Permission

def init_permissions():
    db = SessionLocal()
    
    try:
        print("🔄 Initializing permissions...")
        
        # Check if already initialized
        if db.query(Permission).first():
            print("⚠️  Permissions already exist!")
            return
        
        permissions = [
            # Members
            {"name": "View Members", "code": "member.view", "resource": "member", "action": "read", "category": "Members"},
            {"name": "Create Member", "code": "member.create", "resource": "member", "action": "create", "category": "Members"},
            {"name": "Edit Member", "code": "member.edit", "resource": "member", "action": "update", "category": "Members"},
            {"name": "Delete Member", "code": "member.delete", "resource": "member", "action": "delete", "category": "Members"},
            
            # Users
            {"name": "View Users", "code": "user.view", "resource": "user", "action": "read", "category": "Users"},
            {"name": "Create User", "code": "user.create", "resource": "user", "action": "create", "category": "Users"},
            {"name": "Edit User", "code": "user.edit", "resource": "user", "action": "update", "category": "Users"},
            {"name": "Delete User", "code": "user.delete", "resource": "user", "action": "delete", "category": "Users"},
            
            # Organizations
            {"name": "View Organizations", "code": "org.view", "resource": "organization", "action": "read", "category": "Organizations"},
            {"name": "Edit Organization", "code": "org.edit", "resource": "organization", "action": "update", "category": "Organizations"},
            
            # Roles
            {"name": "View Roles", "code": "role.view", "resource": "role", "action": "read", "category": "Roles"},
            {"name": "Manage Roles", "code": "role.manage", "resource": "role", "action": "manage", "category": "Roles"},
            
            # Membership Fees
            {"name": "View Fees", "code": "fee.view", "resource": "fee", "action": "read", "category": "Membership Fees"},
            {"name": "Manage Fees", "code": "fee.manage", "resource": "fee", "action": "manage", "category": "Membership Fees"},
            
            # Member Types
            {"name": "View Member Types", "code": "member_type.view", "resource": "member_type", "action": "read", "category": "Member Types"},
            {"name": "Manage Member Types", "code": "member_type.manage", "resource": "member_type", "action": "manage", "category": "Member Types"},
            
            # Reports
            {"name": "View Reports", "code": "report.view", "resource": "report", "action": "read", "category": "Reports"},
            {"name": "Export Data", "code": "report.export", "resource": "report", "action": "export", "category": "Reports"},
        ]
        
        for perm_data in permissions:
            perm = Permission(**perm_data)
            db.add(perm)
        
        db.commit()
        print(f"✅ Created {len(permissions)} permissions!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_permissions()
