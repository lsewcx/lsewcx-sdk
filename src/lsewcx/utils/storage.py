import shutil
from os import PathLike

from lsewcx.config import logger

GIB = 1024**3
GB = 1000**3


def left_space(path: str | PathLike[str] = ".") -> float:
    """返回 path 所在卷的可用空间，单位 GB（1000 进制）。"""
    free = shutil.disk_usage(path).free
    logger.debug("还剩空间 {:.1f} GB", free / GB)
    logger.debug("还剩空间 {:.1f} GiB", free / GIB)
    return free / GB
