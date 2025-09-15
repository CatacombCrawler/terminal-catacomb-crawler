"""
Player Character - Handles player stats, inventory, and actions
"""

class Player:
    """Player character class"""
    
    def __init__(self, x=0, y=0):
        # Position
        self.x = x
        self.y = y
        
        # Stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        
        # Display
        self.symbol = '@'
        self.name = "Hero"
        
        # Inventory
        self.inventory = []
        self.max_inventory = 20
        
        # Equipment (for later)
        self.weapon = None
        self.armor = None
        
    def move(self, new_x, new_y):
        """Move player to new position"""
        self.x = new_x
        self.y = new_y
        
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
        
        # Increase stats
        self.max_hp += 20
        self.hp = self.max_hp  # Full heal on level up
        self.attack += 3
        self.defense += 2
        
    def add_item(self, item):
        """Add item to inventory"""
        if len(self.inventory) < self.max_inventory:
            self.inventory.append(item)
            return True
        return False  # Inventory full
        
    def get_stats(self):
        """Get formatted player stats"""
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'position': (self.x, self.y)
        }