import sys

import pytest

from lsewcx.utils import OS, is_linux, is_macos, is_windows


@pytest.mark.parametrize(
    ("platform_value", "expected"),
    [
        ("win32", OS.WINDOWS),
        ("darwin", OS.MACOS),
        ("linux", OS.LINUX),
        ("linux2", OS.LINUX),  # 老值，锁住"兜底到 Linux"的行为
        ("cygwin", OS.LINUX),
    ],
)
def test_current_system(monkeypatch, platform_value, expected):
    monkeypatch.setattr(sys, "platform", platform_value)
    assert OS.current_system() is expected


def test_current_system_on_this_machine():
    # 本机真实环境：不写死 Linux，所以 Windows/macOS 上也能跑
    expected = {"win32": OS.WINDOWS, "darwin": OS.MACOS}.get(sys.platform, OS.LINUX)
    assert OS.current_system() is expected


@pytest.mark.parametrize("platform_value", ["win32", "darwin", "linux"])
def test_exactly_one_helper_is_true(monkeypatch, platform_value):
    monkeypatch.setattr(sys, "platform", platform_value)
    assert sum([is_windows(), is_macos(), is_linux()]) == 1


def test_enum_is_string_compatible():
    # str 枚举：能直接比较、序列化，日志里也好看
    assert OS.LINUX == "linux"
    assert OS("windows") is OS.WINDOWS
