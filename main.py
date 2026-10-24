import pygame
from state_manager import StateManager
from helpers import int_to_roman

# Initialize pygame modules
pygame.init()
pygame.font.init()
pygame.joystick.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

current_act = 1
pygame.display.set_caption(f"The Tragical History of the Mask and the Mind - Act {int_to_roman(current_act)}")

clock = pygame.time.Clock()

# Instantiate the StateManager which controls everything
state_manager = StateManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT, current_act)

# Optional controller check at startup
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    state_manager.settings_menu.controls_options[1] = "Joystick: detected"

running = True
while running:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Delegate event handling to StateManager; returns False if player quits
            running = state_manager.handle_event(event)

    # --- RENDERING & UPDATES ---
    state_manager.update_and_draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()