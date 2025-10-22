import pygame.mixer
import pygame.time
from pathlib import Path


class SoundManager():
    def __init__(self,enabled=True):

        self.enabled=enabled
        current_file = Path(__file__)
        self.sound_dir = current_file.parent/"sounds"

    def play_sound(self,sound,volume=1.0):
        if self.enabled:
                if not pygame.mixer.get_init():
                    print("!! sound manager is not initialized !!")
                    return False
                try:
                    sound_path = self.sound_dir / sound
                    sound_to_init = pygame.mixer.Sound(str(sound_path))
                    sound_to_init.set_volume(volume)
                    sound_to_init.play()
                except FileNotFoundError:
                    print(f"cant find sound file {sound}")
                    return False
                except Exception as e:
                    print (f"Error playing sound {sound}: {e}")
                    return False
        return True

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled
