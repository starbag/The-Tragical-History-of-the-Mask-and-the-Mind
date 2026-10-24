import pygame
from utils import draw_shadowed_text, load_font


class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load fonts
        self.font = load_font('assets/fonts/Shakespeare First Folio Font.otf', 20)
        self.title_font = pygame.font.SysFont('Georgia', 24)

        # Menu tabs
        self.tabs = ["Graphics", "Sound", "Controls", "Exit"]
        self.curr_tab = 0

        # Sub-options for each tab
        self.graphics_options = ["Full screen: disabled", "Resolution: 800x600", "V-Sync: enabled"]
        self.sound_options = ["Volume: 100%", "Music: on"]
        self.controls_options = ["Control Devices: Keyboard", "Joystick: not detected"]
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
        elif tab_name == "Exit":
            return self.exit_options
        return []

    def handle_event(self, event):
        """Handle keyboard input for tab navigation and option modification."""
        if event.type == pygame.KEYDOWN:
            # Back to previous menu via ESC key
            if event.key == pygame.K_ESCAPE:
                return "BACK"

            # Tab navigation (LEFT / RIGHT)
            elif event.key == pygame.K_LEFT:
                self.curr_tab = (self.curr_tab - 1) % len(self.tabs)
                self.selected_option = 0
            elif event.key == pygame.K_RIGHT:
                self.curr_tab = (self.curr_tab + 1) % len(self.tabs)
                self.selected_option = 0

            # Option navigation (UP / DOWN)
            elif event.key == pygame.K_UP:
                current_opts = self._get_current_options()
                if current_opts:
                    self.selected_option = (self.selected_option - 1) % len(current_opts)
            elif event.key == pygame.K_DOWN:
                current_opts = self._get_current_options()
                if current_opts:
                    self.selected_option = (self.selected_option + 1) % len(current_opts)

            # Confirm / Cycle value (ENTER)
            elif event.key == pygame.K_RETURN:
                tab_name = self.tabs[self.curr_tab]

                # Exit menu
                if tab_name == "Exit":
                    return "BACK"

                # Graphics Options
                elif tab_name == "Graphics":
                    if self.selected_option == 0:  # Full screen
                        if "disabled" in self.graphics_options[0]:
                            self.graphics_options[0] = "Full screen: enabled"
                            return "TOGGLE_FULLSCREEN_ON"
                        else:
                            self.graphics_options[0] = "Full screen: disabled"
                            return "TOGGLE_FULLSCREEN_OFF"

                    elif self.selected_option == 1:  # Resolution
                        if "800x600" in self.graphics_options[1]:
                            self.graphics_options[1] = "Resolution: 1024x768"
                            return "RES_1024"
                        else:
                            self.graphics_options[1] = "Resolution: 800x600"
                            return "RES_800"

                    elif self.selected_option == 2:  # V-Sync
                        if "enabled" in self.graphics_options[2]:
                            self.graphics_options[2] = "V-Sync: disabled"
                            return "VSYNC_OFF"
                        else:
                            self.graphics_options[2] = "V-Sync: enabled"
                            return "VSYNC_ON"

                # Sound Options
                elif tab_name == "Sound":
                    if self.selected_option == 0:  # Volume
                        if "100%" in self.sound_options[0]:
                            self.sound_options[0] = "Volume: 75%"
                            return "VOLUME_75"
                        elif "75%" in self.sound_options[0]:
                            self.sound_options[0] = "Volume: 50%"
                            return "VOLUME_50"
                        elif "50%" in self.sound_options[0]:
                            self.sound_options[0] = "Volume: 25%"
                            return "VOLUME_25"
                        elif "25%" in self.sound_options[0]:
                            self.sound_options[0] = "Volume: 0%"
                            return "VOLUME_0"
                        else:
                            self.sound_options[0] = "Volume: 100%"
                            return "VOLUME_100"

                    elif self.selected_option == 1:  # Music On / Off
                        if "on" in self.sound_options[1]:
                            self.sound_options[1] = "Music: off"
                            return "MUSIC_OFF"
                        else:
                            self.sound_options[1] = "Music: on"
                            return "MUSIC_ON"

                # Control Options
                elif tab_name == "Controls":
                    if self.selected_option == 1 or self.selected_option == 0:  # Select device
                        if pygame.joystick.get_count() > 0:
                            if "not detected" in self.controls_options[1] or "Keyboard" in self.controls_options[0]:
                                self.controls_options[0] = "Control Devices: Joystick"
                                self.controls_options[1] = "Joystick: active"
                                return "USE_JOYSTICK"
                            else:
                                self.controls_options[0] = "Control Devices: Keyboard"
                                self.controls_options[1] = "Joystick: detected (inactive)"
                                return "USE_KEYBOARD"
                        else:
                            self.controls_options[1] = "Joystick: not detected"
                            return "NO_JOYSTICK_AVAILABLE"
        return None

    def draw(self, surface):
        """Render the settings menu layout onto the surface."""
        # Background fill
        surface.fill((10, 10, 20))

        # Render category tabs horizontally
        start_x = 80
        tab_y = 40
        for i, tab in enumerate(self.tabs):
            # Highlight active tab
            color = (255, 255, 0) if i == self.curr_tab else (120, 120, 120)
            shadow = (20, 20, 20)

            draw_shadowed_text(surface, tab, self.title_font, color, shadow,
                               start_x + (i * 160), tab_y, center=False)

        # Separator line below tabs
        pygame.draw.line(surface, (80, 80, 110), (60, 80),
                         (self.screen_width - 60, 80), 2)

        # Render options for the currently selected tab
        current_opts = self._get_current_options()
        for i, option in enumerate(current_opts):
            # Highlight selected option and add cursor prefix
            color = (255, 255, 0) if i == self.selected_option else (120, 120, 120)
            shadow = (20, 20, 20)
            prefix = "> " if i == self.selected_option else "  "
            text_to_render = prefix + option

            draw_shadowed_text(
                surface, text_to_render, self.font, color, shadow,
                100, 130 + (i * 45), center=False
            )