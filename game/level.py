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
        
        # Tile types
        self.WALL = '#'
        self.FLOOR = '.'
        self.DOOR = '+'
        self.STAIRS_DOWN = '>'
        self.STAIRS_UP = '<'
        
    def generate(self):
        """Generate a new dungeon level"""
        # Initialize with all walls
        self.tiles = [[self.WALL for _ in range(self.width)] 
                      for _ in range(self.height)]
        
        # Generate rooms
        self.generate_rooms()
        
        # Connect rooms with corridors
        self.connect_rooms()
        
        # Add stairs (for future multi-level support)
        self.add_stairs()
        
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
                
    def add_stairs(self):
        """Add stairs to the level"""
        if self.rooms:
            # Put stairs down in the last room
            room = self.rooms[-1]
            x, y = room.center()
            self.tiles[y][x] = self.STAIRS_DOWN
            
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
        """Get a random walkable position"""
        attempts = 0
        while attempts < 100:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.is_walkable(x, y):
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