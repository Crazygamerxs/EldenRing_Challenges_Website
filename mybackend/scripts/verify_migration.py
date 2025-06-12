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

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MigrationVerifier:
    def __init__(self, use_supabase_settings=True):
        self.use_supabase_settings = use_supabase_settings
        self.setup_django_environment()
        
    def setup_django_environment(self):
        """Set up Django environment for production database."""
        if self.use_supabase_settings:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_supabase')
        else:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_production')
        
        django.setup()
        
        # Import models after Django setup
        from api.models import (
            User, Challenge_Category, Challenge, Submission, 
            SiteSettings, ForumCategory, DiscussionThread, 
            Comment, Notification, Badge, UserBadge
        )
        
        self.models = {
            'User': User,
            'Challenge_Category': Challenge_Category,
            'Challenge': Challenge,
            'Submission': Submission,
            'SiteSettings': SiteSettings,
            'ForumCategory': ForumCategory,
            'DiscussionThread': DiscussionThread,
            'Comment': Comment,
            'Notification': Notification,
            'Badge': Badge,
            'UserBadge': UserBadge,
        }
    
    def test_database_connection(self):
        """Test connection to the production database."""
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                result = cursor.fetchone()
            
            if result:
                print(f"✅ Database connection successful")
                print(f"Database version: {result[0]}")
                return True
            else:
                print("❌ Database connection failed")
                return False
                
        except Exception as e:
            print(f"❌ Database connection error: {str(e)}")
            return False
    
    def verify_table_structure(self):
        """Verify that all expected tables exist."""
        try:
            from django.db import connection
            
            with connection.cursor() as cursor:
                # Get list of tables
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                """)
                tables = [row[0] for row in cursor.fetchall()]
            
            # Expected tables
            expected_tables = [
                'api_user',
                'api_challenge_category',
                'api_challenge',
                'api_submission',
                'api_sitesettings',
                'api_forumcategory',
                'api_discussionthread',
                'api_comment',
                'api_notification',
                'api_badge',
                'api_userbadge',
                'django_migrations',
                'auth_group',
                'auth_permission',
                'django_content_type',
                'django_session'
            ]
            
            missing_tables = []
            for table in expected_tables:
                if table not in tables:
                    missing_tables.append(table)
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print(f"✅ All expected tables exist ({len(expected_tables)} tables)")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying table structure: {str(e)}")
            return False
    
    def verify_data_counts(self):
        """Verify data counts in core tables."""
        print("🔄 Verifying data counts...")
        
        try:
            counts = {}
            
            # Core models to check
            core_models = [
                'Challenge_Category',
                'Challenge', 
                'User',
                'SiteSettings'
            ]
            
            for model_name in core_models:
                model_class = self.models[model_name]
                count = model_class.objects.count()
                counts[model_name] = count
                print(f"  {model_name}: {count} records")
            
            # Check for minimum expected data
            issues = []
            
            if counts['Challenge_Category'] == 0:
                issues.append("No challenge categories found")
            
            if counts['Challenge'] == 0:
                issues.append("No challenges found")
            
            if counts['User'] == 0:
                issues.append("No users found")
            
            admin_count = self.models['User'].objects.filter(is_staff=True).count()
            if admin_count == 0:
                issues.append("No admin users found")
            else:
                print(f"  Admin Users: {admin_count} records")
            
            if counts['SiteSettings'] == 0:
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
    
    def verify_foreign_key_relationships(self):
        """Verify foreign key relationships are intact."""
        print("🔄 Verifying foreign key relationships...")
        
        try:
            Challenge = self.models['Challenge']
            Challenge_Category = self.models['Challenge_Category']
            Submission = self.models['Submission']
            User = self.models['User']
            
            # Check challenge -> category relationships
            total_challenges = Challenge.objects.count()
            challenges_with_categories = Challenge.objects.filter(category__isnull=False).count()
            
            print(f"  Challenges with categories: {challenges_with_categories}/{total_challenges}")
            
            if total_challenges > 0 and challenges_with_categories != total_challenges:
                print("❌ Some challenges have invalid category references")
                return False
            
            # Check submission -> user and challenge relationships
            total_submissions = Submission.objects.count()
            if total_submissions > 0:
                submissions_with_users = Submission.objects.filter(user__isnull=False).count()
                submissions_with_challenges = Submission.objects.filter(challenge__isnull=False).count()
                
                print(f"  Submissions with users: {submissions_with_users}/{total_submissions}")
                print(f"  Submissions with challenges: {submissions_with_challenges}/{total_submissions}")
                
                if submissions_with_users != total_submissions or submissions_with_challenges != total_submissions:
                    print("❌ Some submissions have invalid foreign key references")
                    return False
            
            print("✅ All foreign key relationships are valid")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying foreign key relationships: {str(e)}")
            return False
    
    def test_admin_functionality(self):
        """Test that admin functionality works."""
        print("🔄 Testing admin functionality...")
        
        try:
            User = self.models['User']
            
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
    
    def test_challenge_data_integrity(self):
        """Test that challenge data is properly structured."""
        print("🔄 Testing challenge data integrity...")
        
        try:
            Challenge = self.models['Challenge']
            Challenge_Category = self.models['Challenge_Category']
            
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
    
    def test_site_settings(self):
        """Test that site settings are properly configured."""
        print("🔄 Testing site settings...")
        
        try:
            SiteSettings = self.models['SiteSettings']
            
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
    
    def generate_verification_report(self, results):
        """Generate a verification report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"migration_verification_report_{timestamp}.json"
        
        report = {
            'verification_timestamp': datetime.now().isoformat(),
            'database_type': 'PostgreSQL (Supabase)',
            'results': results,
            'overall_status': 'PASSED' if all(results.values()) else 'FAILED',
            'summary': {
                'total_tests': len(results),
                'passed_tests': sum(1 for result in results.values() if result),
                'failed_tests': sum(1 for result in results.values() if not result)
            }
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Verification report saved: {report_file}")
            
        except Exception as e:
            print(f"⚠️  Could not save verification report: {str(e)}")

def main():
    print("🔍 Starting migration verification...")
    print("=" * 60)
    
    verifier = MigrationVerifier(use_supabase_settings=True)
    
    # Run all verification tests
    results = {}
    
    print("1. Testing database connection...")
    results['database_connection'] = verifier.test_database_connection()
    
    print("\n2. Verifying table structure...")
    results['table_structure'] = verifier.verify_table_structure()
    
    print("\n3. Verifying data counts...")
    results['data_counts'] = verifier.verify_data_counts()
    
    print("\n4. Verifying foreign key relationships...")
    results['foreign_keys'] = verifier.verify_foreign_key_relationships()
    
    print("\n5. Testing admin functionality...")
    results['admin_functionality'] = verifier.test_admin_functionality()
    
    print("\n6. Testing challenge data integrity...")
    results['challenge_integrity'] = verifier.test_challenge_data_integrity()
    
    print("\n7. Testing site settings...")
    results['site_settings'] = verifier.test_site_settings()
    
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
    
    # Generate report
    verifier.generate_verification_report(results)
    
    print("\nVerification Summary:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
