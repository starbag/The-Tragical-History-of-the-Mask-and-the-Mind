import pygame
from utils import draw_shadowed_text, load_font

class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 20)
        self.title_font = pygame.font.SysFont('Georgia', 24)

        self.tabs = ["Graphics", "Sound", "Controls", "Exit"]
        self.curr_tab = 0

        self.graphics_options = ["Full screen: disabled", "Resolution: 800x600", "V-Sync: enabled"]
        self.sound_options = ["Volume: 100%", "Music: on"]
        self.controls_options = ["Control Devices: Keyboard", "Joystick: not detected"]
        self.exit_options = ["Return to Main Menu"]

        self.selected_option = 0

    def _get_current_options(self):
        tab_name = self.tabs[self.curr_tab]
        if tab_name == "Graphics":
            return self.graphics_options
        elif tab_name == "Sound":
            return self.sound_options
        elif tab_name == "Controls":
            return self.controls_options
        elif tab_name == "Exit":
            return self.exit_options
        return []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "BACK"
            elif event.key == pygame.K_LEFT:
                self.curr_tab = (self.curr_tab - 1) % len(self.tabs)
                self.selected_option = 0
            elif event.key == pygame.K_RIGHT:
                self.curr_tab = (self.curr_tab + 1) % len(self.tabs)
                self.selected_option = 0
            elif event.key == pygame.K_UP:
                current_opts = self._get_current_options()
                if current_opts:
                    self.selected_option = (self.selected_option - 1) % len(current_opts)
            elif event.key == pygame.K_DOWN:
                current_opts = self._get_current_options()
                if current_opts:
                    self.selected_option = (self.selected_option + 1) % len(current_opts)
            elif event.key == pygame.K_RETURN:
                if self.tabs[self.curr_tab] == "Exit":
                    return "BACK"
        return None


    def draw(self, surface):
        surface.fill((10, 10, 20))

        start_x = 80
        tab_y = 40
        for i, tab in enumerate(self.tabs):
            # Curr tab highlight
            color = (255, 255, 0) if i == self.curr_tab else (120, 120, 120)
            shadow = (20, 20, 20)

            draw_shadowed_text(surface, tab, self.title_font, color, shadow,
                               start_x + (i * 160), tab_y, center=False)

        # Line
        pygame.draw.line(surface, (80, 80, 110), (60, 80),
                         (self.screen_width - 60, 80), 2)

        # Curr option highlight
        current_opts = self._get_current_options()
        for i, option in enumerate(current_opts):
            color = (255, 255, 0) if i == self.selected_option else (120, 120, 120)
            shadow = (20, 20, 20)
            prefix = "> " if i == self.selected_option else " "
            text_to_render = prefix + option

            draw_shadowed_text(
                surface, text_to_render, self.font, color, shadow,
                100, 130 + (i * 45), center=False
            )

