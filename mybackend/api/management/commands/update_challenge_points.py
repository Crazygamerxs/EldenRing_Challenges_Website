# Create this file as: mybackend/api/management/commands/update_challenge_points.py
# First create the directories: mybackend/api/management/ and mybackend/api/management/commands/
# Add __init__.py files to both directories

from django.core.management.base import BaseCommand
from api.models import Challenge, User

class Command(BaseCommand):
    help = 'Update existing challenges with base points and recalculate user points'

    def handle(self, *args, **options):
        self.stdout.write('Starting points system update...')
        
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
                self.stdout.write(f'Updated {challenge.name}: {challenge.base_points} points')
        
        self.stdout.write(f'Updated {challenges_updated} challenges with base points')
        
        # Update all users' points and challenge counts
        users_updated = 0
        for user in User.objects.all():
            user.update_points_and_challenges()
            users_updated += 1
            self.stdout.write(f'Updated {user.username}: {user.total_points} points, {user.challenges_completed_count} challenges')
        
        self.stdout.write(f'Updated {users_updated} users with points and challenge counts')
        
        # Update existing approved submissions with points
        from api.models import Submission
        submissions_updated = 0
        for submission in Submission.objects.filter(status='approved'):
            if submission.points_awarded == 0:
                submission.points_awarded = submission.challenge.get_total_points()
                submission.save()
                submissions_updated += 1
        
        self.stdout.write(f'Updated {submissions_updated} approved submissions with points')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated points system:\n'
                f'- {challenges_updated} challenges updated\n'
                f'- {users_updated} users updated\n'
                f'- {submissions_updated} submissions updated'
            )
        )