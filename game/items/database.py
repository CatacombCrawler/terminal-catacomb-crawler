"""
Items Database - All game items definitions
"""
# Quality definitions for future use
ITEM_QUALITIES = {
    'normal': {
        'name': 'Normal',
        'color': 'white',
        'stat_modifier': 1.0,
        'rarity': 0.6
    },
    'magic': {
        'name': 'Magic',
        'color': 'blue', 
        'stat_modifier': 1.2,
        'rarity': 0.25
    },
    'rare': {
        'name': 'Rare',
        'color': 'yellow',
        'stat_modifier': 1.5,
        'rarity': 0.12
    },
    'legendary': {
        'name': 'Legendary',
        'color': 'magenta',
        'stat_modifier': 2.0,
        'rarity': 0.03
    }
}

# Item type definitions
ITEM_TYPES = {
    'weapon': {
        'name': 'weapon',
        'slot': 'main_hand',
        'can_equip_multiple': False
    },
    'armor': {
        'name': 'armor',
        'slot': 'chest',
        'can_equip_multiple': False
    },
    'shield': {
        'name': 'shield',
        'slot': 'off_hand',
        'can_equip_multiple': False
    },
    'consumable': {
        'name': 'consumable',
        'slot': None,
        'can_equip_multiple': True,
        'effect': { 
            'heal': 'heal', 
            'poison': 'poison' # Future effects
        }
    }
}

# Actual items database
ITEMS = {
    'weapons': {
        'rusted_sword': {
            'name': 'Rusted Sword',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': True,
            'description': 'An old iron sword, worn by time but still sharp enough to cut.',
            'symbol': '/',
            'color': 'red',
            'stats': {
                'attack': 15,
                'defense': 0,
                'speed': -6,
                'hp': 0
            },
            'requirements': {
                'level': 1,
                'strength': 10
            }
        },
        'wooden_bow': {
            'name': 'Wooden Bow',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': True,
            'description': 'A simple bow made from sturdy oak wood.',
            'symbol': '}',
            'color': 'yellow',
            'stats': {
                'attack': 6,
                'defense': 0,
                'speed': 13,
                'hp': 0
            },
            'requirements': {
                'level': 1,
                'dexterity': 10
            }
        },
        'longbow': {
            'name': 'Longbow',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A tall bow, offering great range and punch, but slower to draw.',
            'symbol': ')',
            'color': 'yellow',
            'stats': {
                'attack': 14,
                'defense': 0,
                'speed': 10,
                'hp': 0
            },
            'requirements': {
                'level': 4,
                'dexterity': 16
            }
        }
    },
    'armor': {
        'rusted_chest': {
            'name': 'Rusted Chestplate',
            'type': ITEM_TYPES['armor']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': True,
            'description': 'Old iron chestplate that has seen better days but still offers protection.',
            'symbol': '[',
            'color': 'white',
            'stats': {
                'attack': 0,
                'defense': 20,
                'speed': -3,
                'hp': 35
            },
            'requirements': {
                'level': 1,
                'strength': 5
            }
        }
    },
    'shields': {
        'round_shield': {
            'name': 'Round Shield',
            'type': ITEM_TYPES['shield']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': True,
            'description': 'A sturdy wooden shield reinforced with iron bands.',
            'symbol': 'O',
            'color': 'blue',
            'stats': {
                'attack': 0,
                'defense': 15,
                'speed': -1,
                'hp': 15
            },
            'requirements': {
                'level': 1,
                'strength': 3
            }
        },
        'broquel': {
            'name': 'Broquel', # light off-hand shield 
            'type': ITEM_TYPES['shield']['name'],  
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': True,
            'description': 'A small round shield used to parry. Light, quick, and handy in close quarters.',
            'symbol': 'o',
            'color': 'gray',
            'stats': {
                'attack': 0,
                'defense': 10,
                'speed': 0,
                'hp': 5
            },
            'requirements': {
                'level': 1,
                'strength': 2
            }
        }
    },
    # Future expansion - non-starting items
    'potions': {
        'health_potion': {
            'name': 'Health Potion',
            'type': ITEM_TYPES['consumable']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A red liquid that restores vitality.',
            'symbol': '!',
            'color': 'red',
            'stats': {
                'attack': 0,
                'defense': 0,
                'speed': 0,
                'hp': 0
            },
            'effect': {
                'type': ITEM_TYPES['consumable']['effect']['heal'],
                'amount': 25
            },
            'requirements': {
                'level': 1
            }
        }
    }
}

