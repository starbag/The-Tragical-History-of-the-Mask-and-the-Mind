import pygame
from enums import MenuAction

class SettingsManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_fullscreen = False
        self.vsync_enabled = 1
        self.active_controller = "keyboard"

    def _rebuild_surface(self) -> pygame.Surface:
        flags = pygame.FULLSCREEN if self.is_fullscreen else 0
        return pygame.display.set_mode(
        (self.screen_width, self.screen_height),
             flags,
             vsync=self.vsync_enabled,
        )

    def apply_action(self, action: MenuAction) -> pygame.Surface | None:
        new_screen = None

        # Graphics Actions
        if action == MenuAction.TOGGLE_FULL_SCREEN_ON:
            self.is_fullscreen = True
            new_screen = self._rebuild_surface()
        elif action == MenuAction.TOGGLE_FULL_SCREEN_OFF:
            self.is_fullscreen = False
            new_screen = self._rebuild_surface()
        elif action == MenuAction.RES_1024:
            self.screen_width, self.screen_height = 1024, 768
            new_screen = self._rebuild_surface()
        elif action == MenuAction.RES_800:
            self.screen_width, self.screen_height = 800, 600
            new_screen = self._rebuild_surface()
        elif action == MenuAction.VSYNC_ON:
            self.vsync_enabled = True
            new_screen = self._rebuild_surface()
        elif action == MenuAction.VSYNC_OFF:
            self.vsync_enabled = False
            new_screen = self._rebuild_surface()

        # Audio Actions
        elif action == MenuAction.VOLUME_100:
            pygame.mixer.music.set_volume(1.0)
        elif action == MenuAction.VOLUME_75:
            pygame.mixer.music.set_volume(0.75)
        elif action == MenuAction.VOLUME_50:
            pygame.mixer.music.set_volume(0.5)
        elif action == MenuAction.VOLUME_25:
            pygame.mixer.music.set_volume(0.25)
        elif action == MenuAction.VOLUME_0:
            pygame.mixer.music.set_volume(0)
        elif action == MenuAction.MUSIC_ON:
            pygame.mixer.music.unpause()
        elif action == MenuAction.MUSIC_OFF:
            pygame.mixer.music.pause()

        # Controller Actions
        elif action == MenuAction.USE_JOYSTICK:
            self.active_controller = "joystick"
        elif action == MenuAction.USE_KEYBOARD:
            self.active_controller = "keyboard"

        return new_screen

