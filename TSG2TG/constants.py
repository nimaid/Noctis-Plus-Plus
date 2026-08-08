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
