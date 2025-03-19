import os
import django
import sys

# Set up Django environment
sys.path.append('mybackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import Challenge, Challenge_Category

def parse_challenges_file(file_path):
    """Parse the challenges.txt file and extract challenge data."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content by categories
    categories = {}
    current_category = None
    current_challenges = []
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if this is a category header
        if line.endswith('Challenges') or 'Challenges for the Brave or Insane' in line or 'Challenge Combination Examples' in line:
            if current_category and current_challenges:
                categories[current_category] = current_challenges
            current_category = line
            current_challenges = []
        elif line and current_category:
            # This is a challenge name or description
            if not line.startswith('NOTE:') and not line.startswith('('):
                current_challenges.append(line)
    
    # Add the last category
    if current_category and current_challenges:
        categories[current_category] = current_challenges
    
    # Process the challenges
    processed_challenges = []
    for category, challenges_list in categories.items():
        i = 0
        while i < len(challenges_list):
            name = challenges_list[i]
            description = ""
            i += 1
            
            # Check if the next line is a description
            if i < len(challenges_list) and not challenges_list[i].endswith('Challenges') and not challenges_list[i].startswith('NOTE:'):
                description = challenges_list[i]
                i += 1
            
            processed_challenges.append({
                'name': name,
                'category': category,
                'details': description,
                'difficulty': determine_difficulty(category)
            })
    
    return processed_challenges

def determine_difficulty(category):
    """Determine the difficulty based on the category."""
    if 'General' in category or 'Basic' in category:
        return 'Easy'
    elif 'Advanced' in category:
        return 'Medium'
    else:
        return 'Hard'

def add_challenges_to_db():
    """Add challenges from the challenges.txt file to the database."""
    challenges = parse_challenges_file('challenges.txt')
    
    # Get existing challenge names
    existing_challenges = set(Challenge.objects.values_list('name', flat=True))
    
    # Create categories if they don't exist
    categories = set(challenge['category'] for challenge in challenges)
    for category_name in categories:
        Challenge_Category.objects.get_or_create(name=category_name)
    
    # Add new challenges
    added_count = 0
    for challenge in challenges:
        if challenge['name'] not in existing_challenges:
            category, _ = Challenge_Category.objects.get_or_create(name=challenge['category'])
            Challenge.objects.create(
                name=challenge['name'],
                category=category,
                details=challenge['details'],
                difficulty=challenge['difficulty']
            )
            added_count += 1
            print(f"Added challenge: {challenge['name']}")
    
    print(f"Added {added_count} new challenges to the database.")

if __name__ == "__main__":
    add_challenges_to_db()
