"""
Player Character - Handles player stats, inventory, and actions
"""

from .items.items import Equipment

class Player:
    """Player character class"""
    
    """Player character class"""
    
    def __init__(self, x=0, y=0):
        # Position
        self.x = x
        self.y = y
        
        # Base stats (before equipment bonuses)
        self.base_max_hp = 100
        self.base_attack = 10
        self.base_defense = 5
        self.base_speed = 12
        
        # Current stats (including equipment bonuses)
        self.max_hp = self.base_max_hp
        self.hp = self.max_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed
        
        # Character progression
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        
        # Display
        self.symbol = '@'
        self.name = "Hero"
        
        # Inventory and Equipment
        self.inventory = []
        self.max_inventory = 20
        self.equipment = Equipment()
        
        # Starting item (will be selected during character creation)
        self.starting_item = None

    def set_starting_item(self, item):
        """Set the player's starting item and equip it"""
        self.starting_item = item
        self.add_item(item)
        
        # Auto-equip the starting item
        success, message = self.equipment.equip_item(item, self)
        return success, message

    def recalculate_stats(self):
        """Recalculate all stats based on base stats + equipment"""
        # Reset to base stats
        self.max_hp = self.base_max_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed
        
        # Apply equipment bonuses
        bonuses = self.equipment.get_total_stat_bonuses()
        self.max_hp += bonuses['hp']
        self.attack += bonuses['attack']
        self.defense += bonuses['defense']
        self.speed += bonuses['speed']
        
        # Ensure HP doesn't exceed max
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def move(self, new_x, new_y):
        """Move player to new position"""
        self.x = new_x
        self.y = new_y
        
    def is_alive(self):
        """Check if player is still alive"""
        return self.hp > 0
        
    def take_damage(self, damage):
        """Player takes damage"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.hp = 0
            return True  # Player died
        return False
        
    def heal(self, amount):
        """Heal the player"""
        self.hp = min(self.max_hp, self.hp + amount)
        
    def gain_exp(self, amount):
        """Gain experience points"""
        self.exp += amount
        
        # Check for level up
        if self.exp >= self.exp_to_next:
            self.level_up()
            
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        
        # Increase base stats
        self.base_max_hp += 20
        self.base_attack += 3
        self.base_defense += 2
        self.base_speed += 1
        
        # Recalculate current stats with equipment
        old_hp_percent = self.hp / self.max_hp if self.max_hp > 0 else 1
        self.recalculate_stats()
        
        # Restore HP percentage after level up
        self.hp = int(self.max_hp * old_hp_percent)
        if self.hp < self.max_hp:
            self.hp = self.max_hp
        
    def attack_enemy(self, enemy):
        """Attack an enemy"""
        import random
        
        damage = self.attack + random.randint(-2, 3)
        damage = max(1, damage)
        
        enemy_died = enemy.take_damage(damage)
        
        if enemy_died:
            self.gain_exp(enemy.exp_reward)
            
        return {
            "type": "combat",
            "attacker": self.name,
            "target": enemy.name,
            "damage": damage,
            "enemy_died": enemy_died,
            "exp_gained": enemy.exp_reward if enemy_died else 0
        }
    
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
            # Remove consumable items after use
            if item.type == 'consumable':
                self.remove_item(item)
            return True, result
        return False, "Cannot use this item"
        
    def get_stats(self):
        """Get formatted player stats"""
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'position': (self.x, self.y)
        }
        
    def get_detailed_stats(self):
        """Get detailed stats including base and equipment bonuses"""
        equipment_bonuses = self.equipment.get_total_stat_bonuses()
        
        return {
            'base_stats': {
                'hp': self.base_max_hp,
                'attack': self.base_attack,
                'defense': self.base_defense,
                'speed': self.base_speed
            },
            'equipment_bonuses': equipment_bonuses,
            'total_stats': {
                'hp': self.max_hp,
                'attack': self.attack,
                'defense': self.defense,
                'speed': self.speed
            }
        }
        
    def get_equipped_items_summary(self):
        """Get a summary of equipped items"""
        equipped = self.equipment.get_equipped_items()
        summary = {}
        
        for slot, item in equipped.items():
            summary[slot] = {
                'name': item.name,
                'stats': item.stats,
                'quality': item.quality
            }
            
        return summary
