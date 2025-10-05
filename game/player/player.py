"""
Player Character - Handles player stats, inventory, and actions
"""
from base_class import BaseClass
from ..items import ItemManager
from ..items.items import Equipment
from .player_database import PlayerDatabase
from .stats_system import StatsSystem, LEGACY_ALIASES

class Player(BaseClass):
    """Player character class"""

    def __init__(self, x=0, y=0, archetype='warrior', allocated_main=None):
        # Position
        self.x = x
        self.y = y

        # Stats system (class/archetype + allocation)
        self.archetype = archetype
        self.stats = StatsSystem(
            db=PlayerDatabase,
            class_name=self.archetype,
            allocated_main=allocated_main or {},
            equipment_bonuses={}
        )

        # Legacy properties for backwards compatibility (will be deprecated)
        self.base_max_hp = self.stats.get_base_stat('hp')
        self.base_attack = self.stats.get_base_stat('attack')
        self.base_defense = self.stats.get_base_stat('defense')
        self.base_speed = self.stats.get_base_stat('speed')

        # Current stats (including equipment bonuses)
        self.max_hp = self.stats.get_stat('hp')
        self.hp = self.max_hp
        self.attack = self.stats.get_stat('attack')
        self.defense = self.stats.get_stat('defense')
        self.speed = self.stats.get_stat('speed')

        # Extended examples (access any as needed)
        self.intelligence = self.stats.get_stat('intelligence')
        self.accuracy = self.stats.get_stat('accuracy')
        self.dodge = self.stats.get_stat('dodge')
        self.parry = self.stats.get_stat('parry')
        self.athletism = self.stats.get_stat('athletism')
        self.cunning = self.stats.get_stat('cunning')
        
        # Combat stats for advanced attack mechanics
        self.crit_chance = self.stats.get_stat('crit_chance')
        self.crit_damage = self.stats.get_stat('crit_damage')
        self.armor = self.stats.get_stat('armor')
        self.block_chance = self.stats.get_stat('block_chance')
        self.armor_penetration = self.stats.get_stat('armor_penetration')
        self.damage_reduction = self.stats.get_stat('damage_reduction')

        # Character progression
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.stat_points = 0  # Available stat points to spend

        # Display
        self.symbol = '@'
        self.name = "Hero"

        # Inventory and Equipment
        self.inventory = []
        self.max_inventory = 20
        self.equipment = Equipment()

        # Starting item
        self.starting_item = None

    # ---- class/archetype & allocation hooks ----
    def set_class(self, class_name):
        self.archetype = class_name
        self.stats.set_class(class_name)
        self.recalculate_stats()

    def allocate_points(self, **kwargs):
        """Example: player.allocate_points(strength=2, vitality=1)"""
        alloc = dict(self.stats.allocated_main)
        for k, v in kwargs.items():
            alloc[k] = alloc.get(k, 0) + int(v)
        self.stats.set_allocated_main(alloc)
        self.recalculate_stats()

    def spend_stat_point(self, stat_name, amount=1):
        """Spend available stat points on a specific stat"""
        if self.stat_points < amount:
            return False, "Not enough stat points available"
        
        if stat_name not in self.stats.db.STATS["main"]:
            return False, f"Invalid stat: {stat_name}"
        
        # Check max value constraint
        current_allocated = self.stats.allocated_main.get(stat_name, 0)
        stat_config = self.stats.db.STATS["main"][stat_name]
        if current_allocated + amount > stat_config["max_value"]:
            return False, f"{stat_name} is already at maximum value"
        
        # Spend the points
        self.stat_points -= amount
        alloc = dict(self.stats.allocated_main)
        alloc[stat_name] = alloc.get(stat_name, 0) + amount
        self.stats.set_allocated_main(alloc)
        
        # Preserve HP ratio when recalculating
        old_ratio = (self.hp / self.max_hp) if self.max_hp else 1.0
        self.recalculate_stats()
        self.hp = min(self.max_hp, int(round(self.max_hp * old_ratio)))
        
        return True, f"Added {amount} point(s) to {stat_name}"

    def get_available_stat_points(self):
        """Get number of available stat points"""
        return self.stat_points

    # ---- items & equipment ----
    def set_starting_item(self, item):
        """Set and auto-equip starting item."""
        self.starting_item = item
        self.add_item(item)
        success, message = self.equipment.equip_item(item, self)
        return success, message

    def recalculate_stats(self):
        """Recalculate all stats based on base + class + equipment"""
        bonuses = self.equipment.get_total_stat_bonuses()  # dict of stat -> bonus
        self.stats.set_equipment_bonuses(bonuses)

        # Update legacy properties (compat)
        self.base_max_hp = self.stats.get_base_stat('hp')
        self.base_attack = self.stats.get_base_stat('attack')
        self.base_defense = self.stats.get_stat('defense')
        self.base_speed = self.stats.get_stat('speed')

        # Update current stats
        old_max = getattr(self, "max_hp", self.stats.get_stat('hp'))
        old_ratio = (self.hp / old_max) if old_max else 1.0

        self.max_hp = self.stats.get_stat('hp')
        self.attack = self.stats.get_stat('attack')
        self.defense = self.stats.get_stat('defense')
        self.speed = self.stats.get_stat('speed')

        # Extended examples
        self.intelligence = self.stats.get_stat('intelligence')
        self.accuracy = self.stats.get_stat('accuracy')
        self.dodge = self.stats.get_stat('dodge')
        self.parry = self.stats.get_stat('parry')
        self.athletism = self.stats.get_stat('athletism')
        self.cunning = self.stats.get_stat('cunning')
        
        # Combat stats for advanced attack mechanics
        self.crit_chance = self.stats.get_stat('crit_chance')
        self.crit_damage = self.stats.get_stat('crit_damage')
        self.armor = self.stats.get_stat('armor')
        self.block_chance = self.stats.get_stat('block_chance')
        self.armor_penetration = self.stats.get_stat('armor_penetration')
        self.damage_reduction = self.stats.get_stat('damage_reduction')

        # Keep current HP proportionally within new max
        self.hp = min(self.max_hp, int(round(self.max_hp * old_ratio)))

    def move(self, new_x, new_y):
        """Move player to new position"""
        self.x = new_x
        self.y = new_y

    def is_alive(self):
        """Check if player is still alive"""
        return self.hp > 0

    def take_damage(self, damage, attacker_armor_penetration=0):
        """Player takes damage with percentage-based damage reduction and armor penetration"""
        # Calculate effective damage reduction based on armor penetration
        effective_damage_reduction = max(0, self.damage_reduction - attacker_armor_penetration)
        
        # Apply percentage-based damage reduction
        damage_reduction_factor = effective_damage_reduction / 100.0
        damage_after_reduction = damage * (1 - damage_reduction_factor)
        
        # Ensure minimum damage of 1
        actual_damage = max(1, int(damage_after_reduction))
        deflected_damage = damage - actual_damage
        
        self.hp -= actual_damage

        died = False
        if self.hp <= 0:
            self.hp = 0
            died = True

        return {
            "died": died,
            "deflected": deflected_damage,
            "damage_reduction": effective_damage_reduction,
            "base_damage_reduction": self.damage_reduction,
            "attacker_armor_penetration": attacker_armor_penetration,
            "original_damage": damage,
            "final_damage": actual_damage
        }

    def heal(self, amount):
        """Heal the player"""
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_exp(self, amount, monster_level=None):
        """Gain experience points and handle level-ups
        
        Args:
            amount: Base experience amount
            monster_level: Optional monster level for multiplier calculation
            
        Returns:
            bool: True if player leveled up, False otherwise
        """
        if monster_level is not None and monster_level > self.level:
            # Apply 2x multiplier for each level above player
            level_difference = monster_level - self.level
            multiplier = 2 ** level_difference
            amount = int(amount * multiplier)
        
        self.exp += amount
        leveled_up = False
        while self.exp >= self.exp_to_next:
            self.level_up()
            leveled_up = True
        
        return leveled_up

    def level_up(self):
        """Level up the player and grant stat points for allocation"""
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        
        # Grant 5 stat points per level
        self.stat_points += 5

        # Recalculate stats (may increase max HP)
        self.recalculate_stats()
        
        # Fully restore health on level up
        self.hp = self.max_hp
        
        return True  # Indicate level up occurred

    def attack_enemy(self, enemy):
        """Basic Attack - Uses full stats system for accuracy, damage, and special mechanics"""
        import random
        
        # === HIT CALCULATION ===
        # Convert our accuracy percentage to 0-1 range
        player_accuracy = min(100, max(10, self.accuracy)) / 100.0
        
        # Enemy dodge chance (if they have it)
        enemy_dodge = getattr(enemy, 'dodge', 0)
        if enemy_dodge > 1.0:  # Convert percentage to decimal if needed
            enemy_dodge = enemy_dodge / 100.0
        
        # Final hit chance = accuracy - enemy dodge (minimum 5% hit chance)
        hit_chance = max(0.05, player_accuracy - enemy_dodge)
        
        # Roll for hit
        hit_roll = random.random()
        if hit_roll > hit_chance:
            # Generate clearer miss message
            miss_reason = ""
            if player_accuracy < 0.6:
                miss_reason = f" (Low accuracy: {player_accuracy*100:.0f}%)"
            elif enemy_dodge > 0.15:
                miss_reason = f" (Enemy dodged)"
            else:
                # Show as "needed X% or lower, rolled Y%" which is more intuitive
                needed = int(hit_chance * 100)
                rolled = int(hit_roll * 100)
                miss_reason = f" (Needed ≤{needed}%, rolled {rolled}%)"
            
            return {
                "type": "combat",
                "attacker": self.name,
                "target": enemy.name,
                "damage": 0,
                "hit": False,
                "enemy_died": False,
                "exp_gained": 0,
                "leveled_up": False,
                "message": f"{self.name} misses {enemy.name}!{miss_reason}",
                "hit_roll": hit_roll,
                "hit_chance": hit_chance,
                "accuracy": player_accuracy,
                "enemy_dodge": enemy_dodge
            }
        
        # === DAMAGE CALCULATION ===
        # Base damage from attack stat
        base_damage = self.attack
        
        # Add variance (-15% to +25% of base damage)
        variance_min = int(base_damage * -0.15)
        variance_max = int(base_damage * 0.25)
        damage_variance = random.randint(variance_min, variance_max)
        
        total_damage = max(1, base_damage + damage_variance)
        
        # === CRITICAL HIT CHECK ===
        crit_chance = min(100, max(0, self.crit_chance)) / 100.0
        crit_roll = random.random()
        is_critical = crit_roll <= crit_chance
        
        if is_critical:
            # Apply critical damage multiplier (e.g., 150% = 1.5x damage)
            crit_multiplier = self.crit_damage / 100.0
            total_damage = int(total_damage * crit_multiplier)
        
        # === ENEMY DEFENSIVE MECHANICS ===
        # Check if enemy can parry (basic implementation)
        enemy_parry = getattr(enemy, 'parry', 0)
        if enemy_parry > 1.0:  # Convert percentage if needed
            enemy_parry = enemy_parry / 100.0
        
        parry_roll = random.random()
        was_parried = parry_roll <= enemy_parry
        
        if was_parried:
            # Parry reduces damage by 50-75%
            parry_reduction = random.uniform(0.5, 0.75)
            total_damage = int(total_damage * (1 - parry_reduction))
            total_damage = max(1, total_damage)  # Minimum 1 damage
        
        # === APPLY DAMAGE ===
        player_armor_penetration = self.armor_penetration
        result = enemy.take_damage(total_damage, player_armor_penetration)
        
        # === EXPERIENCE AND LEVELING ===
        enemy_died = result["died"]
        leveled_up = False
        exp_gained = 0
        if enemy_died:
            monster_level = getattr(enemy, 'level', None)
            exp_gained = getattr(enemy, "exp_reward", 0)
            leveled_up = self.gain_exp(exp_gained, monster_level)
        
        # === COMBAT RESULT ===
        combat_result = {
            "type": "combat",
            "attacker": self.name,
            "target": enemy.name,
            "damage": total_damage,
            "hit": True,
            "critical": is_critical,
            "parried": was_parried,
            "enemy_died": enemy_died,
            "exp_gained": exp_gained,
            "leveled_up": leveled_up,
            "deflected": result.get("deflected", 0),
            "damage_reduction": result.get("damage_reduction", 0)
        }
        
        # Add descriptive message based on what happened
        combat_result["message"] = self._generate_combat_message(
            enemy, total_damage, is_critical, was_parried, base_damage, damage_variance, result
        )
        
        return combat_result

    def _generate_combat_message(self, enemy, total_damage, is_critical, was_parried, base_damage, damage_variance, damage_result=None, attack_type="basic_attack"):
        """Generate descriptive combat messages based on class, attack type, and circumstances"""
        import random
        
        # Determine attack effectiveness based on actual damage vs base damage
        # This gives us a clearer picture of effectiveness after all modifiers
        damage_effectiveness = (total_damage - base_damage) / base_damage if base_damage > 0 else 0
        
        # Get class-specific and attack-type-specific messages
        messages = self._get_class_attack_messages(attack_type, damage_effectiveness)
        base_message = random.choice(messages["base"]).format(
            player=self.name, 
            enemy=enemy.name
        )
        
        # Add critical hit flavor
        if is_critical and was_parried:
            crit_parry_messages = messages.get("critical_parried", [
                f"{base_message} - a critical strike, though partially deflected by {enemy.name}'s defenses",
                f"{base_message} - finding a vital spot despite {enemy.name}'s defensive efforts", 
                f"{base_message} - a devastating blow that overwhelms {enemy.name}'s parry attempt"
            ])
            final_message = random.choice(crit_parry_messages).format(
                base=base_message, player=self.name, enemy=enemy.name
            )
        elif is_critical:
            crit_messages = messages.get("critical", [
                f"{base_message} - finding a critical weakness!",
                f"{base_message} - exploiting a vital opening in {enemy.name}'s guard!",
                f"{base_message} - striking a devastating blow to a vulnerable spot!",
                f"{base_message} - landing a perfectly placed critical hit!"
            ])
            final_message = random.choice(crit_messages).format(
                base=base_message, player=self.name, enemy=enemy.name
            )
        elif was_parried:
            parry_messages = messages.get("parried", [
                f"{base_message}, but {enemy.name} deflects some of the impact",
                f"{base_message}, though {enemy.name} manages to parry part of the attack",
                f"{base_message}, but {enemy.name}'s defenses reduce the damage",
                f"{base_message}, partially blocked by {enemy.name}'s defensive stance"
            ])
            final_message = random.choice(parry_messages).format(
                base=base_message, player=self.name, enemy=enemy.name
            )
        else:
            # Add class-specific skill flavor for normal hits
            skill_flavors = messages.get("skill_flavors", [
                " with practiced skill",
                " using combat expertise", 
                " with trained precision",
                " drawing on battle experience",
                ""  # Sometimes just the basic message
            ])
            final_message = base_message + random.choice(skill_flavors)
        
        # Add deflection information if damage was reduced
        if damage_result and damage_result.get("deflected", 0) > 0:
            deflected_amount = damage_result["deflected"]
            damage_reduction = damage_result.get("damage_reduction", 0)
            
            if damage_reduction > 0:
                final_message += f" ({enemy.name} deflects {deflected_amount} damage with {damage_reduction}% damage reduction)"
            else:
                final_message += f" ({enemy.name} deflects {deflected_amount} damage)"
        
        return final_message

    def _get_class_attack_messages(self, attack_type, damage_effectiveness):
        """Get class and attack-type specific combat message templates from database"""
        from game.player.player_database import PlayerDatabase
        
        # Get messages from database
        class_key = self.archetype.lower()
        class_data = PlayerDatabase.CLASSES.get(class_key)
        
        # Fallback to warrior if class not found
        if not class_data or "combat_messages" not in class_data:
            class_data = PlayerDatabase.CLASSES.get("warrior", {})
        
        combat_messages = class_data.get("combat_messages", {})
        attack_messages = combat_messages.get(attack_type)
        
        # Fallback to basic_attack if attack type not found
        if not attack_messages:
            attack_messages = combat_messages.get("basic_attack", {})
        
        # If still no messages, provide basic fallback
        if not attack_messages:
            attack_messages = {
                "high": ["{player} strikes {enemy} with great force"],
                "low": ["{player} barely hits {enemy}"],
                "normal": ["{player} attacks {enemy}"],
                "critical": ["{base} - a critical hit!"],
                "skill_flavors": [""]
            }
        
        # Select appropriate damage tier based on effectiveness
        # Positive effectiveness = better than base damage (high roll, crit, etc.)
        # Negative effectiveness = worse than base damage (low roll, parried, etc.)
        if damage_effectiveness > 0.20:  # Significantly higher than base damage
            base_messages = attack_messages.get("high", attack_messages.get("normal", ["{player} attacks {enemy}"]))
        elif damage_effectiveness < -0.15:  # Significantly lower than base damage  
            base_messages = attack_messages.get("low", attack_messages.get("normal", ["{player} attacks {enemy}"]))
        else:  # Normal damage range (close to base damage)
            base_messages = attack_messages.get("normal", ["{player} attacks {enemy}"])
            
        return {
            "base": base_messages,
            "critical": attack_messages.get("critical", []),
            "skill_flavors": attack_messages.get("skill_flavors", [""])
        }

    # ---- inventory & equipment passthroughs ----
    def add_item(self, item):
        """Add item to inventory"""
        if len(self.inventory) < self.max_inventory:
            self.inventory.append(item)
            return True
        return False  # Inventory full

    def remove_item(self, item):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def equip_item(self, item):
        """Equip an item"""
        if item not in self.inventory:
            return False, "Item not in inventory"

        success, message = self.equipment.equip_item(item, self)
        if success:
            self.recalculate_stats()
        return success, message

    def unequip_item(self, item):
        """Unequip an item"""
        success, message = self.equipment.unequip_item(item, self)
        if success:
            self.recalculate_stats()
        return success, message

    def use_item(self, item):
        """Use/consume an item"""
        if item not in self.inventory:
            return False, "Item not in inventory"

        result = item.use_item(self)
        if result:
            if getattr(item, "type", None) == 'consumable':
                self.remove_item(item)
            return True, result
        return False, "Cannot use this item"

    # ---- public getters for UI/debug ----
    def get_stats(self):
        """Get formatted player stats (legacy + a few extended fields)"""
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'intelligence': self.intelligence,
            'accuracy': self.accuracy,
            'dodge': self.dodge,
            'parry': self.parry,
            'athletism': self.athletism,
            'cunning': self.cunning,
            'crit_chance': self.crit_chance,
            'crit_damage': self.crit_damage,
            'armor': self.armor,
            'block_chance': self.block_chance,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'position': (self.x, self.y)
        }

    def get_detailed_stats(self):
        """Get detailed stats including base and equipment bonuses"""
        return {
            'base_stats': self.stats.get_all_base_stats(),
            'equipment_bonuses': self.stats.get_all_equipment_bonuses(),
            'total_stats': self.stats.get_all_stats()
        }

    def get_stat_breakdown(self, stat_name):
        """Get detailed breakdown of a specific stat"""
        return self.stats.get_stat_breakdown(stat_name)

    def get_all_available_stats(self):
        """Get list of all available stat names"""
        mains = list(PlayerDatabase.STATS["main"].keys())
        derived = list(PlayerDatabase.STATS["derived"].keys())
        return mains + derived

    def get_equipped_items_summary(self):
        """Get a summary of equipped items"""
        equipped = self.equipment.get_equipped_items()
        summary = {}
        for slot, item in equipped.items():
            summary[slot] = {
                'name': item.name,
                'stats': getattr(item, "stats", {}),
                'quality': getattr(item, "quality", None),
            }
        return summary

    def get_player_dict(self):
        """
        Core method to create player information as a dictionary
        :return: dict of player information
        """
        exclusions = {"stats", "inventory", "equipment", "starting_item"}
        player_data = self._to_dict(self)
        data = {k: v for k, v in player_data.items() if k not in exclusions}
        data['stats'] = self.get_detailed_stats()
        data['starting_item'] = self.starting_item.item_id
        data['inventory'] = [item.item_id for item in self.inventory]
        data['equipments'] = {equip_key: equiv_val.item_id for equip_key, equiv_val in self.equipment.get_equipped_items().items()}
        return data

    def load(self, data):
        """Load data into player
        :param data: data from json file to load
        """
        self.x = data.get('x', 5)
        self.y = data.get('y', 5)

        self.archetype = data.get('archetype', 'warrior')
        self.stats.load(data.get('stats', {}))

        self.base_max_hp = data.get('hp', self.stats.get_base_stat('hp'))
        self.base_attack = data.get('attack', self.stats.get_base_stat('attack'))
        self.base_defense = data.get('defense', self.stats.get_base_stat('defense'))
        self.base_speed = data.get('speed', self.stats.get_base_stat('speed'))

        self.max_hp = data.get('hp', self.stats.get_stat('hp'))
        self.hp = data.get('max_hp', self.max_hp)
        self.attack = data.get('attack', self.stats.get_stat('attack'))
        self.defense = data.get('defense', self.stats.get_stat('defense'))
        self.speed = data.get('speed', self.stats.get_stat('speed'))

        self.intelligence = data.get('intelligence', self.stats.get_stat('intelligence'))
        self.accuracy = data.get('accuracy', self.stats.get_stat('accuracy'))
        self.dodge = data.get('dodge', self.stats.get_stat('dodge'))
        self.parry = data.get('parry', self.stats.get_stat('parry'))
        self.athletism = data.get('athletism', self.stats.get_stat('athletism'))
        self.cunning = data.get('cunning', self.stats.get_stat('cunning'))

        self.crit_chance = data.get('crit_chance', self.stats.get_stat('crit_chance'))
        self.crit_damage = data.get('crit_damage', self.stats.get_stat('crit_damage'))
        self.armor = data.get('armor', self.stats.get_stat('armor'))
        self.block_chance = data.get('block_chance', self.stats.get_stat('block_chance'))
        self.armor_penetration = data.get('armor_penetration', self.stats.get_stat('armor_penetration'))
        self.damage_reduction = data.get('damage_reduction', self.stats.get_stat('damage_reduction'))

        self.level = data.get('level', 1)
        self.exp = data.get('exp', 0)
        self.exp_to_next = data.get('exp_to_next', 100)
        self.stat_points = data.get('stat_points', 0)

        self.symbol = data.get('symbol', '@')
        self.name = data.get('name', "Hero")

        player_inventory = data.get('inventory', [])
        ItemManager.load(player_inventory, self)

        self.max_inventory = data.get('max_inventory', 20)

        player_equipments = data.get('equipments', {})
        self.equipment = Equipment()
        self.equipment.load(player_equipments, self)

        starting_item = data.get('starting_item', None)
        if starting_item:
            self.starting_item = ItemManager.get_items_by_id(starting_item)