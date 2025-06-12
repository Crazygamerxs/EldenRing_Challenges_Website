#!/usr/bin/env python3
"""
Data Export Script for Elden Ring Challenges Website
Exports development data from SQLite to JSON fixtures for production migration.
"""

import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment for development database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from django.core import serializers
from django.contrib.auth.models import Group, Permission
from api.models import (
    User, Challenge_Category, Challenge, Submission, 
    SiteSettings, ForumCategory, DiscussionThread, 
    Comment, Notification, Badge, UserBadge
)

class DataExporter:
    def __init__(self, export_dir='data_exports'):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def export_model_data(self, model_class, filename_prefix, queryset=None, exclude_fields=None):
        """Export data from a model to JSON file."""
        try:
            if queryset is None:
                queryset = model_class.objects.all()
            
            count = queryset.count()
            
            if count == 0:
                print(f"⚠️  No data found for {model_class.__name__}")
                return None
                
            # Serialize the data
            serialized_data = serializers.serialize(
                'json', 
                queryset,
                use_natural_foreign_keys=True,
                use_natural_primary_keys=False
            )
            
            # Parse and clean the data if needed
            data = json.loads(serialized_data)
            
            # Remove excluded fields if specified
            if exclude_fields:
                for item in data:
                    for field in exclude_fields:
                        if field in item['fields']:
                            del item['fields'][field]
            
            # Save to file
            filename = f"{filename_prefix}_{self.timestamp}.json"
            filepath = self.export_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✅ Exported {count} {model_class.__name__} records to {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error exporting {model_class.__name__}: {str(e)}")
            return None
    
    def export_core_data(self):
        """Export essential core data needed for production."""
        print("🔄 Exporting core data...")
        
        core_exports = {}
        
        # 1. Challenge Categories (must be first due to foreign keys)
        core_exports['categories'] = self.export_model_data(
            Challenge_Category, 
            'challenge_categories'
        )
        
        # 2. Challenges (depends on categories)
        core_exports['challenges'] = self.export_model_data(
            Challenge, 
            'challenges'
        )
        
        # 3. Admin Users (exclude sensitive fields)
        admin_users = User.objects.filter(is_staff=True)
        if admin_users.exists():
            core_exports['admin_users'] = self.export_model_data(
                User,
                'admin_users',
                queryset=admin_users,
                exclude_fields=['password']
            )
        
        # 4. Site Settings
        core_exports['site_settings'] = self.export_model_data(
            SiteSettings, 
            'site_settings'
        )
        
        # 5. Django Groups and Permissions (if any custom ones exist)
        if Group.objects.exists():
            core_exports['groups'] = self.export_model_data(Group, 'auth_groups')
        
        return core_exports
    
    def export_optional_data(self):
        """Export optional data that might be useful but not essential."""
        print("🔄 Exporting optional data...")
        
        optional_exports = {}
        
        # Regular users (non-admin)
        regular_users = User.objects.filter(is_staff=False)
        if regular_users.exists():
            optional_exports['users'] = self.export_model_data(
                User,
                'regular_users',
                queryset=regular_users,
                exclude_fields=['password']
            )
        
        # Submissions
        optional_exports['submissions'] = self.export_model_data(
            Submission, 
            'submissions'
        )
        
        # Forum data
        optional_exports['forum_categories'] = self.export_model_data(
            ForumCategory, 
            'forum_categories'
        )
        
        optional_exports['discussions'] = self.export_model_data(
            DiscussionThread, 
            'discussion_threads'
        )
        
        optional_exports['comments'] = self.export_model_data(
            Comment, 
            'comments'
        )
        
        # Notifications
        optional_exports['notifications'] = self.export_model_data(
            Notification, 
            'notifications'
        )
        
        # Badges
        optional_exports['badges'] = self.export_model_data(
            Badge, 
            'badges'
        )
        
        optional_exports['user_badges'] = self.export_model_data(
            UserBadge, 
            'user_badges'
        )
        
        return optional_exports
    
    def create_admin_credentials_file(self):
        """Create a separate file with admin credentials for production setup."""
        admin_users = User.objects.filter(is_staff=True)
        
        if not admin_users.exists():
            print("⚠️  No admin users found in development database")
            return None
        
        admin_data = []
        for user in admin_users:
            admin_data.append({
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),
                'note': 'Password needs to be set manually in production'
            })
        
        filename = f"admin_credentials_{self.timestamp}.json"
        filepath = self.export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(admin_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Admin credentials exported to {filename}")
        return filepath
    
    def create_migration_summary(self, core_exports, optional_exports):
        """Create a summary file of the migration."""
        summary = {
            'export_timestamp': datetime.now().isoformat(),
            'source_database': 'SQLite (development)',
            'target_database': 'PostgreSQL (Supabase)',
            'core_data': {},
            'optional_data': {},
            'notes': [
                'Core data should be imported first',
                'Admin passwords need to be set manually',
                'Verify foreign key relationships after import',
                'Test critical functionality after migration'
            ]
        }
        
        # Add file information
        for key, filepath in core_exports.items():
            if filepath:
                summary['core_data'][key] = {
                    'file': filepath.name,
                    'status': 'exported'
                }
        
        for key, filepath in optional_exports.items():
            if filepath:
                summary['optional_data'][key] = {
                    'file': filepath.name,
                    'status': 'exported'
                }
        
        filename = f"migration_summary_{self.timestamp}.json"
        filepath = self.export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migration summary created: {filename}")
        return filepath

def main():
    print("🚀 Starting data export from development database...")
    print("=" * 60)
    
    exporter = DataExporter()
    
    # Export core data
    core_exports = exporter.export_core_data()
    
    print("\n" + "=" * 60)
    
    # Export optional data
    optional_exports = exporter.export_optional_data()
    
    print("\n" + "=" * 60)
    
    # Create admin credentials file
    exporter.create_admin_credentials_file()
    
    # Create migration summary
    exporter.create_migration_summary(core_exports, optional_exports)
    
    print("\n" + "=" * 60)
    print("✅ Data export completed successfully!")
    print(f"📁 Export files saved in: {exporter.export_dir}")
    print("\nNext steps:")
    print("1. Review the exported files")
    print("2. Run the production setup script")
    print("3. Import the data to Supabase")
    print("4. Verify the migration")

if __name__ == "__main__":
    main()
