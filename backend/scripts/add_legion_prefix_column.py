"""
Add 'prefix' column to 'legions' table if it does not exist.
"""
import sys
from pathlib import Path

# Ensure app is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from sqlalchemy import text


def add_prefix_column():
    db = SessionLocal()
    try:
        print("🔄 Checking/adding prefix column on legions table...")

        # 1) Add prefix column if missing
        db.execute(text("""
            ALTER TABLE legions
            ADD COLUMN IF NOT EXISTS prefix VARCHAR(20);
        """))

        # 2) Fill NULL prefixes with generated values
        db.execute(text("""
            UPDATE legions
            SET prefix = 'LEG_' || id
            WHERE prefix IS NULL;
        """))

        # 3) Set NOT NULL constraint
        db.execute(text("""
            ALTER TABLE legions
            ALTER COLUMN prefix SET NOT NULL;
        """))

        # 4) Add UNIQUE index for prefix
        db.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_legions_prefix
            ON legions(prefix);
        """))

        db.commit()
        print("✅ prefix column ensured on legions table.")
    except Exception as e:
        print(f"❌ Error while adding prefix column: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_prefix_column()
