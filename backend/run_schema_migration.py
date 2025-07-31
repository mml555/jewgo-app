#!/usr/bin/env python3
"""
Database Schema Migration Runner
================================

This script runs the optimized restaurants table schema migration.
It includes safety checks and user confirmation before proceeding.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main migration runner function."""
    print("🚀 JewGo Database Schema Migration")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable is required")
        print("📝 Please set your database URL:")
        print("   export DATABASE_URL='postgresql://username:password@host:port/database'")
        return False
    
    print(f"📊 Database: {database_url[:50]}...")
    
    # Safety check - confirm with user
    print("\n⚠️  WARNING: This migration will:")
    print("   - Add new required fields")
    print("   - Remove deprecated fields")
    print("   - Update field constraints")
    print("   - Add performance indexes")
    print("   - Migrate existing data")
    
    confirm = input("\n🤔 Are you sure you want to proceed? (yes/no): ").lower()
    if confirm not in ['yes', 'y']:
        print("❌ Migration cancelled by user")
        return False
    
    # Backup confirmation
    backup_confirm = input("\n💾 Have you backed up your database? (yes/no): ").lower()
    if backup_confirm not in ['yes', 'y']:
        print("⚠️  WARNING: No backup confirmed!")
        print("   It's highly recommended to backup your database before proceeding.")
        backup_override = input("   Continue anyway? (yes/no): ").lower()
        if backup_override not in ['yes', 'y']:
            print("❌ Migration cancelled - backup recommended")
            return False
    
    try:
        # Import and run migration
        print("\n🔄 Running migration...")
        sys.path.append(os.path.join(os.path.dirname(__file__), 'database', 'migrations'))
        
        from optimize_restaurants_schema import run_migration, verify_migration
        
        # Run the migration
        success = run_migration()
        
        if success:
            print("✅ Migration completed successfully")
            
            # Verify the migration
            print("\n🔍 Verifying migration...")
            if verify_migration():
                print("✅ Migration verification passed")
                print("\n🎉 Database schema optimization complete!")
                print("\n📝 Next steps:")
                print("   1. Test your application functionality")
                print("   2. Monitor database performance")
                print("   3. Update any custom scripts if needed")
                return True
            else:
                print("❌ Migration verification failed")
                print("📝 Please check the logs and contact support if needed")
                return False
        else:
            print("❌ Migration failed")
            print("📝 Please check the logs and try again")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing migration script: {e}")
        print("📝 Make sure you're running this from the backend directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 