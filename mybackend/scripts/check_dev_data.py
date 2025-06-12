#!/usr/bin/env python3
"""
Development Data Check Script
Quick check to see what data exists in your development database before migration.
"""

import os
import sys
import django
from pathlib import Path

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment for development database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import (
    User, Challenge_Category, Challenge, Submission, 
    SiteSettings, ForumCategory, DiscussionThread, 
    Comment, Notification, Badge, UserBadge
)

def check_database_data():
    """Check what data exists in the development database."""
    print("🔍 Checking development database data...")
    print("=" * 60)
    
    # Check if database file exists
    db_path = Path('db.sqlite3')
    if not db_path.exists():
        print("❌ SQLite database file not found: db.sqlite3")
        return False
    
    print(f"✅ Database file found: {db_path} ({db_path.stat().st_size} bytes)")
    print()
    
    # Check core data
    print("📊 Core Data Summary:")
    print("-" * 30)
    
    try:
        # Challenge Categories
        category_count = Challenge_Category.objects.count()
        print(f"Challenge Categories: {category_count}")
        if category_count > 0:
            categories = Challenge_Category.objects.all()[:5]
            for cat in categories:
                print(f"  - {cat.name}")
            if category_count > 5:
                print(f"  ... and {category_count - 5} more")
        
        # Challenges
        challenge_count = Challenge.objects.count()
        print(f"\nChallenges: {challenge_count}")
        if challenge_count > 0:
            challenges = Challenge.objects.all()[:3]
            for challenge in challenges:
                print(f"  - {challenge.name} ({challenge.difficulty})")
            if challenge_count > 3:
                print(f"  ... and {challenge_count - 3} more")
        
        # Users
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_staff=True).count()
        regular_count = user_count - admin_count
        print(f"\nUsers: {user_count} total")
        print(f"  - Admin users: {admin_count}")
        print(f"  - Regular users: {regular_count}")
        
        if admin_count > 0:
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                print(f"    Admin: {admin.email}")
        
        # Site Settings
        settings_count = SiteSettings.objects.count()
        print(f"\nSite Settings: {settings_count}")
        if settings_count > 0:
            settings = SiteSettings.objects.first()
            print(f"  - Site Name: {settings.site_name}")
            print(f"  - Registrations: {'Enabled' if settings.enable_registrations else 'Disabled'}")
            print(f"  - Maintenance Mode: {'On' if settings.maintenance_mode else 'Off'}")
        
        print("\n" + "-" * 30)
        print("📊 Optional Data Summary:")
        print("-" * 30)
        
        # Submissions
        submission_count = Submission.objects.count()
        print(f"Submissions: {submission_count}")
        if submission_count > 0:
            approved_count = Submission.objects.filter(status='approved').count()
            pending_count = Submission.objects.filter(status='pending').count()
            rejected_count = Submission.objects.filter(status='rejected').count()
            print(f"  - Approved: {approved_count}")
            print(f"  - Pending: {pending_count}")
            print(f"  - Rejected: {rejected_count}")
        
        # Forum data
        forum_cat_count = ForumCategory.objects.count()
        thread_count = DiscussionThread.objects.count()
        comment_count = Comment.objects.count()
        print(f"\nForum Data:")
        print(f"  - Categories: {forum_cat_count}")
        print(f"  - Threads: {thread_count}")
        print(f"  - Comments: {comment_count}")
        
        # Notifications
        notification_count = Notification.objects.count()
        print(f"\nNotifications: {notification_count}")
        
        # Badges
        badge_count = Badge.objects.count()
        user_badge_count = UserBadge.objects.count()
        print(f"\nBadges:")
        print(f"  - Badge definitions: {badge_count}")
        print(f"  - User badges: {user_badge_count}")
        
        print("\n" + "=" * 60)
        
        # Migration readiness assessment
        print("🚀 Migration Readiness Assessment:")
        print("-" * 40)
        
        ready_for_migration = True
        issues = []
        
        if category_count == 0:
            issues.append("No challenge categories found")
            ready_for_migration = False
        
        if challenge_count == 0:
            issues.append("No challenges found")
            ready_for_migration = False
        
        if admin_count == 0:
            issues.append("No admin users found")
            ready_for_migration = False
        
        if settings_count == 0:
            issues.append("No site settings found")
        
        if ready_for_migration:
            print("✅ Ready for migration!")
            print(f"   Core data: {category_count} categories, {challenge_count} challenges")
            print(f"   Admin users: {admin_count}")
            print(f"   Optional data: {submission_count} submissions, {notification_count} notifications")
        else:
            print("⚠️  Issues found:")
            for issue in issues:
                print(f"   - {issue}")
            print("\n   Consider running data population scripts first:")
            print("   - python add_complete_challenges.py")
            print("   - python create_default_admin.py")
        
        print("\nNext steps:")
        if ready_for_migration:
            print("1. Run: python scripts/export_dev_data.py")
            print("2. Run: python scripts/setup_production.py")
            print("3. Run: python scripts/verify_migration.py")
        else:
            print("1. Populate missing data")
            print("2. Re-run this check")
            print("3. Proceed with migration")
        
        return ready_for_migration
        
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")
        return False

if __name__ == "__main__":
    check_database_data()
