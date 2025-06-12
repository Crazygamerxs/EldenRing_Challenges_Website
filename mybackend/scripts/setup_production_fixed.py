#!/usr/bin/env python3
"""
Production Setup Script for Elden Ring Challenges Website
Sets up the production database and imports data from development.
"""

import os
import sys
import django
import json
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('.env.prod')

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ProductionSetup:
    def __init__(self, use_supabase_settings=True):
        self.use_supabase_settings = use_supabase_settings
        self.setup_django_environment()
        self.data_dir = Path('data_exports')
        
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
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            
            if result:
                print("✅ Database connection successful")
                print(f"Connected to: {os.environ.get('DB_HOST', 'Unknown host')}")
                return True
            else:
                print("❌ Database connection failed")
                return False
                
        except Exception as e:
            print(f"❌ Database connection error: {str(e)}")
            print(f"Trying to connect to: {os.environ.get('DB_HOST', 'Unknown host')}")
            print(f"Database: {os.environ.get('DB_NAME', 'Unknown database')}")
            print(f"User: {os.environ.get('DB_USER', 'Unknown user')}")
            return False
    
    def run_migrations(self):
        """Run Django migrations on the production database."""
        try:
            print("🔄 Running Django migrations...")
            
            # Set environment variable for migrations
            env = os.environ.copy()
            env['DJANGO_SETTINGS_MODULE'] = 'mybackend.settings_supabase'
            
            # Run migrations
            result = subprocess.run([
                sys.executable, 'manage.py', 'migrate'
            ], capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print("✅ Migrations completed successfully")
                if result.stdout:
                    print("Migration output:")
                    print(result.stdout)
                return True
            else:
                print(f"❌ Migration failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running migrations: {str(e)}")
            return False
    
    def find_latest_export_files(self):
        """Find the most recent export files."""
        if not self.data_dir.exists():
            print(f"❌ Export directory {self.data_dir} not found")
            return None
        
        # Find all export files
        export_files = {}
        
        # Look for core data files
        patterns = {
            'challenge_categories': 'challenge_categories_*.json',
            'challenges': 'challenges_*.json', 
            'admin_users': 'admin_users_*.json',
            'site_settings': 'site_settings_*.json'
        }
        
        for key, pattern in patterns.items():
            files = list(self.data_dir.glob(pattern))
            if files:
                # Get the most recent file
                latest_file = max(files, key=lambda f: f.stat().st_mtime)
                export_files[key] = latest_file
        
        return export_files
    
    def import_json_fixture(self, filepath, model_class):
        """Import data from a JSON fixture file."""
        try:
            if not filepath.exists():
                print(f"⚠️  File not found: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                print(f"⚠️  No data in file: {filepath}")
                return True
            
            imported_count = 0
            skipped_count = 0
            
            for item in data:
                try:
                    # Extract model info
                    model_name = item['model']
                    pk = item['pk']
                    fields = item['fields']
                    
                    # Check if record already exists
                    if model_class.objects.filter(pk=pk).exists():
                        skipped_count += 1
                        continue
                    
                    # Create the record
                    obj = model_class(**fields)
                    obj.pk = pk
                    obj.save()
                    imported_count += 1
                    
                except Exception as e:
                    print(f"⚠️  Error importing record {pk}: {str(e)}")
                    continue
            
            print(f"✅ Imported {imported_count} records, skipped {skipped_count} existing records from {filepath.name}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing from {filepath}: {str(e)}")
            return False
    
    def import_core_data(self, export_files):
        """Import core data in the correct order."""
        print("🔄 Importing core data...")
        
        # Import in dependency order
        import_order = [
            ('challenge_categories', 'Challenge_Category'),
            ('challenges', 'Challenge'),
            ('site_settings', 'SiteSettings'),
        ]
        
        for file_key, model_name in import_order:
            if file_key in export_files:
                model_class = self.models[model_name]
                success = self.import_json_fixture(export_files[file_key], model_class)
                if not success:
                    print(f"❌ Failed to import {file_key}")
                    return False
        
        return True
    
    def create_admin_user(self, admin_credentials_file=None):
        """Create admin user for production."""
        try:
            # Try to load from exported admin credentials first
            admin_files = list(self.data_dir.glob("admin_credentials_*.json"))
            if admin_files:
                admin_credentials_file = admin_files[0]
                
            if admin_credentials_file and admin_credentials_file.exists():
                with open(admin_credentials_file, 'r', encoding='utf-8') as f:
                    admin_data = json.load(f)
                
                if admin_data:
                    admin_info = admin_data[0]  # Use first admin
                    username = admin_info['username']
                    email = admin_info['email']
                else:
                    # Fallback to default
                    username = "admin"
                    email = "admin@eldenring.com"
            else:
                # Default admin credentials
                username = "admin"
                email = "admin@eldenring.com"
            
            # Default password (should be changed after setup)
            password = "EldenRing123!"
            
            User = self.models['User']
            
            # Check if admin user already exists
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.is_staff = True
                user.is_superuser = True
                user.set_password(password)
                user.save()
                print(f"✅ Updated existing admin user: {email}")
            else:
                # Create new admin user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print(f"✅ Created new admin user: {email}")
            
            print(f"\n🔑 Admin Login Credentials:")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print(f"⚠️  IMPORTANT: Change this password after first login!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            return False
    
    def setup_site_settings(self):
        """Ensure site settings are properly configured."""
        try:
            SiteSettings = self.models['SiteSettings']
            
            # Get or create site settings
            settings, created = SiteSettings.objects.get_or_create(pk=1)
            
            if created:
                print("✅ Created default site settings")
            else:
                print("✅ Site settings already exist")
            
            # Display current settings
            print(f"Site Name: {settings.site_name}")
            print(f"Registrations Enabled: {settings.enable_registrations}")
            print(f"Submissions Enabled: {settings.enable_submissions}")
            print(f"Maintenance Mode: {settings.maintenance_mode}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up site settings: {str(e)}")
            return False
    
    def verify_data_integrity(self):
        """Verify that the imported data is correct."""
        print("🔄 Verifying data integrity...")
        
        try:
            # Check core models
            Challenge_Category = self.models['Challenge_Category']
            Challenge = self.models['Challenge']
            User = self.models['User']
            SiteSettings = self.models['SiteSettings']
            
            # Count records
            category_count = Challenge_Category.objects.count()
            challenge_count = Challenge.objects.count()
            admin_count = User.objects.filter(is_staff=True).count()
            settings_count = SiteSettings.objects.count()
            
            print(f"📊 Data Summary:")
            print(f"  Challenge Categories: {category_count}")
            print(f"  Challenges: {challenge_count}")
            print(f"  Admin Users: {admin_count}")
            print(f"  Site Settings: {settings_count}")
            
            # Verify foreign key relationships
            challenges_with_categories = Challenge.objects.filter(category__isnull=False).count()
            print(f"  Challenges with valid categories: {challenges_with_categories}/{challenge_count}")
            
            if challenges_with_categories == challenge_count:
                print("✅ All foreign key relationships are valid")
                return True
            else:
                print("⚠️  Some challenges have invalid category references")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying data integrity: {str(e)}")
            return False

def main():
    print("🚀 Starting production database setup...")
    print("=" * 60)
    
    # Initialize setup
    setup = ProductionSetup(use_supabase_settings=True)
    
    # Test database connection
    if not setup.test_database_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    print("\n" + "=" * 60)
    
    # Run migrations
    if not setup.run_migrations():
        print("❌ Cannot proceed without successful migrations")
        return False
    
    print("\n" + "=" * 60)
    
    # Find export files
    export_files = setup.find_latest_export_files()
    if not export_files:
        print("⚠️  No export files found. Running basic setup only.")
        
        # Create admin user and site settings
        setup.create_admin_user()
        setup.setup_site_settings()
        
    else:
        print(f"📁 Found export files: {list(export_files.keys())}")
        
        # Import core data
        if setup.import_core_data(export_files):
            print("✅ Core data imported successfully")
        else:
            print("❌ Failed to import core data")
            return False
        
        # Create admin user
        setup.create_admin_user()
        
        # Setup site settings
        setup.setup_site_settings()
    
    print("\n" + "=" * 60)
    
    # Verify data integrity
    if setup.verify_data_integrity():
        print("✅ Data integrity verification passed")
    else:
        print("⚠️  Data integrity issues detected")
    
    print("\n" + "=" * 60)
    print("✅ Production setup completed!")
    print("\nNext steps:")
    print("1. Test the admin login")
    print("2. Verify that challenges load correctly")
    print("3. Test core functionality")
    print("4. Change admin password")
    print("5. Configure production environment variables")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
