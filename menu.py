import pygame
from helpers import int_to_roman
from utils import draw_shadowed_text, load_font

class MainMenu:
    def __init__(self, screen_width, screen_height, curr_act_n):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.curr_act_n = curr_act_n
        self.curr_act_r = int_to_roman(self.curr_act_n)
        self.font = load_font("assets/fonts/Shakespeare First Folio Font.otf", 32)
        self.options = [f"Begin act {self.curr_act_r}", "Options", "Leave"]
        self.selected_index = 0

    def draw(self, surface):
        """Render the main menu layout onto the surface."""
        surface.fill((15, 15, 25))

        for i, option in enumerate(self.options):
            # Highlight the currently selected option
            color = (255, 215, 0) if i == self.selected_index else (150, 150, 150)
            shadow = (20, 20, 20)
            x_pos = self.screen_width // 2
            y_pos = 200 + i * 60

            draw_shadowed_text(
                surface,
                option,
                self.font,
                color,
                shadow,
                x_pos,
                y_pos,
                center=True
            )

    def _confirm_selection(self):
        """Helper method to return the chosen menu option string."""
        return self.options[self.selected_index]

    def handle_event(self, event):
        """Handle keyboard and gamepad input for main menu navigation."""
        def move_up():
            # Decrease index to move up (wrap around using modulo)
            self.selected_index = (self.selected_index - 1) % len(self.options)

        def move_down():
            # Increase index to move down (wrap around using modulo)
            self.selected_index = (self.selected_index + 1) % len(self.options)

        # 1. Keyboard input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up()
            elif event.key == pygame.K_DOWN:
                move_down()
            elif event.key == pygame.K_RETURN:
                return self._confirm_selection()

        # 2. Gamepad / Joystick D-Pad (Hat) navigation
        elif event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            if hat_y == 1:
                move_up()
            elif hat_y == -1:
                move_down()

        # 3. Gamepad button confirmation (Button 0 / A on Xbox/PlayStation)
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                return self._confirm_selection()

        return None