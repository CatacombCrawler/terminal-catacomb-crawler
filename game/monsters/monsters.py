"""
Monster System - Handles monster AI, stats, and combat using MonsterDatabase
"""

import random
from .monster_database import MonsterDatabase

class Monster:
    """Base monster class using MonsterDatabase for definitions"""
    
    def __init__(self, x, y, monster_category, monster_type):
        # Position
        self.x = x
        self.y = y
        
        # Monster identity
        self.category = monster_category
        self.type = monster_type
        
        # Get monster data from database
        self.data = MonsterDatabase.MONSTERS[monster_category][monster_type]
        
        # Initialize combat state before setup
        self.attack_cooldowns = {}
        self.status_effects = {}
        
        self.setup_monster_stats()
        
        # AI state
        self.last_seen_player = None
        self.alert_turns = 0
        self.max_alert = 5
        
    def setup_monster_stats(self):
        """Setup stats based on monster data from database"""
        # Basic info
        self.name = self.data['name']
        self.symbol = self.data['symbol']
        self.color = self.data['color']
        self.description = self.data['description']
        
        # Combat stats
        stats = self.data['stats']
        self.max_hp = stats['hp']
        self.hp = self.max_hp
        self.attack = stats['attack']
        self.defense = stats['defense']
        self.speed = stats['speed']
        self.accuracy = stats['accuracy']
        self.exp_reward = stats['exp_reward']
        
        # AI behavior
        ai = self.data['ai']
        self.aggression = ai['aggression']
        self.detection_range = ai['detection_range']
        self.intelligence = ai['intelligence']
        
        # Initialize attack cooldowns
        for attack in self.data['attacks']:
            self.attack_cooldowns[attack['name']] = 0
            
    def is_alive(self):
        """Check if monster is still alive"""
        return self.hp > 0
        
    def take_damage(self, damage):
        """Monster takes damage"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.hp = 0
            return True
        return False
        
    def get_distance_to(self, x, y):
        """Calculate distance to a position"""
        return abs(self.x - x) + abs(self.y - y)
        
    def can_see_player(self, player):
        """Check if monster can detect the player"""
        distance = self.get_distance_to(player.x, player.y)
        return distance <= self.detection_range
        
    def get_available_attacks(self):
        """Get list of attacks that are not on cooldown"""
        available = []
        for attack in self.data['attacks']:
            if self.attack_cooldowns[attack['name']] <= 0:
                available.append(attack)
        return available
        
    def choose_attack(self):
        """Choose an attack based on AI intelligence and available attacks"""
        available_attacks = self.get_available_attacks()
        
        # Always include basic attack as an option
        basic_attack = {
            'name': 'Basic Attack',
            'damage': self.attack,
            'accuracy': self.accuracy,
            'description': f'{self.name} attacks',
            'type': 'basic',
            'cooldown': 0,
            'special_effects': None
        }
        
        # Add basic attack to available options
        all_attacks = available_attacks + [basic_attack]
        
        if not all_attacks:
            # Fallback (should never happen now)
            return basic_attack
            
        if self.intelligence == 'very_low':
            # Random attack selection (50% chance for basic attack)
            if random.random() < 0.5:
                return basic_attack
            return random.choice(available_attacks) if available_attacks else basic_attack
        elif self.intelligence == 'low':
            # Mix of basic attacks and special attacks (30% basic)
            if random.random() < 0.3 or not available_attacks:
                return basic_attack
            return min(available_attacks, key=lambda a: a['cooldown'])
        elif self.intelligence == 'medium':
            # Strategic mix (20% basic attack, prefer efficient specials)
            if random.random() < 0.2:
                return basic_attack
            return max(all_attacks, key=lambda a: a['damage'] * a['accuracy'])
        else:  # high intelligence
            # Smart usage (15% basic attack, prefer special abilities for variety)
            if random.random() < 0.15:
                return basic_attack
            
            # High intelligence monsters prefer using their special abilities
            if available_attacks:
                # Choose best damage attack when HP is low, balanced otherwise
                if self.hp <= self.max_hp * 0.3:
                    return max(available_attacks, key=lambda a: a['damage'])
                else:
                    return max(available_attacks, key=lambda a: a['damage'] * a['accuracy'])
            else:
                # No specials available, use basic attack
                return basic_attack
    
    def update_cooldowns(self):
        """Reduce all attack cooldowns by 1"""
        for attack_name in self.attack_cooldowns:
            if self.attack_cooldowns[attack_name] > 0:
                self.attack_cooldowns[attack_name] -= 1
                
    def update_status_effects(self):
        """Update and apply status effects"""
        effects_to_remove = []
        damage_taken = 0
        
        for effect_name, effect_data in self.status_effects.items():
            effect_data['duration'] -= 1
            
            # Apply effect
            if effect_name == 'poison':
                damage_taken += effect_data['damage_per_turn']
            
            # Remove expired effects
            if effect_data['duration'] <= 0:
                effects_to_remove.append(effect_name)
                
        # Remove expired effects
        for effect_name in effects_to_remove:
            del self.status_effects[effect_name]
            
        # Apply damage from status effects
        if damage_taken > 0:
            self.hp = max(0, self.hp - damage_taken)
            
        return damage_taken
        
    def ai_turn(self, player, level):
        """Execute AI behavior for this turn"""
        if not self.is_alive():
            return None
            
        # Update cooldowns and status effects
        self.update_cooldowns()
        status_damage = self.update_status_effects()
        
        events = []
        if status_damage > 0:
            events.append({
                "type": "status_damage",
                "target": self.name,
                "damage": status_damage
            })
            
        # Check if player is visible
        if self.can_see_player(player):
            self.last_seen_player = (player.x, player.y)
            self.alert_turns = self.max_alert
            
            # If adjacent to player, attack
            if self.get_distance_to(player.x, player.y) == 1:
                attack_event = self.attack_player(player)
                if attack_event:
                    events.append(attack_event)
            
            # Otherwise, move towards player if aggressive enough
            elif random.random() < self.aggression:
                new_x, new_y = self.get_move_towards_player(player, level)
                if level.is_walkable(new_x, new_y):
                    self.x, self.y = new_x, new_y
                    
        elif self.alert_turns > 0:
            # Move towards last known player position
            self.alert_turns -= 1
            if self.last_seen_player:
                target_x, target_y = self.last_seen_player
                new_x, new_y = self.get_move_towards_target(target_x, target_y, level)
                if level.is_walkable(new_x, new_y):
                    self.x, self.y = new_x, new_y
        else:
            # Wander randomly
            self.wander(level)
            
        return events if events else None
        
    def get_move_towards_player(self, player, level):
        """Calculate next move towards player"""
        dx = 0 if self.x == player.x else (1 if self.x < player.x else -1)
        dy = 0 if self.y == player.y else (1 if self.y < player.y else -1)
        
        # Try to move diagonally first, then straight
        if dx != 0 and dy != 0:
            # Try diagonal movement
            if level.is_walkable(self.x + dx, self.y + dy):
                return self.x + dx, self.y + dy
        
        # Try horizontal movement
        if dx != 0 and level.is_walkable(self.x + dx, self.y):
            return self.x + dx, self.y
            
        # Try vertical movement
        if dy != 0 and level.is_walkable(self.x, self.y + dy):
            return self.x, self.y + dy
            
        return self.x, self.y  # Can't move
        
    def get_move_towards_target(self, target_x, target_y, level):
        """Move towards a specific target position"""
        dx = 0 if self.x == target_x else (1 if self.x < target_x else -1)
        dy = 0 if self.y == target_y else (1 if self.y < target_y else -1)
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if level.is_walkable(new_x, new_y):
            return new_x, new_y
        return self.x, self.y
        
    def wander(self, level):
        """Random movement when not alert"""
        if random.random() < 0.3:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            dx, dy = random.choice(directions)
            new_x, new_y = self.x + dx, self.y + dy
            
            if level.is_walkable(new_x, new_y):
                self.x, self.y = new_x, new_y
                
    def attack_player(self, player):
        """Attack the player using monster's attack system"""
        chosen_attack = self.choose_attack()
        
        # Set cooldown for the attack
        if chosen_attack['name'] in self.attack_cooldowns:
            self.attack_cooldowns[chosen_attack['name']] = chosen_attack['cooldown']
        
        # Calculate hit chance
        hit_roll = random.random()
        if hit_roll > chosen_attack['accuracy']:
            return {
                "type": "combat",
                "attacker": self.name,
                "attack_name": chosen_attack['name'],
                "damage": 0,
                "hit": False,
                "description": f"{self.name} misses!",
                "player_died": False
            }
        
        # Calculate damage
        base_damage = chosen_attack['damage']
        damage_variance = random.randint(-4, 2)
        final_damage = max(1, base_damage + damage_variance)
        
        # Apply attack to player
        player_died = player.take_damage(final_damage)
        
        # Handle special effects
        effect_description = chosen_attack['description']
        if chosen_attack['special_effects']:
            effect_description += self.apply_special_effect(chosen_attack['special_effects'], player)
        
        return {
            "type": "combat",
            "attacker": self.name,
            "attack_name": chosen_attack['name'],
            "damage": final_damage,
            "hit": True,
            "description": effect_description,
            "player_died": player_died,
            "special_effects": chosen_attack['special_effects']
        }
        
    def apply_special_effect(self, effect, player):
        """Apply special attack effects"""
        if not effect:
            return ""
            
        effect_type = effect['type']
        
        if effect_type == 'poison':
            # Apply poison to player (would need player to support status effects)
            return f" and inflicts poison!"
        elif effect_type == 'intimidate':
            # Apply intimidation effect
            return f" and intimidates the player!"
        elif effect_type == 'armor_break':
            # Apply armor break effect
            return f" and weakens armor!"
        elif effect_type == 'magic_damage':
            # Magic damage ignores armor
            return f" with magical force!"
        
        return ""
        
    def get_drops(self):
        """Generate random drops based on monster's drop table"""
        drops = []
        drop_chances = self.data['drop_chances']
        possible_drops = self.data.get('possible_drops', {})
        
        for category, chance in drop_chances.items():
            if random.random() < chance and category in possible_drops:
                # Pick a random item from this category
                items = possible_drops[category]
                if items:
                    drops.append(random.choice(items))
                    
        return drops


