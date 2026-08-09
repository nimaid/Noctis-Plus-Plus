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
    "button-text": "#ffffff",
    "viewer": "#18191b",
    "link": "#dddddd",
    "disabled": "#555555",
    "disabled_text": "#888888",
    "clock_background": "#2b2d30",
    "clock_text": "#9a9ba2",
}

# Define paths
PATH = os.path.dirname(Path(__file__).resolve())
RESOURCE_PATH = os.path.join(PATH, "resources")
ICON_PATH = os.path.join(RESOURCE_PATH, "icon.png")
PANIC_ICON_PATH = os.path.join(RESOURCE_PATH, "panic.png")
BUTTON_ICON_PATHS = {
    "build": {
        "up": os.path.join(RESOURCE_PATH, "button_build_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_build_down.png"),
    },
    "calculator": {
        "up": os.path.join(RESOURCE_PATH, "button_calc_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_calc_down.png"),
    },
    "chat": {
        "up": os.path.join(RESOURCE_PATH, "button_chat_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_chat_down.png"),
    },
    "launch": {
        "up": os.path.join(RESOURCE_PATH, "button_launch_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_launch_down.png"),
    },
    "map": {
        "up": os.path.join(RESOURCE_PATH, "button_map_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_map_down.png"),
    },
    "media": {
        "up": os.path.join(RESOURCE_PATH, "button_media_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_media_down.png"),
    },
    "submit": {
        "up": os.path.join(RESOURCE_PATH, "button_outbox_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_outbox_down.png"),
    },
    "update": {
        "up": os.path.join(RESOURCE_PATH, "button_update_up.png"),
        "down": os.path.join(RESOURCE_PATH, "button_update_down.png"),
    },
}
