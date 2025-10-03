"""
Level Up UI - Interface for allocating stat points when leveling up
"""

import contextlib

try:
    import termios
    import tty
except Exception:  # pragma: no cover
    termios = None
    tty = None


class LevelUpUI:
    """Handles the level up interface for stat point allocation"""
    
    def __init__(self, terminal):
        self.terminal = terminal
        
    def show_level_up_screen(self, player):
        """Show the level up screen and handle stat point allocation"""
        if player.stat_points <= 0:
            return  # No points to allocate
            
        while player.stat_points > 0:
            self.render_level_up_screen(player)
            
            # Get user input
            try:
                with self.normal_input_mode():
                    choice = input().strip()
                original_choice = choice  # Keep the original for display
                choice = choice.lower()   # Use lowercase for comparison
                
                # Show what the user typed immediately
                print(f"Your choice: {original_choice}")
                
                if choice == 'q':
                    # Quit and save remaining points for later
                    print(f"{self.terminal.yellow}You chose: quit{self.terminal.normal}")
                    print("Saving remaining stat points for later...")
                    with self.normal_input_mode():
                        input("Press Enter to continue...")
                    break
                elif choice == 'done' or choice == 'd':
                    # Finish allocation
                    print(f"{self.terminal.yellow}You chose: done{self.terminal.normal}")
                    print("Finishing stat allocation...")
                    with self.normal_input_mode():
                        input("Press Enter to continue...")
                    break
                elif choice.isdigit():
                    # User selected a stat by number
                    stat_num = int(choice)
                    stat_names = list(player.stats.db.STATS["main"].keys())
                    
                    if 1 <= stat_num <= len(stat_names):
                        stat_name = stat_names[stat_num - 1]
                        stat_config = player.stats.db.STATS["main"][stat_name]
                        
                        # Show the interpretation of their choice
                        print(f"{self.terminal.cyan}You chose: {stat_num}. {stat_config['name']}{self.terminal.normal}")
                        
                        success, message = player.spend_stat_point(stat_name)
                        
                        if success:
                            print(f"{self.terminal.green}✓ {message}{self.terminal.normal}")
                        else:
                            print(f"{self.terminal.red}✗ {message}{self.terminal.normal}")
                        
                        with self.normal_input_mode():
                            input("\nPress Enter to continue...")
                    else:
                        print(f"{self.terminal.red}✗ Invalid choice. Please enter 1-{len(stat_names)}{self.terminal.normal}")
                        with self.normal_input_mode():
                            input("Press Enter to continue...")
                else:
                    print(f"{self.terminal.red}✗ Invalid input. Enter a number (1-9), 'done', or 'q' to quit{self.terminal.normal}")
                    with self.normal_input_mode():
                        input("Press Enter to continue...")
                    
            except (ValueError, KeyboardInterrupt):
                print(f"\n{self.terminal.red}✗ Invalid input or interrupted{self.terminal.normal}")
                with self.normal_input_mode():
                    input("Press Enter to continue...")
                
        # Show completion message
        if player.stat_points == 0:
            print(self.terminal.clear)
            print(f"{self.terminal.bold}{self.terminal.green}🎉 All stat points allocated! 🎉{self.terminal.normal}")
            print("\nYour character has grown stronger!")
            with self.normal_input_mode():
                input("Press Enter to continue...")
        
    def render_level_up_screen(self, player):
        """Render the level up interface"""
        print(self.terminal.clear)
        
        # Header
        print(f"{self.terminal.bold}{self.terminal.yellow}⭐ LEVEL UP! ⭐{self.terminal.normal}")
        print(f"{self.terminal.bold}Congratulations! You've reached level {player.level}!{self.terminal.normal}")
        
        # Show health restoration benefit
        health_restored = player.max_hp - player.hp
        if health_restored > 0:
            print(f"{self.terminal.green}✚ Health fully restored! (+{health_restored} HP){self.terminal.normal}")
        else:
            print(f"{self.terminal.green}✚ Health fully restored!{self.terminal.normal}")
        
        print(f"You have {self.terminal.bold}{self.terminal.cyan}{player.stat_points}{self.terminal.normal} stat points to allocate.\n")
        
        # Show current stats and allocation options
        print(f"{self.terminal.bold}Choose a stat to improve:{self.terminal.normal}")
        print("-" * 60)
        
        stat_names = list(player.stats.db.STATS["main"].keys())
        
        for i, stat_name in enumerate(stat_names, 1):
            stat_config = player.stats.db.STATS["main"][stat_name]
            current_value = player.stats.get_stat(stat_name)
            base_value = player.stats.get_base_stat(stat_name)
            allocated = player.stats.allocated_main.get(stat_name, 0)
            
            # Color coding based on stat type
            stat_colors = {
                'strength': self.terminal.red,
                'dexterity': self.terminal.green,
                'vitality': self.terminal.blue,
                'intelligence': self.terminal.magenta,
                'athletism': self.terminal.yellow,
                'cunning': self.terminal.cyan,
                'willpower': self.terminal.white,
                'charisma': self.terminal.bright_yellow,
                'luck': self.terminal.bright_green,
            }
            
            color_func = stat_colors.get(stat_name, self.terminal.white)
            
            # Check if stat is at maximum
            can_increase = allocated < stat_config["max_value"]
            status_indicator = "✓" if can_increase else "MAX"
            status_color = self.terminal.green if can_increase else self.terminal.red
            
            print(f"{i:2}. {color_func(stat_config['name'].ljust(12))} "
                  f"Current: {self.terminal.bold}{current_value:3}{self.terminal.normal} "
                  f"(Base: {base_value:2}, Allocated: {allocated:2}) "
                  f"{status_color}[{status_indicator}]{self.terminal.normal}")
            
            # Show what this stat affects (key derived stats)
            affects = self.get_stat_effects(stat_name, player)
            if affects:
                print(f"    {self.terminal.dim}Affects: {affects}{self.terminal.normal}")
            print()
        
        print("-" * 60)
        print(f"{self.terminal.bold}Commands:{self.terminal.normal}")
        print("• Enter a number (1-9) to add 1 point to that stat")
        print("• Type 'done' or 'd' to finish allocating")
        print("• Type 'q' to quit and save remaining points for later")
        print(f"\nRemaining points: {self.terminal.bold}{self.terminal.cyan}{player.stat_points}{self.terminal.normal}")
        print(f"Your choice: ", end="", flush=True)
        
    @contextlib.contextmanager
    def normal_input_mode(self):
        """temporarily switch to cooked mode with echo for line input.
        on platforms without termios (e.g., windows), this is a no-op except for cursor visibility.
        """
        # show cursor while the user types
        try:
            print(self.terminal.show_cursor, end="", flush=True)
        except Exception:
            pass

        if termios is not None and hasattr(self.terminal, "_keyboard_fd") and self.terminal._keyboard_fd is not None:
            fd = self.terminal._keyboard_fd
            try:
                # save current attributes
                saved_attrs = termios.tcgetattr(fd)
                saved_line_buffered = getattr(self.terminal, "_line_buffered", True)

                # enable canonical mode and echo (cooked mode)
                attrs = termios.tcgetattr(fd)
                attrs[3] |= (termios.ICANON | termios.ECHO)
                termios.tcsetattr(fd, termios.TCSANOW, attrs)

                if hasattr(self.terminal, "_line_buffered"):
                    self.terminal._line_buffered = True

                yield
            finally:
                # restore cbreak mode if possible
                try:
                    if tty is not None:
                        tty.setcbreak(fd, termios.TCSANOW)
                except Exception:
                    # best-effort; fall back to restoring saved attrs
                    try:
                        termios.tcsetattr(fd, termios.TCSAFLUSH, saved_attrs)
                    except Exception:
                        pass
                if hasattr(self.terminal, "_line_buffered"):
                    self.terminal._line_buffered = saved_line_buffered
        else:
            # platform without termios; do nothing special
            yield
        # hide cursor again
        try:
            print(self.terminal.hide_cursor, end="", flush=True)
        except Exception:
            pass

    def get_stat_effects(self, stat_name, player):
        """Get a brief description of what derived stats this main stat affects"""
        effects = []
        
        # Check derived stats that use this main stat in their formula
        for derived_name, derived_config in player.stats.db.STATS["derived"].items():
            formula = derived_config["formula"]
            if stat_name in formula:
                # Add important derived stats to the effects list
                important_derived = {
                    'health': 'HP',
                    'attack': 'ATK', 
                    'defense': 'DEF',
                    'speed': 'SPD',
                    'mana': 'MP',
                    'accuracy': 'ACC',
                    'dodge': 'DOD',
                    'parry': 'PAR',
                    'crit_chance': 'CRIT%',
                }
                
                if derived_name in important_derived:
                    effects.append(important_derived[derived_name])
        
        return ", ".join(effects[:4])  # Show max 4 effects to keep it concise
