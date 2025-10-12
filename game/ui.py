"""
UI - User interface and display handling
"""
import time

class UI:
    """Handles all user interface and display operations"""
    
    def __init__(self, terminal):
        self.terminal = terminal
        self.view_radius = 25  # How far player can see - increased for better visibility
        
    def render(self, player, level, enemy_manager=None, combat_messages=None, dungeon_level=1, in_door_room=False, awaiting_stairs_confirmation=False):
        """Render the entire game screen"""
        # Don't clear screen or render anything if waiting for stairs confirmation
        if awaiting_stairs_confirmation:
            return
            
        print(self.terminal.clear)
        
        # Create level info dictionary
        level_info = {
            "dungeon_level": dungeon_level,
            "in_door_room": in_door_room
        }
        
        # Determine combat state
        in_combat = hasattr(enemy_manager, 'combat_manager') and getattr(enemy_manager.combat_manager, 'in_combat', False) if enemy_manager else False
        is_player_turn = False
        if hasattr(enemy_manager, 'combat_manager') and enemy_manager.combat_manager:
            is_player_turn = enemy_manager.combat_manager.is_player_turn()
        
        if in_combat:
            # Combat mode - show only stats and combat info
            self.render_combat_screen(player, enemy_manager, combat_messages, is_player_turn, level_info)
        else:
            # Exploration mode - show map and normal UI
            self.render_exploration_screen(player, level, enemy_manager, combat_messages, level_info)
            
    def render_exploration_screen(self, player, level, enemy_manager, combat_messages, level_info):
        """Render the exploration screen with map"""
        # Render the map
        self.render_map(player, level, enemy_manager)
        
        # Render UI elements
        self.render_status_bar(player, level_info)
        # No combat messages during exploration
        self.render_controls(in_combat=False, is_player_turn=False)

        # Render the mini-map on top of other UI elements
        self.render_mini_map(player, level, enemy_manager)
        
    def render_combat_screen(self, player, enemy_manager, combat_messages, is_player_turn, level_info):
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
                if hasattr(level, 'visited_map') and not level.visited_map[y][x]:
                    row += ' '
                    continue

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

    def render_mini_map(self, player, level, enemy_manager=None):
        """Render a small mini-map in the top-right corner"""
        map_width = 20
        map_height = 10
        
        # Top-right corner positioning
        start_col = self.terminal.width - map_width - 2
        start_row = 1

        with self.terminal.location(x=start_col, y=start_row):
            print("╔" + "═" * map_width + "╗")

        for y in range(map_height):
            with self.terminal.location(x=start_col, y=start_row + y + 1):
                row_str = "║"
                for x in range(map_width):
                    map_x = player.x - (map_width // 2) + x
                    map_y = player.y - (map_height // 2) + y

                    if not (0 <= map_x < level.width and 0 <= map_y < level.height):
                        row_str += ' '
                        continue

                    if hasattr(level, 'visited_map') and not level.visited_map[map_y][map_x]:
                        row_str += ' '
                        continue

                    if map_x == player.x and map_y == player.y:
                        row_str += self.terminal.bold + self.terminal.yellow(player.symbol)
                    elif enemy_manager and enemy_manager.get_enemy_at(map_x, map_y):
                        row_str += self.colorize_enemy(enemy_manager.get_enemy_at(map_x, map_y))
                    else:
                        row_str += self.colorize_tile(level.get_tile(map_x, map_y))
                
                row_str += "║"
                print(row_str)

        with self.terminal.location(x=start_col, y=start_row + map_height + 1):
            print("╚" + "═" * map_width + "╝")
            
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
            
    def render_status_bar(self, player, level_info=None):
        """Render player status information"""
        stats = player.get_stats()
        
        print("\n" + self.terminal.bold + "┌" + "─" * 48 + "┐" + self.terminal.normal)
        
        # Health bar
        health_info = self.create_health_bar_info(player, 20)
        print(f"│ {self.terminal.bold_red}❤️ HP:{self.terminal.normal} {health_info['colored_bar']} ({health_info['text']})")
        
        # Experience bar
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"│ {self.terminal.bold_blue}✨ XP:{self.terminal.normal} {exp_info['colored_bar']} ({exp_info['text']})")
        
        print(self.terminal.bold + "├" + "─" * 48 + "┤" + self.terminal.normal)

        # Location information
        location_text = "Main Level"
        if level_info and level_info.get("in_door_room", False):
            location_text = "Door Room"
        
        dungeon_level = level_info.get("dungeon_level", 1) if level_info else 1
        
        # Stats
        stat_points_text = ""
        if hasattr(player, 'stat_points') and player.stat_points > 0:
            stat_points_text = f" | {self.terminal.bold_yellow}⭐ Stat Points: {player.stat_points}!{self.terminal.normal}"
        
        print(f"│ {self.terminal.bold}📈 Lvl:{self.terminal.normal} {self.terminal.green(str(stats['level']))} | "
              f"{self.terminal.bold} Dungeon:{self.terminal.normal} {self.terminal.cyan(str(dungeon_level))} | "
              f"{self.terminal.bold}⚔️ Atk:{self.terminal.normal} {self.terminal.red(str(stats['attack']))} | "
              f"{self.terminal.bold}🛡️ Def:{self.terminal.normal} {self.terminal.blue(str(stats['defense']))}{stat_points_text}")
        print(f"│ {self.terminal.bold}📍 Loc:{self.terminal.normal} {location_text} | {self.terminal.bold}Pos:{self.terminal.normal} ({stats['position'][0]}, {stats['position'][1]})")
        print(self.terminal.bold + "└" + "─" * 48 + "┘" + self.terminal.normal)

              
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
        """Render recent combat messages using rich data from execute_attack, attack_player, and attack_enemy"""
        if not combat_messages:
            return
            
        print(self.terminal.bold + "┌" + "─" * 12 + " Combat Log " + "─" * 12 + "┐" + self.terminal.normal)
        
        # Show last 5 combat messages to avoid clutter
        recent_messages = combat_messages[-5:] if len(combat_messages) > 5 else combat_messages
        
        for i, msg in enumerate(recent_messages):
            print("│ ", end="")
            if msg["type"] == "combat":
                if "target" in msg:  # Player attacking enemy
                    text = self._format_player_attack(msg)
                    print(f"{self.terminal.green}⚔️  {text}{self.terminal.normal}")
                elif "defender" in msg:  # Defend action
                    print(f"{self.terminal.blue}🛡️ {msg['message']}{self.terminal.normal}")
                else:  # Enemy attacking player
                    text = self._format_monster_attack(msg)
                    color = self.terminal.red
                    if msg.get("player_died"):
                        color = self.terminal.red + self.terminal.bold
                    print(f"{color}💥 {text}{self.terminal.normal}")
            elif msg["type"] == "deflection":
                print(f"{self.terminal.blue + self.terminal.bold}⚡ {msg['message']}{self.terminal.normal}")
            elif msg["type"] == "combat_detail":
                print(f"{self.terminal.dim}💡 {msg['message']}{self.terminal.normal}")
            elif msg["type"] == "round_separator":
                print(f"{self.terminal.dim}{msg['message']}{self.terminal.normal}")
            elif msg["type"] == "system":
                print(f"{self.terminal.yellow}⚙️  {msg['message']}{self.terminal.normal}")
            
            if i == len(recent_messages) - 1:
                print("└" + "─" * 38 + "┘")
    
    def _format_player_attack(self, msg):
        """Format player attack messages using rich data from attack_enemy"""
        if not msg.get("hit", True):
            # Handle miss with clearer explanation
            attacker = msg.get("attacker", "Player")
            target = msg.get("target", "Enemy")
            
            # Simplify miss message - the technical details confuse players
            hit_chance = msg.get("hit_chance", 0)
            if hit_chance < 0.5:
                reason = "low accuracy"
            elif msg.get("enemy_dodge", 0) > 0.15:
                reason = "enemy dodged"
            else:
                reason = "missed"
            
            return f"{attacker} {reason} {target}!"
        
        # Use the detailed message from player.attack_enemy if available
        if msg.get("message"):
            text = msg["message"]
            # Ensure damage is shown if not already in message
            if f"({msg['damage']} damage)" not in text and msg['damage'] > 0:
                text += f" ({msg['damage']} damage)"
        else:
            # Fallback formatting
            text = f"{msg['attacker']} attacks {msg['target']} for {msg['damage']} damage!"
        
        # Add critical hit indicator
        if msg.get("critical"):
            text = "💥 " + text
        
        # Add parry indicator  
        if msg.get("parried"):
            text = "🛡️ " + text
        
        # Don't integrate deflection - it will be shown separately like before
        
        # Add defeat and experience info
        if msg.get("target_died") or msg.get("enemy_died"):
            exp_gained = msg.get("exp_gained", 0)
            target_name = msg.get("target", "Enemy")
            text += f" {target_name} defeated!"
            if exp_gained > 0:
                text += f" (+{exp_gained} XP)"
            
            # Add level up notification
            if msg.get("leveled_up"):
                text += " ⭐ LEVEL UP! ⭐"
        
        return text
    
    def _format_monster_attack(self, msg):
        """Format monster attack messages using rich data from attack_player"""
        attacker = msg['attacker']
        
        if not msg.get("hit", True):
            # Handle miss with clearer explanation
            if msg.get("dodged"):
                return f"You dodge {attacker}'s attack!"
            else:
                # Simplify miss message - remove confusing technical details
                attack_name = msg.get("attack_name", "attack")
                return f"{attacker}'s {attack_name} misses!"
        
        # Hit - build description without deflection (deflection shown separately)
        damage = msg.get('damage', 0)
        
        # Use attack name and description if available (from monster system)
        if msg.get("attack_name") and msg.get("description"):
            attack_name = msg["attack_name"]
            description = msg.get("description", "attacks")
            
            if damage > 0:
                text = f"{attacker} uses {attack_name} - {description} (deals {damage} damage)"
            else:
                text = f"{attacker} uses {attack_name} - {description} but deals no damage!"
        else:
            # Fallback for basic attacks
            if damage > 0:
                text = f"{attacker} attacks you for {damage} damage!"
            else:
                text = f"{attacker} attacks you but deals no damage!"
        
        # Add special effects information
        if msg.get("special_effects"):
            effect = msg["special_effects"]
            effect_type = effect.get("type", "")
            if effect_type:
                # Add special effect icon and description
                effect_icons = {
                    "poison": "☠️",
                    "intimidate": "😨", 
                    "armor_break": "⚔️",
                    "magic_damage": "✨",
                    "stun": "⚡",
                    "chain_attack": "💫"
                }
                icon = effect_icons.get(effect_type, "💫")
                effect_name = effect_type.title().replace('_', ' ')
                text += f" {icon} {effect_name}"
        
        # Add defeat message if player died
        if msg.get("player_died") or msg.get("target_died"):
            text += " 💀 You have fallen!"
        
        return text
              
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
            print("EXPLORATION: WASD/Arrows=Move | E=Interact | Q=Quit | I=Inventory | C=Stats | L=Level Up")
        
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
        
        # Show victory or defeat
        if combat_stats.get("victory", False):
            print(self.terminal.green + self.terminal.bold + "      VICTORY!" + self.terminal.normal)
        else:
            print(self.terminal.red + self.terminal.bold + "      DEFEAT!" + self.terminal.normal)
        print()
        
        print(self.terminal.bold + "┌" + "─" * 12 + " Combat Summary " + "─" * 12 + "┐" + self.terminal.normal)
        
        # Show health lost
        health_lost = combat_stats.get("health_lost", 0)
        if health_lost > 0:
            print(f"│ {self.terminal.red}💔 Health Lost:{self.terminal.normal} {health_lost} HP")
        else:
            print(f"│ {self.terminal.green}❤️ Health Lost:{self.terminal.normal} 0 HP")
            
        # Show experience gained
        exp_gained = combat_stats.get("exp_gained", 0)
        if exp_gained > 0:
            print(f"│ {self.terminal.blue}✨ Experience:{self.terminal.normal} +{exp_gained} XP")
        else:
            print(f"│ {self.terminal.normal}✨ Experience:{self.terminal.normal} +0 XP")
            
        # Show enemies defeated
        enemies_defeated = combat_stats.get("enemies_defeated", 0)
        print(f"│ {self.terminal.yellow}💀 Enemies Slain:{self.terminal.normal} {enemies_defeated}")
        
        print(self.terminal.bold + "├" + "─" * 38 + "┤" + self.terminal.normal)
        
        # Show current player status bars
        health_info = self.create_health_bar_info(player, 20)
        print(f"│ {self.terminal.bold_red}HP:{self.terminal.normal} {health_info['colored_bar']} ({health_info['text']})")
        
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"│ {self.terminal.bold_blue}XP:{self.terminal.normal} {exp_info['colored_bar']} ({exp_info['text']})")
        
        # Show level up if applicable
        if combat_stats.get("level_up", False):
            print(self.terminal.bold + "├" + "─" * 38 + "┤" + self.terminal.normal)
            print(f"│ {self.terminal.yellow + self.terminal.bold}⭐ LEVEL UP!{self.terminal.normal}")
            new_level = combat_stats.get("new_level", 1)
            print(f"│ You are now level {new_level}!")
            print(f"│ {self.terminal.green}✚ Health fully restored!{self.terminal.normal}")
            print(f"│ {self.terminal.cyan}📈 You gained 5 stat points to allocate! (Press 'L' to level up){self.terminal.normal}")
            
        print(self.terminal.bold + "└" + "─" * 38 + "┘" + self.terminal.normal)
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

    def show_character_stats(self, player):
        """Show detailed character statistics"""
        print(self.terminal.clear)
        print(self.terminal.bold + "┌" + "─" * 15 + " Character Stats " + "─" * 15 + "┐" + self.terminal.normal)
        
        stats = player.get_stats()
        detailed = player.get_detailed_stats()
        
        print(f"│ {self.terminal.bold}👤 Name:{self.terminal.normal} {self.terminal.bold}{stats['name']}{self.terminal.normal}")
        print(f"│ {self.terminal.bold}📈 Level:{self.terminal.normal} {stats['level']} (XP: {stats['exp']}/{stats['exp_to_next']})")
        
        print(self.terminal.bold + "├" + "─" * 47 + "┤" + self.terminal.normal)
        
        print("│ " + self.terminal.bold + "Current Stats (Base + Equipment):" + self.terminal.normal)
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
                    f"│   {display_name.upper()}: {total_val} ({base_val} {color}{sign}{bonus_val}{self.terminal.normal})"
                )
            else:
                print(f"│   {display_name.upper()}: {total_val}")
                
        print(f"│   Current HP: {stats['hp']}/{stats['max_hp']}")
        
        # Show equipment bonuses breakdown
        equipped = player.equipment.get_equipped_items()
        if equipped:
            print(self.terminal.bold + "├" + "─" * 47 + "┤" + self.terminal.normal)
            print("│ " + self.terminal.bold + "Equipment Bonuses:" + self.terminal.normal)
            for slot, item in equipped.items():
                stat_parts = []
                for stat, value in item.stats.items():
                    if value != 0:
                        sign = "+" if value > 0 else ""
                        stat_parts.append(f"{stat.upper()}: {sign}{value}")
                
                bonus_text = " | ".join(stat_parts) if stat_parts else "No bonuses"
                print(f"│   {item.name}: {bonus_text}")
        
        print(self.terminal.bold + "└" + "─" * 47 + "┘" + self.terminal.normal)
        print()
        print("Press any key to continue...")
        self.terminal.inkey()

    def show_inventory(self, player):
        """Show enhanced inventory with item management"""
        while True:  # Keep inventory open until user explicitly exits
            print(self.terminal.clear)
            print(self.terminal.bold + "┌" + "─" * 18 + " Inventory " + "─" * 18 + "┐" + self.terminal.normal)
            
            if not player.inventory:
                print("│ Your inventory is empty.")
            else:
                print("│ Items in your inventory:")
                print(self.terminal.bold + "├" + "─" * 48 + "┤" + self.terminal.normal)
                
                for i, item in enumerate(player.inventory, 1):
                    # Show item with quality color and equipment status
                    quality_info = item.get_quality_info()
                    equipped_text = f" {self.terminal.green}[EQUIPPED]{self.terminal.normal}" if item.equipped else ""
                    
                    print(f"│ {i}. {item.symbol} {self.terminal.bold}{item.name}{self.terminal.normal}{equipped_text}")
                    print(f"│    Type: {item.type.title()} | Quality: {quality_info['name']}")
                    print(f"│    {item.description}")
                    
                    # Show stats
                    stat_parts = []
                    for stat, value in item.stats.items():
                        if value != 0:
                            sign = "+" if value > 0 else ""
                            color = self.terminal.green if value > 0 else self.terminal.red
                            stat_parts.append(f"{stat.upper()}: {color}{sign}{value}{self.terminal.normal}")
                    
                    if stat_parts:
                        print(f"│    Stats: {' | '.join(stat_parts)}")
                    print("│")
            
            # Show equipped items summary
            equipped = player.equipment.get_equipped_items()
            if equipped:
                print(self.terminal.bold + "├" + "─" * 48 + "┤" + self.terminal.normal)
                print("│ " + self.terminal.bold + "Currently Equipped:" + self.terminal.normal)
                for slot, item in equipped.items():
                    print(f"│   {slot.replace('_', ' ').title()}: {self.terminal.yellow}{item.name}{self.terminal.normal}")
                print("│")
            
            print(self.terminal.bold + "└" + "─" * 48 + "┘" + self.terminal.normal)
            print(self.terminal.bold + "Commands:" + self.terminal.normal)
            print("E = Equip/Unequip item")
            print("U = Use item") 
            print("Any other key = Back to game")
            print()
            print("Choose an action: ", end="", flush=True)
            
            key = self.terminal.inkey()
            print(key)  # Show what key was pressed
            
            if key.lower() == 'e':
                self.handle_equip_unequip(player)
                # Continue the loop to stay in inventory
            elif key.lower() == 'u':
                self.handle_use_item(player)
                # Continue the loop to stay in inventory
            else:
                print("Returning to game...")
                break

    def handle_equip_unequip(self, player):
        """Handle equipping/unequipping items"""
        if not player.inventory:
            print("No items to equip!")
            print("Press any key to continue...")
            self.terminal.inkey()
            return
            
        while True:
            print(f"\nSelect item number to equip/unequip (1-{len(player.inventory)}) or 0 to cancel: ", end="", flush=True)
            
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
                elif 1 <= choice <= len(player.inventory):
                    item = player.inventory[choice - 1]
                    print(f"Selected: {item.name}")
                    
                    if item.equipped:
                        success, message = player.unequip_item(item)
                    else:
                        success, message = player.equip_item(item)
                        
                    print(f"{message}")
                    print("Press any key to continue...")
                    self.terminal.inkey()
                    break
                else:
                    print(f"Please enter a number between 1 and {len(player.inventory)}, or 0 to cancel.")
                    print("Try again...")
                    
            except ValueError:
                if choice_str:
                    print(f"'{choice_str}' is not a valid number!")
                else:
                    print("Please enter a number!")
                print("Try again...")

    def handle_use_item(self, player):
        """Handle using/consuming items"""
        if not player.inventory:
            print("No items to use!")
            print("Press any key to continue...")
            self.terminal.inkey()
            return
            
        while True:
            print(f"\nSelect item number to use (1-{len(player.inventory)}) or 0 to cancel: ", end="", flush=True)
            
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
                elif 1 <= choice <= len(player.inventory):
                    item = player.inventory[choice - 1]
                    print(f"Selected: {item.name}")
                    
                    success, message = player.use_item(item)
                    print(f"{message}")
                    print("Press any key to continue...")
                    self.terminal.inkey()
                    break
                else:
                    print(f"Please enter a number between 1 and {len(player.inventory)}, or 0 to cancel.")
                    print("Try again...")
                    
            except ValueError:
                if choice_str:
                    print(f"'{choice_str}' is not a valid number!")
                else:
                    print("Please enter a number!")
                print("Try again...")