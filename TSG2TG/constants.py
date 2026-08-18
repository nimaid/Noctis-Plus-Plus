import os
import sys
from enum import Enum
from pathlib import Path

TITLE = "The Stardrifter's GUIDE to the Galaxy"

class PlatformCode(Enum):
    WINDOWS = "win32"
    LINUX = "linux"
    MAC = "darwin"
    UNKNOWN = "unknown"

class HorizontalAlign(Enum):
    LEFT = "left"
    CENTER = "hcenter"
    RIGHT = "right"

class VerticalAlign(Enum):
    TOP = "top"
    CENTER = "vcenter"
    BOTTOM = "bottom"

class TextAlign(Enum):
    FLUSH_LEFT = "left"
    CENTERED = "center"
    FLUSH_RIGHT = "right"

# Set platform dependent variables
USER_DIR = os.path.expanduser("~")

if sys.platform == PlatformCode.WINDOWS.value:
    PLATFORM = PlatformCode.WINDOWS
    APPDATA_DIR = os.path.join(USER_DIR, "AppData", "Roaming")
elif sys.platform == PlatformCode.LINUX.value:
    PLATFORM = PlatformCode.LINUX
    APPDATA_DIR = os.path.join(USER_DIR, ".local", "share")
elif sys.platform == PlatformCode.MAC.value:
    PLATFORM = PlatformCode.MAC
    APPDATA_DIR = os.path.join(USER_DIR, "Library", "Application Support")
else:
    PLATFORM = PlatformCode.UNKNOWN
    # Unknown platform, save to wherever os.path thinks the home dir is
    APPDATA_DIR = USER_DIR

# Define colors
COLORS = {
    "background": "#1e1f22",
    "foreground": "#333333",
    "text": "#dddddd",
    "button_text": "#ffffff",
    "viewer": "#18191b",
    "link": "#dddddd",
    "disabled": "#555555",
    "disabled_text": "#888888",
    "clock_background": "#2b2d30",
    "clock_text": "#9a9ba2",
    "tab_background": "#2a2c30",
    "tab_foreground": "#4a4d54",
    "tab_inactive_border": "#3d3f45",
    "tab_active_border": "#959aa8",
}

# Define paths
PATH = Path(__file__).parent.resolve()
RESOURCE_PATH = os.path.join(PATH, "resources")

ICON_PATH = os.path.join(RESOURCE_PATH, "icon.png")
PANIC_ICON_PATH = os.path.join(RESOURCE_PATH, "panic.png")
BUTTON_ICON_PATHS = {
    "red": {
        "up": os.path.join(RESOURCE_PATH, "button00.png"),
        "down": os.path.join(RESOURCE_PATH, "button01.png"),
    },
    "orange": {
        "up": os.path.join(RESOURCE_PATH, "button02.png"),
        "down": os.path.join(RESOURCE_PATH, "button03.png"),
    },
    "yellow": {
        "up": os.path.join(RESOURCE_PATH, "button04.png"),
        "down": os.path.join(RESOURCE_PATH, "button05.png"),
    },
    "green": {
        "up": os.path.join(RESOURCE_PATH, "button06.png"),
        "down": os.path.join(RESOURCE_PATH, "button07.png"),
    },
    "cyan": {
        "up": os.path.join(RESOURCE_PATH, "button08.png"),
        "down": os.path.join(RESOURCE_PATH, "button09.png"),
    },
    "blue": {
        "up": os.path.join(RESOURCE_PATH, "button10.png"),
        "down": os.path.join(RESOURCE_PATH, "button11.png"),
    },
    "purple": {
        "up": os.path.join(RESOURCE_PATH, "button12.png"),
        "down": os.path.join(RESOURCE_PATH, "button13.png"),
    },
    "magenta": {
        "up": os.path.join(RESOURCE_PATH, "button14.png"),
        "down": os.path.join(RESOURCE_PATH, "button15.png"),
    }
}
BUTTON_LABEL_ADJUST = {
    "up": (0, -3),
    "down": (0, 0)
}
IMAGE_FONT_PATHS = {
    "noctis": os.path.join(RESOURCE_PATH, "font_noctis.png"),
    "microfont": os.path.join(RESOURCE_PATH, "microfont", "Microfont_1D.png"),
}
TRUETYPE_FONT_PATHS = {
    "microfont": os.path.join(RESOURCE_PATH, "microfont", "Microfont.ttf"),
    "microfont_mono": os.path.join(RESOURCE_PATH, "microfont", "Microfont-Mono.ttf"),
}
