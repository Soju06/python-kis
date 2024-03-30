from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisObjectBase:
    """한국투자증권 API 객체"""

    kis: "PyKis"
    """
    한국투자증권 API.
    
    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    def __kis_init__(self, kis: "PyKis"):
        self.kis = kis

    def __kis_post_init__(self):
        pass

    def _kis_spread(
        self,
        object: "KisObjectBase | Iterable[KisObjectBase] | Iterable[KisObjectBase | None] | dict | None",
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
