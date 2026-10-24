from operator import truediv

import pygame
from pygame.display import is_fullscreen

from menu import MainMenu
from settings import SettingsMenu
from helpers import int_to_roman

pygame.init()
pygame.font.init()
pygame.joystick.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
is_fullscreen = False
active_controller = "keyboard"

vsync_enabled = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

current_act = 1
pygame.display.set_caption(f"The Tragical History of the Mask and the Mind - Act {int_to_roman(current_act)}")

clock = pygame.time.Clock()

main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT, current_act)
settings_menu = SettingsMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    settings_menu.controls_options[1] = "Joystick: detected"

current_state = "MENU"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == "MENU":
            action = main_menu.handle_event(event)
            if action == f"Begin act {main_menu.curr_act_r}":
                current_state = "GAME"
            elif action == "Options":
                current_state = "SETTINGS"
            elif action == "Leave":
                running = False

        elif current_state == "SETTINGS":
            action = settings_menu.handle_event(event)

            # returning back to menu
            if action == "BACK":
                current_state = "MENU"

            # graphics
            elif action == "TOGGLE_FULLSCREEN_ON":
                is_fullscreen = True
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, vsync=vsync_enabled)

            elif action == "TOGGLE_FULLSCREEN_OFF":
                is_fullscreen = False
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, vsync=vsync_enabled)

            elif action == "RES_1024":
                SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
                flags = pygame.FULLSCREEN if is_fullscreen else 0
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=vsync_enabled)

            elif action == "RES_800":
                SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
                flags = pygame.FULLSCREEN if is_fullscreen else 0
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=vsync_enabled)

            elif action == "VSYNC_ON":
                vsync_enabled = 1
                flags = pygame.FULLSCREEN if is_fullscreen else 0
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=vsync_enabled)

            elif action == "VSYNC_OFF":
                vsync_enabled = 0
                flags = pygame.FULLSCREEN if is_fullscreen else 0
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=vsync_enabled)

            # sound
            elif action == "VOLUME_100":
                pygame.mixer.music.set_volume(1.0)

            elif action == "VOLUME_75":
                pygame.mixer.music.set_volume(0.75)

            elif action == "VOLUME_50":
                pygame.mixer.music.set_volume(0.5)

            elif action == "VOLUME_25":
                pygame.mixer.music.set_volume(0.25)

            elif action == "VOLUME_0":
                pygame.mixer.music.set_volume(0)

            elif action == "MUSIC_OFF":
                pygame.mixer.music.pause()

            elif action == "MUSIC_ON":
                pygame.mixer.music.unpause()

            # control
            elif action == "USE_JOYSTICK":
                active_controller = "joystick"
                print("Switched to joystick")
            elif action == "USE_KEYBOARD":
                active_controller = "keyboard"
                print("Switched to keyboard")

    if current_state == "MENU":
        main_menu.draw(screen)

    elif current_state == "SETTINGS":
        settings_menu.draw(screen)

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