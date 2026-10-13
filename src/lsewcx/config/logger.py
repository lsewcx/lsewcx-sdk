import os
import sys

from dotenv import find_dotenv, load_dotenv
from loguru import logger

ENV_VAR = "LSEWCX_LOG_LEVEL"
VALID_LEVELS = ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")


def _setup_logging() -> None:
    """在 import 时配置全局日志：读取 .env 并把日志统一到一个 sink、一个等级。

    等级来自环境变量 ``LSEWCX_LOG_LEVEL``（默认 ``INFO``）；``.env`` 文件从
    当前工作目录向上查找，值非法时回退到 ``INFO`` 并在 stderr 提示。

    ``loguru`` 是全局单例，这里会用唯一的新 sink 替换掉已有 sink（含自带默认
    sink），因此 import 本库会覆盖宿主的日志配置 —— 适合"自己当应用/CLI 用"。
    """
    load_dotenv(find_dotenv(usecwd=True))

    level = os.getenv(ENV_VAR, "INFO").strip().upper()
    if level not in VALID_LEVELS:
        print(f"[lsewcx] 无效的 {ENV_VAR}={level!r}，回退到 INFO", file=sys.stderr)
        level = "INFO"

    logger.remove()  # 去掉自带默认 sink，否则 DEBUG 仍会输出
    logger.add(sys.stderr, level=level)  # 全局唯一 sink：所有日志统一按 .env 等级


_setup_logging()
