import contextlib
import io

import daft
import daft.functions as F
from daft.exceptions import DaftCoreException


def image_infos(paths: list[str]) -> list[dict]:
    """批量获取图片基本信息，单个坏文件不会让整批失败。

    读取顺序与 ``paths`` 一致，每个元素为两种形态之一：成功时是包含
    ``path`` / ``width`` / ``height`` / ``format`` / ``mode`` / ``size_bytes``
    六个键的字典；失败时是包含 ``path`` 与 ``error`` 两个键的字典。

    只读取文件头、不解码像素。正常情况下批量并行读取；一旦批内出现坏文件，
    降级为逐条读取以定位并跳过失败项。失败原因只出现在返回值的 ``error``
    字段，Daft 的内部错误日志已在函数内屏蔽。

    Args:
        paths: 图片文件路径列表。

    Returns:
        与 ``paths`` 等长的列表，顺序与输入一致；失败项以 ``error`` 键标记。
    """
    paths = list(paths)

    # Daft 在读取失败时会向 stderr 打印内部错误行，而失败原因已经写进返回值。
    # 注意：redirect_stderr 是进程级的，多线程并发写 stderr 时窗口内的输出
    # 会被一并吞掉（本函数窗口很短，正常可接受）。
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            return _read_batch(paths)
        except DaftCoreException:
            return [_read_one(path) for path in paths]


def _read_batch(paths: list[str]) -> list[dict]:
    """一次批量读取（快路径）；任一路径失败都会抛 DaftCoreException。"""
    if not paths:
        return []

    df = daft.from_pydict({"path": paths})
    df = df.with_column("file", F.image_file(daft.col("path")))
    df = df.select(
        F.file_path(daft.col("file")).alias("path"),
        F.image_file_metadata(daft.col("file")).alias("meta"),
        F.file_size(daft.col("file")).alias("size_bytes"),
    )
    data = df.to_pydict()

    return [
        {
            "path": path,
            "width": meta["width"],
            "height": meta["height"],
            "format": meta["format"],
            "mode": meta["mode"],
            "size_bytes": size,
        }
        for path, meta, size in zip(
            data["path"], data["meta"], data["size_bytes"], strict=True
        )
    ]


def _read_one(path: str) -> dict:
    """逐条读取（慢路径）：失败时返回 path + error，而不是抛异常。"""
    try:
        (info,) = _read_batch([path])
        return info
    except Exception as exc:  # 逐条模式下任何读取失败都转化为 error 项
        return {"path": path, "error": _error_text(exc)}


def _error_text(exc: Exception) -> str:
    """取异常的第一行并去掉 Daft 前缀，得到可读的错误信息。"""
    text = str(exc).strip().splitlines()[0].strip() if str(exc).strip() else ""
    if not text:
        return type(exc).__name__
    for prefix in (
        "DaftError::ComputeError ",
        "DaftError::ValueError ",
        "DaftError::FileNotFound ",
        "DaftError::TypeError ",
    ):
        if text.startswith(prefix):
            return text[len(prefix) :]
    return text
