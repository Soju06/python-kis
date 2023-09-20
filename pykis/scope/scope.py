from typing import TYPE_CHECKING, TypeVar


if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisScope:
    """한국투자증권 API Scope"""

    kis: "PyKis"
    """한국투자증권 API"""

    def __init__(self, kis: "PyKis"):
        self.kis = kis

    def __post_init__(self, *args, **kwargs):
        pass

TScope = TypeVar("TScope", bound=KisScope)
