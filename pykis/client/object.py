from typing import TYPE_CHECKING, Any, Iterable, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisObjectProtocol",
    "KisObjectBase",
    "kis_object_init",
]


@runtime_checkable
class KisObjectProtocol(Protocol):
    @property
    def kis(self) -> "PyKis":
        """
        한국투자증권 API.

        Note:
            기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
            라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
        """
        ...


class KisObjectBase:
    """한국투자증권 API 객체"""

    kis: "PyKis"
    """
    한국투자증권 API.

    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    def __kis_init__(self, kis: "PyKis") -> None:
        self.kis = kis

    def __kis_post_init__(self) -> None:
        pass

    def _kis_spread(
        self,
        object: "KisObjectBase | Iterable[KisObjectBase] | Iterable[KisObjectBase | None] | dict[Any, KisObjectBase | None] | None",
    ) -> None:
        if isinstance(object, dict):
            for o in object.values():
                if o is not None:
                    self._kis_spread(o)
        elif isinstance(object, Iterable):
            for o in object:
                if o is not None:
                    self._kis_spread(o)
        elif isinstance(object, KisObjectBase):
            object.__kis_init__(self.kis)
            object.__kis_post_init__()
        elif object is not None:
            raise ValueError(f"Invalid object type: {type(object)}")


def kis_object_init(kis: "PyKis", object: KisObjectBase):
    object.__kis_init__(kis)
    object.__kis_post_init__()
