"""
Items Database - All game items definitions
"""

ITEMS = {
    'weapons': {
        'rusted_sword': {
            'name': 'Rusted Sword',
            'type': 'weapon',
            'quality': 'normal',
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
            'type': 'weapon',
            'quality': 'normal',
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
            'type': 'weapon',
            'quality': 'normal',
            'starting_item': False,
            'description': 'A Bronze Sword.',
            'symbol': '/',
            'color': 'orange',
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
        },'iron_bow': {
            'name': 'Iron Bow',
            'type': 'weapon',
            'quality': 'normal',
            'starting_item': False,
            'description': 'A sturdy bow made from iron.',
            'symbol': '}',
            'color': 'blue',
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
        },'silver_bow': {
            'name': 'Silver Bow',
            'type': 'weapon',
            'quality': 'rare',
            'starting_item': False,
            'description': 'A sturdy bow made from silver.',
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
        },'master_sword': {
            'name': 'Master Sword',
            'type': 'weapon',
            'quality': 'legendary',
            'starting_item': False,
            'description': 'A legendary sword wielded by a great hero.',
            'symbol': '/',
            'color': 'purple',
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
        },'artemis_bow': {
            'name': 'Artemis Bow',
            'type': 'weapon',
            'quality': 'legendary',
            'starting_item': False,
            'description': 'A legendary bow said to be favored by the goddess Artemis.',
            'symbol': '}',
            'color': 'purple',
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
        },
    },
    'armor': {
        'rusted_chest': {
            'name': 'Rusted Chestplate',
            'type': 'armor',
            'quality': 'normal',
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
            'type': 'armor',
            'quality': 'normal',
            'starting_item': True,
            'description': 'Iron chestplate that offers good protection.',
            'symbol': '[',
            'color': 'white',
            'stats': {
                'attack': 0,
                'defense': 20,
                'speed': -3,
                'hp': 35
            },
            'requirements': {
                'level': 3,
                'strength': 8
            }
        },'plate_armor': {
            'name': 'Plate Armor',
            'type': 'armor',
            'quality': 'rare',
            'starting_item': True,
            'description': 'Heavy plate armor that offers excellent protection.',
            'symbol': '[',
            'color': 'yellow',
            'stats': {
                'attack': 0,
                'defense': 20,
                'speed': -3,
                'hp': 35
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
            'type': 'shield',
            'quality': 'normal',
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
            'type': 'shield',
            'quality': 'normal',
            'starting_item': False,
            'description': 'A sturdy wooden shield reinforced with iron bands.',
            'symbol': 'K',
            'color': 'blue',
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
        }
    },
    # Future expansion - non-starting items
    'potions': {
        'health_potion': {
            'name': 'Health Potion',
            'type': 'consumable',
            'quality': 'normal',
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
                'type': 'heal',
                'amount': 25
            },
            'requirements': {
                'level': 1
            }
        },
        'greater_health_potion': {
            'name': 'Greater Health Potion',
            'type': 'consumable',
            'quality': 'rare',
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
                'type': 'heal',
                'amount': 50
            },
            'requirements': {
                'level': 3
            }
        }
    }
}

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
        'slot': 'main_hand',
        'can_equip_multiple': False
    },
    'armor': {
        'slot': 'chest',
        'can_equip_multiple': False
    },
    'shield': {
        'slot': 'off_hand',
        'can_equip_multiple': False
    },
    'consumable': {
        'slot': None,
        'can_equip_multiple': True
    }
}