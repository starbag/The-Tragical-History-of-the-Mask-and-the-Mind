import pygame
from enums import MenuAction
from utils import draw_shadowed_text, load_font

class CreditsMenu:
    def __init__(self, screen_width, screen_height, settings_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings_manager = settings_manager

        # Load fonts
        self.title_font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 24)
        self.font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 18)

        self.credits_lines = [
            "THE TRAGICAL HISTORY",
            "OF THE MASK AND THE MIND",
            "— A Play in One Person —",
            "",
            "Written, Directed, and Programmed by",
            "starbag",
            "",
            "All roles, voices, and stage management",
            "executed by the same exhausted mind.",
            "",
            "One man in his time plays many parts...",
            "- William Shakespeare",
            "",
            "Technology and Tools",
            "Python and pygamece (Community Edition)",
            "",
            "Typography",
            "Shakespeare First Folio Font",
            "",
            "Special Thanks",
            "To everyone who sits before this stage.",
            "",
            "Exeunt."
        ]

        self.line_spacing = 45
        self.max_scroll_y = len(self.credits_lines) * self.line_spacing + self.screen_height + 50

        self.reset_scroll()

        try:
            self.key_enter_icon = pygame.image.load('assets/icons/key_enter.svg').convert_alpha()
            self.btn_cross_icon = pygame.image.load('assets/icons/btn_cross.svg').convert_alpha()

            self.key_enter_icon = pygame.transform.scale(self.key_enter_icon, (36, 36))
            self.btn_cross_icon = pygame.transform.scale(self.btn_cross_icon, (36, 36))
        except (pygame.error, FileNotFoundError):
            self.key_enter_icon = None
            self.btn_cross_icon = None

    def reset_scroll(self):
        """Reset scroll position to the beginning."""
        self.scroll_y = 0.0
        self.scroll_speed = 1.2
        self.finished = False

    def handle_event(self, event):
        """Handle input to allow returning back to settings (works anytime or when finished)."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return MenuAction.BACK
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 or event.button == 1:
                return MenuAction.BACK
        return None

    def update(self):
        """Update scroll position and stop when credits finish."""
        if not self.finished:
            self.scroll_y += self.scroll_speed
            if self.scroll_y >= self.max_scroll_y:
                self.scroll_y = self.max_scroll_y
                self.finished = True

    def draw(self, surface):
        surface.fill((10, 10, 20))
        start_y = self.screen_height - self.scroll_y

        for i, line in enumerate(self.credits_lines):
            y_pos = start_y + (i * self.line_spacing)

            if -50 < y_pos < self.screen_height + 50:
                if i == 0 or i == 1 or line == "starbag":
                    color = (255, 215, 0)
                    current_font = self.title_font
                elif line.startswith("—") or line.startswith("\""):
                    color = (150, 150, 180)
                    current_font = self.font
                else:
                    color = (200, 200, 200)
                    current_font = self.font

                draw_shadowed_text(
                    surface, line, current_font, color, (20, 20, 20),
                    self.screen_width // 2, y_pos, center=True
                )

        # When credits are over, render return text and icon
        if self.finished:
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            action_text = "to Return"

            # selecting valid icon
            if self.settings_manager.active_controller == "joystick":
                active_icon = self.btn_cross_icon
            else:
                active_icon = self.key_enter_icon

            # if icon loaded
            if active_icon:
                icon_rect = active_icon.get_rect(center=(center_x, center_y - 20))
                surface.blit(active_icon, icon_rect)

                draw_shadowed_text(
                    surface, action_text, self.font, (200, 200, 200), (10, 10, 10),
                    center_x, center_y + 20, center=True
                )
            else:
                fallback_text = "Press A / ENTER to Return"
                draw_shadowed_text(
                    surface, fallback_text, self.font, (255, 255, 255), (10, 10, 10),
                    center_x, center_y, center=True
                )