"""
Enemy System - Handles monster AI, stats, and combat
"""

import random

class Enemy:
    """Base enemy class - extensible for different monster types"""
    
    def __init__(self, x, y, enemy_type="goblin"):
        # Position
        self.x = x
        self.y = y
        
        # Enemy type defines stats and appearance
        self.type = enemy_type
        self.setup_enemy_stats()
        
        # AI state
        self.last_seen_player = None
        self.alert_turns = 0
        self.max_alert = 5
        
    def setup_enemy_stats(self):
        """Setup stats based on enemy type - easily extensible"""
        enemy_data = {
            "goblin": {
                "name": "Goblin",
                "symbol": "g",
                "color": "green",
                "hp": 20,
                "attack": 6,
                "defense": 2,
                "speed": 8,
                "exp_reward": 15,
                "aggression": 0.7,
                "detection_range": 5
            },
            "orc": {
                "name": "Orc",
                "symbol": "o", 
                "color": "red",
                "hp": 35,
                "attack": 10,
                "defense": 4,
                "speed": 6,
                "exp_reward": 25,
                "aggression": 0.8,
                "detection_range": 6
            },
            "skeleton": {
                "name": "Skeleton",
                "symbol": "s",
                "color": "white", 
                "hp": 15,
                "attack": 8,
                "defense": 1,
                "speed": 14,
                "exp_reward": 12,
                "aggression": 0.9,
                "detection_range": 7
            }
        }
        
        data = enemy_data.get(self.type, enemy_data["goblin"])
        
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.color = data["color"]
        self.max_hp = data["hp"]
        self.hp = self.max_hp
        self.attack = data["attack"]
        self.defense = data["defense"]
        self.speed = data["speed"]
        self.exp_reward = data["exp_reward"]
        self.aggression = data["aggression"]
        self.detection_range = data["detection_range"]
        
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.hp > 0
        
    def take_damage(self, damage):
        """Enemy takes damage"""
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
        """Check if enemy can detect the player"""
        distance = self.get_distance_to(player.x, player.y)
        return distance <= self.detection_range
        
    def move_towards(self, target_x, target_y):
        """Move one step towards target (basic AI)"""
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        elif self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
            
    def ai_turn(self, player, level):
        """Execute AI behavior for this turn"""
        if not self.is_alive():
            return None
            
        # Check if player is visible
        if self.can_see_player(player):
            self.last_seen_player = (player.x, player.y)
            self.alert_turns = self.max_alert
            
            # If adjacent to player, attack
            if self.get_distance_to(player.x, player.y) == 1:
                return self.attack_player(player)
            
            # Otherwise, move towards player if aggressive enough
            if random.random() < self.aggression:
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
            
        return None
        
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
        """Attack the player"""
        damage = self.attack + random.randint(-2, 2)
        damage = max(1, damage)
        
        player_died = player.take_damage(damage)
        
        return {
            "type": "combat",
            "attacker": self.name,
            "damage": damage,
            "player_died": player_died
        }

class EnemyManager:
    """Manages all enemies on the current level"""
    
    def __init__(self):
        self.enemies = []
        
    def spawn_enemy(self, x, y, enemy_type="goblin"):
        """Spawn a new enemy at position"""
        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)
        return enemy
        
    def get_enemy_at(self, x, y):
        """Get enemy at specific position"""
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y and enemy.is_alive():
                return enemy
        return None
        
    def remove_dead_enemies(self):
        """Remove dead enemies from the list"""
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
        
    def update_all(self, player, level):
        """Update all enemies (AI turns)"""
        combat_events = []
        
        for enemy in self.enemies[:]:
            if enemy.is_alive():
                event = enemy.ai_turn(player, level)
                if event:
                    combat_events.append(event)
                    
        self.remove_dead_enemies()
        
        return combat_events
        
    def get_all_positions(self):
        """Get positions of all living enemies"""
        return [(enemy.x, enemy.y) for enemy in self.enemies if enemy.is_alive()]
