#!/usr/bin/env python3
"""
Fix Challenges Import Script
Properly imports challenges with correct foreign key relationships.
"""

import os
import sys
import django
import json
from pathlib import Path
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('.env.prod')

# Add the parent directory to the path to import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment for production database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_supabase')
django.setup()

from api.models import Challenge_Category, Challenge

def fix_challenges_import():
    """Import challenges with proper foreign key relationships."""
    print("🔄 Fixing challenges import...")
    
    # Find the challenges export file
    data_dir = Path('data_exports')
    challenge_files = list(data_dir.glob('challenges_*.json'))
    
    if not challenge_files:
        print("❌ No challenges export file found")
        return False
    
    challenge_file = challenge_files[0]  # Use the most recent
    print(f"📁 Using file: {challenge_file}")
    
    try:
        with open(challenge_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        for item in data:
            try:
                pk = item['pk']
                fields = item['fields']
                
                # Check if challenge already exists
                if Challenge.objects.filter(pk=pk).exists():
                    skipped_count += 1
                    continue
                
                # Get the category by ID
                category_id = fields['category']
                try:
                    category = Challenge_Category.objects.get(pk=category_id)
                except Challenge_Category.DoesNotExist:
                    print(f"⚠️  Category {category_id} not found for challenge {pk}")
                    error_count += 1
                    continue
                
                # Create the challenge
                challenge = Challenge(
                    pk=pk,
                    name=fields['name'],
                    details=fields['details'],
                    difficulty=fields['difficulty'],
                    category=category,
                    is_dlc=fields.get('is_dlc', False),
                    is_combination=fields.get('is_combination', False),
                    base_points=fields.get('base_points', 0)
                )
                challenge.save()
                imported_count += 1
                
                if imported_count % 20 == 0:
                    print(f"  Imported {imported_count} challenges...")
                
            except Exception as e:
                print(f"⚠️  Error importing challenge {pk}: {str(e)}")
                error_count += 1
                continue
        
        print(f"\n✅ Challenge import completed:")
        print(f"  Imported: {imported_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"  Errors: {error_count}")
        
        # Verify the import
        total_challenges = Challenge.objects.count()
        total_categories = Challenge_Category.objects.count()
        challenges_with_categories = Challenge.objects.filter(category__isnull=False).count()
        
        print(f"\n📊 Final counts:")
        print(f"  Total categories: {total_categories}")
        print(f"  Total challenges: {total_challenges}")
        print(f"  Challenges with categories: {challenges_with_categories}")
        
        if challenges_with_categories == total_challenges:
            print("✅ All challenges have valid category relationships")
            return True
        else:
            print("⚠️  Some challenges have missing category relationships")
            return False
            
    except Exception as e:
        print(f"❌ Error reading challenges file: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_challenges_import()
    if success:
        print("\n🎉 Challenges import fixed successfully!")
    else:
        print("\n❌ Challenges import fix failed")
    sys.exit(0 if success else 1)
