#!/usr/bin/env python
"""
Complete script to add ALL Elden Ring challenges with proper categories
Save this as add_complete_challenges_fixed.py in your mybackend directory
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
    """Add ALL challenges with proper categories"""
    categories = create_categories()
    
    # Complete list of ALL challenges from your document
    all_challenges = [
        # General Challenges (7 total)
        {'name': 'The Salty Scrub', 'details': 'No Spirit Ashes, NPC Summons, or Multiplayer/Cooperative Summons can ever be used (This challenge should be implied/inherent in any and all challenge runs, but it is listed here to be included in the Grand Compendium)', 'difficulty': 'Easy', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Off The Sauce', 'details': 'You cannot ever drink from/use the Flask of Wondrous Physick', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Talisman Teetotaler', 'details': 'No Talismans can ever be equipped', 'difficulty': 'Hard', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Daring Disrobement', 'details': 'You cannot wear/equip any type of armor', 'difficulty': 'Hard', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Intrepid Infantry', 'details': 'You cannot ever mount or ride Torrent in combat (you can still mount and ride him to traverse the overworld, explore, jump, etc., but you cannot use him in any fights)', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Great Rune Restriction', 'details': 'You cannot activate, equip, or use any Great Runes (Rennala\'s Great Rune, as a passive, is allowed)', 'difficulty': 'Medium', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Lay of The Land', 'details': 'You cannot pick up/acquire any Map Fragments', 'difficulty': 'Easy', 'category': 'General Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Basic Weaponry Challenges (27 total)
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
        
        # Advanced Weaponry Challenges (9 total)
        {'name': 'Master of Magic', 'details': 'You can only use weapons and Spells that deal Magic damage.', 'difficulty': 'Medium', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Lightning Lord', 'details': 'You can only use weapons and Spells that deal Lightning damage.', 'difficulty': 'Medium', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Habitué of Heat', 'details': 'You can only use weapons and Spells that deal Fire damage.', 'difficulty': 'Medium', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Sacred Soldier', 'details': 'You can only use weapons and Spells that deal Holy damage.', 'difficulty': 'Medium', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Madness Mukbang', 'details': 'You can only use weapons and Spells that inflict Madness.', 'difficulty': 'Hard', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Ashen Aggression', 'details': 'You can only deal damage by using Weapon Skills/Ashes of War.', 'difficulty': 'Hard', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Original Flavor', 'details': 'You cannot modify any weapon with Ashes of War or change any weapon\'s Affinity (any weapon\'s normal/base Weapon Skill can still be used)', 'difficulty': 'Medium', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Substance Over Style', 'details': 'No Weapon Skills/Ashes of War can ever be used', 'difficulty': 'Hard', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Tool Temerity', 'details': 'You can only deal damage with Tools', 'difficulty': 'Hard', 'category': 'Advanced Weaponry Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Advanced Spell Challenges (21 total)
        {'name': 'Mage of Convenience', 'details': 'The only spells you can cast are Glintstone Sorceries.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Black Arts of the Blade', 'details': 'The only spells you can cast are Carian Sorceries.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Withering Witchcraft', 'details': 'The only spells you can cast are Servants of Rot Incantations and Saint of the Bud Incantations.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Crepuscular Casting', 'details': 'The only spells you can cast are Night Sorceries.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Fancy the Necromancy', 'details': 'The only spells you can cast are Death Sorceries.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Gravitation Invocation', 'details': 'The only spells you can cast are Gravity Sorceries.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Charms of the Cold Coven', 'details': 'The only spells you can cast are Snow Witch Sorceries and Full Moon Sorceries.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Spells of the Stonemen', 'details': 'The only spells you can cast are Claymen Sorceries and Crystalian Sorceries.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Conflagration Conjuring', 'details': 'The only spells you can cast are Magma Sorceries, Fire Monk Incantations, Fire Giant Incantations, and Messmer Fire Incantations.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Hemo-Hocus-Pocus', 'details': 'The only spells you can cast are Aberrant Sorceries and Blood Incantations.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Draconic Domination', 'details': 'The only spells you can cast are Dragon Communion Incantations.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Thaumaturge of Thunder', 'details': 'The only spells you can cast are Dragon Cult Incantations.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Wild Wizardry', 'details': 'The only spells you can cast are Bestial Incantations.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Teachings of the Trees', 'details': 'The only spells you can cast are Erdtree Incantations and Scadutree Sorceries.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': True, 'is_combination': False},
        {'name': 'Follower of the Fingers', 'details': 'The only spells you can cast are Two Fingers Incantations and Finger Sorceries.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Golden Boy', 'details': 'The only spells you can cast are Golden Order Incantations.', 'difficulty': 'Medium', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Incantations of Insanity', 'details': 'The only spells you can cast are Frenzied Flame Incantations.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'By the Skin of the Gods', 'details': 'The only spells you can cast are Godskin Apostle Incantations.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Occultism of Oblivion', 'details': 'The only spells you can cast are Primeval Sorceries.', 'difficulty': 'Hard', 'category': 'Advanced Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Magic of the Missing', 'details': 'The only spells you can cast are those not part of a great spell family: Loretta\'s Sorceries, Spiral Incantations, Placidusax\'s Ruin, Light of Miquella, Divine Beast Tornado, and Divine Bird Feathers', 'difficulty': 'Extreme', 'category': 'Advanced Spell Challenges', 'is_dlc': True, 'is_combination': False},
        
        # Extreme Weaponry/Spell Challenges (6 total)
        {'name': 'Arsenal Aesthete', 'details': 'Each time you acquire a new weapon, you must immediately equip it and only use that weapon (until you find/acquire another new weapon, and so on). You cannot use any of the weapons you previously used again; once it is replaced by a new weapon, it is gone.', 'difficulty': 'Hard', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Magic Maven', 'details': 'Each time you acquire a new Sorcery or Incantation, you must permanently retire 1 Sorcery or Incantation that is already in your inventory (it can never be used again in that playthrough). This challenge begins once you have 3 Spells/Incantations in your inventory.', 'difficulty': 'Hard', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Night Gaol Spelunking', 'details': 'Each and every time you defeat a Legend or Shardbearer, before proceeding to the next Legend or Shardbearer, you must first defeat 2 of the following 3 (your choice each time): A Night Boss, An Evergaol Boss, A Cave/Catacombs/Hero\'s Grave Boss', 'difficulty': 'Hard', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Wheel', 'details': 'If you die three times in a row while using the same weapon, you must immediately Discard that weapon, thereby losing it forever. (Thus, either change up your weapons consistently, or risk losing them)', 'difficulty': 'Hard', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Magic Wheel', 'details': 'If you die three times in a row while using the same Sorceries/Incantations, you must immediately Discard the Sorcery or Incantation that you last used, thereby losing it forever. (Thus, either change up your magic consistently, or risk losing your go-to, favorite spells)', 'difficulty': 'Hard', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Boss and Toss', 'details': 'Each and every time you defeat a Great Enemy, Legend, or Shardbearer, you must Discard ALL of the weapons/shields you used to beat them. If you used magic, you must also Discard ALL of the Sorceries/Incantations you used to beat them (you can keep all Staffs/Seals).', 'difficulty': 'Extreme', 'category': 'Extreme Weaponry/Spell Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Status Challenges (8 total)
        {'name': 'QuikClot', 'details': 'You cannot inflict Hemorrhage/Blood Loss on any enemy', 'difficulty': 'Medium', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Warm Heart', 'details': 'You cannot inflict Frostbite on any enemy', 'difficulty': 'Medium', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Antidote Inherent', 'details': 'You cannot inflict Poison on any enemy', 'difficulty': 'Medium', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Putrefaction Preventative', 'details': 'You cannot inflict Scarlet Rot on any enemy', 'difficulty': 'Medium', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Emissary of Insomnia', 'details': 'You cannot inflict Sleep on any enemy', 'difficulty': 'Easy', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Panacea Playthrough', 'details': 'No status effects of any kind can be inflicted on any enemy', 'difficulty': 'Hard', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': '100% Organic', 'details': 'No Spells or Incantations can be used to remove/cure status ailments (consumables only!)', 'difficulty': 'Medium', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Bugchaser', 'details': 'You cannot ever remove/cure any status ailment (You must heal through it and let it run out!)', 'difficulty': 'Hard', 'category': 'Status Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Crafting and Item Challenges (6 total)
        {'name': 'Living Off The Land', 'details': 'The only damage-inflicting things you can use are craftable items (pots, perfumes, craftable arrows, darts, etc.) If it\'s not craftable/in a cookbook, it CANNOT be used to deal damage. Thus, Greases cannot be used, as any weapon they are applied to deals damage by itself.', 'difficulty': 'Hard', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Apeshit Assault', 'details': 'The only damage-inflicting things you can use are throwables: pots, throwing daggers, fan daggers, kukri, poisoned stones and stone clumps, explosive stones and stone clumps, gravity stone chunks and fans, darts of all types, dragon communion harpoons, etc.', 'difficulty': 'Hard', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Scavenger', 'details': 'You cannot buy anything from anyone (or trade a Remembrance for anything)', 'difficulty': 'Medium', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Rune Ruin', 'details': 'You cannot gain Runes by using any consumable Runes (this includes Remembrances)', 'difficulty': 'Medium', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Fastest Draw in The Lands Between', 'details': 'You can only use a Grease if it\'s a Drawstring Grease', 'difficulty': 'Easy', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Hygienic Hero', 'details': 'You cannot use any Greases of any type', 'difficulty': 'Easy', 'category': 'Crafting and Item Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Healing and FP Recovery Challenges (12 total)
        {'name': 'Magic Mending', 'details': 'You can only heal using Incantations', 'difficulty': 'Medium', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Rejuvenating Rocks', 'details': 'You can only heal using Warming Stones, Frenzyflame Stones, and/or Sunwarmth Stones', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Raw Remedy', 'details': 'You can only heal using Raw Meat Dumplings', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Physick Fixer-Upper', 'details': 'You can only heal using the Flask of Wondrous Physick', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Critical Convalescence', 'details': 'You can only heal through Critical Hits (with Assassin\'s Crimson Dagger equipped)', 'difficulty': 'Extreme', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Isai', 'details': 'You cannot ever heal in any way (except as noted below)', 'difficulty': 'Extreme', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'No Need for Golden Seed', 'details': 'You cannot ever upgrade your Crimson and Cerulean Flasks using Golden Seeds', 'difficulty': 'Medium', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'No Tears, No Fears', 'details': 'You cannot ever upgrade your Crimson and Cerulean Flasks using Sacred Tears', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Mana From The Heavens', 'details': 'You can only recover FP by using Starlight Shards', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Spell Sprig', 'details': 'You can only recover FP by using Lulling Branches', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Focus Fighter', 'details': 'You can only recover FP by using the Assassin\'s Cerulean Dagger, the Ancestral Spirit\'s Horn, the Sacrificial Axe, and the Sword of Milos', 'difficulty': 'Hard', 'category': 'Healing and FP Recovery Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Level/Stats Challenges (6 total)
        {'name': 'Vigor Vexation', 'details': 'You cannot increase your Vigor level higher than 30', 'difficulty': 'Medium', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Fettered Focus', 'details': 'You cannot increase your Mind higher than 25', 'difficulty': 'Medium', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Stymied Stamina', 'details': 'You cannot increase your Endurance higher than 20', 'difficulty': 'Medium', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Hellish Hundred', 'details': 'You cannot increase your total level above 99 (you cannot get to level 100)', 'difficulty': 'Hard', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Thin Crust', 'details': 'You must always maintain a Light Equip Load', 'difficulty': 'Medium', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        {'name': 'Deep Dish', 'details': 'As soon as possible, you must achieve and always maintain a Heavy Equip Load', 'difficulty': 'Hard', 'category': 'Level/Stats Challenges', 'is_dlc': False, 'is_combination': False},
        
        # Challenges for the Brave or Insane (15 total)
        {'name': 'Soul Simplicity', 'details': 'You cannot increase your player level (you must always stay at Level 1)', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Scadutree Simplicity', 'details': 'You cannot use Scadutree Fragments to increase your Scadutree Blessing level.', 'difficulty': 'Hard', 'category': 'Challenges for the Brave or Insane', 'is_dlc': True, 'is_combination': False},
        {'name': 'Tactical Trek', 'details': 'You cannot ever mount or ride Torrent.', 'difficulty': 'Hard', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Expert Evasion', 'details': 'You cannot ever dodge/roll.', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Blunt Instrument', 'details': 'You cannot ever upgrade any weapons/shields using Smithing Stones/Somber Smithing Stones.', 'difficulty': 'Hard', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'The Waver', 'details': 'You can only ever have 1 hand equipped with/holding a weapon/shield/etc. (One hand must ALWAYS be empty, free to "wave" at enemies. You cannot two-hand a weapon, either!)', 'difficulty': 'Hard', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'How Can She Slap?', 'details': 'You cannot deal damage with anything other than your empty hands: no weapons, spells, throwables, or anything other than empty hands can be used to deal damage', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Globetrotter', 'details': 'You cannot ever warp using Sites of Grace (unless absolutely necessary, i.e. to get to Farum Azula or the Roundtable Hold and back)', 'difficulty': 'Hard', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Amnesiac', 'details': 'You cannot acquire any Memory Stones or equip the Moon of Nokstella', 'difficulty': 'Medium', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Three Strikes', 'details': 'If you die 3 times to the same Boss, regardless of its status/class, it\'s game over. You must delete that character and restart the challenge. (3 lives/attempts per Boss. Thus, dying twice to an optional boss is acceptable, but you might want to walk away or consider if the reward is worth it to risk a third, run-ending death!)', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': '1UP', 'details': 'You start with 1 Extra Life, and each time you defeat a Great Enemy, Legend, or Shardbearer you get another Extra Life. Each time you die, you lose a life. If you run out of lives, it\'s game over. You must delete that character and restart the challenge. (Thus, if you die twice before ever defeating a Great Enemy, Legend, or Shardbearer, you ran out of lives, and it\'s GG. You do NOT get an Extra Life for defeating an Enemy class boss. The mandatory death that occurs at the very beginning of the game against/after the Grafted Scion does not count as a death)', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        {'name': 'Git Gud', 'details': 'If you die even once, you\'re done. You must delete that character and start over. (The mandatory death that occurs at the very beginning of the game against/after the Grafted Scion does not count)', 'difficulty': 'Extreme', 'category': 'Challenges for the Brave or Insane', 'is_dlc': False, 'is_combination': False},
        
        # Challenge Combinations (16 total)
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
    
    print(f"\nSummary:")
    print(f"Added: {added_count} challenges")
    print(f"Skipped: {skipped_count} challenges (already exist)")
    print(f"Total challenges in document: {len(all_challenges)}")
    
    # Show breakdown by category
    print(f"\nBreakdown by category:")
    category_counts = {}
    for challenge in all_challenges:
        cat = challenge['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in category_counts.items():
        print(f"  {cat}: {count} challenges")

if __name__ == '__main__':
    print("Adding ALL challenges to the database with proper categories...")
    add_all_challenges()
    print("Done!")