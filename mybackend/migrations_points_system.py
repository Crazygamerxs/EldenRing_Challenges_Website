#!/usr/bin/env python
"""
Database migration script for the enhanced points system
Run this after updating your models
Save as migrate_points_system.py in your mybackend directory
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from django.core.management import execute_from_command_line

def run_migrations():
    """Run Django migrations for the new fields"""
    print("Creating and running migrations for the enhanced points system...")
    
    # Make migrations
    print("\n1. Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Run migrations
    print("\n2. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n3. Migrations completed successfully!")

if __name__ == '__main__':
    run_migrations()
    
    # After migrations, update the challenge points
    print("\n4. Updating challenge points...")
    from api.models import Challenge, Submission, User
    
    # Update all challenges with proper points
    for challenge in Challenge.objects.all():
        if challenge.base_points == 0:
            challenge.save()  # This will trigger the auto-calculation
            print(f"Updated {challenge.name}: {challenge.base_points} points")
    
    # Update all user point totals
    print("\n5. Updating user point totals...")
    for user in User.objects.all():
        user.update_points_and_challenges()
        if user.total_points > 0:
            print(f"Updated {user.username}: {user.total_points} points, {user.challenges_completed_count} challenges")
    
    print("\nMigration and data update completed successfully!")