class MonsterManager:
    """Manages all monsters on the current level - replaces EnemyManager"""
    
    def __init__(self):
        self.enemies = []  # Keep the same attribute name for compatibility
        self.monsters = []  # Additional reference for clarity
                    
    def spawn_monster(self, x, y, category, monster_type):
        """Spawn a specific monster type"""
        monster = Monster(x, y, category, monster_type)
        self.enemies.append(monster)
        self.monsters.append(monster)
        return monster
        
    def get_enemy_at(self, x, y):
        """Get monster at specific position - maintains EnemyManager interface"""
        for monster in self.enemies:
            if monster.x == x and monster.y == y and monster.is_alive():
                return monster
        return None
        
    def get_monster_at(self, x, y):
        """Get monster at specific position"""
        return self.get_enemy_at(x, y)
        
    def remove_dead_enemies(self):
        """Remove dead monsters from the list"""
        alive_monsters = [monster for monster in self.enemies if monster.is_alive()]
        self.enemies = alive_monsters
        self.monsters = alive_monsters
        
    def update_all(self, player, level):
        """Update all monsters (AI turns) - maintains EnemyManager interface"""
        combat_events = []
        
        for monster in self.enemies[:]:
            if monster.is_alive():
                events = monster.ai_turn(player, level)
                if events:
                    if isinstance(events, list):
                        combat_events.extend(events)
                    else:
                        combat_events.append(events)
                        
        self.remove_dead_enemies()
        
        return combat_events
        
    def get_all_positions(self):
        """Get positions of all living monsters"""
        return [(monster.x, monster.y) for monster in self.enemies if monster.is_alive()]
        
    def get_monsters_by_category(self, category):
        """Get all monsters of a specific category"""
        return [monster for monster in self.monsters if monster.category == category and monster.is_alive()]
        
    def get_total_exp_value(self):
        """Get total experience value of all living monsters"""
        return sum(monster.exp_reward for monster in self.monsters if monster.is_alive())
    
    def spawn_random_monster(self, x, y, difficulty_tier="easy"):
        """Spawn a random monster from the database by difficulty tier"""
        category, monster_type = MonsterDatabase.get_random_monster_by_tier(difficulty_tier)
        return self.spawn_monster(x, y, category, monster_type)
    
    def spawn_random_monster_by_exp(self, x, y, min_exp=0, max_exp=30):
        """Spawn a random monster within an exp reward range"""
        category, monster_type = MonsterDatabase.get_random_monster_by_difficulty(min_exp, max_exp)
        return self.spawn_monster(x, y, category, monster_type)
    
    def spawn_monster_from_category(self, x, y, category):
        """Spawn a random monster from a specific category"""
        available_types = MonsterDatabase.get_monsters_in_category(category)
        if not available_types:
            # Fallback to easy monster if category doesn't exist
            return self.spawn_random_monster(x, y, "easy")
        
        import random
        monster_type = random.choice(available_types)
        return self.spawn_monster(x, y, category, monster_type)


# Alias for backward compatibility
EnemyManager = MonsterManager
Enemy = Monster
