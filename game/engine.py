"""
Game Engine - Core game loop and state management
"""

import time
from blessed import Terminal
from .player import Player
from .level import Level
from .ui import UI
from .enemy import EnemyManager
from .combat import CombatManager, COMBAT_ACTIONS

class GameEngine:
    """Main game engine that handles the core game loop"""
    
    def __init__(self):
        self.terminal = Terminal()
        self.running = False
        self.player = None
        self.level = None
        self.ui = None
        self.enemy_manager = None
        self.combat_manager = CombatManager()
        self.combat_messages = []
        
    def initialize(self):
        """Initialize game components"""
        # Create game objects
        self.player = Player(x=5, y=5)  # Starting position
        self.level = Level(width=60, height=30)  # Made level bigger too
        self.ui = UI(self.terminal)
        self.enemy_manager = EnemyManager()
        
        # Generate initial level
        self.level.generate()
        
        # Place player in a valid starting position
        start_x, start_y = self.level.get_random_floor_position()
        self.player.x = start_x
        self.player.y = start_y
        
        # Spawn some enemies
        self.spawn_initial_enemies()
        
        print("Game initialized successfully!")
        time.sleep(1)  # Brief pause
        
    def run(self):
        """Main game loop"""
        self.running = True
        self.initialize()
        self.needs_render = True  # Flag to control when to render
        
        with self.terminal.cbreak(), self.terminal.hidden_cursor():
            while self.running:
                # Only render if something changed
                if self.needs_render:
                    # Add combat manager to enemy manager for UI access
                    self.enemy_manager.combat_manager = self.combat_manager
                    self.ui.render(self.player, self.level, self.enemy_manager, self.combat_messages)
                    # Clear old combat messages after showing them
                    if len(self.combat_messages) > 5:
                        self.combat_messages = self.combat_messages[-3:]
                    self.needs_render = False
                
                # Handle input
                self.handle_input()
                
                # Update game state
                self.update()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.05)
        
        # Game ended
        print(self.terminal.clear)
        print("Thanks for playing Terminal Dungeon Crawler!")
        
    def handle_input(self):
        """Handle player input"""
        key = self.terminal.inkey(timeout=0.1)
        
        if not key:
            return
            
        # Global commands (work in and out of combat)
        if key.lower() == 'q':
            self.running = False
            return
        elif key.lower() == 'i':
            self.ui.show_inventory(self.player)
            self.needs_render = True
            return
            
        # Combat input handling
        if self.combat_manager.in_combat:
            self.handle_combat_input(key)
        else:
            self.handle_exploration_input(key)
            
    def handle_exploration_input(self, key):
        """Handle input during exploration (non-combat)"""
        # Movement keys
        new_x, new_y = self.player.x, self.player.y
        
        if key.lower() == 'w' or key.code == self.terminal.KEY_UP:
            new_y -= 1
        elif key.lower() == 's' or key.code == self.terminal.KEY_DOWN:
            new_y += 1
        elif key.lower() == 'a' or key.code == self.terminal.KEY_LEFT:
            new_x -= 1
        elif key.lower() == 'd' or key.code == self.terminal.KEY_RIGHT:
            new_x += 1
        else:
            return  # Invalid exploration key
            
        # Check if there's an enemy at the target position
        enemy = self.enemy_manager.get_enemy_at(new_x, new_y)
        if enemy:
            # Start combat!
            nearby_enemies = self.get_nearby_enemies(self.player.x, self.player.y, radius=1)
            combat_start_msg = self.combat_manager.start_combat(self.player, nearby_enemies)
            self.combat_messages.append({"type": "system", "message": combat_start_msg})
            self.needs_render = True
            return
            
        # Try to move player
        if self.can_move_to(new_x, new_y):
            self.player.move(new_x, new_y)
            self.check_for_enemy_encounters()
            self.needs_render = True
            
    def handle_combat_input(self, key):
        """Handle input during combat"""
        if not self.combat_manager.is_player_turn():
            return  # Not player's turn
            
        # Combat action keys
        if key.lower() == 'a':  # Attack
            self.player_combat_action("attack")
        elif key.lower() == 'd':  # Defend  
            self.player_combat_action("defend")
        # Future: More combat actions
        # elif key.lower() == 'h':  # Heal/use item
        # elif key.lower() == 's':  # Cast spell
            
    def can_move_to(self, x, y):
        """Check if the player can move to the given position"""
        # Check bounds
        if not (0 <= x < self.level.width and 0 <= y < self.level.height):
            return False
            
        # Check if it's a walkable tile
        if not self.level.is_walkable(x, y):
            return False
            
        # Check if there's an enemy (can't move into enemy, must attack)
        if self.enemy_manager.get_enemy_at(x, y):
            return False
            
        return True
        
    def update(self):
        """Update game state each frame"""
        if self.combat_manager.in_combat:
            self.update_combat()
        else:
            # Check for random enemy encounters or other events
            pass
        
        # Check if player died
        if self.player.hp <= 0:
            self.game_over()
            
    def update_combat(self):
        """Update combat state"""
        # Process enemy turns
        if not self.combat_manager.is_player_turn():
            current_actor = self.combat_manager.get_current_actor()
            if current_actor and current_actor["type"] == "enemy":
                enemy = current_actor["entity"]
                if enemy.is_alive():
                    # Enemy takes action
                    action_result = self.enemy_combat_action(enemy)
                    if action_result:
                        self.combat_messages.append(action_result)
                        self.needs_render = True
                        
                # End enemy turn
                turn_msg = self.combat_manager.end_turn()
                if turn_msg:
                    self.combat_messages.append({"type": "system", "message": turn_msg})
                    self.needs_render = True
            
    def spawn_initial_enemies(self):
        """Spawn initial enemies on the level"""
        import random
        
        # Spawn 3-6 enemies randomly
        num_enemies = random.randint(3, 6)
        
        for _ in range(num_enemies):
            # Find a random floor position away from player
            attempts = 0
            while attempts < 50:  # Don't infinite loop
                x, y = self.level.get_random_floor_position()
                
                # Make sure enemy isn't too close to player
                distance = abs(x - self.player.x) + abs(y - self.player.y)
                if distance > 8:  # At least 8 tiles away
                    # Randomly choose enemy type
                    enemy_types = ["goblin", "goblin", "orc", "skeleton"]  # More goblins
                    enemy_type = random.choice(enemy_types)
                    self.enemy_manager.spawn_enemy(x, y, enemy_type)
                    break
                attempts += 1
                
    def game_over(self):
        """Handle game over"""
        print(self.terminal.clear)
        print(self.terminal.red + self.terminal.bold + "GAME OVER" + self.terminal.normal)
        print(f"You reached level {self.player.level}")
        print("Press any key to exit...")
        self.terminal.inkey()
        self.running = False
        
    def player_combat_action(self, action_name):
        """Execute a player combat action"""
        if action_name not in COMBAT_ACTIONS:
            return
            
        action = COMBAT_ACTIONS[action_name]
        
        # Get target if needed
        target = None
        if action.target_type == "enemy":
            target = self.get_combat_target()
            
        if action.target_type == "enemy" and not target:
            self.combat_messages.append({"type": "system", "message": "No valid target!"})
            return
            
        # Execute action
        result = action.execute(self.player, target)
        
        if result["success"]:
            self.combat_messages.append({"type": "combat", **result})
            
            # End player turn
            turn_msg = self.combat_manager.end_turn()
            if turn_msg:
                self.combat_messages.append({"type": "system", "message": turn_msg})
        else:
            self.combat_messages.append({"type": "system", "message": result.get("message", "Action failed!")})
            
        self.needs_render = True
        
    def enemy_combat_action(self, enemy):
        """Execute an enemy combat action"""
        # Simple AI: always attack player if alive
        if self.player.hp > 0:
            action = COMBAT_ACTIONS["attack"]
            result = action.execute(enemy, self.player)
            
            if result["success"]:
                return {"type": "combat", **result}
                
        return None
        
    def get_combat_target(self):
        """Get the closest enemy as combat target"""
        min_distance = float('inf')
        closest_enemy = None
        
        for participant in self.combat_manager.combat_participants:
            if participant["type"] == "enemy" and participant["entity"].is_alive():
                enemy = participant["entity"]
                distance = abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                    
        return closest_enemy
        
    def get_nearby_enemies(self, x, y, radius=1):
        """Get all enemies within radius of position"""
        nearby = []
        for enemy in self.enemy_manager.enemies:
            if enemy.is_alive():
                distance = abs(enemy.x - x) + abs(enemy.y - y)
                if distance <= radius:
                    nearby.append(enemy)
        return nearby
        
    def check_for_enemy_encounters(self):
        """Check if player has moved adjacent to enemies"""
        adjacent_enemies = self.get_nearby_enemies(self.player.x, self.player.y, radius=1)
        if adjacent_enemies:
            # Start combat with adjacent enemies
            combat_start_msg = self.combat_manager.start_combat(self.player, adjacent_enemies)
            self.combat_messages.append({"type": "system", "message": combat_start_msg})
            self.needs_render = True