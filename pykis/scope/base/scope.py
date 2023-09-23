from typing import TYPE_CHECKING, TypeVar

from pykis.client.object import KisObjectBase


if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisScope(KisObjectBase):
    """한국투자증권 API Scope"""

    def __init__(self, kis: "PyKis"):
        self.kis = kis


TScope = TypeVar("TScope", bound=KisScope)
