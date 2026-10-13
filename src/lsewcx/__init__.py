from lsewcx.config.logger import logger


def main() -> None:
    """CLI 入口（pyproject.toml 的 [project.scripts] 指向这里）。

    目前只输出一条欢迎日志，后续可在这里编排子命令。
    """
    logger.info("Hello from lsewcx!")
