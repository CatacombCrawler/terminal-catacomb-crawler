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
        
        # Show player vs enemy health bars side by side
        self.render_combat_health_comparison(player, enemy_manager)
        
        # Show combat status above combat log
        if hasattr(enemy_manager, 'combat_manager') and enemy_manager.combat_manager:
            combat_status = enemy_manager.combat_manager.get_combat_status()
            print(self.terminal.yellow(combat_status))
            print()
        
        # Show combat messages
        self.render_combat_messages(combat_messages)
        
        # Show combat controls
        self.render_controls(in_combat=True, is_player_turn=is_player_turn)
        
    def render_combat_health_comparison(self, player, enemy_manager):
        """Render player vs enemy health bars side by side"""
        if not hasattr(enemy_manager, 'combat_manager') or not enemy_manager.combat_manager:
            return
            
        # Get current enemy target (first alive enemy in combat)
        current_enemy = None
        for participant in enemy_manager.combat_manager.combat_participants:
            if participant["type"] == "enemy" and participant["entity"].is_alive():
                current_enemy = participant["entity"]
                break
                
        if not current_enemy:
            return
            
        print("=" * 70)
        print()
        
        # Create the simplified VS layout
        # Player info
        player_name = f"⚡ {player.name}"
        player_hp_percent = player.hp / player.max_hp
        player_hp_color = self.terminal.green if player_hp_percent > 0.6 else \
                         self.terminal.yellow if player_hp_percent > 0.3 else \
                         self.terminal.red
        player_hp_bar = self.create_bar(player.hp, player.max_hp, 15)
        player_hp_text = f"{player.hp}/{player.max_hp}"
        
        # Enemy info
        enemy_name = f"👹 {current_enemy.name}"
        enemy_hp_percent = current_enemy.hp / current_enemy.max_hp
        enemy_hp_color = self.terminal.green if enemy_hp_percent > 0.6 else \
                        self.terminal.yellow if enemy_hp_percent > 0.3 else \
                        self.terminal.red
        enemy_hp_bar = self.create_bar(current_enemy.hp, current_enemy.max_hp, 15)
        enemy_hp_text = f"{current_enemy.hp}/{current_enemy.max_hp}"
        
        # Format with more spacing
        player_section = f"{self.terminal.blue(player_name):<25}"
        enemy_section = f"{self.terminal.red(enemy_name):>25}"
        print(f"{player_section}        {enemy_section}")
        
        # Health bars with VS in the middle
        player_health = f"{player_hp_color(player_hp_bar)} {player_hp_text}"
        enemy_health = f"{enemy_hp_color(enemy_hp_bar)} {enemy_hp_text}"
        vs_text = self.terminal.bold + self.terminal.red(" VS ") + self.terminal.normal
        
        # Format health line with proper spacing
        print(f"{player_health:<35}{vs_text}{enemy_health:>35}")
        
        print()
        print("=" * 70)
        print()
        
    def format_combatant_info(self, combatant, combatant_type):
        """Format info for a combat participant"""
        if combatant_type == "player":
            name = f"{combatant.name}"
            name_color = self.terminal.blue
        else:
            name = f"{combatant.name}"
            name_color = self.terminal.red
            
        # Health info
        hp_percent = combatant.hp / combatant.max_hp
        hp_color = self.terminal.green if hp_percent > 0.6 else \
                   self.terminal.yellow if hp_percent > 0.3 else \
                   self.terminal.red
        
        hp_bar = self.create_bar(combatant.hp, combatant.max_hp, 15)
        hp_text = f"{combatant.hp}/{combatant.max_hp}"
        
        # Additional stats
        if combatant_type == "player":
            stats_line = f"ATK:{combatant.attack} DEF:{combatant.defense}"
            level_line = f"Level {combatant.level}"
        else:
            stats_line = f"ATK:{combatant.attack} DEF:{combatant.defense}"
            level_line = f"Type: {combatant.type.title()}"
            
        # Format the info block
        info_lines = [
            name_color(name) + self.terminal.normal,
            hp_color(hp_bar) + self.terminal.normal + f" {hp_text}",
            stats_line,
            level_line
        ]
        
        return '\n'.join(info_lines)
        
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
        
        # Health bar using helper function
        health_info = self.create_health_bar_info(player, 20)
        print(f"Health: {health_info['colored_bar']} ({health_info['text']})")
        
        # Experience bar using helper function
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"EXP:    {exp_info['colored_bar']} ({exp_info['text']})")
        
        # Stats
        print(f"Level: {stats['level']} | "
              f"Attack: {stats['attack']} | "
              f"Defense: {stats['defense']} | "
              f"Position: ({stats['position'][0]}, {stats['position'][1]})")

              
    def render_combat_status_bar(self, player):
        """Render compact player status for combat (legacy method - now unused)"""
        print("=" * 50)
        
        # Health bar using helper function
        health_info = self.create_health_bar_info(player, 20)
        print(f"Health: {health_info['colored_bar']} ({health_info['text']})")
        
        # Experience bar using helper function
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"EXP:    {exp_info['colored_bar']} ({exp_info['text']})")
        
        print()
        
              
    def render_combat_messages(self, combat_messages):
        """Render recent combat messages"""
        if not combat_messages:
            return
            
        print(self.terminal.bold + "Combat Log:" + self.terminal.normal)
        
        # Show last 3 combat messages to avoid clutter
        recent_messages = combat_messages[-3:] if len(combat_messages) > 3 else combat_messages
        
        for msg in recent_messages:
            if msg["type"] == "combat":
                if "target" in msg:  # Player attacking enemy
                    text = f"{msg['attacker']} attacks {msg['target']} for {msg['damage']} damage!"
                    if msg.get("target_died"):
                        text += f" {msg['target']} defeated! (+{msg.get('exp_gained', 0)} XP)"
                    print(f"  {self.terminal.green(text)}")
                elif "defender" in msg:  # Defend action
                    print(f"  {self.terminal.blue(msg['message'])}")
                else:  # Enemy attacking player - use rich monster attack info
                    if msg.get("hit", True):
                        # Check for rich attack information from monster system
                        if msg.get("attack_name") and msg.get("description"):
                            damage = msg.get('damage', 0)
                            if damage > 0:
                                text = f"{msg['attacker']} uses {msg['attack_name']} - {msg.get('description', 'attacks')} ({damage} damage)"
                            else:
                                text = f"{msg['attacker']} uses {msg['attack_name']} - {msg.get('description', 'attacks')} but deals no damage!"
                        else:
                            damage = msg.get('damage', 0)
                            if damage > 0:
                                text = f"{msg['attacker']} attacks you for {damage} damage!"
                            else:
                                text = f"{msg['attacker']} attacks you but deals no damage!"
                        
                        # Add special effects description
                        if msg.get("special_effects"):
                            effect_type = msg["special_effects"].get("type", "")
                            if effect_type:
                                text += f" [Special: {effect_type.title()}]"
                    else:
                        text = f"{msg['attacker']} misses completely!"
                    
                    if msg.get("player_died"):
                        text += " You have fallen!"
                    print(f"  {self.terminal.red(text)}")
            elif msg["type"] == "system":
                print(f"  {self.terminal.yellow(msg['message'])}")
              
    def create_bar(self, current, maximum, width):
        """Create a text-based progress bar"""
        if maximum == 0:
            return "█" * width
            
        filled = int((current / maximum) * width)
        return "█" * filled + "░" * (width - filled)
        
    def render_controls(self, in_combat=False, is_player_turn=False):
        """Render control instructions"""
        print("-" * 50)
        
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
        
    def show_combat_summary(self, combat_stats, player):
        """Show combat summary screen before returning to exploration"""
        print(self.terminal.clear)
        print(self.terminal.bold + "=== COMBAT ENDED ===" + self.terminal.normal)
        print()
        
        # Show victory or defeat
        if combat_stats.get("victory", False):
            print(self.terminal.green + self.terminal.bold + "VICTORY!" + self.terminal.normal)
        else:
            print(self.terminal.red + self.terminal.bold + "DEFEAT!" + self.terminal.normal)
        print()
        
        print("=" * 50)
        print("COMBAT SUMMARY")
        print("=" * 50)
        
        # Show health change
        health_lost = combat_stats.get("health_lost", 0)
        if health_lost > 0:
            print(f"Health Lost:    {self.terminal.red}{health_lost}{self.terminal.normal} HP")
        else:
            print(f"Health Lost:    {self.terminal.green}0{self.terminal.normal} HP")
            
        # Show experience gained
        exp_gained = combat_stats.get("exp_gained", 0)
        if exp_gained > 0:
            print(f"Experience:     {self.terminal.blue}+{exp_gained}{self.terminal.normal} XP")
        else:
            print(f"Experience:     {self.terminal.normal}+0{self.terminal.normal} XP")
            
        # Show enemies defeated
        enemies_defeated = combat_stats.get("enemies_defeated", 0)
        print(f"Enemies Slain:  {enemies_defeated}")
        
        print("=" * 50)
        
        # Show current player status bars
        health_info = self.create_health_bar_info(player, 20)
        print(f"Health: {health_info['colored_bar']} ({health_info['text']})")
        
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"EXP:    {exp_info['colored_bar']} ({exp_info['text']})")
        
        # Show level up if applicable
        if combat_stats.get("level_up", False):
            print()
            print(self.terminal.yellow + self.terminal.bold + "LEVEL UP!" + self.terminal.normal)
            new_level = combat_stats.get("new_level", 1)
            print(f"You are now level {new_level}!")
            
        print()
        print("=" * 50)
        print()
        print("Press any key to return to exploration...")
        
        self.terminal.inkey()

    def create_health_bar_info(self, entity, bar_width=15):
        """Create health bar information for any entity"""
        hp_percent = entity.hp / entity.max_hp
        hp_color = self.terminal.green if hp_percent > 0.6 else \
                   self.terminal.yellow if hp_percent > 0.3 else \
                   self.terminal.red
        hp_bar = self.create_bar(entity.hp, entity.max_hp, bar_width)
        hp_text = f"{entity.hp}/{entity.max_hp}"
        
        return {
            "percent": hp_percent,
            "color": hp_color,
            "bar": hp_bar,
            "text": hp_text,
            "colored_bar": hp_color(hp_bar) + self.terminal.normal
        }
    
    def create_exp_bar_info(self, player, bar_width=20):
        """Create experience bar information for player"""
        exp_bar = self.create_bar(player.exp, player.exp_to_next, bar_width)
        exp_text = f"{player.exp}/{player.exp_to_next}"
        colored_bar = self.terminal.blue(exp_bar) + self.terminal.normal
        
        return {
            "bar": exp_bar,
            "text": exp_text,
            "colored_bar": colored_bar
        }    

    def show_message(self, message, duration=2):
        """Show a temporary message"""
        # For now, just print it. Later we can add a message log
        print(f"\n>>> {message}")
        time.sleep(duration)