import pygame
from enums import MenuAction
from utils import draw_shadowed_text, load_font

class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load fonts
        self.font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 20)
        self.title_font = pygame.font.SysFont('Georgia', 24)

        # Menu tabs
        self.tabs = ["Graphics", "Sound", "Controls", "Credits", "Exit"]
        self.curr_tab = 0

        # Sub-options for each tab
        self.graphics_options = ["Full screen: disabled", "Resolution: 800x600", "V-Sync: enabled"]
        self.sound_options = ["Volume: 100%", "Music: on"]
        self.controls_options = ["Control Devices: Keyboard", "Joystick: not detected"]
        self.credits_options = ["View Credits Roll"]
        self.exit_options = ["Return to Main Menu"]

        self.selected_option = 0

    def _get_current_options(self):
        """Helper method returning options for the currently active tab."""
        tab_name = self.tabs[self.curr_tab]
        if tab_name == "Graphics":
            return self.graphics_options
        elif tab_name == "Sound":
            return self.sound_options
        elif tab_name == "Controls":
            return self.controls_options
        elif tab_name == "Credits":
            return self.credits_options
        elif tab_name == "Exit":
            return self.exit_options
        return []

    def _confirm_selection(self):
        """Helper method to handle option changes and actions using MenuAction enums."""
        tab_name = self.tabs[self.curr_tab]

        # Exit menu
        if tab_name == "Exit":
            return MenuAction.BACK

        # Credits tab trigger
        elif tab_name == "Credits":
            return MenuAction.SHOW_CREDITS

        # Graphics Options
        elif tab_name == "Graphics":
            if self.selected_option == 0:  # Full screen
                if "disabled" in self.graphics_options[0]:
                    self.graphics_options[0] = "Full screen: enabled"
                    return MenuAction.TOGGLE_FULL_SCREEN_ON
                else:
                    self.graphics_options[0] = "Full screen: disabled"
                    return MenuAction.TOGGLE_FULL_SCREEN_OFF

            elif self.selected_option == 1:  # Resolution
                if "800x600" in self.graphics_options[1]:
                    self.graphics_options[1] = "Resolution: 1024x768"
                    return MenuAction.RES_1024
                else:
                    self.graphics_options[1] = "Resolution: 800x600"
                    return MenuAction.RES_800

            elif self.selected_option == 2:  # V-Sync
                if "enabled" in self.graphics_options[2]:
                    self.graphics_options[2] = "V-Sync: disabled"
                    return MenuAction.VSYNC_OFF
                else:
                    self.graphics_options[2] = "V-Sync: enabled"
                    return MenuAction.VSYNC_ON

        # Sound Options
        elif tab_name == "Sound":
            if self.selected_option == 0:  # Volume
                if "100%" in self.sound_options[0]:
                    self.sound_options[0] = "Volume: 75%"
                    return MenuAction.VOLUME_75
                elif "75%" in self.sound_options[0]:
                    self.sound_options[0] = "Volume: 50%"
                    return MenuAction.VOLUME_50
                elif "50%" in self.sound_options[0]:
                    self.sound_options[0] = "Volume: 25%"
                    return MenuAction.VOLUME_25
                elif "25%" in self.sound_options[0]:
                    self.sound_options[0] = "Volume: 0%"
                    return MenuAction.VOLUME_0
                else:
                    self.sound_options[0] = "Volume: 100%"
                    return MenuAction.VOLUME_100

            elif self.selected_option == 1:  # Music On / Off
                if "on" in self.sound_options[1]:
                    self.sound_options[1] = "Music: off"
                    return MenuAction.MUSIC_OFF
                else:
                    self.sound_options[1] = "Music: on"
                    return MenuAction.MUSIC_ON

        # Control Options
        elif tab_name == "Controls":
            if self.selected_option == 1 or self.selected_option == 0:
                if pygame.joystick.get_count() > 0:
                    if "not detected" in self.controls_options[1] or "Keyboard" in self.controls_options[0]:
                        self.controls_options[0] = "Control Devices: Joystick"
                        self.controls_options[1] = "Joystick: active"
                        return MenuAction.USE_JOYSTICK
                    else:
                        self.controls_options[0] = "Control Devices: Keyboard"
                        self.controls_options[1] = "Joystick: detected (inactive)"
                        return MenuAction.USE_KEYBOARD
                else:
                    self.controls_options[1] = "Joystick: not detected"
        return None

    def handle_event(self, event):
        """Handle keyboard and gamepad input for navigation and option modification."""
        def move_left():
            self.curr_tab = (self.curr_tab - 1) % len(self.tabs)
            self.selected_option = 0

        def move_right():
            self.curr_tab = (self.curr_tab + 1) % len(self.tabs)
            self.selected_option = 0

        def move_up():
            current_opts = self._get_current_options()
            if current_opts:
                self.selected_option = (self.selected_option - 1) % len(current_opts)

        def move_down():
            current_opts = self._get_current_options()
            if current_opts:
                self.selected_option = (self.selected_option + 1) % len(current_opts)

        # 1. Keyboard Input Handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return MenuAction.BACK
            elif event.key == pygame.K_LEFT:
                move_left()
            elif event.key == pygame.K_RIGHT:
                move_right()
            elif event.key == pygame.K_UP:
                move_up()
            elif event.key == pygame.K_DOWN:
                move_down()
            elif event.key == pygame.K_RETURN:
                return self._confirm_selection()

        # 2. Gamepad / Joystick D-Pad (Hat) Navigation
        elif event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            if hat_y == 1:  # Up
                move_up()
            elif hat_y == -1:  # Down
                move_down()
            elif hat_x == -1:  # Left
                move_left()
            elif hat_x == 1:  # Right
                move_right()

        # 3. Gamepad Button Press Handling
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A / Cross -> Confirm
                return self._confirm_selection()
            elif event.button == 1:  # B / Circle -> Back
                return MenuAction.BACK

        return None

    def draw(self, surface):
        """Render the settings menu layout onto the surface."""
        surface.fill((10, 10, 20))

        # Render category tabs horizontally
        start_x = 50
        tab_y = 40
        for i, tab in enumerate(self.tabs):
            color = (255, 255, 0) if i == self.curr_tab else (120, 120, 120)
            shadow = (20, 20, 20)

            draw_shadowed_text(surface, tab, self.title_font, color, shadow,
                               start_x + (i * 140), tab_y, center=False)

        # Separator line below tabs
        pygame.draw.line(surface, (80, 80, 110), (60, 80),
                         (self.screen_width - 60, 80), 2)

        # Render options for the currently selected tab
        current_opts = self._get_current_options()
        for i, option in enumerate(current_opts):
            color = (255, 255, 0) if i == self.selected_option else (120, 120, 120)
            shadow = (20, 20, 20)
            prefix = "> " if i == self.selected_option else "  "
            text_to_render = prefix + option

            draw_shadowed_text(
                surface, text_to_render, self.font, color, shadow,
                100, 130 + (i * 45), center=False
            )