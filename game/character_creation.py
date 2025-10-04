"""
Character Creation - Starting item selection and character setup
"""

from .items.items import ItemManager, Item

class CharacterCreator:
    """Handles character creation process"""
    
    def __init__(self, terminal):
        self.terminal = terminal
        
    def create_character(self, player):
        """Run the character creation process"""
        print(self.terminal.clear)
        
        # Get player name
        player_name = self.get_player_name()
        if not player_name:
            return False
        player.name = player_name
        
        # Show equipment info
        print(self.terminal.clear)
        self.show_equipment_info()

        # Get starting items available for selection
        starting_items = ItemManager.get_starting_items()
        
        # Let player select starting item
        selected_item = self.select_starting_item(starting_items)
        
        if selected_item:
            # Create the item instance and give to player
            item = ItemManager.create_item(selected_item['id'], selected_item['category'])
            success, message = player.set_starting_item(item)
            
            if success:
                self.show_character_summary(player)
                return True
            else:
                print(f"Error equipping starting item: {message}")
                return False
        
        return False
    
    def get_player_name(self):
        """Get the player's chosen hero name"""
        print(self.terminal.bold + "🏰 Welcome to Terminal Dungeon Crawler! 🏰" + self.terminal.normal)
        print()
        print(self.terminal.bold + "⚔️  Create Your Hero ⚔️" + self.terminal.normal)
        print()
        print("Every hero needs a name to be remembered by...")
        print()
        
        while True:
            try:
                print("Enter your hero's name: ", end="", flush=True)
                name = input().strip()
                
                # Validate name
                if not name:
                    print("Your hero needs a name! Please enter something.")
                    print()
                    continue
                    
                if len(name) > 20:
                    print("That name is too long! Please keep it under 20 characters.")
                    print()
                    continue
                    
                if len(name) < 2:
                    print("Please enter a name with at least 2 characters.")
                    print()
                    continue
                
                # Confirm the name
                print()
                print(f"Your hero shall be known as: {self.terminal.bold}{name}{self.terminal.normal}")
                confirm = input("Is this correct? (y/n): ").strip().lower()
                
                if confirm in ['y', 'yes']:
                    print()
                    return name
                else:
                    print()
                    print("Let's try again...")
                    print()
                    
            except KeyboardInterrupt:
                print()
                return None
        
    def show_equipment_info(self):
        print("Before venturing into the dangerous catacombs, you must choose")
        print("your starting equipment. Each item grants different bonuses:")
        print()
        print("📊 Stats:")
        print("  • Attack: Increases damage dealt to enemies")
        print("  • Defense: Reduces damage taken from enemies")
        print("  • Speed: Affects turn order in combat")
        print("  • HP: Increases your maximum health")
        print()
    
    def select_starting_item(self, starting_items):
        """Let player select their starting item"""
        # Create a flat list of all starting items with their categories
        item_options = []
        
        for category, items in starting_items.items():
            for item_id, item_data in items.items():
                item_options.append({
                    'id': item_id,
                    'category': category,
                    'data': item_data
                })
        
        if not item_options:
            print("No starting items available!")
            return None
            
        while True:
            print(self.terminal.bold + "Choose your starting item:" + self.terminal.normal)
            print()
            
            # Display options
            for i, option in enumerate(item_options, 1):
                self.display_item_option(i, option)
                
            print()
            print(f"Enter your choice (1-{len(item_options)}): ", end="", flush=True)
            
            try:
                choice = input().strip()
                if choice.lower() == 'q':
                    return None
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(item_options):
                    selected = item_options[choice_num - 1]
                    
                    # Confirm selection
                    if self.confirm_selection(selected):
                        return selected
                else:
                    print(f"Please enter a number between 1 and {len(item_options)}")
                    
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return None
                
            print()
            
    def display_item_option(self, number, option):
        """Display a single item option"""
        data = option['data']
        
        # Get color for item type
        type_colors = {
            'weapon': self.terminal.red,
            'armor': self.terminal.blue,
            'shield': self.terminal.cyan,
        }
        
        color_func = type_colors.get(data['type'], self.terminal.white)
        
        # Format the item display
        print(f"{number}. {color_func(data['symbol'])} {self.terminal.bold}{data['name']}{self.terminal.normal}")
        print(f"   Type: {data['type'].title()}")
        print(f"   {data['description']}")
        
        # Display stats
        stats = data['stats']
        stat_parts = []
        
        for stat, value in stats.items():
            if value != 0:
                sign = "+" if value > 0 else ""
                color = self.terminal.green if value > 0 else self.terminal.red if value < 0 else self.terminal.normal
                stat_parts.append(f"{stat.upper()}: {color}{sign}{value}{self.terminal.normal}")
                
        if stat_parts:
            print(f"   Stats: {' | '.join(stat_parts)}")
            
        print()
        
    def confirm_selection(self, selected):
        """Confirm the player's item selection"""
        data = selected['data']
        
        print(self.terminal.clear)
        print(self.terminal.bold + "Confirm Your Choice:" + self.terminal.normal)
        print()
        
        # Show selected item details
        print(f"Selected: {self.terminal.bold}{data['name']}{self.terminal.normal}")
        print(f"Description: {data['description']}")
        print()
        
        # Show stat changes
        print("This item will modify your stats:")
        for stat, value in data['stats'].items():
            if value != 0:
                sign = "+" if value > 0 else ""
                color = self.terminal.green if value > 0 else self.terminal.red
                base_values = {
                    'hp': 100,
                    'attack': 10,
                    'defense': 5,
                    'speed': 12
                }
                base = base_values.get(stat, 0)
                new_value = base + value
                print(f"  {stat.upper()}: {base} → {color}{new_value}{self.terminal.normal} ({sign}{value})")
                
        print()
        
        while True:
            confirm = input("Confirm this choice? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")
                
    def show_character_summary(self, player):
        """Show final character summary"""
        print(self.terminal.clear)
        print(self.terminal.bold + "🎉 Character Created Successfully! 🎉" + self.terminal.normal)
        print()
        
        print(f"Hero Name: {self.terminal.bold}{player.name}{self.terminal.normal}")
        print(f"Level: {player.level}")
        print()
        
        print("Starting Stats:")
        stats = player.get_stats()
        print(f"  Health:  {stats['hp']}/{stats['max_hp']}")
        print(f"  Attack:  {stats['attack']}")
        print(f"  Defense: {stats['defense']}")  
        print(f"  Speed:   {stats['speed']}")
        print()
        
        # Show equipped item
        equipped = player.equipment.get_equipped_items()
        if equipped:
            print("Starting Equipment:")
            for slot, item in equipped.items():
                print(f"  {slot.replace('_', ' ').title()}: {item.name}")
                
        print()
        print("Press any key to begin your adventure...")
        self.terminal.inkey()