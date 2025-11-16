"""
Initialize default permissions with correct format
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.permission import Permission

def init_permissions():
    db = SessionLocal()
    
    try:
        print("🔄 Initializing default permissions...")
        
        # Check if permissions already exist
        existing = db.query(Permission).first()
        if existing:
            print("⚠️  Permissions already exist. Skipping initialization.")
            return
        
        permissions = [
            # Members Management
            {
                "name": "View Members",
                "code": "member.view",
                "resource": "member",
                "action": "read",
                "category": "Member Management",
                "description": "View member list and details"
            },
            {
                "name": "Create Member",
                "code": "member.create",
                "resource": "member",
                "action": "create",
                "category": "Member Management",
                "description": "Add new members"
            },
            {
                "name": "Edit Member",
                "code": "member.edit",
                "resource": "member",
                "action": "update",
                "category": "Member Management",
                "description": "Edit member information"
            },
            {
                "name": "Delete Member",
                "code": "member.delete",
                "resource": "member",
                "action": "delete",
                "category": "Member Management",
                "description": "Delete members"
            },
            
            # User Management
            {
                "name": "View Users",
                "code": "user.view",
                "resource": "user",
                "action": "read",
                "category": "User Management",
                "description": "View staff/admin users"
            },
            {
                "name": "Create User",
                "code": "user.create",
                "resource": "user",
                "action": "create",
                "category": "User Management",
                "description": "Add new staff/admin users"
            },
            {
                "name": "Edit User",
                "code": "user.edit",
                "resource": "user",
                "action": "update",
                "category": "User Management",
                "description": "Edit user information"
            },
            {
                "name": "Delete User",
                "code": "user.delete",
                "resource": "user",
                "action": "delete",
                "category": "User Management",
                "description": "Delete users"
            },
            
            # Organization Management
            {
                "name": "View Organizations",
                "code": "org.view",
                "resource": "organization",
                "action": "read",
                "category": "Organizations",
                "description": "View organization details"
            },
            {
                "name": "Edit Organization",
                "code": "org.edit",
                "resource": "organization",
                "action": "update",
                "category": "Organizations",
                "description": "Edit organization information"
            },
            
            # Role Management
            {
                "name": "View Roles",
                "code": "role.view",
                "resource": "role",
                "action": "read",
                "category": "Role Management",
                "description": "View roles and permissions"
            },
            {
                "name": "Manage Roles",
                "code": "role.manage",
                "resource": "role",
                "action": "manage",
                "category": "Role Management",
                "description": "Create, edit, and delete roles"
            },
            
            # Membership Fees
            {
                "name": "View Fees",
                "code": "fee.view",
                "resource": "fee",
                "action": "read",
                "category": "Membership Fees",
                "description": "View membership fee packages"
            },
            {
                "name": "Manage Fees",
                "code": "fee.manage",
                "resource": "fee",
                "action": "manage",
                "category": "Membership Fees",
                "description": "Create, edit, and delete fee packages"
            },
            
            # Member Types
            {
                "name": "View Member Types",
                "code": "member_type.view",
                "resource": "member_type",
                "action": "read",
                "category": "Member Types",
                "description": "View member type categories"
            },
            {
                "name": "Manage Member Types",
                "code": "member_type.manage",
                "resource": "member_type",
                "action": "manage",
                "category": "Member Types",
                "description": "Create, edit, and delete member types"
            },
            
            # Reports
            {
                "name": "View Reports",
                "code": "report.view",
                "resource": "report",
                "action": "read",
                "category": "Reports",
                "description": "View system reports"
            },
            {
                "name": "Export Data",
                "code": "report.export",
                "resource": "report",
                "action": "export",
                "category": "Reports",
                "description": "Export data to Excel/CSV"
            },
        ]
        
        for perm_data in permissions:
            perm = Permission(**perm_data)
            db.add(perm)
        
        db.commit()
        print(f"✅ Created {len(permissions)} default permissions!")
        
        # Print summary
        print("\n📋 Permissions by Category:")
        categories = {}
        for p in permissions:
            cat = p["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(p["name"])
        
        for cat, perms in categories.items():
            print(f"\n  {cat}:")
            for perm_name in perms:
                print(f"    • {perm_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_permissions()
