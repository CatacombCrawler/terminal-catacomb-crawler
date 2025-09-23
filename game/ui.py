from bearlibterminal import terminal
from ui import render, render_help_screen, add_message, init_message_log
from level import Level
from player.character_creation import Player
from monsters.monsters import MonsterManager

def main():
    # Setup terminal
    terminal.open()
    terminal.set("window: size=80x50, title='Catacomb Crawler'; font: default")

    # Initialize game components
    init_message_log()
    level = Level()
    player = Player()
    monsters = MonsterManager()
    dungeon_level = 1

    add_message("Welcome to Catacomb Crawler!")

    # Main game loop
    while True:
        render(player, level, monsters, dungeon_level)
        key = terminal.read()

        if key == terminal.TK_Q:
            add_message("You quit the game.")
            break
        elif key == terminal.TK_H:
            render_help_screen()
        elif key == terminal.TK_UP:
            player.move(0, -1, level)
            add_message("You moved north.")
        elif key == terminal.TK_DOWN:
            player.move(0, 1, level)
            add_message("You moved south.")
        elif key == terminal.TK_LEFT:
            player.move(-1, 0, level)
            add_message("You moved west.")
        elif key == terminal.TK_RIGHT:
            player.move(1, 0, level)
            add_message("You moved east.")

        monsters.update(player)

    terminal.close()

if __name__ == "__main__":
    main()