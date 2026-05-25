"""
Item Classes - Item objects and management
"""

from .database import ITEMS, ITEM_QUALITIES, ITEM_TYPES

class Item:
    """Base item class"""
    
    def __init__(self, item_id, category=None):
        self.item_id = item_id
        self.category = category or self._find_category(item_id)
        
        if not self.category:
            raise ValueError(f"Item '{item_id}' not found in database")
            
        # Load item data from database
        self.data = ITEMS[self.category][item_id].copy()
        
        # Basic properties
        self.name = self.data['name']
        self.type = self.data['type']
        self.quality = self.data['quality']
        self.starting_item = self.data['starting_item']
        self.description = self.data['description']
        self.symbol = self.data['symbol']
        self.color = self.data['color']
        
        # Stats
        self.stats = self.data['stats'].copy()
        self.requirements = self.data.get('requirements', {})
        
        # Special effects (for consumables, etc.)
        self.effect = self.data.get('effect', None)
        
        # Instance properties
        self.equipped = False
        self.quantity = 1  # For stackable items
        
    def _find_category(self, item_id):
        """Find which category an item belongs to"""
        for category, items in ITEMS.items():
            if item_id in items:
                return category
        return None
        
    def can_be_equipped_by(self, player):
        """Check if player meets requirements to equip this item"""
        if not self.requirements:
            return True
            
        # Check level requirement
        if 'level' in self.requirements:
            if player.level < self.requirements['level']:
                return False
                
        # Future: Check other requirements like strength, dexterity
        # if 'strength' in self.requirements:
        #     if player.strength < self.requirements['strength']:
        #         return False
                
        return True
        
    def get_stat_bonus(self, stat_name):
        """Get the bonus this item provides to a specific stat"""
        return self.stats.get(stat_name, 0)
        
    def get_total_stats(self):
        """Get all stat bonuses as a dict"""
        return self.stats.copy()
        
    def use_item(self, player):
        """Use/consume the item (for consumables)"""
        if self.type != 'consumable' or not self.effect:
            return False
            
        if self.effect['type'] == 'heal':
            heal_amount = self.effect['amount']
            old_hp = player.hp
            player.heal(heal_amount)
            actual_heal = player.hp - old_hp
            return f"Healed for {actual_heal} HP!"
        elif self.effect['type'] == 'exp':
            exp_amount = self.effect['amount']
            player.gain_exp(exp_amount)
            return f"Gained {exp_amount} experience!"
            
        # Future: Add more effect types
        return False
        
    def get_quality_info(self):
        """Get quality information for display"""
        if self.quality in ITEM_QUALITIES:
            return ITEM_QUALITIES[self.quality]
        return ITEM_QUALITIES['normal']
        
    def get_type_info(self):
        """Get type information"""
        if self.type in ITEM_TYPES:
            return ITEM_TYPES[self.type]
        return {}
        
    def __str__(self):
        """String representation of the item"""
        quality_info = self.get_quality_info()
        return f"{quality_info['name']} {self.name}"


class ItemManager:
    """Manages item creation and database access"""
    
    @staticmethod
    def create_item(item_id, category=None):
        """Create a new item instance"""
        return Item(item_id, category)
        
    @staticmethod
    def get_starting_items():
        """Get all items that can be starting items"""
        starting_items = {}
        
        for category, items in ITEMS.items():
            starting_items[category] = {}
            for item_id, item_data in items.items():
                if item_data.get('starting_item', False):
                    starting_items[category][item_id] = item_data
                    
        return starting_items
        
    @staticmethod
    def get_items_by_category(category):
        """Get all items in a specific category"""
        return ITEMS.get(category, {})
        
    @staticmethod
    def get_items_by_type(item_type):
        """Get all items of a specific type"""
        result = {}
        
        for category, items in ITEMS.items():
            for item_id, item_data in items.items():
                if item_data['type'] == item_type:
                    if category not in result:
                        result[category] = {}
                    result[category][item_id] = item_data
                    
        return result
        
    @staticmethod
    def item_exists(item_id, category=None):
        """Check if an item exists in the database"""
        if category:
            return category in ITEMS and item_id in ITEMS[category]
        else:
            for cat_items in ITEMS.values():
                if item_id in cat_items:
                    return True
        return False


class Equipment:
    """Manages equipped items for a character"""
    
    def __init__(self):
        # Equipment slots
        self.main_hand = None    # Weapons
        self.off_hand = None     # Shields
        self.chest = None        # Armor
        # Future slots: helmet, boots, gloves, rings, etc.
        
    def equip_item(self, item, player):
        """Equip an item to the appropriate slot"""
        if not item.can_be_equipped_by(player):
            return False, f"You don't meet the requirements for {item.name}"
            
        type_info = item.get_type_info()
        slot = type_info.get('slot')
        
        if not slot:
            return False, f"{item.name} cannot be equipped"
            
        # Get current item in slot
        current_item = getattr(self, slot, None)
        
        # Unequip current item if exists
        if current_item:
            self.unequip_item(current_item, player)
            
        # Equip new item
        setattr(self, slot, item)
        item.equipped = True
        
        # Apply stat bonuses to player
        self._apply_item_stats(item, player, equip=True)
        
        return True, f"Equipped {item.name}"
        
    def unequip_item(self, item, player):
        """Unequip an item"""
        type_info = item.get_type_info()
        slot = type_info.get('slot')
        
        if slot and getattr(self, slot) == item:
            setattr(self, slot, None)
            item.equipped = False
            
            # Remove stat bonuses from player
            self._apply_item_stats(item, player, equip=False)
            
            return True, f"Unequipped {item.name}"
            
        return False, f"{item.name} is not equipped"
        
    def _apply_item_stats(self, item, player, equip=True):
        """Apply or remove item stat bonuses to/from player"""
        multiplier = 1 if equip else -1
        
        for stat_name, bonus in item.stats.items():
            if hasattr(player, stat_name):
                current_value = getattr(player, stat_name)
                setattr(player, stat_name, current_value + (bonus * multiplier))
                
        # Handle max_hp changes specially
        if 'hp' in item.stats and item.stats['hp'] != 0:
            hp_change = item.stats['hp'] * multiplier
            player.max_hp += hp_change
            
            # If equipping and player is at full health, give them the bonus HP
            if equip and player.hp == player.max_hp - hp_change:
                player.hp = player.max_hp
                
    def get_equipped_items(self):
        """Get all currently equipped items"""
        equipped = {}
        
        if self.main_hand:
            equipped['main_hand'] = self.main_hand
        if self.off_hand:
            equipped['off_hand'] = self.off_hand
        if self.chest:
            equipped['chest'] = self.chest
            
        return equipped
        
    def get_total_stat_bonuses(self):
        """Get total stat bonuses from all equipped items"""
        # Import here to avoid circular imports
        from ..player.player_database import PlayerDatabase
        
        # Initialize all possible stats to 0
        total_bonuses = {}
        for stat_name in PlayerDatabase.get_all_stat_names():
            total_bonuses[stat_name] = 0
        
        # Add bonuses from all equipped items  
        for item in self.get_equipped_items().values():
            for stat, bonus in item.stats.items():
                if stat in total_bonuses:
                    total_bonuses[stat] += bonus
                    
        return total_bonuses