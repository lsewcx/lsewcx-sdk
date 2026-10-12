import os
import sys

from dotenv import find_dotenv, load_dotenv
from loguru import logger

ENV_VAR = "LSEWCX_LOG_LEVEL"
VALID_LEVELS = ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")


def _setup_logging() -> None:
    """import 时自动执行：读 .env，把全局日志统一到一个 sink、一个等级。

    注意：loguru 是全局单例，这里会用唯一的新 sink 替换掉已有 sink（含自带默认
    sink），所以 import 本库会覆盖宿主的日志配置 —— 适合"自己当应用/CLI 用"。
    """
    load_dotenv(find_dotenv(usecwd=True))

    level = os.getenv(ENV_VAR, "INFO").strip().upper()
    if level not in VALID_LEVELS:
        print(f"[lsewcx] 无效的 {ENV_VAR}={level!r}，回退到 INFO", file=sys.stderr)
        level = "INFO"

    logger.remove()                      # 去掉自带默认 sink，否则 DEBUG 仍会输出
    logger.add(sys.stderr, level=level)  # 全局唯一 sink：所有日志统一按 .env 等级


_setup_logging()
