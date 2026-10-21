from enum import Enum


class URLType(str, Enum):
    """URL 类型。

    Attributes:
        OSS: 以 ``oss://`` 开头的对象存储 URL。
        COMMON: 其他普通 URL。
    """

    OSS = "OSS"
    COMMON = "COMMON"


def url_type(url: str) -> URLType:
    """判断 URL 的类型。

    Args:
        url: 待判断的 URL 字符串。

    Returns:
        ``URLType.OSS``（以 ``oss://`` 开头）或 ``URLType.COMMON``。
    """
    if url.startswith("oss://"):
        return URLType.OSS
    return URLType.COMMON
