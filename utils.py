import pygame
import os

def draw_shadowed_text(surface, text, font, text_color, shadow_color, x_pos, y_pos, center=False):
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect()

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    if center:
        shadow_rect.center = (x_pos + 2, y_pos + 2)
        text_rect.center = (x_pos, y_pos)
    else:
        shadow_rect.topleft = (x_pos + 2, y_pos + 2)
        text_rect.topleft = (x_pos, y_pos)

    surface.blit(shadow_surface, shadow_rect)
    surface.blit(text_surface, text_rect)

def load_font(filename, size):
    if os.path.exists(filename):
        return pygame.font.Font(filename, size)
    else:
        return pygame.font.SysFont("Georgia", size)

def draw_panel(surface, color, border_color, rect, border_width=2):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, border_color, rect, border_width)