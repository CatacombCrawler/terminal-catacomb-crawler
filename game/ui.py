"""
UI - User interface and display handling
"""

import time

class UI:
    """Handles all user interface and display operations"""
    
    def __init__(self, terminal):
        self.terminal = terminal
        self.view_radius = 25  # How far player can see - increased for better visibility
        
    def render(self, player, level, enemy_manager=None, combat_messages=None):
        """Render the entire game screen"""
        print(self.terminal.clear)
        
        # Determine combat state
        in_combat = hasattr(enemy_manager, 'combat_manager') and getattr(enemy_manager.combat_manager, 'in_combat', False) if enemy_manager else False
        is_player_turn = False
        if hasattr(enemy_manager, 'combat_manager') and enemy_manager.combat_manager:
            is_player_turn = enemy_manager.combat_manager.is_player_turn()
        
        if in_combat:
            # Combat mode - show only stats and combat info
            self.render_combat_screen(player, enemy_manager, combat_messages, is_player_turn)
        else:
            # Exploration mode - show map and normal UI
            self.render_exploration_screen(player, level, enemy_manager, combat_messages)
            
    def render_exploration_screen(self, player, level, enemy_manager, combat_messages):
        """Render the exploration screen with map"""
        # Render the map
        self.render_map(player, level, enemy_manager)
        
        # Render UI elements
        self.render_status_bar(player)
        # No combat messages during exploration
        self.render_controls(in_combat=False, is_player_turn=False)
        
    def render_combat_screen(self, player, enemy_manager, combat_messages, is_player_turn):
        """Render the combat screen without map"""
        print(self.terminal.bold + "=== COMBAT MODE ===" + self.terminal.normal)
        print()
        
        # Show combat status
        if hasattr(enemy_manager, 'combat_manager') and enemy_manager.combat_manager:
            combat_status = enemy_manager.combat_manager.get_combat_status()
            print(self.terminal.yellow(combat_status))
            print()
        
        # Show only health and exp (compact version)
        self.render_combat_status_bar(player)
        
        # Show combat participants
        self.render_combat_participants(enemy_manager)
        
        # Show combat messages
        self.render_combat_messages(combat_messages)
        
        # Show combat controls
        self.render_controls(in_combat=True, is_player_turn=is_player_turn)
        
    def render_map(self, player, level, enemy_manager=None):
        """Render the dungeon map centered on player"""
        # Calculate view bounds
        start_x = max(0, player.x - self.view_radius)
        end_x = min(level.width, player.x + self.view_radius + 1)
        start_y = max(0, player.y - self.view_radius)
        end_y = min(level.height, player.y + self.view_radius + 1)
        
        # Render each row
        for y in range(start_y, end_y):
            row = ""
            for x in range(start_x, end_x):
                if x == player.x and y == player.y:
                    # Player position
                    row += self.terminal.bold + self.terminal.yellow(player.symbol)
                elif enemy_manager and enemy_manager.get_enemy_at(x, y):
                    # Enemy position
                    enemy = enemy_manager.get_enemy_at(x, y)
                    row += self.colorize_enemy(enemy)
                else:
                    # Get the tile and apply color
                    tile = level.get_tile(x, y)
                    row += self.colorize_tile(tile)
            print(row)
            
    def colorize_tile(self, tile):
        """Apply colors to different tile types"""
        if tile == '#':  # Wall
            return self.terminal.white(tile)
        elif tile == '.':  # Floor
            return self.terminal.normal + tile
        elif tile == '+':  # Door
            return self.terminal.yellow(tile)
        elif tile == '>':  # Stairs down
            return self.terminal.cyan(tile)
        elif tile == '<':  # Stairs up
            return self.terminal.cyan(tile)
        else:
            return tile
            
    def colorize_enemy(self, enemy):
        """Apply colors to enemy symbols"""
        color_map = {
            "green": self.terminal.green,
            "red": self.terminal.red,
            "white": self.terminal.white,
            "blue": self.terminal.blue,
            "magenta": self.terminal.magenta
        }
        
        color_func = color_map.get(enemy.color, self.terminal.red)
        return color_func(enemy.symbol)
            
    def render_status_bar(self, player):
        """Render player status information"""
        stats = player.get_stats()
        
        print("\n" + "=" * 50)
        
        # Health bar
        hp_percent = stats['hp'] / stats['max_hp']
        hp_color = self.terminal.green if hp_percent > 0.6 else \
                   self.terminal.yellow if hp_percent > 0.3 else \
                   self.terminal.red
        
        hp_bar = self.create_bar(stats['hp'], stats['max_hp'], 20)
        print(f"Health: {hp_color}{hp_bar}{self.terminal.normal} "
              f"({stats['hp']}/{stats['max_hp']})")
        
        # Experience bar
        exp_bar = self.create_bar(stats['exp'], stats['exp_to_next'], 20)
        print(f"EXP:    {self.terminal.blue}{exp_bar}{self.terminal.normal} "
              f"({stats['exp']}/{stats['exp_to_next']})")
        
        # Stats
        print(f"Level: {stats['level']} | "
              f"Attack: {stats['attack']} | "
              f"Defense: {stats['defense']} | "
              f"Position: ({stats['position'][0]}, {stats['position'][1]})")
              
    def render_combat_status_bar(self, player):
        """Render compact player status for combat"""
        stats = player.get_stats()
        
        print("=" * 50)
        
        # Health bar
        hp_percent = stats['hp'] / stats['max_hp']
        hp_color = self.terminal.green if hp_percent > 0.6 else \
                   self.terminal.yellow if hp_percent > 0.3 else \
                   self.terminal.red
        
        hp_bar = self.create_bar(stats['hp'], stats['max_hp'], 20)
        print(f"Health: {hp_color}{hp_bar}{self.terminal.normal} "
              f"({stats['hp']}/{stats['max_hp']})")
        
        # Experience bar
        exp_bar = self.create_bar(stats['exp'], stats['exp_to_next'], 20)
        print(f"EXP:    {self.terminal.blue}{exp_bar}{self.terminal.normal} "
              f"({stats['exp']}/{stats['exp_to_next']})")
        
        print()
        
    def render_combat_participants(self, enemy_manager):
        """Show all participants in combat"""
        if not hasattr(enemy_manager, 'combat_manager') or not enemy_manager.combat_manager:
            return
            
        print(self.terminal.bold + "Combat Participants:" + self.terminal.normal)
        
        for i, participant in enumerate(enemy_manager.combat_manager.combat_participants):
            entity = participant["entity"]
            is_current = i == enemy_manager.combat_manager.current_turn_index
            
            if participant["type"] == "player":
                name = f"⚡ {entity.name}"
                hp_info = f"HP: {entity.hp}/{entity.max_hp}"
            else:  # enemy
                name = f"👹 {entity.name}"
                hp_info = f"HP: {entity.hp}/{entity.max_hp}" if entity.is_alive() else "DEAD"
                
            marker = " <-- CURRENT TURN" if is_current else ""
            color = self.terminal.yellow if is_current else self.terminal.normal
            
            print(color + f"  {name} - {hp_info}{marker}" + self.terminal.normal)
            
        print()
              
    def render_combat_messages(self, combat_messages):
        """Render recent combat messages"""
        if not combat_messages:
            return
            
        print("\n" + "-" * 50)
        print("Combat Log:")
        
        # Show last 3 combat messages to avoid clutter
        recent_messages = combat_messages[-3:] if len(combat_messages) > 3 else combat_messages
        
        for msg in recent_messages:
            if msg["type"] == "combat":
                if "target" in msg:  # Player attacking enemy
                    text = f"{msg['attacker']} attacks {msg['target']} for {msg['damage']} damage!"
                    if msg.get("target_died"):
                        text += f" {msg['target']} defeated! (+{msg.get('exp_gained', 0)} XP)"
                    print(self.terminal.green(text))
                elif "defender" in msg:  # Defend action
                    print(self.terminal.blue(msg["message"]))
                else:  # Enemy attacking player
                    text = f"{msg['attacker']} attacks you for {msg['damage']} damage!"
                    if msg.get("player_died"):
                        text += " You have fallen!"
                    print(self.terminal.red(text))
            elif msg["type"] == "system":
                print(self.terminal.yellow(msg["message"]))
              
    def create_bar(self, current, maximum, width):
        """Create a text-based progress bar"""
        if maximum == 0:
            return "█" * width
            
        filled = int((current / maximum) * width)
        return "█" * filled + "░" * (width - filled)
        
    def render_controls(self, in_combat=False, is_player_turn=False):
        """Render control instructions"""
        print("\n" + "-" * 50)
        
        if in_combat:
            if is_player_turn:
                print("COMBAT - Your Turn: A=Attack | D=Defend | Q=Quit | I=Inventory")
            else:
                print("COMBAT - Enemy Turn: Wait for your turn...")
        else:
            print("EXPLORATION: WASD/Arrows=Move | Q=Quit | I=Inventory")
        
    def show_inventory(self, player):
        """Display player inventory (placeholder for now)"""
        print(self.terminal.clear)
        print(self.terminal.bold + "=== INVENTORY ===" + self.terminal.normal)
        
        if not player.inventory:
            print("Your inventory is empty.")
        else:
            for i, item in enumerate(player.inventory):
                print(f"{i + 1}. {item}")
                
        print("\nPress any key to continue...")
        self.terminal.inkey()
        
    def show_message(self, message, duration=2):
        """Show a temporary message"""
        # For now, just print it. Later we can add a message log
        print(f"\n>>> {message}")
        time.sleep(duration)