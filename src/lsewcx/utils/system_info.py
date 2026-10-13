import sys
from enum import Enum


class OS(str, Enum):
    """可识别的操作系统类型（粗粒度，够用来做分支）。

    Attributes:
        LINUX: Linux 及常见兼容环境；无法识别的平台也归入此类（见
            ``OS.current_system``）。
        MACOS: macOS（``sys.platform == "darwin"``）。
        WINDOWS: Windows（``sys.platform == "win32"``，64 位同样是 ``win32``）。
    """

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"

    @classmethod
    def current_system(cls) -> "OS":
        """返回当前运行的操作系统。

        Returns:
            与 ``sys.platform`` 对应的成员；无法识别时返回 ``OS.LINUX``。
        """
        if sys.platform == "win32":
            return cls.WINDOWS
        if sys.platform == "darwin":
            return cls.MACOS
        return cls.LINUX


def is_windows() -> bool:
    """判断当前系统是否为 Windows。

    Returns:
        是 Windows 时为 True，否则为 False。
    """
    return OS.current_system() is OS.WINDOWS


def is_macos() -> bool:
    """判断当前系统是否为 macOS。

    Returns:
        是 macOS 时为 True，否则为 False。
    """
    return OS.current_system() is OS.MACOS


def is_linux() -> bool:
    """判断当前系统是否为 Linux（含无法识别的其他平台）。

    Returns:
        是 Linux 时为 True，否则为 False。
    """
    return OS.current_system() is OS.LINUX
