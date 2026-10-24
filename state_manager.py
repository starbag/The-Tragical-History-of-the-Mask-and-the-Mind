import pygame
from enums import GameState, MenuAction
from menu import MainMenu
from settings import SettingsMenu
from credits import CreditsMenu
from settings_manager import SettingsManager

class StateManager:
    """Manages application states, views, and delegates events."""

    def __init__(self, screen: pygame.Surface, screen_width: int, screen_height: int, current_act: int):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_act = current_act

        # Initialize game state and managers/menus
        self.state = GameState.MENU

        self.main_menu = MainMenu(self.screen_width, self.screen_height, self.current_act)
        self.settings_menu = SettingsMenu(self.screen_width, self.screen_height)
        self.settings_manager = SettingsManager(self.screen_width, self.screen_height)
        self.credits_menu = CreditsMenu(self.screen_width, self.screen_height, self.settings_manager)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles events based on the current active state. Returns False to quit."""
        action = None

        # State: Main Menu
        if self.state == GameState.MENU:
            action = self.main_menu.handle_event(event)
            if action == f"Begin act {self.main_menu.curr_act_r}":
                self.state = GameState.GAME
            elif action == "Options":
                self.state = GameState.SETTINGS
            elif action == "Leave":
                return False

        # State: Settings Menu
        elif self.state == GameState.SETTINGS:
            action = self.settings_menu.handle_event(event)
            if action == MenuAction.BACK:
                self.state = GameState.MENU
            elif action == MenuAction.SHOW_CREDITS:
                self.state = GameState.CREDITS
                self.credits_menu.reset_scroll()
            else:
                # Apply changes via settings_manager and update surface if resized
                new_screen = self.settings_manager.apply_action(action)
                if new_screen:
                    self.screen = new_screen

        # State: Credits
        elif self.state == GameState.CREDITS:
            action = self.credits_menu.handle_event(event)
            if action == MenuAction.BACK:
                self.state = GameState.SETTINGS
                self.credits_menu.reset_scroll()

        # State: Game Loop
        elif self.state == GameState.GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

        return True

    def update_and_draw(self):
        """Updates and renders the active screen state."""
        if self.state == GameState.MENU:
            self.main_menu.draw(self.screen)

        elif self.state == GameState.SETTINGS:
            self.settings_menu.draw(self.screen)

        elif self.state == GameState.CREDITS:
            self.credits_menu.update()
            self.credits_menu.draw(self.screen)

        elif self.state == GameState.GAME:
            self.screen.fill((20, 10, 30))
            font = pygame.font.SysFont("Arial", 20)
            txt = font.render(
                f"Act {self.current_act}",
                True,
                (200, 200, 200)
            )
            self.screen.blit(txt, (10, 10))