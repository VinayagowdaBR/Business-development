"""
Fix legacy 'code' column on legions table so it no longer breaks inserts.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text


def fix_legions_code():
    db = SessionLocal()
    try:
        print("🔄 Fixing legions.code column...")

        # Option A: If you don't need 'code' at all, drop NOT NULL and make it optional:
        db.execute(text("""
            ALTER TABLE legions
            ALTER COLUMN code DROP NOT NULL;
        """))

        # Optional: if you really don't need 'code', you can later drop it entirely:
        # db.execute(text("ALTER TABLE legions DROP COLUMN IF EXISTS code;"))

        db.commit()
        print("✅ legions.code is now nullable (won't block inserts).")
    except Exception as e:
        print(f"❌ Error fixing legions.code: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_legions_code()
