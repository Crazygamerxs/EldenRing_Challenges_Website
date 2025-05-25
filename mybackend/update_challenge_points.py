#!/usr/bin/env python
"""
Script to update existing challenges with points based on difficulty and combination status
Save this as update_challenge_points.py in your mybackend directory
Run with: python update_challenge_points.py
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import Challenge, Submission, User

def calculate_combination_points(challenge):
    """Calculate points for combination challenges more intelligently"""
    if not challenge.is_combination:
        return 0
    
    # Base points for the challenge's stated difficulty
    difficulty_points = {
        'Easy': 50,
        'Medium': 100,
        'Hard': 200,
        'Extreme': 400
    }
    base_points = difficulty_points.get(challenge.difficulty, 50)
    
    # Try to parse the combination details to get a more accurate count
    details = challenge.details.lower()
    
    # Count individual challenges mentioned in combination
    # Look for '+' signs as separators
    plus_count = challenge.details.count('+')
    
    # Some combinations are more complex than others
    if plus_count >= 3:  # 4+ challenges combined
        multiplier = 3.0
    elif plus_count >= 2:  # 3 challenges combined
        multiplier = 2.5
    elif plus_count >= 1:  # 2 challenges combined
        multiplier = 2.0
    else:
        # If no '+' found, estimate based on difficulty and "combination" status
        multiplier = 2.0
    
    # Apply additional multiplier for extreme combinations
    if challenge.difficulty == 'Extreme':
        multiplier *= 1.5
    
    final_points = int(base_points * multiplier)
    print(f"Combination '{challenge.name}': {base_points} base × {multiplier} = {final_points} points")
    
    return final_points

def update_challenge_points():
    """Update all challenges with appropriate points"""
    challenges = Challenge.objects.all()
    updated_count = 0
    
    difficulty_points = {
        'Easy': 50,
        'Medium': 100,
        'Hard': 200,
        'Extreme': 400
    }
    
    print("Updating challenge points...")
    
    for challenge in challenges:
        old_points = challenge.base_points
        
        if challenge.is_combination:
            new_points = calculate_combination_points(challenge)
        else:
            new_points = difficulty_points.get(challenge.difficulty, 50)
        
        challenge.base_points = new_points
        challenge.save()
        
        if old_points != new_points:
            print(f"Updated '{challenge.name}': {old_points} → {new_points} points")
            updated_count += 1
        else:
            print(f"No change '{challenge.name}': {new_points} points")
    
    print(f"\nUpdated {updated_count} challenges with new points")
    
    # Now update all users' points based on their approved submissions
    update_user_points()

def update_user_points():
    """Recalculate all user points based on approved submissions"""
    print("\nUpdating user points...")
    
    # First, recalculate points for all approved submissions
    approved_submissions = Submission.objects.filter(status='approved')
    
    for submission in approved_submissions:
        old_points = submission.points_awarded
        new_points = submission.challenge.get_total_points()
        
        if old_points != new_points:
            submission.points_awarded = new_points
            submission.save()
            print(f"Updated submission points: {submission.user.username} - {submission.challenge.name}: {old_points} → {new_points}")
    
    # Now update all user totals
    users_with_submissions = User.objects.filter(submission__status='approved').distinct()
    
    for user in users_with_submissions:
        old_total = user.total_points
        old_count = user.challenges_completed_count
        
        user.update_points_and_challenges()
        
        print(f"Updated user {user.username}: {old_total} → {user.total_points} points, {old_count} → {user.challenges_completed_count} challenges")
    
    print(f"\nUpdated points for {users_with_submissions.count()} users")

def show_points_breakdown():
    """Show a breakdown of points by difficulty and type"""
    print("\n" + "="*50)
    print("POINTS BREAKDOWN")
    print("="*50)
    
    # Regular challenges
    print("\nRegular Challenges:")
    for difficulty in ['Easy', 'Medium', 'Hard', 'Extreme']:
        challenges = Challenge.objects.filter(difficulty=difficulty, is_combination=False)
        if challenges.exists():
            points = challenges.first().get_total_points()
            print(f"  {difficulty}: {points} points ({challenges.count()} challenges)")
    
    # Combination challenges
    print(f"\nCombination Challenges:")
    combo_challenges = Challenge.objects.filter(is_combination=True).order_by('base_points')
    for challenge in combo_challenges:
        print(f"  {challenge.name} ({challenge.difficulty}): {challenge.base_points} points")
    
    # Total points possible
    total_possible = sum(c.base_points for c in Challenge.objects.all())
    print(f"\nTotal points possible: {total_possible}")

if __name__ == '__main__':
    print("Starting challenge points update...")
    update_challenge_points()
    show_points_breakdown()
    print("Done!")