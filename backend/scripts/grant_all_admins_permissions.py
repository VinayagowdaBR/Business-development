"""
Grant all permissions to Admin roles
"""
import sys
from pathlib import Path

# Add the backend directory to path - PROPER WAY
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission


def grant_all_admins_permissions():
    """Grant all permissions to all Admin roles"""
    db = SessionLocal()
    
    try:
        all_permissions = db.query(Permission).all()
        
        if not all_permissions:
            print("⚠️  No permissions found! Run init_permissions.py first")
            return
        
        print(f"✅ Found {len(all_permissions)} permissions\n")
        
        admin_roles = db.query(Role).filter(Role.name == "Admin").all()
        
        if not admin_roles:
            print("❌ No Admin roles found!")
            return
        
        print(f"✅ Found {len(admin_roles)} Admin role(s)\n")
        
        for admin_role in admin_roles:
            admin_role.permissions = all_permissions
            print(f"✅ Granted permissions to Admin role (Org ID: {admin_role.organization_id})")
        
        db.commit()
        
        print("\n" + "="*80)
        print("🎉 SUCCESS! All Admin roles now have full permissions!")
        print("="*80)
        print("\n🚀 Logout and login again in the frontend.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    grant_all_admins_permissions()
