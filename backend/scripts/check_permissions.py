"""
Check permissions in database
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.permission import Permission
from app.models.role import Role
from sqlalchemy import text

def check_permissions():
    db = SessionLocal()
    try:
        # Check permissions table
        perm_count = db.query(Permission).count()
        print(f"📊 Total permissions in database: {perm_count}")
        
        if perm_count > 0:
            print("\n✅ Permissions found:")
            perms = db.query(Permission).all()
            for p in perms:
                print(f"  • {p.resource}:{p.action}")
        else:
            print("\n❌ No permissions found!")
        
        # Check Super Admin role
        super_admin = db.query(Role).filter(Role.name == "Super Admin").first()
        if super_admin:
            print(f"\n✅ Super Admin role found (ID: {super_admin.id})")
            print(f"   Permissions assigned: {len(super_admin.permissions)}")
            if super_admin.permissions:
                for p in super_admin.permissions:
                    print(f"     • {p.resource}:{p.action}")
        else:
            print("\n❌ Super Admin role not found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_permissions()
