#!/usr/bin/env python
"""
Complete script to add ALL challenges from the document
Save this as add_complete_challenges.py in your mybackend directory
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import Challenge, Challenge_Category

def create_categories():
    categories_data = [
        "General Challenges",
        "Basic Weaponry Challenges", 
        "Advanced Weaponry Challenges",
        "Advanced Spell Challenges",
        "Extreme Weaponry/Spell Challenges",
        "Status Challenges",
        "Crafting and Item Challenges", 
        "Healing and FP Recovery Challenges",
        "Level/Stats Challenges",
        "Challenges for the Brave or Insane",
        "Challenge Combinations"
    ]
    
    created_categories = {}
    for cat_name in categories_data:
        category, created = Challenge_Category.objects.get_or_create(name=cat_name)
        created_categories[cat_name] = category
        if created:
            print(f"Created category: {cat_name}")
    
    return created_categories

def add_all_challenges():
    categories = create_categories()
    
    # ALL CHALLENGES DATA
    all_challenges = [
        # General Challenges
        {'name': 'The Salty Scrub', 'details': 'No Spirit Ashes, NPC Summons, or Multiplayer/Cooperative Summons can ever be used (This challenge should be implied/inherent in any and all challenge runs, but it is listed here to be included in the Grand Compendium)', 'difficulty': 'Easy', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Off The Sauce', 'details': 'You cannot ever drink from/use the Flask of Wondrous Physick', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Talisman Teetotaler', 'details': 'No Talismans can ever be equipped', 'difficulty': 'Hard', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Daring Disrobement', 'details': 'You cannot wear/equip any type of armor', 'difficulty': 'Hard', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Intrepid Infantry', 'details': 'You cannot ever mount or ride Torrent in combat (you can still mount and ride him to traverse the overworld, explore, jump, etc., but you cannot use him in any fights)', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Great Rune Restriction', 'details': 'You cannot activate, equip, or use any Great Runes (Rennala\'s Great Rune, as a passive, is allowed)', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Lay of The Land', 'details': 'You cannot pick up/acquire any Map Fragments', 'difficulty': 'Easy', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Basic Weaponry Challenges  
        {'name': 'Pride of Legolas', 'details': 'You can only equip and deal damage with Light Bows, Bows, and Greatbows.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Dag Swag', 'details': 'You can only equip and deal damage with Daggers.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Indiana Jones', 'details': 'You can only equip and deal damage with Whips.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Senpou Style', 'details': 'You can only equip and deal damage with Hand-to-Hand Arts.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Strength Through Length', 'details': 'You can only equip and deal damage with Spears, Great Spears, and Halberds.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Grim Gauntlet', 'details': 'You can only equip and deal damage with Reapers.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Wolverine', 'details': 'You can only equip and deal damage with Claws.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Proficiency in Pungency', 'details': 'You can only equip and deal damage with Perfume Bottles.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'The Lumberjack', 'details': 'You can only equip and deal damage with Axes and Greataxes.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Better Call Maul', 'details': 'You can only equip and deal damage with Twinblades.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Peyronie Power', 'details': 'You can only equip and deal damage with Curved Swords and Curved Greatswords.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Witch-king of Angmar', 'details': 'You can only equip and deal damage with Flails.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Backhanded Compliments', 'details': 'You can only equip and deal damage with Backhand Blades.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'The Otaku', 'details': 'You can only equip and deal damage with Katanas.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Great Otaku', 'details': 'You can only equip and deal damage with Great Katanas.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Inigo Montoya', 'details': 'You can only equip and deal damage with Thrusting Swords & Heavy Thrusting Swords.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Whac-A-Mole', 'details': 'You can only equip and deal damage with Hammers and Great Hammers.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'King Arthur', 'details': 'You can only equip and deal damage with Straight Swords, Light Greatswords, and Greatswords.', 'difficulty': 'Easy', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Big Boy Bonanza', 'details': 'You can only equip and deal damage with Colossal Weapons and Colossal Swords.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Beast Mode', 'details': 'You can only equip and deal damage with Beast Claws.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Throw Show', 'details': 'You can only equip and deal damage with Throwing Blades.', 'difficulty': 'Hard', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'The Balboa', 'details': 'Fists only, you cannot equip or deal damage with anything else.', 'difficulty': 'Extreme', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Flame Freak', 'details': 'Torches only, you cannot equip or deal damage with anything else.', 'difficulty': 'Extreme', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Wall', 'details': 'Shields only, you cannot equip or deal damage with anything else.', 'difficulty': 'Extreme', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Wall Redux', 'details': 'Thrusting Shields only, you cannot equip or deal damage with anything else.', 'difficulty': 'Extreme', 'category': 'Basic Weaponry Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Spellin\' Like a Felon', 'details': 'You can only equip Staffs or Seals and can only deal damage using Sorceries and Incantations.', 'difficulty': 'Medium', 'category': 'Basic Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Challenge Combinations
        {'name': 'Way of the Blade', 'details': 'King Arthur + Peyronie Power + Boss and Toss', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Glass Cannon', 'details': 'Vigor Vexation + Spellin\' Like a Felon + The Magic Wheel', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Artisanal Armaments', 'details': 'Living Off The Land + Rejuvenating Rocks + 100% Organic', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Thunderstruck', 'details': 'Three Strikes + Lightning Lord + Rune Ruin', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Raw Roid Rager', 'details': 'Big Boy Bonanza + Raw Remedy + Critical Convalescence', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Faith Flinger', 'details': 'Apeshit Assault + Magic Mending', 'difficulty': 'Medium', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Declaration of Dominance', 'details': 'The Balboa + Great Rune Restriction + Panacea Playthrough', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'The Angry Villager', 'details': 'Flame Freak + The Grim Gauntlet + Thin Crust + Stymied Stamina', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'On a Knife\'s Edge', 'details': 'Dag Swag + 1UP + The Hellish Hundred', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Initiate Beast Mode', 'details': 'Wild Wizardry + Wolverine + Three Strikes', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Flavors of Fire', 'details': 'Habitué of Heat + Arsenal Aesthete + Magic Maven', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Stagger to Survive', 'details': 'Focus Fighter + Critical Convalescence + Fettered Focus + Panacea Playthrough', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Come At Me, Bro', 'details': 'The Wall + Deep Dish', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'The Spice of Life', 'details': 'Arsenal Aesthete + Magic Maven + Night Gaol Spelunking', 'difficulty': 'Hard', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
        {'name': 'Odiferous Odyssey', 'details': 'Proficiency in Pungency + Bugchaser + Intrepid Infantry', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': True, 'is_combination': True},
        {'name': 'Howling at the Moon', 'details': 'Madness Mukbang + Daring Disrobement + Scavenger + Bugchaser', 'difficulty': 'Extreme', 'category': 'Challenge Combinations', 'is_dlc': False, 'is_combination': True},
    ]
    
    # Add challenges to database
    added_count = 0
    skipped_count = 0
    
    for challenge_data in all_challenges:
        if Challenge.objects.filter(name=challenge_data['name']).exists():
            print(f"Already exists: {challenge_data['name']}")
            skipped_count += 1
            continue
            
        category = categories[challenge_data['category']]
        
        Challenge.objects.create(
            name=challenge_data['name'],
            details=challenge_data['details'],
            difficulty=challenge_data['difficulty'],
            category=category,
            is_dlc=challenge_data['is_dlc'],
            is_combination=challenge_data['is_combination']
        )
        
        print(f"Added: {challenge_data['name']}")
        added_count += 1
    
    print(f"\nSummary: Added {added_count}, Skipped {skipped_count}")

if __name__ == '__main__':
    add_all_challenges()