"""
Game Engine - Core game loop and state management
"""

import time
from blessed import Terminal
from .player import Player
from .level import Level, DoorRoom
from .ui import UI
from .monsters.monsters import MonsterManager as EnemyManager
from .combat import CombatManager, COMBAT_ACTIONS
from .character_creation import CharacterCreator
from .level_up_ui import LevelUpUI
from .terminal_utils import normal_input_mode


# Sounds
import pygame.mixer
import pygame.time

pygame.mixer.init()

game_initiate_sound = pygame.mixer.Sound('game/sounds/game-start-sound.wav')

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



        # Door room system
        self.door_rooms = {}  # Dictionary mapping door positions to DoorRoom objects
        self.current_door_room = None
        self.in_door_room = False
        
        # Level progression system
        self.dungeon_level = 1  # Current dungeon level (not player level)
        self.awaiting_stairs_confirmation = False
        
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
        
        # Sound
        character_cancel_sound = pygame.mixer.Sound('game/sounds/character_cancel_sound.wav')

        # Run character creation process
        # use try-except to handle Ctrl+C gracefully
        try:
            if not self.character_creator.create_character(self.player):
                 
                character_cancel_sound.play()
                while pygame.mixer.get_busy():
                    pygame.time.wait(1)

                print("Character creation cancelled. Exiting...")
                return False
            
        except KeyboardInterrupt:

            # Sound
            character_cancel_sound.play()
            while pygame.mixer.get_busy():
                pygame.time.wait(1)  # Waits for sound to finish

            print("\nCharacter creation cancelled. Exiting...")
            return False
        
        # Create other game objects
        self.level = Level(width=60, height=30)
        self.ui = UI(self.terminal)
        self.level_up_ui = LevelUpUI(self.terminal)
        self.enemy_manager = EnemyManager()
        
        # Generate initial level
        self.level.generate()
        
        # Place player in a valid starting position
        start_x, start_y = self.level.get_random_floor_position()
        self.player.x = start_x

        self.player.y = start_y
        # Spawn some enemies
        self.spawn_initial_enemies()

        # sound
        game_initiate_sound.play()


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
                    current_level = self.current_door_room if self.in_door_room else self.level
                    self.ui.render(self.player, current_level, self.enemy_manager, self.combat_messages, 
                                 self.dungeon_level, self.in_door_room, self.awaiting_stairs_confirmation)
                    # Clear old combat messages after showing them
                    if len(self.combat_messages) > 8:
                        self.combat_messages = self.combat_messages[-5:]
                    self.needs_render = False
                
                # Handle input
                self.handle_input()
                
                # Update game state
                self.update()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.05)
        
        # Game ended
        print(self.terminal.clear)

        # --ADD SOUND IN FUTURE VERSIONS

        print("Thanks for playing Terminal Dungeon Crawler!")
        
    def handle_input(self):
        """Handle player input"""
        key = self.terminal.inkey(timeout=0.1)
        
        if not key:
            return
        
        # Handle stairs confirmation input
        if self.awaiting_stairs_confirmation:
            if key.lower() == 'y':
                self.confirm_stairs_descent(True)
            elif key.lower() == 'n':
                self.confirm_stairs_descent(False)
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
        elif key.lower() == 'l':  # Level up / stat allocation
            if self.player.stat_points > 0:
                self.level_up_ui.show_level_up_screen(self.player)
                self.needs_render = True
            else:
                # Show a message that no stat points are available
                print(self.terminal.clear)
                print(f"{self.terminal.yellow}No stat points available to allocate.{self.terminal.normal}")
                print("Gain experience and level up to earn more stat points!")
                print("Press Enter to continue...")
                # use inkey so it works under cbreak on all platforms
                self.terminal.inkey()
                self.needs_render = True
            return
            
        # Combat input handling
        if self.combat_manager.in_combat:
            self.handle_combat_input(key)
        else:
            self.handle_exploration_input(key)
            
    def handle_exploration_input(self, key):
        """Handle input during exploration (non-combat)"""


        # -- ADD SOUND
        key_sound = pygame.mixer.Sound('game/sounds/ui-button-click-5-327756.wav')
        key_sound.set_volume(0.2)


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
            
        elif key.lower() == 'e':
            # Interaction key - check for doors
            self.handle_door_interaction()
            return
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
        
        key_sound.play()   

        # Try to move player
        if self.can_move_to(new_x, new_y):
            self.player.move(new_x, new_y)
            self.check_for_enemy_encounters()
            self.needs_render = True
    
    def handle_door_interaction(self):
        """Handle interaction with doors and stairs"""
        player_x, player_y = self.player.x, self.player.y
        
        if self.in_door_room:
            # Check if player is at the exit door
            if self.current_door_room and self.current_door_room.get_tile(player_x, player_y) == '+':
                # Exit the door room
                self.exit_door_room()
                return
        else:
            # Check if player is standing on something interactable
            current_tile = self.level.get_tile(player_x, player_y)
            
            if current_tile == self.level.DOOR:
                self.enter_door_room(player_x, player_y)
                return
            elif current_tile == self.level.STAIRS_DOWN:
                # Show warning and handle stairs down
                self.handle_stairs_down()
                return
            
            # Also check adjacent tiles for interactables on the main level
            adjacent_positions = [
                (player_x, player_y - 1),  # North
                (player_x, player_y + 1),  # South
                (player_x - 1, player_y),  # West
                (player_x + 1, player_y)   # East
            ]
            
            for x, y in adjacent_positions:
                if (0 <= x < self.level.width and 0 <= y < self.level.height):
                    tile = self.level.get_tile(x, y)
                    if tile == self.level.DOOR:
                        # Enter the door room
                        self.enter_door_room(x, y)
                        return
                    elif tile == self.level.STAIRS_DOWN:
                        # Show warning and handle stairs down
                        self.handle_stairs_down()
                        return
    
    def enter_door_room(self, door_x, door_y):
        """Enter a door room"""
        door_key = f"{door_x},{door_y}"
        
        # Create door room if it doesn't exist
        if door_key not in self.door_rooms:
            self.door_rooms[door_key] = DoorRoom(door_x, door_y)
        
        door_room = self.door_rooms[door_key]
        
        # Generate the room if not already generated
        if not door_room.generated:
            door_room.generate()
        
        # Set current state
        self.current_door_room = door_room
        self.in_door_room = True
        
        # Move player to entrance
        self.player.move(door_room.entrance_x, door_room.entrance_y)
        
        # Spawn enemies in the door room
        self.spawn_door_room_enemies()
        
        self.needs_render = True
    
    def exit_door_room(self):
        """Exit the current door room"""
        if self.current_door_room:
            # Return player to door position on main level
            self.player.move(self.current_door_room.door_x, self.current_door_room.door_y)
            
            # Reset door room state (but keep the room in memory)
            self.current_door_room = None
            self.in_door_room = False
            
            self.needs_render = True
    
    def spawn_door_room_enemies(self):
        """Spawn enemies in the current door room (only if not already spawned)"""
        if not self.current_door_room:
            return
        
        # Get active enemy positions (those that haven't been defeated)
        active_positions = self.current_door_room.get_active_enemy_positions()
        
        # Check if enemies are already spawned in this room
        enemies_already_present = False
        for x, y in active_positions:
            if self.enemy_manager.get_enemy_at(x, y):
                enemies_already_present = True
                break
        
        # Only spawn enemies if they haven't been spawned yet and room hasn't been fully cleared
        if not enemies_already_present and active_positions:
            # Spawn enemies at the active positions only
            for x, y in active_positions:
                # Use level-based spawning for door rooms, but keep them slightly easier
                # Cap the effective level to make door rooms more manageable
                effective_player_level = max(1, self.player.level - 1)
                self.enemy_manager.spawn_monster_by_level(x, y, effective_player_level)
            
            # Mark that enemies have been spawned for this room
            self.current_door_room.enemies_spawned = True
    
    def clear_door_room_enemies(self):
        """Clear all enemies from the current door room"""
        if not self.current_door_room:
            return
        
        # Remove enemies at door room positions
        enemies_to_remove = []
        for enemy in self.enemy_manager.enemies:
            for x, y in self.current_door_room.enemy_positions:
                if enemy.x == x and enemy.y == y:
                    enemies_to_remove.append(enemy)
        
        for enemy in enemies_to_remove:
            if hasattr(self.enemy_manager, 'remove_enemy'):
                self.enemy_manager.remove_enemy(enemy)
            else:
                # Fallback: just remove from the list
                if enemy in self.enemy_manager.enemies:
                    self.enemy_manager.enemies.remove(enemy)
    
    def track_defeated_door_enemies(self):
        """Track which enemies in door rooms have been defeated"""
        if not self.in_door_room or not self.current_door_room:
            return
        
        # Check each enemy position in the current door room
        for x, y in self.current_door_room.enemy_positions:
            # If there's no enemy at this position anymore, mark it as defeated
            if not self.enemy_manager.get_enemy_at(x, y):
                if (x, y) not in self.current_door_room.defeated_enemy_positions:
                    self.current_door_room.mark_enemy_defeated(x, y)
    
    def handle_stairs_down(self):
        """Handle stairs down interaction with warning"""
        if not self.awaiting_stairs_confirmation:
            # Show warning screen
            self.show_stairs_warning()
            self.awaiting_stairs_confirmation = True
            # Don't set needs_render = True here, let the warning stay on screen
        
    def show_stairs_warning(self):
        """Show warning about going down stairs"""
        # Sound
        warning_sound = pygame.mixer.Sound('game/sounds/quotwarningquot-175692.wav')
        warning_sound.play()

        print(self.terminal.clear)
        print(self.terminal.bold + self.terminal.red + "WARNING!" + self.terminal.normal)
        print()
        print("You are about to descend to the next dungeon level.")
        print()
        print(self.terminal.yellow + "Benefits of going down:" + self.terminal.normal)
        print("• +20% Maximum Health")
        print("• +20% Experience Bonus")
        print("• New challenges and enemies")
        print()
        print(self.terminal.red + "WARNING: You cannot return to previous levels!" + self.terminal.normal)
        print()
        print("Are you sure you want to continue?")
        print()
        print(self.terminal.bold + "Y = Yes, descend to next level" + self.terminal.normal)
        print(self.terminal.bold + "N = No, stay on current level" + self.terminal.normal)
        print()
        
    def confirm_stairs_descent(self, confirm):
        """Handle stairs descent confirmation"""
        self.awaiting_stairs_confirmation = False
        
        if confirm:
            self.descend_to_next_level()
        else:
            # Player chose not to descend, just return to normal game
            self.needs_render = True
    
    def descend_to_next_level(self):
        """Descend to the next dungeon level"""
        # Increment dungeon level
        self.dungeon_level += 1
        
        # Apply bonuses to player
        old_max_hp = self.player.max_hp
        
        # +20% health bonus
        health_bonus = int(self.player.base_max_hp * 0.2)
        self.player.base_max_hp += health_bonus
        self.player.recalculate_stats()  # This will update max_hp
        
        # Heal player to full health (they earned it!)
        self.player.hp = self.player.max_hp
        
        # +20% experience bonus (based on exp needed for next level)
        exp_bonus = int(self.player.exp_to_next * 0.2)
        self.player.gain_exp(exp_bonus)
        
        # Clear all enemies and door rooms
        self.enemy_manager.enemies.clear()
        if hasattr(self.enemy_manager, 'monsters'):
            self.enemy_manager.monsters.clear()
        self.door_rooms.clear()
        self.current_door_room = None
        self.in_door_room = False
        
        # Generate new level
        self.level.generate()
        
        # Place player in a new starting position
        start_x, start_y = self.level.get_random_floor_position()
        self.player.x = start_x
        self.player.y = start_y
        
        # Spawn enemies for the new level (more challenging)
        self.spawn_enemies_for_level(self.dungeon_level)
        
        # Show level transition message
        self.show_level_transition_message(health_bonus, exp_bonus)
        
        # Now render the new level
        self.needs_render = True
    
    def spawn_enemies_for_level(self, dungeon_level):

        """Spawn enemies appropriate for the dungeon level"""
        # More enemies on deeper levels
        base_enemies = 3
        bonus_enemies = min(dungeon_level - 1, 4)  # Cap at +4 bonus enemies
        num_enemies = random.randint(base_enemies + bonus_enemies, base_enemies + bonus_enemies + 2)
        
        for _ in range(num_enemies):
            attempts = 0
            while attempts < 50:
                x, y = self.level.get_random_floor_position()
                
                # Make sure enemy isn't too close to player
                distance = abs(x - self.player.x) + abs(y - self.player.y)
                if distance > 8:
                    # Use level-based spawning - the deeper you go, the slightly higher level monsters
                    # Dungeon level adds some challenge by occasionally spawning higher level enemies
                    effective_player_level = self.player.level
                    if dungeon_level > 3:
                        # At deeper levels, occasionally spawn enemies 1-2 levels higher
                        if random.random() < 0.3:  # 30% chance
                            effective_player_level += min(2, dungeon_level - 3)
                    
                    self.enemy_manager.spawn_monster_by_level(x, y, effective_player_level)
                    break
                attempts += 1
    
    def show_level_transition_message(self, health_bonus, exp_bonus):
        """Show message about level transition bonuses"""
        print(self.terminal.clear)
        print(self.terminal.bold + self.terminal.green + f"Welcome to Dungeon Level {self.dungeon_level}!" + self.terminal.normal)
        print()
        print("You have been strengthened by your descent:")
        print(f"• Health increased by {health_bonus} points!")
        print(f"• Gained {exp_bonus} bonus experience!")
        print(f"• Your maximum health is now {self.player.max_hp}")
        print()
        print("New challenges await...")
        print()
        print("Press any key to continue...")
        
        # Wait for user input
        self.terminal.inkey()
            
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
        
        stat_map = {"hp": "health", "attack": "attack", "defense": "defense", "speed": "speed"}
        for display_name, internal_name in stat_map.items():
            base_val = base.get(internal_name, 0)
            bonus_val = bonuses.get(internal_name, 0)
            total_val = total.get(internal_name, 0)

            if bonus_val != 0:
                sign = "+" if bonus_val > 0 else ""
                color = self.terminal.green if bonus_val > 0 else self.terminal.red
                print(
                    f"  {display_name.upper()}: {total_val} ({base_val} {color}{sign}{bonus_val}{self.terminal.normal})"
                )
            else:
                print(f"  {display_name.upper()}: {total_val}")
                
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
        if self.in_door_room and self.current_door_room:
            # Check bounds for door room
            if not (0 <= x < self.current_door_room.width and 0 <= y < self.current_door_room.height):
                return False
                
            # Check if it's a walkable tile in door room
            if not self.current_door_room.is_walkable(x, y):
                return False
        else:
            # Check bounds for main level
            if not (0 <= x < self.level.width and 0 <= y < self.level.height):
                return False
                
            # Check if it's a walkable tile on main level
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
        
        # Track defeated enemies in door rooms
        self.track_defeated_door_enemies()
        
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
                        # Handle both single message and list of messages
                        if isinstance(action_result, list):
                            self.combat_messages.extend(action_result)
                        else:
                            self.combat_messages.append(action_result)
                        self.needs_render = True
                        
                # End enemy turn
                turn_msg = self.combat_manager.end_turn()
                if turn_msg:
                    # Add separator for new rounds to make them more readable
                    if "Round" in turn_msg and "begins" in turn_msg:
                        # Keep important message types and recent combat actions
                        if len(self.combat_messages) > 8:
                            # Preserve important message types in the last few messages
                            important_messages = []
                            for msg in self.combat_messages[-8:]:
                                msg_type = msg.get("type", "")
                                if msg_type in ["combat", "deflection", "combat_detail", "system"]:
                                    important_messages.append(msg)
                            self.combat_messages = important_messages[-6:] if important_messages else self.combat_messages[-3:]
                        self.combat_messages.append({"type": "round_separator", "message": "---"})
                    
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
                    # Use level-based spawning system
                    self.enemy_manager.spawn_monster_by_level(x, y, self.player.level)
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
        
        # Check for level up and show stat allocation if needed
        if level_up and self.player.stat_points > 0:
            self.level_up_ui.show_level_up_screen(self.player)
        
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
            
            # Add separate deflection message if damage was deflected (user prefers this format)
            deflected = result.get("deflected", 0)
            if deflected > 0:
                damage_reduction = result.get("damage_reduction", 0)
                if damage_reduction > 0:
                    detailed_message = f"Hero deflects {deflected} damage ({damage_reduction:.1f}% reduction)"
                else:
                    detailed_message = f"Hero deflects {deflected} damage"
                
                self.combat_messages.append({
                    "type": "deflection", 
                    "message": detailed_message
                })
            
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
        """Execute an enemy combat action - Use monster's detailed attack system directly"""
        if self.player.hp > 0:
            # Call monster's attack_player method directly to get rich, detailed messages
            monster_result = enemy.attack_player(self.player)
            
            # Create the combat message using the monster's detailed info
            combat_message = {
                "type": "combat",
                "success": monster_result.get("hit", False),
                "attacker": monster_result.get("attacker", enemy.name),
                "attack_name": monster_result.get("attack_name", "Attack"),
                "damage": monster_result.get("damage", 0),
                "deflected": monster_result.get("deflected", 0),
                "hit": monster_result.get("hit", False),
                "description": monster_result.get("description", ""),
                "special_effects": monster_result.get("special_effects")
            }
            
            messages = [combat_message]
            
            # Add separate deflection message if damage was deflected (user prefers this format)
            deflected = monster_result.get("deflected", 0)
            if deflected > 0:
                damage_reduction = monster_result.get("damage_reduction", 0)
                if damage_reduction > 0:
                    detailed_message = f"Hero deflects {deflected} damage ({damage_reduction:.1f}% reduction)"
                else:
                    detailed_message = f"Hero deflects {deflected} damage"
                messages.append({"type": "deflection", "message": detailed_message})
            
            # Add detailed miss/dodge information if attack failed
            elif not monster_result.get("hit", False):
                if monster_result.get("dodged"):
                    dodge_roll = monster_result.get("dodge_roll", 0) * 100
                    dodge_chance = monster_result.get("player_dodge_chance", 0) * 100
                    detail_msg = f"💨 Dodge successful: Rolled {dodge_roll:.0f}% ≤ {dodge_chance:.0f}% dodge chance"
                    messages.append({"type": "combat_detail", "message": detail_msg})
                elif monster_result.get("hit_roll") is not None:
                    hit_roll = monster_result.get("hit_roll", 0) * 100
                    accuracy = monster_result.get("monster_accuracy", 0) * 100
                    detail_msg = f"🎯 Attack missed: Needed ≤{accuracy:.0f}%, rolled {hit_roll:.0f}%"
                    messages.append({"type": "combat_detail", "message": detail_msg})
            
            return messages if len(messages) > 1 else combat_message
            
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