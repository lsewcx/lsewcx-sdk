import shutil
from os import PathLike

from lsewcx.config import logger

GB = 1000**3
TB = 1000**4


def left_space(path: str | PathLike[str] = ".") -> float:
    """返回 path 所在卷的可用空间，单位 GB（1000 进制）。"""
    free = shutil.disk_usage(path).free
    if free < TB:
        logger.debug("还剩空间 {:.1f} GB", free / GB)
    else:
        logger.debug("还剩空间 {:.1f} TB", free / TB)
    return free / GB
