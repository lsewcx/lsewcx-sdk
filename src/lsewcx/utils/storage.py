import shutil
from os import PathLike

from lsewcx.config import logger

GB = 1000**3
TB = 1000**4


def left_space(path: str | PathLike[str] = ".") -> float:
    """返回 path 所在卷的可用空间。

    单位为 GB（1000 进制，1 GB = 1000³ 字节）；日志按容量大小自动选择以
    GB 或 TB 展示。

    Args:
        path: 任意文件或目录路径，默认当前目录（读取其所在卷）。

    Returns:
        可用空间的数值，单位为 GB。

    Raises:
        OSError: 路径不存在或不可访问时（``FileNotFoundError`` 是其子类）。
    """
    free = shutil.disk_usage(path).free
    if free < TB:
        logger.debug("还剩空间 {:.1f} GB", free / GB)
    else:
        logger.debug("还剩空间 {:.1f} TB", free / TB)
    return free / GB
