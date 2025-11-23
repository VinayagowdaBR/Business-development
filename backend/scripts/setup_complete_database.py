"""
Complete database setup with test data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_database():
    db = SessionLocal()
    try:
        print("🔄 Setting up complete database...")

        # 1. Create Organization
        print("\n1️⃣ Creating organization...")
        db.execute(text("""
            INSERT INTO organizations (id, name, code, email, phone, is_active)
            VALUES (1, 'Head Office', 'HQ', 'admin@company.com', '1234567890', true)
            ON CONFLICT (id) DO NOTHING;
        """))
        db.commit()
        print("✅ Organization created")

        # 2. Create Roles
        print("\n2️⃣ Creating roles...")
        db.execute(text("""
            INSERT INTO roles (id, name, organization_id, is_active)
            VALUES 
                (1, 'Super Admin', 1, true),
                (2, 'Admin', 1, true),
                (3, 'Manager', 1, true)
            ON CONFLICT (id) DO NOTHING;
        """))
        db.commit()
        print("✅ Roles created")

        # 3. Create Super Admin User
        print("\n3️⃣ Creating super admin user...")
        hashed_password = pwd_context.hash("admin123")
        db.execute(text("""
            INSERT INTO users (
                id, username, email, hashed_password, 
                organization_id, first_name, last_name, 
                is_active, is_super_admin
            )
            VALUES (
                1, 'admin', 'admin@example.com', :password,
                1, 'Super', 'Admin',
                true, true
            )
            ON CONFLICT (id) DO NOTHING;
        """), {"password": hashed_password})
        db.commit()
        print("✅ Super admin created")

        # 4. Assign role to user
        print("\n4️⃣ Assigning role to user...")
        db.execute(text("""
            INSERT INTO user_roles (user_id, role_id)
            VALUES (1, 1)
            ON CONFLICT DO NOTHING;
        """))
        db.commit()
        print("✅ Role assigned")

        # 5. Create States
        print("\n5️⃣ Creating states...")
        db.execute(text("""
            INSERT INTO states (id, name, code, is_active)
            VALUES 
                (1, 'Maharashtra', 'MH', true),
                (2, 'Karnataka', 'KA', true),
                (3, 'Delhi', 'DL', true)
            ON CONFLICT (id) DO NOTHING;
        """))
        db.commit()
        print("✅ States created")

        # 6. Create Districts
        print("\n6️⃣ Creating districts...")
        db.execute(text("""
            INSERT INTO districts (id, name, prefix, state_id, is_active)
            VALUES 
                (1, 'Pune', 'MH_PUNE', 1, true),
                (2, 'Mumbai', 'MH_MUM', 1, true),
                (3, 'Bangalore', 'KA_BLR', 2, true),
                (4, 'New Delhi', 'DL_ND', 3, true)
            ON CONFLICT (id) DO NOTHING;
        """))
        db.commit()
        print("✅ Districts created")

        print("\n" + "="*50)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*50)
        print("\n📝 Login Credentials:")
        print("   Email/Username: admin@example.com  OR  admin")
        print("   Password: admin123")
        print("\n🌐 Access:")
        print("   Swagger UI: http://127.0.0.1:8000/docs")
        print("   Frontend: http://localhost:5173")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
