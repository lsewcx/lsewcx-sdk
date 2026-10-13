import daft
import daft.functions as F


def image_infos(paths: list[str]) -> list[dict]:
    """批量获取图片基本信息。

    只读取文件头，不解码像素，适合大批量扫描；返回顺序与 ``paths`` 一致。

    Args:
        paths: 图片文件路径列表。

    Returns:
        与 ``paths`` 等长的列表，每项为包含以下键的字典：

        - ``path``: 图片路径
        - ``width``: 宽度（像素）
        - ``height``: 高度（像素）
        - ``format``: 文件格式，如 ``"PNG"``
        - ``mode``: 颜色模式，如 ``"RGB"``
        - ``size_bytes``: 文件大小（字节）

    Raises:
        daft.exceptions.DaftCoreException: 任一路径不存在或不是图片文件
            （整批失败）。
    """
    df = daft.from_pydict({"path": list(paths)})
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
