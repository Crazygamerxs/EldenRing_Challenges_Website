#!/usr/bin/env python3
"""
Complete Migration Runner Script
Orchestrates the entire migration process from SQLite to Supabase PostgreSQL.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, title):
    """Print a formatted step."""
    print(f"\n📋 Step {step_num}: {title}")
    print("-" * 40)

def run_script(script_path, description):
    """Run a Python script and return success status."""
    print(f"🔄 {description}...")
    
    try:
        # Change to mybackend directory
        os.chdir('mybackend')
        
        # Run the script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True)
        
        # Change back to root directory
        os.chdir('..')
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed!")
            if result.stderr:
                print("Error:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False

def check_prerequisites():
    """Check that all prerequisites are met."""
    print_step(0, "Checking Prerequisites")
    
    issues = []
    
    # Check if mybackend directory exists
    if not Path('mybackend').exists():
        issues.append("mybackend directory not found")
    
    # Check if SQLite database exists
    if not Path('mybackend/db.sqlite3').exists():
        issues.append("Development database (db.sqlite3) not found")
    
    # Check if .env.prod exists
    if not Path('mybackend/.env.prod').exists():
        issues.append("Production environment file (.env.prod) not found")
    
    # Check if scripts exist
    required_scripts = [
        'mybackend/scripts/check_dev_data.py',
        'mybackend/scripts/export_dev_data.py',
        'mybackend/scripts/setup_production.py',
        'mybackend/scripts/verify_migration.py'
    ]
    
    for script in required_scripts:
        if not Path(script).exists():
            issues.append(f"Required script not found: {script}")
    
    if issues:
        print("❌ Prerequisites not met:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All prerequisites met!")
        return True

def get_user_confirmation(message):
    """Get user confirmation before proceeding."""
    while True:
        response = input(f"\n{message} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main migration orchestration function."""
    print_header("Elden Ring Challenges - Database Migration")
    print("This script will migrate your data from SQLite to Supabase PostgreSQL")
    print("\nMigration Process:")
    print("1. Check development data")
    print("2. Export development data to JSON fixtures")
    print("3. Setup production database and import data")
    print("4. Verify migration success")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Cannot proceed with migration. Please fix the issues above.")
        return False
    
    # Step 1: Check development data
    print_step(1, "Check Development Data")
    if not get_user_confirmation("Check what data exists in your development database?"):
        print("Skipping development data check...")
    else:
        if not run_script('scripts/check_dev_data.py', 'Checking development data'):
            if not get_user_confirmation("Development data check had issues. Continue anyway?"):
                return False
    
    # Step 2: Export development data
    print_step(2, "Export Development Data")
    if not get_user_confirmation("Export data from SQLite development database?"):
        print("❌ Cannot proceed without exporting data.")
        return False
    
    if not run_script('scripts/export_dev_data.py', 'Exporting development data'):
        print("❌ Data export failed. Cannot proceed.")
        return False
    
    # Step 3: Setup production database
    print_step(3, "Setup Production Database")
    print("⚠️  This will connect to your Supabase database and import data.")
    print("   Make sure your .env.prod file has the correct credentials.")
    
    if not get_user_confirmation("Proceed with production database setup?"):
        print("❌ Production setup cancelled by user.")
        return False
    
    if not run_script('scripts/setup_production.py', 'Setting up production database'):
        print("❌ Production setup failed.")
        if not get_user_confirmation("Continue with verification anyway?"):
            return False
    
    # Step 4: Verify migration
    print_step(4, "Verify Migration")
    if not get_user_confirmation("Run migration verification tests?"):
        print("Skipping verification...")
    else:
        if not run_script('scripts/verify_migration.py', 'Verifying migration'):
            print("⚠️  Verification had issues. Please review the output above.")
        else:
            print("🎉 Migration verification passed!")
    
    # Final summary
    print_header("Migration Complete!")
    print("✅ Database migration process finished!")
    print("\nNext steps:")
    print("1. Test admin login with the provided credentials")
    print("2. Verify that challenges are loading correctly")
    print("3. Test core website functionality")
    print("4. Change the admin password")
    print("5. Configure your production environment")
    print("\nFiles created during migration:")
    print("- mybackend/data_exports/ (exported data)")
    print("- migration_verification_report_*.json (verification results)")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Migration completed successfully!")
        else:
            print("\n❌ Migration failed or was cancelled.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during migration: {str(e)}")
