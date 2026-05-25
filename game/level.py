"""
Level - Dungeon generation and map management
"""

import random

class Level:
    """Represents a dungeon level with map generation"""
    
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.tiles = []
        self.rooms = []
        self.chests = {}
        
        # Tile types
        self.WALL = '#'
        self.FLOOR = '.'
        self.DOOR = '+'
        self.STAIRS_DOWN = '>'
        self.STAIRS_UP = '<'
        self.CHEST = '*'
        
    def generate(self, dungeon_level=1):
        """Generate a new dungeon level"""
        # Initialize with all walls
        self.tiles = [[self.WALL for _ in range(self.width)] 
                      for _ in range(self.height)]
        
        # Generate rooms
        self.generate_rooms()
        
        # Connect rooms with corridors
        self.connect_rooms()
        
        # Add doors to floor tiles
        self.add_doors()
        
        # Add stairs (for future multi-level support)
        self.add_stairs()
        
        # Add treasure chests
        self.add_chests(dungeon_level)
        
    def generate_rooms(self):
        """Generate random rooms"""
        self.rooms = []
        attempts = 0
        max_attempts = 50
        
        while len(self.rooms) < 8 and attempts < max_attempts:
            # Random room size and position
            room_width = random.randint(4, 8)
            room_height = random.randint(4, 6)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            
            new_room = Room(x, y, room_width, room_height)
            
            # Check if room overlaps with existing rooms
            if not self.room_overlaps(new_room):
                self.carve_room(new_room)
                self.rooms.append(new_room)
                
            attempts += 1
            
    def room_overlaps(self, new_room):
        """Check if a room overlaps with existing rooms"""
        for room in self.rooms:
            if (new_room.x1 <= room.x2 and new_room.x2 >= room.x1 and
                new_room.y1 <= room.y2 and new_room.y2 >= room.y1):
                return True
        return False
        
    def carve_room(self, room):
        """Carve out a room in the dungeon"""
        for y in range(room.y1, room.y2 + 1):
            for x in range(room.x1, room.x2 + 1):
                self.tiles[y][x] = self.FLOOR
                
    def connect_rooms(self):
        """Connect all rooms with corridors"""
        for i in range(len(self.rooms) - 1):
            self.create_corridor(self.rooms[i], self.rooms[i + 1])
            
    def create_corridor(self, room1, room2):
        """Create a corridor between two rooms"""
        # Get center points of rooms
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        
        # Create L-shaped corridor
        if random.choice([True, False]):
            # Horizontal then vertical
            self.carve_horizontal_corridor(x1, x2, y1)
            self.carve_vertical_corridor(y1, y2, x2)
        else:
            # Vertical then horizontal
            self.carve_vertical_corridor(y1, y2, x1)
            self.carve_horizontal_corridor(x1, x2, y2)
            
    def carve_horizontal_corridor(self, x1, x2, y):
        """Carve a horizontal corridor"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = self.FLOOR
                
    def carve_vertical_corridor(self, y1, y2, x):
        """Carve a vertical corridor"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = self.FLOOR
                
    def add_doors(self):
        """Add doors to random floor positions"""
        # Add 2-4 doors randomly on floor tiles
        doors_to_add = random.randint(2, 4)
        
        for _ in range(doors_to_add):
            attempts = 0
            while attempts < 30:  # Limit attempts to avoid infinite loop
                # Get a random floor position
                x, y = self.get_random_floor_position()
                
                # Make sure it's actually a floor tile and not stairs
                if (self.tiles[y][x] == self.FLOOR and 
                    self.tiles[y][x] != self.STAIRS_DOWN and
                    self.tiles[y][x] != self.STAIRS_UP):
                    # Place the door
                    self.tiles[y][x] = self.DOOR
                    break
                
                attempts += 1

    def add_stairs(self):
        """Add stairs to the level"""
        if self.rooms:
            # Put stairs down in the last room
            room = self.rooms[-1]
            x, y = room.center()
            self.tiles[y][x] = self.STAIRS_DOWN
            
    def add_chests(self, dungeon_level=1):
        """Add treasure chests to the level"""
        self.chests = {}
        chest_count = 1 if dungeon_level == 1 else (1 if random.random() < 0.25 else 0)
        for _ in range(chest_count):
            position = self.get_random_floor_position()
            if not position:
                break
            x, y = position
            self.tiles[y][x] = self.CHEST
            self.chests[(x, y)] = []
    
    def is_walkable(self, x, y):
        """Check if a position is walkable"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.tiles[y][x] != self.WALL
        
    def get_tile(self, x, y):
        """Get the tile at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return self.WALL
        
    def get_random_floor_position(self):
        """Get a random floor position"""
        attempts = 0
        while attempts < 100:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.tiles[y][x] == self.FLOOR:
                return x, y
            attempts += 1
        
        # Fallback: return center of first room
        if self.rooms:
            return self.rooms[0].center()
        return 1, 1


