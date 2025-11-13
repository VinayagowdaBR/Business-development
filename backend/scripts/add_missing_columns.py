"""
Add missing columns to existing database tables
"""
import sys
sys.path.append('..')

from app.database import engine
from sqlalchemy import text

def add_missing_columns():
    """Add updated_at column to tables"""
    
    with engine.connect() as conn:
        try:
            # Add updated_at to users table
            print("Adding updated_at to users table...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            conn.commit()
            print("✅ Added updated_at to users")
            
            # Add updated_at to organizations table
            print("Adding updated_at to organizations table...")
            conn.execute(text("""
                ALTER TABLE organizations 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            conn.commit()
            print("✅ Added updated_at to organizations")
            
            # Add updated_at to roles table
            print("Adding updated_at to roles table...")
            conn.execute(text("""
                ALTER TABLE roles 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            conn.commit()
            print("✅ Added updated_at to roles")
            
            # Add updated_at to members table (if exists)
            print("Adding updated_at to members table...")
            conn.execute(text("""
                ALTER TABLE members 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            conn.commit()
            print("✅ Added updated_at to members")
            
            print("\n🎉 All columns added successfully!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    add_missing_columns()
