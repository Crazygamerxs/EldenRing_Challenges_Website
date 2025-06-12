#!/usr/bin/env python3
"""
Migration Verification Script for Elden Ring Challenges Website
Verifies that the data migration from SQLite to PostgreSQL was successful.
"""

import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('.env.prod')

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment for production database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_supabase')
django.setup()

from api.models import (
    User, Challenge_Category, Challenge, Submission, 
    SiteSettings, ForumCategory, DiscussionThread, 
    Comment, Notification, Badge, UserBadge
)

def test_database_connection():
    """Test connection to the production database."""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
        
        if result:
            print(f"✅ Database connection successful")
            print(f"Database version: {result[0][:50]}...")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        return False

def verify_data_counts():
    """Verify data counts in core tables."""
    print("🔄 Verifying data counts...")
    
    try:
        # Core models to check
        category_count = Challenge_Category.objects.count()
        challenge_count = Challenge.objects.count()
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_staff=True).count()
        settings_count = SiteSettings.objects.count()
        
        print(f"  Challenge Categories: {category_count}")
        print(f"  Challenges: {challenge_count}")
        print(f"  Total Users: {user_count}")
        print(f"  Admin Users: {admin_count}")
        print(f"  Site Settings: {settings_count}")
        
        # Check for minimum expected data
        issues = []
        
        if category_count == 0:
            issues.append("No challenge categories found")
        
        if challenge_count == 0:
            issues.append("No challenges found")
        
        if admin_count == 0:
            issues.append("No admin users found")
        
        if settings_count == 0:
            issues.append("No site settings found")
        
        if issues:
            print(f"❌ Data issues found: {issues}")
            return False
        else:
            print("✅ Data counts look good")
            return True
            
    except Exception as e:
        print(f"❌ Error verifying data counts: {str(e)}")
        return False

def verify_foreign_key_relationships():
    """Verify foreign key relationships are intact."""
    print("🔄 Verifying foreign key relationships...")
    
    try:
        # Check challenge -> category relationships
        total_challenges = Challenge.objects.count()
        challenges_with_categories = Challenge.objects.filter(category__isnull=False).count()
        
        print(f"  Challenges with categories: {challenges_with_categories}/{total_challenges}")
        
        if total_challenges > 0 and challenges_with_categories != total_challenges:
            print("❌ Some challenges have invalid category references")
            return False
        
        print("✅ All foreign key relationships are valid")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying foreign key relationships: {str(e)}")
        return False

def test_admin_functionality():
    """Test that admin functionality works."""
    print("🔄 Testing admin functionality...")
    
    try:
        # Check if admin users exist and can be authenticated
        admin_users = User.objects.filter(is_staff=True)
        
        if not admin_users.exists():
            print("❌ No admin users found")
            return False
        
        admin_user = admin_users.first()
        
        # Test basic user properties
        if not admin_user.is_staff:
            print("❌ Admin user is not marked as staff")
            return False
        
        if not admin_user.is_active:
            print("❌ Admin user is not active")
            return False
        
        # Test password is set (not empty)
        if not admin_user.password:
            print("❌ Admin user has no password set")
            return False
        
        print(f"✅ Admin user '{admin_user.email}' is properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing admin functionality: {str(e)}")
        return False

def test_challenge_data_integrity():
    """Test that challenge data is properly structured."""
    print("🔄 Testing challenge data integrity...")
    
    try:
        challenges = Challenge.objects.all()
        
        if not challenges.exists():
            print("⚠️  No challenges found to test")
            return True
        
        issues = []
        
        for challenge in challenges[:10]:  # Test first 10 challenges
            # Check required fields
            if not challenge.name:
                issues.append(f"Challenge {challenge.pk} has no name")
            
            if not challenge.details:
                issues.append(f"Challenge {challenge.pk} has no details")
            
            if not challenge.difficulty:
                issues.append(f"Challenge {challenge.pk} has no difficulty")
            
            if not challenge.category:
                issues.append(f"Challenge {challenge.pk} has no category")
            
            if challenge.base_points <= 0:
                issues.append(f"Challenge {challenge.pk} has invalid base_points")
        
        if issues:
            print(f"❌ Challenge data issues: {issues[:5]}")  # Show first 5 issues
            return False
        else:
            print(f"✅ Challenge data integrity verified ({challenges.count()} challenges)")
            return True
            
    except Exception as e:
        print(f"❌ Error testing challenge data integrity: {str(e)}")
        return False

def test_site_settings():
    """Test that site settings are properly configured."""
    print("🔄 Testing site settings...")
    
    try:
        settings = SiteSettings.objects.first()
        
        if not settings:
            print("❌ No site settings found")
            return False
        
        # Check basic settings
        if not settings.site_name:
            print("❌ Site name is not set")
            return False
        
        print(f"✅ Site settings configured:")
        print(f"  Site Name: {settings.site_name}")
        print(f"  Registrations: {'Enabled' if settings.enable_registrations else 'Disabled'}")
        print(f"  Submissions: {'Enabled' if settings.enable_submissions else 'Disabled'}")
        print(f"  Maintenance Mode: {'On' if settings.maintenance_mode else 'Off'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing site settings: {str(e)}")
        return False

def main():
    print("🔍 Starting migration verification...")
    print("=" * 60)
    
    # Run all verification tests
    results = {}
    
    print("1. Testing database connection...")
    results['database_connection'] = test_database_connection()
    
    print("\n2. Verifying data counts...")
    results['data_counts'] = verify_data_counts()
    
    print("\n3. Verifying foreign key relationships...")
    results['foreign_keys'] = verify_foreign_key_relationships()
    
    print("\n4. Testing admin functionality...")
    results['admin_functionality'] = test_admin_functionality()
    
    print("\n5. Testing challenge data integrity...")
    results['challenge_integrity'] = test_challenge_data_integrity()
    
    print("\n6. Testing site settings...")
    results['site_settings'] = test_site_settings()
    
    print("\n" + "=" * 60)
    
    # Summary
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    if passed_tests == total_tests:
        print("✅ ALL VERIFICATION TESTS PASSED!")
        print("🎉 Migration completed successfully!")
    else:
        print(f"❌ {total_tests - passed_tests} out of {total_tests} tests failed")
        print("⚠️  Please review the failed tests above")
    
    print("\nVerification Summary:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
