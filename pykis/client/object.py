from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisObjectBase:
    """한국투자증권 API 객체"""

    kis: "PyKis"
    """한국투자증권 API"""
