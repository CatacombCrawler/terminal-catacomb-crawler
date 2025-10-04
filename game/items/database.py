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
            'bronze_sword': {
            'name': 'Bronze Sword',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A well-crafted bronze blade with a sharp edge and balanced weight.',
            'symbol': '/',
            'color': 'bright_yellow',
            'stats': {
                'attack': 17,
                'defense': 0,
                'speed': -6,
                'hp': 0
            },
            'requirements': {
                'level': 2,
                'strength': 12
            }
        },
        'iron_bow': {
            'name': 'Iron Bow',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A sturdy bow made from iron with reinforced limbs for increased power.',
            'symbol': '}',
            'color': 'cyan',
            'stats': {
                'attack': 8,
                'defense': 0,
                'speed': 15,
                'hp': 0
            },
            'requirements': {
                'level': 3,
                'dexterity': 14
            }
        },
        'silver_bow': {
            'name': 'Silver Bow',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['rare']['name'],
            'starting_item': False,
            'description': 'An elegant bow forged from pure silver, gleaming with otherworldly beauty.',
            'symbol': '}',
            'color': 'yellow',
            'stats': {
                'attack': 12,
                'defense': 0,
                'speed': 18,
                'hp': 0
            },
            'requirements': {
                'level': 5,
                'dexterity': 16
            }
        },
        'master_sword': {
            'name': 'Master Sword',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['legendary']['name'],
            'starting_item': False,
            'description': 'A legendary blade wielded by a great hero, its steel gleams with ancient power.',
            'symbol': '/',
            'color': 'magenta',
            'stats': {
                'attack': 25,
                'defense': 0,
                'speed': -6,
                'hp': 0
            },
            'requirements': {
                'level': 10,
                'strength': 18
            }
        },
        'artemis_bow': {
            'name': 'Artemis Bow',
            'type': ITEM_TYPES['weapon']['name'],
            'quality': ITEM_QUALITIES['legendary']['name'],
            'starting_item': False,
            'description': 'A divine bow blessed by the goddess Artemis, arrows shot from it never miss their mark.',
            'symbol': '}',
            'color': 'magenta',
            'stats': {
                'attack': 24,
                'defense': 0,
                'speed': 18,
                'hp': 0
            },
            'requirements': {
                'level': 10,
                'dexterity': 20
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
        },'iron_chest': {
            'name': 'Iron Chestplate',
            'type': ITEM_TYPES['armor']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A well-forged iron chestplate that provides reliable protection in battle.',
            'symbol': '[',
            'color': 'cyan',
            'stats': {
                'attack': 0,
                'defense': 25,
                'speed': -4,
                'hp': 45
            },
            'requirements': {
                'level': 3,
                'strength': 8
            }
        },
        'plate_armor': {
            'name': 'Plate Armor',
            'type': ITEM_TYPES['armor']['name'],
            'quality': ITEM_QUALITIES['rare']['name'],
            'starting_item': False,
            'description': 'Masterfully crafted full plate armor that turns aside even the mightiest blows.',
            'symbol': '[',
            'color': 'yellow',
            'stats': {
                'attack': 0,
                'defense': 35,
                'speed': -6,
                'hp': 60
            },
            'requirements': {
                'level': 5,
                'strength': 10
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
        'kite_shield': {
            'name': 'Kite Shield',
            'type': ITEM_TYPES['shield']['name'],
            'quality': ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A large teardrop-shaped shield that provides excellent protection from head to knee.',
            'symbol': 'K',
            'color': 'cyan',
            'stats': {
                'attack': 0,
                'defense': 20,
                'speed': -1,
                'hp': 20
            },
            'requirements': {
                'level': 3,
                'strength': 5
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
        },
        'greater_health_potion': {
            'name': 'Greater Health Potion',
            'type': ITEM_TYPES['consumable']['name'],
            'quality':  ITEM_QUALITIES['normal']['name'],
            'starting_item': False,
            'description': 'A large red liquid that restores vitality.',
            'symbol': '!',
            'color': 'red',
            'stats': {
                'attack': 0,
                'defense': 0,
                'speed': 0,
                'hp': 0
            },
            'effect': {
                'type':  ITEM_TYPES['consumable']['effect']['heal'],
                'amount': 50
            },
            'requirements': {
                'level': 3
            }
        }
    }
}

