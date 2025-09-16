"""
Game Engine - Core game loop and state management
"""

import time
from blessed import Terminal
from .player import Player
from .level import Level
from .ui import UI
from .monsters.monsters import MonsterManager as EnemyManager
from .combat import CombatManager, COMBAT_ACTIONS
from .character_creation import CharacterCreator

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
        self.character_creator = None
        
        # Combat tracking
        self.combat_stats = {
            "starting_hp": 0,
            "starting_level": 0,
            "starting_exp": 0,
            "exp_gained": 0,
            "enemies_defeated": 0
        }
        
    def initialize(self):
        """Initialize game components"""
        # Create character creator
        self.character_creator = CharacterCreator(self.terminal)
        
        # Create player and run character creation
        self.player = Player(x=5, y=5)
        
        # Run character creation process
        if not self.character_creator.create_character(self.player):
            print("Character creation cancelled. Exiting...")
            return False
        
        # Create other game objects
        self.level = Level(width=60, height=30)
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
        time.sleep(1)
        return True
        
    def run(self):
        """Main game loop"""
        self.running = True
        
        # Initialize game - if it fails, exit
        if not self.initialize():
            return
            
        self.needs_render = True
        
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
            self.show_inventory()
            self.needs_render = True
            return
        elif key.lower() == 'c':  # Character stats
            self.show_character_stats()
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
            self.start_combat_tracking()
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
            
    def show_inventory(self):
        """Show enhanced inventory with item management"""
        while True:  # Keep inventory open until user explicitly exits
            print(self.terminal.clear)
            print(self.terminal.bold + "=== INVENTORY ===" + self.terminal.normal)
            print()
            
            if not self.player.inventory:
                print("Your inventory is empty.")
                print()
            else:
                print("Items in your inventory:")
                print()
                
                for i, item in enumerate(self.player.inventory, 1):
                    # Show item with quality color and equipment status
                    quality_info = item.get_quality_info()
                    equipped_text = f" {self.terminal.green}[EQUIPPED]{self.terminal.normal}" if item.equipped else ""
                    
                    print(f"{i}. {item.symbol} {self.terminal.bold}{item.name}{self.terminal.normal}{equipped_text}")
                    print(f"   Type: {item.type.title()} | Quality: {quality_info['name']}")
                    print(f"   {item.description}")
                    
                    # Show stats
                    stat_parts = []
                    for stat, value in item.stats.items():
                        if value != 0:
                            sign = "+" if value > 0 else ""
                            color = self.terminal.green if value > 0 else self.terminal.red
                            stat_parts.append(f"{stat.upper()}: {color}{sign}{value}{self.terminal.normal}")
                    
                    if stat_parts:
                        print(f"   Stats: {' | '.join(stat_parts)}")
                    print()
            
            # Show equipped items summary
            equipped = self.player.equipment.get_equipped_items()
            if equipped:
                print(self.terminal.bold + "Currently Equipped:" + self.terminal.normal)
                for slot, item in equipped.items():
                    print(f"  {slot.replace('_', ' ').title()}: {self.terminal.yellow}{item.name}{self.terminal.normal}")
                print()
            
            print(self.terminal.bold + "Commands:" + self.terminal.normal)
            print("E = Equip/Unequip item")
            print("U = Use item") 
            print("Any other key = Back to game")
            print()
            print("Choose an action: ", end="", flush=True)
            
            key = self.terminal.inkey()
            print(key)  # Show what key was pressed
            
            if key.lower() == 'e':
                self.handle_equip_unequip()
                # Continue the loop to stay in inventory
            elif key.lower() == 'u':
                self.handle_use_item()
                # Continue the loop to stay in inventory
            else:
                print("Returning to game...")
                break
                
    def show_character_stats(self):
        """Show detailed character statistics"""
        print(self.terminal.clear)
        print(self.terminal.bold + "=== CHARACTER STATS ===" + self.terminal.normal)
        print()
        
        stats = self.player.get_stats()
        detailed = self.player.get_detailed_stats()
        
        print(f"Name: {self.terminal.bold}{stats['name']}{self.terminal.normal}")
        print(f"Level: {stats['level']} (XP: {stats['exp']}/{stats['exp_to_next']})")
        print()
        
        print("Current Stats (Base + Equipment):")
        base = detailed['base_stats']
        bonuses = detailed['equipment_bonuses']
        total = detailed['total_stats']
        
        for stat_name in ['hp', 'attack', 'defense', 'speed']:
            base_val = base[stat_name]
            bonus_val = bonuses[stat_name]
            total_val = total[stat_name]
            
            if bonus_val != 0:
                sign = "+" if bonus_val > 0 else ""
                color = self.terminal.green if bonus_val > 0 else self.terminal.red
                print(f"  {stat_name.upper()}: {total_val} ({base_val} {color}{sign}{bonus_val}{self.terminal.normal})")
            else:
                print(f"  {stat_name.upper()}: {total_val}")
                
        print(f"  Current HP: {stats['hp']}/{stats['max_hp']}")
        print()
        
        # Show equipment bonuses breakdown
        equipped = self.player.equipment.get_equipped_items()
        if equipped:
            print("Equipment Bonuses:")
            for slot, item in equipped.items():
                stat_parts = []
                for stat, value in item.stats.items():
                    if value != 0:
                        sign = "+" if value > 0 else ""
                        stat_parts.append(f"{stat.upper()}: {sign}{value}")
                
                bonus_text = " | ".join(stat_parts) if stat_parts else "No bonuses"
                print(f"  {item.name}: {bonus_text}")
        
        print()
        print("Press any key to continue...")
        self.terminal.inkey()
        
    def handle_equip_unequip(self):
        """Handle equipping/unequipping items"""
        if not self.player.inventory:
            print("No items to equip!")
            print("Press any key to continue...")
            self.terminal.inkey()
            return
            
        while True:
            print(f"\nSelect item number to equip/unequip (1-{len(self.player.inventory)}) or 0 to cancel: ", end="", flush=True)
            
            # Use terminal.inkey() to get visible input character by character
            choice_str = ""
            while True:
                key = self.terminal.inkey()
                
                # Handle backspace
                if key.name == 'KEY_BACKSPACE' and choice_str:
                    choice_str = choice_str[:-1]
                    print('\b \b', end="", flush=True)  # Clear last character
                # Handle enter
                elif key.name == 'KEY_ENTER' or key == '\r' or key == '\n':
                    break
                # Handle escape or cancel
                elif key.name == 'KEY_ESCAPE' or key.lower() == 'q':
                    print("0")  # Show cancellation
                    choice_str = "0"
                    break
                # Handle digits
                elif key.isdigit():
                    choice_str += key
                    print(key, end="", flush=True)  # Show the digit
                    
            print()  # New line after input
            
            try:
                choice = int(choice_str) if choice_str else 0
                
                if choice == 0:
                    print("Cancelled.")
                    break
                elif 1 <= choice <= len(self.player.inventory):
                    item = self.player.inventory[choice - 1]
                    print(f"Selected: {item.name}")
                    
                    if item.equipped:
                        success, message = self.player.unequip_item(item)
                    else:
                        success, message = self.player.equip_item(item)
                        
                    print(f"{message}")
                    print("Press any key to continue...")
                    self.terminal.inkey()
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.player.inventory)}, or 0 to cancel.")
                    print("Try again...")
                    
            except ValueError:
                if choice_str:
                    print(f"'{choice_str}' is not a valid number!")
                else:
                    print("Please enter a number!")
                print("Try again...")
            
    def handle_use_item(self):
        """Handle using/consuming items"""
        if not self.player.inventory:
            print("No items to use!")
            print("Press any key to continue...")
            self.terminal.inkey()
            return
            
        while True:
            print(f"\nSelect item number to use (1-{len(self.player.inventory)}) or 0 to cancel: ", end="", flush=True)
            
            # Use terminal.inkey() for visible input
            choice_str = ""
            while True:
                key = self.terminal.inkey()
                
                # Handle backspace
                if key.name == 'KEY_BACKSPACE' and choice_str:
                    choice_str = choice_str[:-1]
                    print('\b \b', end="", flush=True)
                # Handle enter
                elif key.name == 'KEY_ENTER' or key == '\r' or key == '\n':
                    break
                # Handle escape or cancel
                elif key.name == 'KEY_ESCAPE' or key.lower() == 'q':
                    print("0")
                    choice_str = "0"
                    break
                # Handle digits
                elif key.isdigit():
                    choice_str += key
                    print(key, end="", flush=True)
                    
            print()  # New line after input
            
            try:
                choice = int(choice_str) if choice_str else 0
                
                if choice == 0:
                    print("Cancelled.")
                    break
                elif 1 <= choice <= len(self.player.inventory):
                    item = self.player.inventory[choice - 1]
                    print(f"Selected: {item.name}")
                    
                    success, message = self.player.use_item(item)
                    print(f"{message}")
                    print("Press any key to continue...")
                    self.terminal.inkey()
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.player.inventory)}, or 0 to cancel.")
                    print("Try again...")
                    
            except ValueError:
                if choice_str:
                    print(f"'{choice_str}' is not a valid number!")
                else:
                    print("Please enter a number!")
                print("Try again...")
            
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
                    
                    # Check if combat ended
                    if not self.combat_manager.in_combat:
                        self.end_combat_tracking()
                        
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
                    # Dynamic monster spawning based on player level
                    if self.player.level <= 3:
                        # Early game: spawn easy monsters
                        self.enemy_manager.spawn_random_monster(x, y, "easy")
                    elif self.player.level <= 6:
                        # Mid game: mix of easy and medium monsters
                        difficulty = random.choice(["easy", "easy", "medium"])  # More easy
                        self.enemy_manager.spawn_random_monster(x, y, difficulty)
                    elif self.player.level <= 10:
                        # Late game: medium and hard monsters
                        difficulty = random.choice(["medium", "medium", "hard"])  # More medium
                        self.enemy_manager.spawn_random_monster(x, y, difficulty)
                    else:
                        # End game: hard and boss monsters
                        difficulty = random.choice(["hard", "boss"])
                        self.enemy_manager.spawn_random_monster(x, y, difficulty)
                    break
                attempts += 1
                
    def game_over(self):
        """Handle game over"""
        print(self.terminal.clear)
        print(self.terminal.red + self.terminal.bold + "GAME OVER" + self.terminal.normal)
        print(f"You reached level {self.player.level}")
        
        # Show final stats
        equipped = self.player.equipment.get_equipped_items()
        if equipped:
            print("\nFinal Equipment:")
            for slot, item in equipped.items():
                print(f"  {slot.replace('_', ' ').title()}: {item.name}")
        
        print("Press any key to exit...")
        self.terminal.inkey()
        self.running = False
        
    def start_combat_tracking(self):
        """Initialize combat statistics tracking"""
        self.combat_stats = {
            "starting_hp": self.player.hp,
            "starting_level": self.player.level,
            "starting_exp": self.player.exp,
            "exp_gained": 0,
            "enemies_defeated": 0
        }
        
    def end_combat_tracking(self):
        """Finalize combat stats and show summary"""
        # Calculate final stats
        health_lost = self.combat_stats["starting_hp"] - self.player.hp
        self.combat_stats["exp_gained"] = self.player.exp - self.combat_stats["starting_exp"]
        level_up = self.player.level > self.combat_stats["starting_level"]
        victory = self.player.hp > 0
        
        # Prepare summary data
        summary = {
            "victory": victory,
            "health_lost": health_lost,
            "exp_gained": self.combat_stats["exp_gained"],
            "enemies_defeated": self.combat_stats["enemies_defeated"],
            "level_up": level_up,
            "new_level": self.player.level if level_up else self.combat_stats["starting_level"]
        }
        
        # Show combat summary screen
        self.ui.show_combat_summary(summary, self.player)
        self.needs_render = True
        
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
            
            # Track enemy defeats
            if result.get("target_died", False):
                self.combat_stats["enemies_defeated"] += 1
            
            # End player turn
            turn_msg = self.combat_manager.end_turn()
            if turn_msg:
                self.combat_messages.append({"type": "system", "message": turn_msg})
                
                # Check if combat ended
                if not self.combat_manager.in_combat:
                    self.end_combat_tracking()
        else:
            self.combat_messages.append({"type": "system", "message": result.get("message", "Action failed!")})
            
        self.needs_render = True
        
    def enemy_combat_action(self, enemy):
        """Execute an enemy combat action"""
        # Simple AI: always attack player if alive
        if self.player.hp > 0:
            # Use the combat system's execute_attack method directly to get rich monster attacks
            action = COMBAT_ACTIONS["attack"]
            result = action.execute_attack(enemy, self.player)
            
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
            self.start_combat_tracking()
            combat_start_msg = self.combat_manager.start_combat(self.player, adjacent_enemies)
            self.combat_messages.append({"type": "system", "message": combat_start_msg})
            self.needs_render = True