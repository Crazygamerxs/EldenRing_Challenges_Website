#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

# Now we can import Django models
from api.models import Challenge, User, Submission, SiteSettings

def update_points_system():
    print('Starting points system update...')
    
    # Create default site settings if they don't exist
    try:
        settings = SiteSettings.get_settings()
        print(f'Site settings initialized: {settings.site_name}')
    except Exception as e:
        print(f'Error initializing settings: {e}')
    
    # Update all challenges with base points
    challenges_updated = 0
    for challenge in Challenge.objects.all():
        if challenge.base_points == 0:
            # Auto-calculate base points based on difficulty
            difficulty_points = {
                'Easy': 50,
                'Medium': 100,
                'Hard': 200,
                'Extreme': 350
            }
            challenge.base_points = difficulty_points.get(challenge.difficulty, 50)
            challenge.save()
            challenges_updated += 1
            print(f'Updated {challenge.name}: {challenge.base_points} points')
    
    print(f'Updated {challenges_updated} challenges with base points')
    
    # Update all users' points and challenge counts
    users_updated = 0
    for user in User.objects.all():
        old_points = user.total_points
        old_challenges = user.challenges_completed_count
        
        user.update_points_and_challenges()
        
        if user.total_points != old_points or user.challenges_completed_count != old_challenges:
            users_updated += 1
            print(f'Updated {user.username}: {user.total_points} points, {user.challenges_completed_count} challenges')
    
    print(f'Updated {users_updated} users with points and challenge counts')
    
    # Update existing approved submissions with points
    submissions_updated = 0
    for submission in Submission.objects.filter(status='approved'):
        if submission.points_awarded == 0:
            submission.points_awarded = submission.challenge.get_total_points()
            submission.save()
            submissions_updated += 1
    
    print(f'Updated {submissions_updated} approved submissions with points')
    
    print(f'''
✅ Successfully updated points system:
- {challenges_updated} challenges updated
- {users_updated} users updated  
- {submissions_updated} submissions updated
- Site settings initialized
    ''')

if __name__ == '__main__':
    update_points_system()