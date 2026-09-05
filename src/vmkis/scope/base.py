from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

from vmkis.client.object import KisObjectBase, KisObjectProtocol

if TYPE_CHECKING:
    from vmkis.kis import VmKis


__all__ = [
    "KisScope",
    "KisScopeBase",
    "TScope",
]


@runtime_checkable
class KisScope(KisObjectProtocol, Protocol):
    """한국투자증권 API Scope"""


class KisScopeBase(KisObjectBase):
    """한국투자증권 API Scope"""

    def __init__(self, kis: "VmKis"):
        self.kis = kis


TScope = TypeVar("TScope", bound=KisScope)
