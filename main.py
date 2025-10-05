#!/usr/bin/env python3
"""
Terminal Dungeon Crawler - Main Entry Point
A classic ASCII roguelike adventure game
"""

import sys
import os

# Add the game directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from game.engine import GameEngine


import pygame.mixer
pygame.mixer.init()
game_welcome_sound = pygame.mixer.Sound('game/sounds/gamestart-272829.wav')
game_welcome_sound.set_volume(0.5)

def main():
    """Main entry point for the game"""
    try:
        game_welcome_sound.play()
        print("🏰 Welcome to Terminal Dungeon Crawler! 🏰")
        print("Initializing game...")
        
        game = GameEngine()
        game.run()
        
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Adventure awaits your return...")
    except Exception as e:
        print(f"\n💥 Game crashed: {e}")
        print("Please report this bug on GitHub!")
        sys.exit(1)

if __name__ == "__main__":
    main()