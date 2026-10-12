import sys
from enum import Enum


class OS(str, Enum):
    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"

    @classmethod
    def current_system(cls) -> "OS":
        if sys.platform == "win32":
            return cls.WINDOWS
        if sys.platform == "darwin":
            return cls.MACOS
        return cls.LINUX


def is_windows() -> bool:
    return OS.current_system() is OS.WINDOWS


def is_macos() -> bool:
    return OS.current_system() is OS.MACOS


def is_linux() -> bool:
    return OS.current_system() is OS.LINUX
