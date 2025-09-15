"""
Game Engine - Core game loop and state management
"""

import time
from blessed import Terminal
from .player import Player
from .level import Level
from .ui import UI

class GameEngine:
    """Main game engine that handles the core game loop"""
    
    def __init__(self):
        self.terminal = Terminal()
        self.running = False
        self.player = None
        self.level = None
        self.ui = None
        
    def initialize(self):
        """Initialize game components"""
        # Create game objects
        self.player = Player(x=5, y=5)  # Starting position
        self.level = Level(width=40, height=20)
        self.ui = UI(self.terminal)
        
        # Generate initial level
        self.level.generate()
        
        # Place player in a valid starting position
        start_x, start_y = self.level.get_random_floor_position()
        self.player.x = start_x
        self.player.y = start_y
        
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
                    self.ui.render(self.player, self.level)
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
        elif key.lower() == 'q':
            self.running = False
            return
        elif key.lower() == 'i':
            self.ui.show_inventory(self.player)
            self.needs_render = True  # Inventory closed, need to re-render
            return
            
        # Try to move player
        if self.can_move_to(new_x, new_y):
            self.player.move(new_x, new_y)
            self.needs_render = True  # Player moved, need to re-render
            
    def can_move_to(self, x, y):
        """Check if the player can move to the given position"""
        # Check bounds
        if not (0 <= x < self.level.width and 0 <= y < self.level.height):
            return False
            
        # Check if it's a walkable tile
        return self.level.is_walkable(x, y)
        
    def update(self):
        """Update game state each frame"""
        # Here we'll add monster AI, combat, etc. later
        pass