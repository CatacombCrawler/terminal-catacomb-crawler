"""
UI - User interface and display handling
"""

import time

class UI:
    """Handles all user interface and display operations"""
    
    def __init__(self, terminal):
        self.terminal = terminal
        self.view_radius = 15  # How far player can see
        
    def render(self, player, level):
        """Render the entire game screen"""
        print(self.terminal.clear)
        
        # Render the map
        self.render_map(player, level)
        
        # Render UI elements
        self.render_status_bar(player)
        self.render_controls()
        
    def render_map(self, player, level):
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
              
    def create_bar(self, current, maximum, width):
        """Create a text-based progress bar"""
        if maximum == 0:
            return "█" * width
            
        filled = int((current / maximum) * width)
        return "█" * filled + "░" * (width - filled)
        
    def render_controls(self):
        """Render control instructions"""
        print("\n" + "-" * 50)
        print("Controls: WASD/Arrows=Move | Q=Quit | I=Inventory")
        
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