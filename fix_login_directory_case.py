#!/usr/bin/env python3
"""
Fix Login directory case sensitivity issue for Render deployment.

This script addresses the case sensitivity problem where:
- Local Windows environment has 'Login' directory
- Render Linux environment shows 'LogIn' directory
- This causes module resolution failures during build
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_login_directory_case():
    """Fix the Login directory case sensitivity issue."""
    
    print("🔧 Fixing Login directory case sensitivity issue...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('myfrontend/src/components'):
        print("❌ Error: Not in the correct project directory")
        print("   Please run this script from the project root directory")
        return False
    
    login_dir = Path('myfrontend/src/components/Login')
    temp_dir = Path('myfrontend/src/components/LoginTemp')
    
    # Check if Login directory exists
    if not login_dir.exists():
        print("❌ Error: Login directory not found")
        return False
    
    print(f"📂 Found Login directory: {login_dir}")
    
    # List files in Login directory
    login_files = list(login_dir.glob('*'))
    print(f"📄 Files in Login directory: {[f.name for f in login_files]}")
    
    try:
        # Step 1: Rename to temporary directory
        print("🔄 Step 1: Renaming Login to LoginTemp...")
        shutil.move(str(login_dir), str(temp_dir))
        
        # Step 2: Git add the removal
        print("🔄 Step 2: Git add the directory removal...")
        success, stdout, stderr = run_command("git add -A")
        if not success:
            print(f"⚠️  Warning: Git add failed: {stderr}")
        
        # Step 3: Commit the removal
        print("🔄 Step 3: Committing directory removal...")
        success, stdout, stderr = run_command('git commit -m "Remove Login directory for case fix"')
        if not success:
            print(f"⚠️  Warning: Git commit failed: {stderr}")
        
        # Step 4: Rename back to Login (with correct case)
        print("🔄 Step 4: Renaming LoginTemp back to Login...")
        shutil.move(str(temp_dir), str(login_dir))
        
        # Step 5: Git add the new directory
        print("🔄 Step 5: Git add the new directory...")
        success, stdout, stderr = run_command("git add -A")
        if not success:
            print(f"⚠️  Warning: Git add failed: {stderr}")
        
        # Step 6: Commit the addition
        print("🔄 Step 6: Committing new directory...")
        success, stdout, stderr = run_command('git commit -m "Add Login directory with correct case"')
        if not success:
            print(f"⚠️  Warning: Git commit failed: {stderr}")
        
        print("✅ Login directory case fix completed!")
        print("📋 Next steps:")
        print("   1. Push changes to repository: git push")
        print("   2. Trigger new Render deployment")
        print("   3. Monitor build logs for success")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during fix: {e}")
        
        # Try to restore if temp directory exists
        if temp_dir.exists() and not login_dir.exists():
            print("🔄 Attempting to restore from temp directory...")
            try:
                shutil.move(str(temp_dir), str(login_dir))
                print("✅ Restored Login directory")
            except Exception as restore_error:
                print(f"❌ Failed to restore: {restore_error}")
        
        return False

def verify_git_status():
    """Verify git status and provide recommendations."""
    print("\n🔍 Checking Git status...")
    
    # Check if we're in a git repository
    success, stdout, stderr = run_command("git status")
    if not success:
        print("❌ Not in a Git repository or Git not available")
        return False
    
    print("✅ Git repository detected")
    
    # Check for uncommitted changes
    success, stdout, stderr = run_command("git status --porcelain")
    if success and stdout.strip():
        print("⚠️  Warning: You have uncommitted changes:")
        print(stdout)
        print("   Consider committing or stashing changes before running the fix")
        return False
    
    print("✅ Working directory is clean")
    return True

def main():
    """Main function."""
    print("🚀 Login Directory Case Sensitivity Fix")
    print("=" * 50)
    print()
    print("This script will fix the case sensitivity issue where:")
    print("- Local environment has 'Login' directory")
    print("- Render environment shows 'LogIn' directory")
    print("- This causes build failures on Linux (case-sensitive)")
    print()
    
    # Verify git status
    if not verify_git_status():
        print("\n❌ Git verification failed. Please resolve issues and try again.")
        return 1
    
    # Ask for confirmation
    response = input("Do you want to proceed with the fix? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Operation cancelled by user")
        return 1
    
    # Run the fix
    if fix_login_directory_case():
        print("\n🎉 Fix completed successfully!")
        print("   The Login directory case has been corrected.")
        print("   Push the changes and redeploy to Render.")
        return 0
    else:
        print("\n❌ Fix failed!")
        print("   Please check the errors above and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
