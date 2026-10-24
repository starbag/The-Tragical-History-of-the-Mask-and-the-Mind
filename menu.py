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

        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("The Tragical History of the Mask and the Mind")
        clock = pygame.time.Clock()

    def draw(self, surface):
        surface.fill((15, 15, 25))

        for i, option in enumerate(self.options):
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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]

        return None