from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    SETTINGS = auto()
    CREDITS = auto()
    GAME = auto()

class MenuAction(Enum):
    # navigation
    BACK = auto()
    BEGIN_ACT = auto()
    SHOW_CREDITS = auto()
    QUIT_GAME = auto()

    # graphics opts
    TOGGLE_FULL_SCREEN_ON = auto()
    TOGGLE_FULL_SCREEN_OFF = auto()
    RES_1024 = auto()
    RES_800 = auto()
    VSYNC_ON = auto()
    VSYNC_OFF = auto()

    # audio opts
    VOLUME_100 = auto()
    VOLUME_75 = auto()
    VOLUME_50 = auto()
    VOLUME_25 = auto()
    VOLUME_0 = auto()
    MUSIC_ON = auto()
    MUSIC_OFF = auto()

    # input device opts
    USE_JOYSTICK = auto()
    USE_KEYBOARD = auto()
