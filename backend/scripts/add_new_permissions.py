"""
Add permissions for Membership Fees, Areas, and Legions
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.permission import Permission

# Import all models to register relationships
from app.models import user, role, permission, organization, member

def add_new_permissions():
    """Add permissions for new features"""
    db: Session = SessionLocal()
    
    try:
        # Define new permissions using your resource:action pattern
        new_permissions = [
            # Membership Fees
            {"resource": "membership_fees", "action": "read", "description": "View membership fees"},
            {"resource": "membership_fees", "action": "write", "description": "Create/Update membership fees"},
            {"resource": "membership_fees", "action": "delete", "description": "Delete membership fees"},
            
            # Areas
            {"resource": "areas", "action": "read", "description": "View areas"},
            {"resource": "areas", "action": "write", "description": "Create/Update areas"},
            {"resource": "areas", "action": "delete", "description": "Delete areas"},
            
            # Legions
            {"resource": "legions", "action": "read", "description": "View legions"},
            {"resource": "legions", "action": "write", "description": "Create/Update legions"},
            {"resource": "legions", "action": "delete", "description": "Delete legions"},
        ]
        
        added_count = 0
        for perm_data in new_permissions:
            # Check if permission already exists
            existing = db.query(Permission).filter(
                Permission.resource == perm_data["resource"],
                Permission.action == perm_data["action"]
            ).first()
            
            if not existing:
                permission = Permission(**perm_data)
                db.add(permission)
                added_count += 1
                print(f"✓ Added: {perm_data['resource']}:{perm_data['action']}")
            else:
                print(f"⊗ Exists: {perm_data['resource']}:{perm_data['action']}")
        
        db.commit()
        print(f"\n✅ Successfully added {added_count} new permissions!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding permissions for Membership Fees, Areas, and Legions...\n")
    add_new_permissions()
