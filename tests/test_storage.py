from collections import namedtuple
from types import SimpleNamespace

import pytest

from lsewcx.utils import storage

Usage = namedtuple("usage", "total used free")


def _patch_disk_usage(monkeypatch, free: int) -> None:
    """把 storage 里的 shutil 换成一个返回固定 free 值的替身。"""
    fake = Usage(total=0, used=0, free=free)
    monkeypatch.setattr(
        storage, "shutil", SimpleNamespace(disk_usage=lambda path: fake)
    )


def test_left_space_returns_positive_on_this_machine():
    assert storage.left_space(".") > 0


def test_left_space_forwards_path(monkeypatch):
    seen = []

    def fake_disk_usage(path):
        seen.append(path)
        return Usage(0, 0, storage.GB)

    monkeypatch.setattr(storage, "shutil", SimpleNamespace(disk_usage=fake_disk_usage))

    storage.left_space("/some/path")

    assert seen == ["/some/path"]


def test_left_space_default_path_is_current_dir(monkeypatch):
    seen = []

    def fake_disk_usage(path):
        seen.append(path)
        return Usage(0, 0, storage.GB)

    monkeypatch.setattr(storage, "shutil", SimpleNamespace(disk_usage=fake_disk_usage))

    storage.left_space()

    assert seen == ["."]


def test_left_space_uses_free_not_total_or_used(monkeypatch):
    fake = Usage(total=100 * storage.GB, used=40 * storage.GB, free=60 * storage.GB)
    monkeypatch.setattr(
        storage, "shutil", SimpleNamespace(disk_usage=lambda path: fake)
    )

    assert storage.left_space(".") == pytest.approx(60.0)


def test_left_space_unit_is_decimal_gb(monkeypatch):
    """单位是 GB（1000³），不是 GiB（1024³）——两者相差 7.4%。"""
    _patch_disk_usage(monkeypatch, free=storage.GB)
    assert storage.left_space(".") == pytest.approx(1.0)

    _patch_disk_usage(monkeypatch, free=storage.GIB)
    assert storage.left_space(".") == pytest.approx(1024**3 / 1000**3)
