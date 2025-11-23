"""
Assign all permissions to Super Admin role
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from sqlalchemy import text

def assign_super_admin_permissions():
    db = SessionLocal()
    try:
        print("🔄 Assigning all permissions to Super Admin role...")

        # Get Super Admin role
        super_admin_role = db.query(Role).filter(Role.name == "Super Admin").first()
        
        if not super_admin_role:
            print("❌ Super Admin role not found!")
            return

        # Get all permissions
        all_permissions = db.query(Permission).all()
        
        if not all_permissions:
            print("❌ No permissions found! Run create_permissions.py first.")
            return

        # Assign all permissions to Super Admin
        super_admin_role.permissions = all_permissions
        
        db.commit()
        
        print(f"✅ Assigned {len(all_permissions)} permissions to Super Admin role!")
        print("\nPermissions assigned:")
        for perm in all_permissions:
            print(f"  • {perm.resource}:{perm.action}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_super_admin_permissions()