class Room:
    """Represents a rectangular room in the dungeon"""
    
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        
    def center(self):
        """Get the center coordinates of the room"""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y


class DoorRoom:
    """Represents a small room accessible through doors"""
    
    def __init__(self, door_x, door_y):
        self.door_x = door_x  # Original door position on main map
        self.door_y = door_y
        self.generated = False
        
        # Room properties
        self.room_size = random.choice(["small", "small", "medium", "large"])  # Weighted toward small
        self.width = 0
        self.height = 0
        self.tiles = []
        
        # Player spawn and exit positions
        self.entrance_x = 1
        self.entrance_y = 0
        self.exit_x = 0
        self.exit_y = 0
        
        # Enemy spawn positions and state tracking
        self.enemy_positions = []
        self.enemies_spawned = False  # Track if enemies have been spawned
        self.defeated_enemy_positions = set()  # Track which enemy positions have been defeated
        
    def generate(self):
        """Generate the door room layout and enemy positions"""
        if self.generated:
            return
            
        # Set room dimensions based on size
        if self.room_size == "small":
            self.width = random.randint(8, 12)
            self.height = random.randint(6, 8)
        elif self.room_size == "medium":
            self.width = random.randint(12, 16)
            self.height = random.randint(8, 12)
        else:  # large
            self.width = random.randint(16, 20)
            self.height = random.randint(12, 16)
        
        # Initialize with walls
        self.tiles = [['#' for _ in range(self.width)] for _ in range(self.height)]
        
        # Create floor area (leave 1-tile border as walls)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.tiles[y][x] = '.'
        
        # Set entrance position (left side)
        self.entrance_x = 1
        self.entrance_y = self.height // 2
        
        # Set exit door position (right side)
        self.exit_x = self.width - 2
        self.exit_y = self.height // 2
        self.tiles[self.exit_y][self.exit_x] = '+'
        
        # Generate enemy positions
        self.generate_enemy_positions()
        
        self.generated = True
    
    def generate_enemy_positions(self):
        """Generate enemy spawn positions based on room size"""
        # Determine number of enemies
        enemy_counts = {"small": (1, 2), "medium": (2, 3), "large": (2, 3)}
        min_enemies, max_enemies = enemy_counts[self.room_size]
        num_enemies = random.randint(min_enemies, max_enemies)
        
        self.enemy_positions = []
        attempts = 0
        
        while len(self.enemy_positions) < num_enemies and attempts < 50:
            # Random position in the room (avoid edges and entrance/exit)
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            # Make sure it's not too close to entrance or exit
            entrance_dist = abs(x - self.entrance_x) + abs(y - self.entrance_y)
            exit_dist = abs(x - self.exit_x) + abs(y - self.exit_y)
            
            if entrance_dist > 2 and exit_dist > 2:
                # Check if position is already taken
                if (x, y) not in self.enemy_positions:
                    self.enemy_positions.append((x, y))
            
            attempts += 1
    
    def is_walkable(self, x, y):
        """Check if a position is walkable"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.tiles[y][x] != '#'
    
    def get_tile(self, x, y):
        """Get the tile at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return '#'
    
    def mark_enemy_defeated(self, x, y):
        """Mark an enemy position as defeated"""
        self.defeated_enemy_positions.add((x, y))
    
    def get_active_enemy_positions(self):
        """Get enemy positions that haven't been defeated"""
        return [(x, y) for (x, y) in self.enemy_positions if (x, y) not in self.defeated_enemy_positions]