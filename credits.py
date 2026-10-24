import pygame
from utils import draw_shadowed_text, load_font


class CreditsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load fonts
        self.title_font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 24)
        self.font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 18)

        # Theatrical credits lines
        self.credits_lines = [
            "THE TRAGICAL HISTORY",
            "OF THE MASK AND THE MIND"
            "",
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

        self.reset_scroll()

    def reset_scroll(self):
        """Reset scroll position so credits start from below the screen."""
        self.scroll_y = 0.0
        self.scroll_speed = 1.2  # Speed of auto-scrolling (pixels per frame)

    def handle_event(self, event):
        """Handle input to allow skipping credits back to menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "BACK"
        elif event.type == pygame.JOYBUTTONDOWN:
            # Button 0 (A) or Button 1 (B) on gamepad returns to menu
            if event.button == 0 or event.button == 1:
                return "BACK"
        return None

    def update(self):
        """Update the auto-scroll offset every frame."""
        self.scroll_y += self.scroll_speed

        # Automatically loop or stop when credits finish scrolling past the top
        total_height = len(self.credits_lines) * 40 + self.screen_height
        if self.scroll_y > total_height:
            self.reset_scroll()

    def draw(self, surface):
        """Render the credits centered and moving upwards."""
        # Background fill
        surface.fill((10, 10, 20))

        line_spacing = 45
        # Start rendering text from the bottom of the screen and move upwards based on scroll_y
        start_y = self.screen_height - self.scroll_y

        for i, line in enumerate(self.credits_lines):
            y_pos = start_y + (i * line_spacing)

            # Render only lines that are visible on screen to optimize performance
            if -50 < y_pos < self.screen_height + 50:
                # Highlight title and developer name
                if i == 0 or line == "starbag":
                    color = (255, 215, 0)
                    current_font = self.title_font
                elif line.startswith("—") or line.startswith("\""):
                    color = (150, 150, 180)
                    current_font = self.font
                else:
                    color = (200, 200, 200)
                    current_font = self.font

                shadow = (20, 20, 20)

                # Render perfectly centered horizontally
                draw_shadowed_text(
                    surface,
                    line,
                    current_font,
                    color,
                    shadow,
                    self.screen_width // 2,
                    y_pos,
                    center=True
                )