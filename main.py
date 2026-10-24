import pygame
from menu import MainMenu
from settings import SettingsMenu
from helpers import int_to_roman

pygame.init()
pygame.font.init()
pygame.joystick.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

current_act = 1
pygame.display.set_caption(f"The Tragical History of the Mask and the Mind - Act {int_to_roman(current_act)}")

clock = pygame.time.Clock()

main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT, current_act)
settings_menu = SettingsMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

current_state = "MENU"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if current_state == "MENU":
            action = main_menu.handle_event(event)
            if action == "Begin act I":
                current_state = "GAME"
            elif action == "Options":
                current_state = "SETTINGS"
            elif action == "Leave":
                running = False
        elif current_state == "SETTINGS":
            action = settings_menu.handle_event(event)
            if action == "Back":
                current_state = "MENU"

    if current_state == "MENU":
        main_menu.draw(screen)
    elif current_state == "SETTINGS":
        settings_menu.draw(screen)
        if action == "BACK":
            current_state = "MENU"
    elif current_state == "GAME":
        screen.fill((20, 10, 30))
        font = pygame.font.SysFont("Arial", 12)
        txt = font.render(f"Act {int_to_roman(current_act)} (Press ESC to return)",
                        True, (200, 200, 200))
        screen.blit(txt, (10, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            current_state = "MENU"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
