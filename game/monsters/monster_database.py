"""
Monster Database - All game monster definitions with drop chances and attacks
"""

import random

class MonsterDatabase:
    """Central database of all monsters and related functionality"""
    
    MONSTERS = {
        'undead': {
            'skeleton': {
                'name': 'Skeleton',
                'type': 'undead',
                'symbol': 's',
                'color': 'white',
                'description': 'The animated bones of a long-dead warrior, still clinging to unlife.',
                'stats': {
                    'hp': 25,
                    'attack': 8,
                    'defense': 2,
                    'speed': 12,
                    'accuracy': 0.85,
                    'exp_reward': 15
                },
                'ai': {
                    'aggression': 0.9,
                    'detection_range': 7,
                    'intelligence': 'low'
                },
                'drop_chances': {
                    'weapons': 0.15,
                    'armor': 0.05,
                    'shields': 0.08,
                    'potions': 0.25
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Bone Strike',
                        'damage': 8,
                        'accuracy': 0.85,
                        'description': 'Strikes with bony fists',
                        'type': 'special',
                        'cooldown': 1,
                        'special_effects': None
                    },
                    {
                        'name': 'Rattling Charge',
                        'damage': 12,
                        'accuracy': 0.70,
                        'description': 'Charges forward with bones clattering',
                        'type': 'special',
                        'cooldown': 3,
                        'special_effects': {
                            'type': 'intimidate',
                            'duration': 2,
                            'effect': 'reduces_player_accuracy'
                        }
                    }
                ]
            },
            'zombie': {
                'name': 'Zombie',
                'type': 'undead',
                'symbol': 'z',
                'color': 'green',
                'description': 'A shambling corpse driven by dark magic, slow but relentless.',
                'stats': {
                    'hp': 40,
                    'attack': 12,
                    'defense': 3,
                    'speed': 6,
                    'accuracy': 0.75,
                    'exp_reward': 20
                },
                'ai': {
                    'aggression': 0.95,
                    'detection_range': 4,
                    'intelligence': 'very_low'
                },
                'drop_chances': {
                    'weapons': 0.10,
                    'armor': 0.15,
                    'shields': 0.05,
                    'potions': 0.30
                },
                'possible_drops': {
                    'armor': ['rusted_chest'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Diseased Bite',
                        'damage': 10,
                        'accuracy': 0.75,
                        'description': 'Bites with rotting teeth',
                        'type': 'special',
                        'cooldown': 2,
                        'special_effects': {
                            'type': 'poison',
                            'duration': 3,
                            'damage_per_turn': 2
                        }
                    },
                    {
                        'name': 'Zombie Slam',
                        'damage': 15,
                        'accuracy': 0.60,
                        'description': 'Slams with decaying fists',
                        'type': 'special',
                        'cooldown': 1,
                        'special_effects': None
                    }
                ]
            },
            'wraith': {
                'name': 'Wraith',
                'type': 'undead',
                'symbol': 'W',
                'color': 'cyan',
                'description': 'A spectral being that phases through reality, emanating cold dread.',
                'stats': {
                    'hp': 35,
                    'attack': 15,
                    'defense': 1,
                    'speed': 18,
                    'accuracy': 0.90,
                    'exp_reward': 35
                },
                'ai': {
                    'aggression': 0.8,
                    'detection_range': 8,
                    'intelligence': 'high'
                },
                'drop_chances': {
                    'weapons': 0.25,
                    'armor': 0.10,
                    'shields': 0.15,
                    'potions': 0.20
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Life Drain',
                        'damage': 8,
                        'accuracy': 0.90,
                        'description': 'Drains life force from the target',
                        'type': 'special',
                        'cooldown': 2,
                        'special_effects': {
                            'type': 'heal_self',
                            'amount': 4
                        }
                    },
                    {
                        'name': 'Spectral Touch',
                        'damage': 12,
                        'accuracy': 0.80,
                        'description': 'Touches with ethereal hands',
                        'type': 'special',
                        'cooldown': 1,
                        'special_effects': {
                            'type': 'phase_through_armor',
                            'duration': 1,
                            'effect': 'ignores_defense'
                        }
                    },
                    {
                        'name': 'Wail of Despair',
                        'damage': 5,
                        'accuracy': 0.95,
                        'description': 'Emits a soul-chilling wail',
                        'type': 'special',
                        'cooldown': 3,
                        'special_effects': {
                            'type': 'fear',
                            'duration': 2,
                            'effect': 'reduces_player_attack'
                        }
                    }
                ]
            }
        },
        'magic': {
            'imp': {
                'name': 'Imp',
                'type': 'magic',
                'symbol': 'i',
                'color': 'red',
                'description': 'A small demonic creature with sharp claws and a mischievous grin.',
                'stats': {
                    'hp': 20,
                    'attack': 10,
                    'defense': 1,
                    'speed': 15,
                    'accuracy': 0.85,
                    'exp_reward': 18
                },
                'ai': {
                    'aggression': 0.7,
                    'detection_range': 6,
                    'intelligence': 'medium'
                },
                'drop_chances': {
                    'weapons': 0.20,
                    'armor': 0.05,
                    'shields': 0.10,
                    'potions': 0.35
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Fire Bolt',
                        'damage': 12,
                        'accuracy': 0.85,
                        'description': 'Hurls a small ball of fire',
                        'type': 'special',
                        'cooldown': 2,
                        'special_effects': {
                            'type': 'burn',
                            'duration': 2,
                            'damage_per_turn': 3
                        }
                    },
                    {
                        'name': 'Teleport Strike',
                        'damage': 8,
                        'accuracy': 0.95,
                        'description': 'Teleports behind target and strikes',
                        'type': 'special',
                        'cooldown': 1,
                        'special_effects': {
                            'type': 'surprise_attack',
                            'effect': 'cannot_be_blocked'
                        }
                    }
                ]
            },
            'wizard': {
                'name': 'Dark Wizard',
                'type': 'magic',
                'symbol': 'W',
                'color': 'magenta',
                'description': 'A robed figure wielding forbidden magic and ancient knowledge.',
                'stats': {
                    'hp': 30,
                    'attack': 18,
                    'defense': 2,
                    'speed': 10,
                    'accuracy': 0.80,
                    'exp_reward': 40
                },
                'ai': {
                    'aggression': 0.6,
                    'detection_range': 9,
                    'intelligence': 'very_high'
                },
                'multi_attack': {
                    'chance': 0.3,
                    'max_attacks': 2
                },
                'drop_chances': {
                    'weapons': 0.30,
                    'armor': 0.20,
                    'shields': 0.15,
                    'potions': 0.40
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Magic Missile',
                        'damage': 15,
                        'accuracy': 0.95,
                        'description': 'Launches guided magical projectiles',

                        'type': 'special',

                        'cooldown': 1,
                        'special_effects': None
                    },
                    {
                        'name': 'Armor Break',
                        'damage': 8,
                        'accuracy': 0.80,
                        'description': 'Casts a spell to weaken armor',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'armor_break',
                            'duration': 4,
                            'effect': 'reduces_defense_by_half'
                        }
                    },
                    {
                        'name': 'Lightning Strike',
                        'damage': 20,
                        'accuracy': 0.70,
                        'description': 'Calls down a bolt of lightning',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'stun',
                            'duration': 1,
                            'effect': 'skip_next_turn'
                        }
                    }
                ]
            },
            'elemental': {
                'name': 'Fire Elemental',
                'type': 'magic',
                'symbol': 'E',
                'color': 'red',
                'description': 'A being of pure flame, crackling with elemental energy.',
                'stats': {
                    'hp': 45,
                    'attack': 16,
                    'defense': 3,
                    'speed': 12,
                    'accuracy': 0.80,

                    'exp_reward': 45
                },
                'ai': {
                    'aggression': 0.85,
                    'detection_range': 7,
                    'intelligence': 'medium'
                },
                'drop_chances': {
                    'weapons': 0.25,
                    'armor': 0.30,
                    'shields': 0.20,
                    'potions': 0.25
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Flame Burst',
                        'damage': 14,
                        'accuracy': 0.85,
                        'description': 'Erupts in a burst of flames',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'burn',
                            'duration': 3,
                            'damage_per_turn': 4
                        }
                    },
                    {
                        'name': 'Heat Wave',
                        'damage': 10,
                        'accuracy': 0.90,
                        'description': 'Radiates intense heat',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'exhaustion',
                            'duration': 2,
                            'effect': 'reduces_speed'
                        }
                    },
                    {
                        'name': 'Inferno',
                        'damage': 22,
                        'accuracy': 0.60,
                        'description': 'Creates a devastating inferno',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'burn',
                            'duration': 4,
                            'damage_per_turn': 5
                        }
                    }
                ]
            }
        },
        'flying': {
            'bat': {
                'name': 'Giant Bat',
                'type': 'flying',
                'symbol': 'b',
                'color': 'black',
                'description': 'A massive bat with leathery wings and razor-sharp fangs.',
                'stats': {
                    'hp': 18,
                    'attack': 7,
                    'defense': 1,
                    'speed': 20,
                    'accuracy': 0.80,

                    'exp_reward': 12
                },
                'ai': {
                    'aggression': 0.8,
                    'detection_range': 8,
                    'intelligence': 'low'
                },
                'drop_chances': {
                    'weapons': 0.08,
                    'armor': 0.03,
                    'shields': 0.05,
                    'potions': 0.20
                },
                'possible_drops': {
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Swoop Attack',
                        'damage': 6,
                        'accuracy': 0.90,
                        'description': 'Swoops down from above',

                        'type': 'special',

                        'cooldown': 1,
                        'special_effects': None
                    },
                    {
                        'name': 'Echolocation Screech',
                        'damage': 3,
                        'accuracy': 0.95,
                        'description': 'Emits a disorienting screech',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'disorient',
                            'duration': 1,
                            'effect': 'reduces_accuracy'
                        }
                    }
                ]
            },
            'harpy': {
                'name': 'Harpy',
                'type': 'flying',
                'symbol': 'H',
                'color': 'yellow',
                'description': 'A winged creature with the torso of a woman and talons of a bird.',
                'stats': {
                    'hp': 28,
                    'attack': 11,
                    'defense': 2,
                    'speed': 16,
                    'accuracy': 0.80,

                    'exp_reward': 25
                },
                'ai': {
                    'aggression': 0.75,
                    'detection_range': 10,
                    'intelligence': 'medium'
                },
                'drop_chances': {
                    'weapons': 0.18,
                    'armor': 0.12,
                    'shields': 0.08,
                    'potions': 0.22
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Talon Strike',
                        'damage': 10,
                        'accuracy': 0.85,
                        'description': 'Rakes with sharp talons',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'bleed',
                            'duration': 2,
                            'damage_per_turn': 2
                        }
                    },
                    {
                        'name': 'Siren Song',
                        'damage': 0,
                        'accuracy': 0.80,
                        'description': 'Sings an enchanting but dangerous song',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'charm',
                            'duration': 1,
                            'effect': 'skip_turn'
                        }
                    },
                    {
                        'name': 'Dive Bomb',
                        'damage': 15,
                        'accuracy': 0.75,
                        'description': 'Dives from high altitude',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockdown',
                            'duration': 1,
                            'effect': 'reduces_defense'
                        }
                    }
                ]
            },
            'dragon': {
                'name': 'Young Dragon',
                'type': 'flying',
                'symbol': 'D',
                'color': 'red',
                'description': 'A mighty dragon, still young but already fearsome with scales and flame.',
                'stats': {
                    'hp': 80,
                    'attack': 25,
                    'defense': 8,
                    'speed': 14,
                    'accuracy': 0.80,
                    'exp_reward': 100
                },
                'ai': {
                    'aggression': 0.9,
                    'detection_range': 12,
                    'intelligence': 'very_high'
                },
                'multi_attack': {
                    'chance': 0.4,
                    'max_attacks': 3
                },
                'drop_chances': {
                    'weapons': 0.40,
                    'armor': 0.35,
                    'shields': 0.30,
                    'potions': 0.50
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Fire Breath',
                        'damage': 20,
                        'accuracy': 0.85,
                        'description': 'Breathes a cone of intense flame',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'burn',
                            'duration': 4,
                            'damage_per_turn': 5
                        }
                    },
                    {
                        'name': 'Claw Slash',
                        'damage': 18,
                        'accuracy': 0.90,
                        'description': 'Slashes with massive claws',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'deep_wound',
                            'duration': 3,
                            'damage_per_turn': 3
                        }
                    },
                    {
                        'name': 'Wing Buffet',
                        'damage': 12,
                        'accuracy': 0.95,
                        'description': 'Beats wings to create powerful winds',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockback',
                            'duration': 1,
                            'effect': 'reduces_accuracy_and_speed'
                        }
                    },
                    {
                        'name': 'Tail Whip',
                        'damage': 16,
                        'accuracy': 0.80,
                        'description': 'Swipes with armored tail',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'stun',
                            'duration': 1,
                            'effect': 'skip_next_turn'
                        }
                    },
                    {
                        'name': 'Dragon Roar',
                        'damage': 8,
                        'accuracy': 0.95,
                        'description': 'Lets out a terrifying roar',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'fear',
                            'duration': 3,
                            'effect': 'reduces_all_stats'
                        }
                    }
                ]
            }
        },
        'insects': {
            'spider': {
                'name': 'Giant Spider',
                'type': 'insects',
                'symbol': 'x',
                'color': 'black',
                'description': 'A massive arachnid with venomous fangs and sticky webs.',
                'stats': {
                    'hp': 22,
                    'attack': 9,
                    'defense': 3,
                    'speed': 14,
                    'accuracy': 0.80,

                    'exp_reward': 16
                },
                'ai': {
                    'aggression': 0.85,
                    'detection_range': 6,
                    'intelligence': 'low'
                },
                'drop_chances': {
                    'weapons': 0.12,
                    'armor': 0.08,
                    'shields': 0.06,
                    'potions': 0.18
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Venomous Bite',
                        'damage': 8,
                        'accuracy': 0.85,
                        'description': 'Bites with poison-dripping fangs',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'poison',
                            'duration': 4,
                            'damage_per_turn': 3
                        }
                    },
                    {
                        'name': 'Web Trap',
                        'damage': 2,
                        'accuracy': 0.90,
                        'description': 'Shoots sticky web to entangle',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'entangle',
                            'duration': 2,
                            'effect': 'cannot_move_or_dodge'
                        }
                    }
                ]
            },
            'mantis': {
                'name': 'Praying Mantis',
                'type': 'insects',
                'symbol': 'M',
                'color': 'green',
                'description': 'A towering insect predator with scythe-like forearms.',
                'stats': {
                    'hp': 35,
                    'attack': 14,
                    'defense': 4,
                    'speed': 16,
                    'accuracy': 0.80,

                    'exp_reward': 28
                },
                'ai': {
                    'aggression': 0.9,
                    'detection_range': 8,
                    'intelligence': 'medium'
                },
                'multi_attack': {
                    'chance': 0.35,
                    'max_attacks': 2
                },
                'drop_chances': {
                    'weapons': 0.22,
                    'armor': 0.15,
                    'shields': 0.10,
                    'potions': 0.20
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Scythe Strike',
                        'damage': 12,
                        'accuracy': 0.90,
                        'description': 'Slashes with razor-sharp forearms',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'precise_cut',
                            'effect': 'ignores_partial_armor'
                        }
                    },
                    {
                        'name': 'Lightning Fast Strike',
                        'damage': 16,
                        'accuracy': 0.75,
                        'description': 'Strikes with incredible speed',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'speed_attack',
                            'effect': 'cannot_be_blocked'
                        }
                    },
                    {
                        'name': 'Predator Gaze',
                        'damage': 0,
                        'accuracy': 0.85,
                        'description': 'Stares with unblinking compound eyes',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'intimidate',
                            'duration': 2,
                            'effect': 'reduces_player_attack'
                        }
                    }
                ]
            },
            'beetle': {
                'name': 'Armored Beetle',
                'type': 'insects',
                'symbol': 'B',
                'color': 'brown',
                'description': 'A heavily armored insect with a thick carapace and powerful mandibles.',
                'stats': {
                    'hp': 50,
                    'attack': 10,
                    'defense': 7,
                    'speed': 8,
                    'accuracy': 0.80,

                    'exp_reward': 22
                },
                'ai': {
                    'aggression': 0.7,
                    'detection_range': 5,
                    'intelligence': 'low'
                },
                'drop_chances': {
                    'weapons': 0.10,
                    'armor': 0.25,
                    'shields': 0.20,
                    'potions': 0.15
                },
                'possible_drops': {
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Mandible Crush',
                        'damage': 11,
                        'accuracy': 0.80,
                        'description': 'Crushes with powerful jaws',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'armor_damage',
                            'duration': 2,
                            'effect': 'reduces_armor_effectiveness'
                        }
                    },
                    {
                        'name': 'Charge Attack',
                        'damage': 14,
                        'accuracy': 0.70,
                        'description': 'Charges forward with horn lowered',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockdown',
                            'duration': 1,
                            'effect': 'reduces_defense'
                        }
                    }
                ]
            }
        },
        'elemental': {
            'earth_golem': {
                'name': 'Earth Golem',
                'type': 'elemental',
                'symbol': 'G',
                'color': 'brown',
                'description': 'A massive construct of stone and earth, slow but incredibly durable.',
                'stats': {
                    'hp': 70,
                    'attack': 18,
                    'defense': 10,
                    'speed': 6,
                    'accuracy': 0.80,

                    'exp_reward': 50
                },
                'ai': {
                    'aggression': 0.6,
                    'detection_range': 4,
                    'intelligence': 'very_low'
                },
                'drop_chances': {
                    'weapons': 0.15,
                    'armor': 0.30,
                    'shields': 0.25,
                    'potions': 0.10
                },
                'possible_drops': {
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Boulder Fist',
                        'damage': 20,
                        'accuracy': 0.75,
                        'description': 'Pounds with massive stone fists',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockdown',
                            'duration': 1,
                            'effect': 'reduces_defense'
                        }
                    },
                    {
                        'name': 'Earth Tremor',
                        'damage': 12,
                        'accuracy': 0.90,
                        'description': 'Causes the ground to shake',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'tremor',
                            'duration': 1,
                            'effect': 'reduces_accuracy_and_speed'
                        }
                    }
                ]
            },
            'water_spirit': {
                'name': 'Water Spirit',
                'type': 'elemental',
                'symbol': '~',
                'color': 'blue',
                'description': 'A flowing being of pure water, shifting and changing like the tide.',
                'stats': {
                    'hp': 40,
                    'attack': 12,
                    'defense': 3,
                    'speed': 18,
                    'accuracy': 0.80,

                    'exp_reward': 35
                },
                'ai': {
                    'aggression': 0.7,
                    'detection_range': 7,
                    'intelligence': 'medium'
                },
                'drop_chances': {
                    'weapons': 0.18,
                    'armor': 0.08,
                    'shields': 0.12,
                    'potions': 0.40
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Water Whip',
                        'damage': 10,
                        'accuracy': 0.85,
                        'description': 'Lashes out with a tendril of water',

                        'type': 'special',

                        'cooldown': 1,
                        'special_effects': None
                    },
                    {
                        'name': 'Tidal Wave',
                        'damage': 15,
                        'accuracy': 0.75,
                        'description': 'Crashes forward in a wave',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockback',
                            'duration': 1,
                            'effect': 'reduces_accuracy_and_speed'
                        }
                    },
                    {
                        'name': 'Healing Flow',
                        'damage': 0,
                        'accuracy': 1.0,
                        'description': 'Channels water to heal wounds',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'heal_self',
                            'amount': 15
                        }
                    }
                ]
            },
            'air_wisp': {
                'name': 'Air Wisp',
                'type': 'elemental',
                'symbol': 'o',
                'color': 'cyan',
                'description': 'A swirling vortex of wind and cloud, barely visible but deadly.',
                'stats': {
                    'hp': 25,
                    'attack': 8,
                    'defense': 1,
                    'speed': 22,
                    'accuracy': 0.80,

                    'exp_reward': 20
                },
                'ai': {
                    'aggression': 0.8,
                    'detection_range': 9,
                    'intelligence': 'medium'
                },
                'drop_chances': {
                    'weapons': 0.12,
                    'armor': 0.05,
                    'shields': 0.08,
                    'potions': 0.25
                },
                'possible_drops': {
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Wind Blade',
                        'damage': 7,
                        'accuracy': 0.95,
                        'description': 'Slices with razor-sharp wind',

                        'type': 'special',

                        'cooldown': 1,
                        'special_effects': None
                    },
                    {
                        'name': 'Whirlwind',
                        'damage': 10,
                        'accuracy': 0.80,
                        'description': 'Creates a spinning vortex',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'disorient',
                            'duration': 2,
                            'effect': 'reduces_accuracy'
                        }
                    }
                ]
            }
        },
        'beasts': {
            'wolf': {
                'name': 'Dire Wolf',
                'type': 'beasts',
                'symbol': 'w',
                'color': 'gray',
                'description': 'A massive wolf with glowing eyes and razor-sharp fangs.',
                'stats': {
                    'hp': 32,
                    'attack': 13,
                    'defense': 4,
                    'speed': 16,
                    'accuracy': 0.80,

                    'exp_reward': 24
                },
                'ai': {
                    'aggression': 0.85,
                    'detection_range': 8,
                    'intelligence': 'medium'
                },
                'multi_attack': {
                    'chance': 0.2,
                    'max_attacks': 2
                },
                'drop_chances': {
                    'weapons': 0.15,
                    'armor': 0.12,
                    'shields': 0.08,
                    'potions': 0.18
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Savage Bite',
                        'damage': 12,
                        'accuracy': 0.85,
                        'description': 'Bites with powerful jaws',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'bleed',
                            'duration': 3,
                            'damage_per_turn': 2
                        }
                    },
                    {
                        'name': 'Pack Howl',
                        'damage': 0,
                        'accuracy': 0.90,
                        'description': 'Howls to intimidate prey',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'fear',
                            'duration': 2,
                            'effect': 'reduces_player_attack'
                        }
                    },
                    {
                        'name': 'Pounce',
                        'damage': 15,
                        'accuracy': 0.75,
                        'description': 'Leaps forward with claws extended',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'knockdown',
                            'duration': 1,
                            'effect': 'reduces_defense'
                        }
                    }
                ]
            },
            'bear': {
                'name': 'Cave Bear',
                'type': 'beasts',
                'symbol': 'B',
                'color': 'brown',
                'description': 'An enormous bear with thick fur and crushing claws.',
                'stats': {
                    'hp': 65,
                    'attack': 20,
                    'defense': 6,
                    'speed': 10,
                    'accuracy': 0.80,

                    'exp_reward': 45
                },
                'ai': {
                    'aggression': 0.9,
                    'detection_range': 6,
                    'intelligence': 'low'
                },
                'multi_attack': {
                    'chance': 0.3,
                    'max_attacks': 2
                },
                'drop_chances': {
                    'weapons': 0.20,
                    'armor': 0.25,
                    'shields': 0.15,
                    'potions': 0.30
                },
                'possible_drops': {
                    'weapons': ['rusted_sword'],
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield'],
                    'potions': ['health_potion']
                },
                'attacks': [
                    {
                        'name': 'Claw Swipe',
                        'damage': 18,
                        'accuracy': 0.80,
                        'description': 'Swipes with massive claws',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'deep_wound',
                            'duration': 2,
                            'damage_per_turn': 4
                        }
                    },
                    {
                        'name': 'Bear Hug',
                        'damage': 15,
                        'accuracy': 0.85,
                        'description': 'Grapples and crushes',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'grapple',
                            'duration': 2,
                            'effect': 'cannot_move_reduces_damage'
                        }
                    },
                    {
                        'name': 'Intimidating Roar',
                        'damage': 5,
                        'accuracy': 0.95,
                        'description': 'Lets out a terrifying roar',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'fear',
                            'duration': 2,
                            'effect': 'reduces_all_stats'
                        }
                    }
                ]
            }
        },
        'constructs': {
            'golem': {
                'name': 'Stone Golem',
                'type': 'constructs',
                'symbol': 'G',
                'color': 'gray',
                'description': 'An ancient construct of carved stone, powered by mysterious runes.',
                'stats': {
                    'hp': 85,
                    'attack': 22,
                    'defense': 12,
                    'speed': 4,
                    'accuracy': 0.80,

                    'exp_reward': 60
                },
                'ai': {
                    'aggression': 0.5,
                    'detection_range': 3,
                    'intelligence': 'very_low'
                },
                'multi_attack': {
                    'chance': 0.25,
                    'max_attacks': 2
                },
                'drop_chances': {
                    'weapons': 0.10,
                    'armor': 0.35,
                    'shields': 0.30,
                    'potions': 0.05
                },
                'possible_drops': {
                    'armor': ['rusted_chest'],
                    'shields': ['round_shield']
                },
                'attacks': [
                    {
                        'name': 'Stone Fist',
                        'damage': 25,
                        'accuracy': 0.70,
                        'description': 'Pounds with enormous stone fists',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'armor_break',
                            'duration': 3,
                            'effect': 'reduces_defense_by_half'
                        }
                    },
                    {
                        'name': 'Rune Burst',
                        'damage': 18,
                        'accuracy': 0.85,
                        'description': 'Magical runes flare with power',

                        'type': 'special',

                        'cooldown': 2,
                        'special_effects': {
                            'type': 'magic_damage',
                            'effect': 'ignores_all_armor'
                        }
                    }
                ]
            }
        }
    }
    
    @classmethod
    def get_all_categories(cls):
        """Get all available monster categories"""
        return list(cls.MONSTERS.keys())
    
    @classmethod
    def get_monsters_in_category(cls, category):
        """Get all monster types in a specific category"""
        return list(cls.MONSTERS.get(category, {}).keys())
    
    @classmethod
    def get_all_monster_types(cls):
        """Get all available monster types with their categories"""
        all_types = []
        for category, monsters in cls.MONSTERS.items():
            for monster_type in monsters.keys():
                all_types.append((category, monster_type))
        return all_types
    
    @classmethod
    def get_random_monster_by_difficulty(cls, min_exp=0, max_exp=float('inf')):
        """Get a random monster within exp reward range"""
        valid_monsters = []
        for category, monsters in cls.MONSTERS.items():
            for monster_type, data in monsters.items():
                exp_reward = data['stats']['exp_reward']
                if min_exp <= exp_reward <= max_exp:
                    valid_monsters.append((category, monster_type))
        
        if not valid_monsters:
            # Fallback to skeleton if no monsters match criteria
            return ("undead", "skeleton")
        
        import random
        return random.choice(valid_monsters)
    
    @classmethod
    def get_monsters_by_difficulty_tier(cls, tier="easy"):
        """Get monsters by difficulty tier based on exp reward"""
        tiers = {
            "easy": (0, 20),      # 0-20 exp
            "medium": (21, 40),   # 21-40 exp  
            "hard": (41, 60),     # 41-60 exp
            "boss": (61, 999)     # 61+ exp
        }
        
        min_exp, max_exp = tiers.get(tier, (0, 20))
        monsters = []
        
        for category, monster_dict in cls.MONSTERS.items():
            for monster_type, data in monster_dict.items():
                exp_reward = data['stats']['exp_reward']
                if min_exp <= exp_reward <= max_exp:
                    monsters.append((category, monster_type))
        
        return monsters
    
    @classmethod
    def get_random_monster_by_tier(cls, tier="easy"):
        """Get a random monster from a specific difficulty tier"""
        monsters = cls.get_monsters_by_difficulty_tier(tier)
        if not monsters:
            return ("undead", "skeleton")  # Fallback
        
        import random
        return random.choice(monsters)
    
    @classmethod
    def monster_exists(cls, category, monster_type):
        """Check if a specific monster exists in the database"""
        return category in cls.MONSTERS and monster_type in cls.MONSTERS[category]
