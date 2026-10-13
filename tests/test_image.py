import struct
import zlib
from pathlib import Path

import pytest
from daft.exceptions import DaftCoreException

from lsewcx.utils.image import image_infos


def make_png(w: int, h: int) -> bytes:
    """纯标准库造一张纯色 PNG：不需要 Pillow，也不往仓库塞图片文件。"""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload))
        )

    raw = b"".join(b"\x00" + bytes((255, 0, 0)) * w for _ in range(h))
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


@pytest.fixture
def png_file(tmp_path):
    """生成真实 PNG 文件的工厂 fixture。"""

    def _make(name: str, w: int, h: int) -> Path:
        path = tmp_path / name
        path.write_bytes(make_png(w, h))
        return path

    return _make


def test_basic_fields(png_file):
    """宽度、高度、格式、模式应来自文件头，且内容正确。"""
    path = png_file("a.png", 7, 3)

    (info,) = image_infos([str(path)])

    assert info["width"] == 7
    assert info["height"] == 3
    assert info["format"] == "PNG"
    assert info["mode"] == "RGB"


def test_size_bytes_matches_disk(png_file):
    """size_bytes 应与磁盘上的实际文件大小一致。"""
    path = png_file("a.png", 7, 3)

    (info,) = image_infos([str(path)])

    assert info["size_bytes"] == path.stat().st_size


def test_order_is_preserved(png_file):
    """返回顺序应与输入顺序一致。"""
    a = png_file("a.png", 7, 3)
    b = png_file("b.png", 120, 80)

    infos = image_infos([str(a), str(b)])

    assert [i["path"] for i in infos] == [str(a), str(b)]
    assert [i["width"] for i in infos] == [7, 120]


def test_empty_input():
    """空输入返回空列表，而不是报错。"""
    assert image_infos([]) == []


def test_missing_file_raises(tmp_path):
    """路径不存在时整批失败。"""
    with pytest.raises(DaftCoreException):
        image_infos([str(tmp_path / "不存在.png")])


def test_not_an_image_raises(tmp_path):
    """扩展名像图片但内容不是时整批失败。"""
    fake = tmp_path / "fake.png"
    fake.write_text("这不是图片")

    with pytest.raises(DaftCoreException):
        image_infos([str(fake)])
