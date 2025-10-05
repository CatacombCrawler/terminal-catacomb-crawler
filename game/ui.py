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
            
    def render_status_bar(self, player, level_info=None):
        """Render player status information"""
        stats = player.get_stats()
        
        print("\n" + "=" * 50)
        
        # Health bar using helper function
        health_info = self.create_health_bar_info(player, 20)
        print(f"Health: {health_info['colored_bar']} ({health_info['text']})")
        
        # Experience bar using helper function
        exp_info = self.create_exp_bar_info(player, 20)
        print(f"EXP:    {exp_info['colored_bar']} ({exp_info['text']})")
        
        # Location information
        location_text = "Main Level"
        if level_info and level_info.get("in_door_room", False):
            location_text = "Door Room"
        
        dungeon_level = level_info.get("dungeon_level", 1) if level_info else 1
        
        # Stats
        stat_points_text = ""
        if hasattr(player, 'stat_points') and player.stat_points > 0:
            stat_points_text = f" | {self.terminal.bold}{self.terminal.yellow}Stat Points: {player.stat_points}!{self.terminal.normal}"
        
        print(f"Player Level: {stats['level']} | "
              f"Dungeon Level: {self.terminal.cyan(str(dungeon_level))} | "
              f"Attack: {stats['attack']} | "
              f"Defense: {stats['defense']}{stat_points_text}")
        print(f"Location: {location_text} | Position: ({stats['position'][0]}, {stats['position'][1]})")

              
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
            
        print(self.terminal.bold + "Combat Log:" + self.terminal.normal)
        
        # Show last 5 combat messages to avoid clutter
        recent_messages = combat_messages[-5:] if len(combat_messages) > 5 else combat_messages
        
        for msg in recent_messages:
            if msg["type"] == "combat":
                if "target" in msg:  # Player attacking enemy - use rich player attack data
                    text = self._format_player_attack(msg)
                    print(f"  {self.terminal.green(text)}")
                elif "defender" in msg:  # Defend action
                    print(f"  {self.terminal.blue(msg['message'])}")
                else:  # Enemy attacking player - use rich monster attack data
                    text = self._format_monster_attack(msg)
                    color = self.terminal.red
                    if msg.get("player_died"):
                        color = self.terminal.red + self.terminal.bold
                    print(f"  {color(text)}")
            elif msg["type"] == "deflection":
                print(f"  {self.terminal.blue + self.terminal.bold}⚡ {msg['message']}{self.terminal.normal}")
            elif msg["type"] == "combat_detail":
                print(f"  {self.terminal.dim}💡 {msg['message']}{self.terminal.normal}")
            elif msg["type"] == "round_separator":
                print(f"  {self.terminal.dim}{msg['message']}{self.terminal.normal}")
            elif msg["type"] == "system":
                print(f"  {self.terminal.yellow(msg['message'])}")
    
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
            print("EXPLORATION: WASD/Arrows=Move | E=Interact | Q=Quit | I=Inventory | C=Stats | L=Level Up | Z=Save")
        
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
            print(f"{self.terminal.green}✚ Health fully restored!{self.terminal.normal}")
            print(f"{self.terminal.cyan}📈 You gained 5 stat points to allocate! (Press 'L' to level up){self.terminal.normal}")
            
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