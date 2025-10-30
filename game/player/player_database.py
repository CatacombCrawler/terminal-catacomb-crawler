"""
Player Database - Defines base stats and stat configurations for players
"""

class PlayerDatabase:
    """Central database for player stat & class definitions"""

    STATS = {
        "main": {
            "strength":     {"name": "Strength", "description": "Physical power & parry", "base_value": 10, "min_value": 1, "max_value": 99},
            "dexterity":    {"name": "Dexterity", "description": "Accuracy, finesse, speed", "base_value": 10, "min_value": 1, "max_value": 99},
            "cunning":      {"name": "Cunning", "description": "Trickery, crits, stealth", "base_value": 10, "min_value": 1, "max_value": 99},
            "athletism":    {"name": "Athletism", "description": "Stamina & mobility", "base_value": 10, "min_value": 1, "max_value": 99},
            "vitality":     {"name": "Vitality", "description": "Health & resilience", "base_value": 10, "min_value": 1, "max_value": 120},
            "intelligence": {"name": "Intelligence", "description": "Mana & magic", "base_value": 10, "min_value": 1, "max_value": 99},
            "willpower":    {"name": "Willpower", "description": "Focus & status resist", "base_value": 8,  "min_value": 1, "max_value": 99},
            "charisma":     {"name": "Charisma", "description": "Persuasion & trading", "base_value": 5,  "min_value": 1, "max_value": 99},
            "luck":         {"name": "Luck", "description": "Loot & random rolls", "base_value": 5,  "min_value": 1, "max_value": 99},
        },
        "derived": {
            # existing
            "health":           {"name": "Health", "description": "HP pool", "formula": "vitality * 10 + strength * 2", "min_value": 1,  "max_value": 9999},
            "mana":             {"name": "Mana", "description": "Spell resource", "formula": "intelligence * 12 + willpower * 5", "min_value": 0, "max_value": 999},
            "stamina":          {"name": "Stamina", "description": "Action energy", "formula": "athletism * 8 + vitality * 2", "min_value": 0,  "max_value": 500},
            "parry":            {"name": "Parry Chance", "description": "Deflect hits", "formula": "strength * 0.5", "min_value": 0,  "max_value": 90},
            "dodge":            {"name": "Dodge Chance", "description": "Avoid hits", "formula": "dexterity * 1.0 + athletism * 0.3", "min_value": 0, "max_value": 95},
            "accuracy":         {"name": "Accuracy", "description": "Hit chance", "formula": "70 + dexterity * 1.5 + cunning * 0.8", "min_value": 10, "max_value": 100},
            "crit_chance":      {"name": "Critical Hit Chance", "description": "Crit probability", "formula": "cunning * 0.5 + luck * 0.2", "min_value": 0, "max_value": 100},
            "crit_damage":      {"name": "Critical Damage", "description": "Crit multiplier %", "formula": "150 + (cunning * 0.3)", "min_value": 100, "max_value": 300},
            "defense":          {"name": "Defense", "description": "Base defensive capability", "formula": "vitality * 0.6 + strength * 0.6 + athletism * 0.4", "min_value": 0, "max_value": 999},
            # "magic_resistance": {"name": "Magic Resistance", "description": "Reduce magic dmg (%)", "formula": "willpower * 0.5 + intelligence * 0.2", "min_value": 0, "max_value": 90},
            "resilience":       {"name": "Resilience", "description": "Status effect resistance", "formula": "vitality * 0.3 + willpower * 0.5", "min_value": 0, "max_value": 95},
            "attack":           {"name": "Attack", "description": "Physical damage scaler", "formula": "strength * 2 + dexterity * 0.5 + luck * 0.3", "min_value": 1, "max_value": 999},
            "speed":            {"name": "Speed", "description": "Movement/turn pacing", "formula": "dexterity * 0.5 + athletism * 0.5", "min_value": 1, "max_value": 200},
            # new high-impact
            "initiative":   {"name": "Initiative", "description": "Turn order / action speed", "formula": "dexterity * 0.7 + athletism * 0.3", "min_value": 0, "max_value": 200},
            "armor":        {"name": "Armor", "description": "Flat physical damage reduction", "formula": "vitality * 0.4 + strength * 0.2", "min_value": 0, "max_value": 500},
            "block_chance": {"name": "Block Chance", "description": "Chance to block with a shield", "formula": "strength * 0.2 + athletism * 0.1", "min_value": 0, "max_value": 80},
            "block_amount": {"name": "Block Amount", "description": "Damage reduced on block", "formula": "armor * 0.6 + defense * 0.4", "min_value": 0, "max_value": 400},

            "hp_regen":     {"name": "HP Regeneration", "description": "HP per turn", "formula": "max(0, vitality * 0.2 + willpower * 0.05)", "min_value": 0, "max_value": 50},
            "mana_regen":   {"name": "Mana Regeneration", "description": "Mana per turn", "formula": "max(0, intelligence * 0.3 + willpower * 0.2)", "min_value": 0, "max_value": 50},
            "stamina_regen":{"name": "Stamina Regeneration", "description": "Stamina per turn", "formula": "max(0, athletism * 0.3 + vitality * 0.1)", "min_value": 0, "max_value": 50},

            "spell_power":  {"name": "Spell Power", "description": "Spell damage/healing scaler", "formula": "intelligence * 1.0 + willpower * 0.5", "min_value": 0, "max_value": 999},
            "status_power": {"name": "Status Power", "description": "Potency of DoTs/CC", "formula": "cunning * 0.6 + intelligence * 0.4", "min_value": 0, "max_value": 100},
            "healing_power":{"name": "Healing Power", "description": "Effectiveness of healing", "formula": "willpower * 0.8 + intelligence * 0.4", "min_value": 0, "max_value": 300},

            "stealth":      {"name": "Stealth", "description": "Avoid detection / ambush", "formula": "cunning * 0.7 + dexterity * 0.3", "min_value": 0, "max_value": 100},
            "perception":   {"name": "Perception", "description": "Detect traps & secrets", "formula": "cunning * 0.5 + luck * 0.5", "min_value": 0, "max_value": 100},
            "light_radius": {"name": "Light Radius", "description": "Sight distance in darkness", "formula": "perception * 0.3 + (luck * 0.1)", "min_value": 1, "max_value": 15},
            "carry_capacity":{"name": "Carry Capacity", "description": "Encumbrance threshold", "formula": "50 + strength * 5 + athletism * 2", "min_value": 10, "max_value": 999},
            
            # Combat penetration and resistance
            "armor_penetration": {"name": "Armor Penetration", "description": "Bypasses enemy armor %", "formula": "cunning * 0.8 + willpower * 0.4 + luck * 0.2 + strength * 0.1", "min_value": 0, "max_value": 80},
            "damage_reduction": {"name": "Damage Reduction", "description": "% of damage that can be reduced", "formula": "defense * 0.6 + willpower * 0.4", "min_value": 0, "max_value": 75},
        },
    }

    CLASSES = {
        # melee bruiser / off-tank
        "warrior": {
            "labels": ["melee", "bruiser", "tankish"],
            "starting_main_bonus": {"strength": +4, "vitality": +6},
            "main_affinity": {
                "strength": 1.15, "vitality": 1.10, "athletism": 1.05,
                "dexterity": 1.00, "cunning": 0.95, "intelligence": 0.90,
                "willpower": 1.00, "charisma": 1.00, "luck": 1.00,
            },
            "derived_affinity": {
                # existing
                "health": 1.20, "defense": 1.30, "parry": 1.25, "stamina": 1.20,
                "accuracy": 1.00, "dodge": 0.90, "crit_chance": 0.95, "crit_damage": 1.00,
                "mana": 0.80, "magic_resistance": 1.00, "resilience": 1.10,
                # new
                "initiative": 1.00, "armor": 1.25, "block_chance": 1.25, "block_amount": 1.20,
                "hp_regen": 1.15, "mana_regen": 0.85, "stamina_regen": 1.10,
                "spell_power": 0.85, "status_power": 0.95, "healing_power": 0.95,
                "stealth": 0.90, "perception": 1.00, "light_radius": 1.00, "carry_capacity": 1.25,
                "armor_penetration": 1.05, "damage_reduction": 1.10,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} strikes {enemy} with devastating force",
                        "{player} delivers a crushing blow to {enemy}",
                        "{player} lands a mighty strike on {enemy}",
                        "{player} hammers {enemy} with brutal strength",
                        "{player} overwhelms {enemy} with raw power"
                    ],
                    "low": [
                        "{player} grazes {enemy} with a glancing blow",
                        "{player} barely connects with {enemy}",
                        "{player} lands a weak strike on {enemy}",
                        "{player} hits {enemy} with reduced impact"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with trained precision",
                        "{player} hits {enemy} with disciplined force",
                        "{player} connects solidly with {enemy}",
                        "{player} lands a practiced blow on {enemy}",
                        "{player} attacks {enemy} with warrior's skill"
                    ],
                    "critical": [
                        "{base} - finding a gap in {enemy}'s armor!",
                        "{base} - exploiting {enemy}'s weakness with warrior's instinct!",
                        "{base} - delivering a devastating battle-tested strike!",
                        "{base} - overwhelming {enemy} with superior combat training!"
                    ],
                    "skill_flavors": [
                        " with battle-hardened experience",
                        " using warrior's discipline", 
                        " with military precision",
                        " drawing on countless battles",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player} lunges forward, piercing {enemy} with brutal force!",
                        "{player} dashes, slamming the spearpoint home!",
                        "{player} charges, {enemy} cannot stop the spear's impact!"
                    ],
                    "low": [
                        "{player} dashes, grazing {enemy} with the spear.",
                        "{player} commits to a lunge but {enemy} barely avoids it."
                    ],
                    "normal": [
                        "{player} dashes forward, landing a solid piercing strike!",
                        "{player} uses the spear's reach to dash and strike {enemy}!",
                        "{player} lunges past {enemy}'s guard!"
                    ],
                    "critical": [
                        "{base} - a perfect, armor-shattering lunge!",
                        "{base} - the spear finds a vital point with unstoppable force!"
                    ],
                    "skill_flavors": [
                        " with disciplined power",
                        " in a flash of steel",
                        " with a warrior's charge"
                    ]
                }
                # --- END NEW ---
            },
        },

        # glass cannon caster
        "mage": {
            "labels": ["caster", "glass_cannon"],
            "starting_main_bonus": {"intelligence": +3, "willpower": +1},
            "main_affinity": {
                "intelligence": 1.20, "willpower": 1.10, "luck": 1.05,
                "dexterity": 1.00, "cunning": 1.00, "strength": 0.85,
                "athletism": 0.95, "vitality": 0.95, "charisma": 1.00,
            },
            "derived_affinity": {
                "mana": 1.25, "magic_resistance": 1.10, "accuracy": 1.05,
                "crit_chance": 1.05, "crit_damage": 1.10,
                "health": 0.90, "defense": 0.85, "parry": 0.85, "dodge": 0.70, "stamina": 0.95, "resilience": 1.00,
                # new
                "initiative": 1.00, "armor": 0.85, "block_chance": 0.80, "block_amount": 0.85,
                "hp_regen": 0.95, "mana_regen": 1.25, "stamina_regen": 0.95,
                "spell_power": 1.30, "status_power": 1.20, "healing_power": 1.10,
                "stealth": 0.95, "perception": 1.05, "light_radius": 1.10, "carry_capacity": 0.85,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} channels arcane energy into a powerful strike against {enemy}",
                        "{player} delivers a magically-enhanced blow to {enemy}",
                        "{player} strikes {enemy} with spell-augmented force",
                        "{player} hits {enemy} with crackling magical energy",
                        "{player} overwhelms {enemy} with mystical power"
                    ],
                    "low": [
                        "{player} barely manages to graze {enemy}",
                        "{player} strikes {enemy} but the magic fizzles",
                        "{player} lands a weak, unfocused hit on {enemy}",
                        "{player} hits {enemy} with diminished magical force"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with focused magical energy",
                        "{player} hits {enemy} using arcane-enhanced precision",
                        "{player} connects with {enemy} through mystical force",
                        "{player} attacks {enemy} with scholarly precision",
                        "{player} channels magic into a measured strike against {enemy}"
                    ],
                    "critical": [
                        "{base} - unleashing a surge of arcane power!",
                        "{base} - channeling pure magical energy into {enemy}!",
                        "{base} - weaving a devastating spell-strike!",
                        "{base} - focusing mystical forces with deadly effect!"
                    ],
                    "skill_flavors": [
                        " with arcane knowledge",
                        " using mystical training", 
                        " with scholarly precision",
                        " drawing on magical studies",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player} infuses the spear with magic and lunges!",
                        "{player} teleports a short distance, piercing {enemy}!",
                        "{player} uses arcane speed to dash and strike {enemy}!"
                    ],
                    "low": [
                        "{player} attempts a lunge, but their focus wavers.",
                        "{player} dashes, barely grazing {enemy}."
                    ],
                    "normal": [
                        "{player} lunges with magically-guided precision!",
                        "{player} channels energy into the spear tip and dashes!",
                        "{player} pierces {enemy} with an arcane-honed lunge!"
                    ],
                    "critical": [
                        "{base} - a perfect lunge, amplified by arcane power!",
                        "{base} - the spearpoint erupts with energy on impact!"
                    ],
                    "skill_flavors": [
                        " with focused energy",
                        " using spell-like precision"
                    ]
                }
                # --- END NEW ---
            },
        },

        # stealth assassin (note: 'rogue', not 'rouge')
        "rogue": {
            "labels": ["stealth", "assassin"],
            "starting_main_bonus": {"dexterity": +3, "cunning": +3, "luck": +2},
            "main_affinity": {
                "dexterity": 1.20, "cunning": 1.15, "luck": 1.10,
                "strength": 0.95, "athletism": 1.05, "vitality": 0.95,
                "intelligence": 1.00, "willpower": 1.00, "charisma": 1.00,
            },
            "derived_affinity": {
                "accuracy": 1.15, "dodge": 1.10, "crit_chance": 1.20, "crit_damage": 1.10,
                "parry": 0.95, "defense": 0.90, "health": 0.95, "mana": 1.00, "stamina": 1.10,
                "magic_resistance": 0.95, "resilience": 1.00,
                # new
                "initiative": 1.20, "armor": 0.90, "block_chance": 0.85, "block_amount": 0.85,
                "hp_regen": 1.00, "mana_regen": 1.00, "stamina_regen": 1.10,
                "spell_power": 0.95, "status_power": 1.10, "healing_power": 0.95,
                "stealth": 1.30, "perception": 1.20, "light_radius": 1.05, "carry_capacity": 1.00,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} strikes {enemy} from an unexpected angle",
                        "{player} delivers a precise blow to {enemy}'s vitals",
                        "{player} finds a critical opening in {enemy}'s guard",
                        "{player} exploits {enemy}'s blind spot expertly",
                        "{player} strikes {enemy} with lethal accuracy"
                    ],
                    "low": [
                        "{player} attempts a strike but {enemy} shifts away",
                        "{player} barely scratches {enemy}",
                        "{player} lands a glancing hit on {enemy}",
                        "{player} strikes {enemy} but misjudges the angle"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with cunning precision",
                        "{player} hits {enemy} from the shadows",
                        "{player} connects with {enemy} using stealth and skill",
                        "{player} lands a calculated strike on {enemy}",
                        "{player} attacks {enemy} with rogue's finesse"
                    ],
                    "critical": [
                        "{base} - finding the perfect moment to strike!",
                        "{base} - exploiting {enemy}'s vulnerability with deadly precision!",
                        "{base} - striking a vital point with assassin's skill!",
                        "{base} - delivering a perfectly timed critical blow!"
                    ],
                    "skill_flavors": [
                        " with shadowy finesse",
                        " using stealth and cunning", 
                        " with thief's precision",
                        " drawing on underhanded tactics",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player} darts from the shadows, spear first!",
                        "{player} lunges from an impossible angle, piercing {enemy}!",
                        "{player}'s dash is a blur, ending with a spear in {enemy}!"
                    ],
                    "low": [
                        "{player} dashes, but {enemy} sidesteps the spear's tip.",
                        "{player}'s lunge is quick, but fails to find purchase."
                    ],
                    "normal": [
                        "{player} dashes, landing a precise strike!",
                        "{player} exploits an opening with a quick spear lunge!",
                        "{player} pierces {enemy} with a rogue's deadly dash!"
                    ],
                    "critical": [
                        "{base} - a dagger-fast lunge finds {enemy}'s heart!",
                        "{base} - pure speed! The spear pierces a vital organ!"
                    ],
                    "skill_flavors": [
                        " with deadly precision",
                        " from an unseen angle",
                        " with lethal grace"
                    ]
                }
                # --- END NEW ---
            },
        },

        # trickster skirmisher
        "bandit": {
            "labels": ["skirmisher", "trickster"],
            "starting_main_bonus": {"dexterity": +1, "cunning": +2, "luck": +4},
            "main_affinity": {
                "cunning": 1.15, "dexterity": 1.10, "luck": 1.15,
                "strength": 1.00, "athletism": 1.05, "vitality": 0.95,
                "intelligence": 1.00, "willpower": 0.95, "charisma": 1.05,
            },
            "derived_affinity": {
                "accuracy": 1.10, "crit_chance": 1.25, "crit_damage": 1.05, "dodge": 1.10,
                "parry": 0.95, "defense": 0.90, "health": 0.95, "stamina": 1.05, "mana": 0.95,
                "magic_resistance": 0.95, "resilience": 0.95,
                # new
                "initiative": 1.15, "armor": 0.90, "block_chance": 0.90, "block_amount": 0.90,
                "hp_regen": 1.00, "mana_regen": 0.95, "stamina_regen": 1.05,
                "spell_power": 0.95, "status_power": 1.15, "healing_power": 0.95,
                "stealth": 1.20, "perception": 1.15, "light_radius": 1.00, "carry_capacity": 1.05,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} strikes {enemy} with ruthless efficiency",
                        "{player} delivers a dirty blow to {enemy}",
                        "{player} hits {enemy} with street-smart brutality",
                        "{player} exploits {enemy}'s guard with cunning force",
                        "{player} overwhelms {enemy} with underhanded tactics"
                    ],
                    "low": [
                        "{player} barely scratches {enemy}",
                        "{player} attempts a cheap shot but misses the mark",
                        "{player} lands a weak hit on {enemy}",
                        "{player} strikes {enemy} but lacks proper technique"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with street-wise cunning",
                        "{player} hits {enemy} using underhanded methods",
                        "{player} connects with {enemy} through dirty fighting",
                        "{player} attacks {enemy} with bandit's opportunism",
                        "{player} lands a calculated cheap shot on {enemy}"
                    ],
                    "critical": [
                        "{base} - exploiting {enemy}'s trust with a devastating betrayal!",
                        "{base} - landing a perfectly timed sucker punch!",
                        "{base} - striking {enemy} where it hurts most!",
                        "{base} - using dirty tactics to devastating effect!"
                    ],
                    "skill_flavors": [
                        " with street-smart brutality",
                        " using underhanded tactics", 
                        " with criminal cunning",
                        " drawing on outlaw experience",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player} kicks up dirt then lunges, piercing {enemy}!",
                        "{player} feints high and dashes low, sinking the spear in!",
                        "{player} lunges with a sudden, vicious burst of speed!"
                    ],
                    "low": [
                        "{player} dashes, but {enemy} isn't fooled.",
                        "{player}'s lunge is wide and easily avoided."
                    ],
                    "normal": [
                        "{player} takes an opportunity to dash and strike {enemy}!",
                        "{player} lunges, landing a dirty but effective hit!",
                        "{player} pierces {enemy} with an opportunistic lunge!"
                    ],
                    "critical": [
                        "{base} - a vicious lunge to {enemy}'s kidneys!",
                        "{base} - right in the back! A perfect cheap shot!"
                    ],
                    "skill_flavors": [
                        " with cruel efficiency",
                        " like a cornered rat"
                    ]
                }
                # --- END NEW ---
            },
        },

        # drainy caster with resilience
        "warlock": {
            "labels": ["dark_caster", "drains"],
            "starting_main_bonus": {"intelligence": +2, "willpower": +2, "vitality": +3},
            "main_affinity": {
                "intelligence": 1.15, "willpower": 1.20, "luck": 1.05,
                "cunning": 1.05, "vitality": 0.95, "strength": 0.90,
                "dexterity": 0.95, "athletism": 0.95, "charisma": 1.00,
            },
            "derived_affinity": {
                "mana": 1.20, "magic_resistance": 1.15, "resilience": 1.10,
                "crit_chance": 1.05, "crit_damage": 1.05,
                "health": 0.95, "defense": 0.90, "parry": 0.90, "dodge": 0.50, "accuracy": 1.00, "stamina": 0.95,
                # new
                "initiative": 0.95, "armor": 0.90, "block_chance": 0.85, "block_amount": 0.85,
                "hp_regen": 1.05, "mana_regen": 1.20, "stamina_regen": 0.95,
                "spell_power": 1.25, "status_power": 1.30, "healing_power": 1.00,
                "stealth": 1.00, "perception": 1.05, "light_radius": 1.05, "carry_capacity": 0.90,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} strikes {enemy} with dark energy",
                        "{player} delivers a shadow-infused blow to {enemy}",
                        "{player} hits {enemy} with corrupting force",
                        "{player} channels eldritch power into a strike against {enemy}",
                        "{player} overwhelms {enemy} with forbidden magic"
                    ],
                    "low": [
                        "{player} barely grazes {enemy} with dark energy",
                        "{player} strikes {enemy} but the shadows waver",
                        "{player} lands a weak, unfocused dark strike on {enemy}",
                        "{player} hits {enemy} with diminished eldritch force"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with shadowy power",
                        "{player} hits {enemy} using dark magic",
                        "{player} connects with {enemy} through eldritch force",
                        "{player} attacks {enemy} with warlock's cunning",
                        "{player} channels forbidden energy into a strike against {enemy}"
                    ],
                    "critical": [
                        "{base} - unleashing a torrent of dark power!",
                        "{base} - channeling eldritch horror into {enemy}!",
                        "{base} - weaving shadows into a devastating strike!",
                        "{base} - cursing {enemy} with forbidden magic!"
                    ],
                    "skill_flavors": [
                        " with dark knowledge",
                        " using forbidden arts", 
                        " with eldritch precision",
                        " drawing on shadow magic",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player}'s spear becomes a lance of shadow as they lunge!",
                        "{player} pierces {enemy} with a spear wreathed in dark magic!",
                        "{player} lunges, draining life as the spear connects!"
                    ],
                    "low": [
                        "{player} dashes, but the dark energy dissipates.",
                        "{player}'s spear scrapes harmlessly against {enemy}."
                    ],
                    "normal": [
                        "{player} lunges with a spear of solid shadow!",
                        "{player} dashes, landing a chillingly precise strike!",
                        "{player} pierces {enemy} with dark intent!"
                    ],
                    "critical": [
                        "{base} - a soul-piercing lunge!",
                        "{base} - the spear tears through {enemy}'s defenses and spirit!"
                    ],
                    "skill_flavors": [
                        " with forbidden power",
                        " with chilling accuracy"
                    ]
                }
                # --- END NEW ---
            },
        },

        # holy knight: tank/support hybrid
        "paladin": {
            "labels": ["holy_knight", "tank_support"],
            "starting_main_bonus": {"strength": +1, "vitality": +5, "willpower": +3},
            "main_affinity": {
                "vitality": 1.15, "willpower": 1.10, "strength": 1.10,
                "dexterity": 1.00, "athletism": 1.05, "intelligence": 1.00,
                "cunning": 0.95, "charisma": 1.05, "luck": 1.00,
            },
            "derived_affinity": {
                "health": 1.15, "defense": 1.20, "parry": 1.10, "resilience": 1.15, "magic_resistance": 1.10,
                "mana": 1.05, "accuracy": 1.00, "dodge": 0.70, "crit_chance": 0.95, "crit_damage": 1.00, "stamina": 1.10,
                # new
                "initiative": 1.00, "armor": 1.25, "block_chance": 1.25, "block_amount": 1.25,
                "hp_regen": 1.15, "mana_regen": 1.10, "stamina_regen": 1.10,
                "spell_power": 1.05, "status_power": 0.95, "healing_power": 1.25,
                "stealth": 0.90, "perception": 1.05, "light_radius": 1.10, "carry_capacity": 1.10,
            },
            "combat_messages": {
                "basic_attack": {
                    "high": [
                        "{player} strikes {enemy} with righteous fury",
                        "{player} delivers a holy-blessed blow to {enemy}",
                        "{player} smites {enemy} with divine power",
                        "{player} channels sacred energy into a mighty strike against {enemy}",
                        "{player} overwhelms {enemy} with blessed strength"
                    ],
                    "low": [
                        "{player} barely connects with {enemy}",
                        "{player} lands a glancing blessed strike on {enemy}",
                        "{player} hits {enemy} with diminished holy power",
                        "{player} strikes {enemy} but wavers in conviction"
                    ],
                    "normal": [
                        "{player} strikes {enemy} with holy determination",
                        "{player} hits {enemy} with righteous purpose",
                        "{player} connects with {enemy} through divine guidance",
                        "{player} attacks {enemy} with sacred resolve",
                        "{player} delivers a blessed strike to {enemy}"
                    ],
                    "critical": [
                        "{base} - channeling divine wrath against evil!",
                        "{base} - delivering sacred justice to {enemy}!",
                        "{base} - smiting {enemy} with holy power!",
                        "{base} - unleashing righteous fury upon {enemy}!"
                    ],
                    "skill_flavors": [
                        " with divine blessing",
                        " using sacred training", 
                        " with righteous conviction",
                        " drawing on holy power",
                        ""
                    ]
                },
                # --- NEW ---
                "spear_dash": {
                    "high": [
                        "{player} charges, spear glowing with holy light!",
                        "{player} lunges, piercing {enemy} with divine judgment!",
                        "{player} dashes, a beacon of light, and strikes {enemy}!"
                    ],
                    "low": [
                        "{player} lunges, but their faith wavers.",
                        "{player} dashes, but the holy light sputters."
                    ],
                    "normal": [
                        "{player} dashes forward, striking {enemy} with a blessed spear!",
                        "{player} lunges with righteous purpose!",
                        "{player} pierces {enemy} with a sacred lunge!"
                    ],
                    "critical": [
                        "{base} - a divine charge that purges darkness!",
                        "{base} - the spear smites {enemy} with holy vengeance!"
                    ],
                    "skill_flavors": [
                        " with righteous conviction",
                        " with sacred power"
                    ]
                }
                # --- END NEW ---
            },
        },
    }

    @classmethod
    def get_all_stat_names(cls):
        """Get all available stat names (main + derived)"""
        main_stats = list(cls.STATS["main"].keys())
        derived_stats = list(cls.STATS["derived"].keys())
        return main_stats + derived_stats
