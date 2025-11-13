"""
Reset database (drop and recreate all tables)
"""
import sys
sys.path.append('..')

from app.database import Base, engine

def reset_database():
    """Drop and recreate all tables"""
    print("⚠️  WARNING: This will delete ALL data!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("❌ Aborted")
        return
    
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database reset complete!")
    print("📝 Run: python scripts/init_permissions.py")

if __name__ == "__main__":
    reset_database()
