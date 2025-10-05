"""
Level - Dungeon generation and map management
"""

import random

from base_class import BaseClass
from constants import Constants as GAME_CONSTANTS

class Level(BaseClass):
    """Represents a dungeon level with map generation"""
    
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.tiles = []
        self.rooms = []
        
    def generate(self):
        """Generate a new dungeon level"""
        # Initialize with all walls
        self.tiles = [[GAME_CONSTANTS.WALL for _ in range(self.width)]
                      for _ in range(self.height)]
        
        # Generate rooms
        self.generate_rooms()
        
        # Connect rooms with corridors
        self.connect_rooms()
        
        # Add doors to floor tiles
        self.add_doors()
        
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
                self.tiles[y][x] = GAME_CONSTANTS.FLOOR
                
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
                self.tiles[y][x] = GAME_CONSTANTS.FLOOR
                
    def carve_vertical_corridor(self, y1, y2, x):
        """Carve a vertical corridor"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = GAME_CONSTANTS.FLOOR
                
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
                if (self.tiles[y][x] == GAME_CONSTANTS.FLOOR and
                    self.tiles[y][x] != GAME_CONSTANTS.STAIRS_DOWN and
                    self.tiles[y][x] != GAME_CONSTANTS.STAIRS_UP):
                    # Place the door
                    self.tiles[y][x] = GAME_CONSTANTS.DOOR
                    break
                
                attempts += 1

    def add_stairs(self):
        """Add stairs to the level"""
        if self.rooms:
            # Put stairs down in the last room
            room = self.rooms[-1]
            x, y = room.center()
            self.tiles[y][x] = GAME_CONSTANTS.STAIRS_DOWN
            
    def is_walkable(self, x, y):
        """Check if a position is walkable"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.tiles[y][x] != GAME_CONSTANTS.WALL
        
    def get_tile(self, x, y):
        """Get the tile at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return GAME_CONSTANTS.WALL
        
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

    def get_level_dict(self):
        """
        Core method to get level data as a dictionary
        :return:
        """
        # Use this to exclude any object from putting in dictionary
        exclusions = {"tiles"}
        level_data = self._to_dict(self)
        data = {k: v for k, v in level_data.items() if k not in exclusions}
        r, c, floors, doors, stairs_down, stairs_up = self.get_level_components()
        data = self.update_level_dict_data_by_components(data, r, c, floors, doors, stairs_down, stairs_up)
        return data

    def update_level_dict_data_by_components(self, data, r, c, floors, doors, stairs_down, stairs_up):
        """
        Core method to update level data by components
        :param data: existing level data dictionary
        :param r: tiles rows
        :param c: tiles columns
        :param floors: floor locations coordinates
        :param doors: door locations coordinates
        :param stairs_down: stairs down locations coordinates
        :param stairs_up: stairs up locations coordinates
        :return: updated level data dictionary
        """
        data.update({GAME_CONSTANTS.TILES: {GAME_CONSTANTS.X: r, GAME_CONSTANTS.Y: c}})
        if floors:
            data.update({GAME_CONSTANTS.FLOORS_COORD: floors})

        if doors:
            data.update({GAME_CONSTANTS.DOORS_COORD: doors})

        if stairs_down:
            data.update({GAME_CONSTANTS.STAIRS_DOWN_COORD: stairs_down})

        if stairs_up:
            data.update({GAME_CONSTANTS.STAIRS_UP_COORD: stairs_up})
        return data

    def get_level_components(self):
        """
        Core method to get level components such as tiles, floors, doors, stairs_down, stairs_up
        :return: rows, cols, floors, doors, stairs_down, stairs_up
        """
        floors, doors, stairs_down, stairs_up = list(), list(), list(), list()
        r, c = len(self.tiles), len(self.tiles[0])
        for i in range(r):
            for j in range(c):
                if self.tiles[i][j] == GAME_CONSTANTS.FLOOR:
                    floors.append([i, j])
                elif self.tiles[i][j] == GAME_CONSTANTS.DOOR:
                    doors.append([i, j])
                elif self.tiles[i][j] == GAME_CONSTANTS.STAIRS_DOWN:
                    stairs_down.append([i, j])
                elif self.tiles[i][j] == GAME_CONSTANTS.STAIRS_UP:
                    stairs_up.append([i, j])
        return r, c, floors, doors, stairs_down, stairs_up

    def set_level_components(self, data):
        """
        Core method to set level components from existing json
        :param data: data from json for tiles, floors, doors, stairs_down, stairs_up
        """
        if data:
            tiles = data.get(GAME_CONSTANTS.TILES, {})
            x, y = tiles.get(GAME_CONSTANTS.X, 0), tiles.get(GAME_CONSTANTS.Y, 0)
            self.tiles = [[GAME_CONSTANTS.WALL for _ in range(y)] for _ in range(x)]

            layout_info = {GAME_CONSTANTS.FLOORS_COORD: GAME_CONSTANTS.FLOOR,
                           GAME_CONSTANTS.DOORS_COORD: GAME_CONSTANTS.DOOR,
                           GAME_CONSTANTS.STAIRS_DOWN_COORD: GAME_CONSTANTS.STAIRS_DOWN,
                           GAME_CONSTANTS.STAIRS_UP_COORD: GAME_CONSTANTS.STAIRS_UP}

            for key, value in layout_info.items():
                existing_data = data.get(key, [])
                for i, j in existing_data:
                    self.tiles[i][j] = value

    def set_rooms(self, data):
        """
        Core method to set room data from existing json
        :param data: data from json
        """
        rooms_data = data.get(GAME_CONSTANTS.ROOMS, [])
        for room in rooms_data:
            x1, y1, x2, y2 = room.get('x1'), room.get('y1'), room.get('x2'), room.get('y2')
            room_obj = Room(x1, y1, self.width, self.height)
            room_obj.x2, room_obj.y2 = x2, y2
            self.rooms.append(room_obj)

    def load(self, data):
        if data:
            self.width = data.get(GAME_CONSTANTS.WIDTH, self.width)
            self.height = data.get(GAME_CONSTANTS.HEIGHT, self.height)

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


class DoorRoom(BaseClass, Level):
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

    def get_door_room_dict(self):
        """Get the door room dict"""
        exclusions = {"tiles", "defeated_enemy_positions"}
        door_room_data = self._to_dict(self)
        data = {k: v for k, v in door_room_data.items() if k not in exclusions}
        data["defeated_enemy_positions"] = list(self.defeated_enemy_positions)
        r, c, floors, doors, stairs_down, stairs_up = super().get_level_components()
        data = super().update_level_dict_data_by_components(data, r, c, floors, doors, stairs_down, stairs_up)
        return data

    def load(self, data):
        """
        Core method that loads door room data from existing json
        :param data: json data for door room
        """
        # Room properties
        self.generated = data.get('generated', False)
        self.room_size = data.get('room_size', '')
        self.width = data.get(GAME_CONSTANTS.WIDTH, 0)
        self.height = data.get(GAME_CONSTANTS.HEIGHT, 0)

        super().set_level_components(data)

        # Player spawn and exit positions
        self.entrance_x = data.get('entrance_x', 1)
        self.entrance_y = data.get('entrance_y', 0)
        self.exit_x = data.get('exit_x', 0)
        self.exit_y = data.get('exit_y', 0)

        # Enemy spawn positions and state tracking
        self.enemy_positions = []
        enemy_positions = data.get('enemy_positions', [])
        for pos in enemy_positions:
            self.enemy_positions.append(tuple(pos))

        self.enemies_spawned = data.get('enemies_spawned', False)

        self.defeated_enemy_positions = set()
        defeated_enemy_positions = data.get('defeated_enemy_positions', [])
        for pos in defeated_enemy_positions:
            self.defeated_enemy_positions.add(tuple(pos))