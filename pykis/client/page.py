from typing import Any, Literal

from pykis.client.form import KisForm
from pykis.responses.dynamic import KisDynamic
from pykis.utils.repr import kis_repr

__all__ = [
    "KisPageStatus",
    "to_page_status",
    "KisPage",
]

KisPageStatus = Literal["begin", "end"]


def to_page_status(status: str) -> KisPageStatus:
    if status == "F" or status == "M":
        return "begin"
    elif status == "D" or status == "E":
        return "end"
    else:
        raise ValueError(f"Invalid page status: {status}")


@kis_repr(
    "size",
    "search",
    "key",
    lines="single",
)
class KisPage(KisDynamic, KisForm):
    """한국투자증권 페이지 커서"""

    search: str
    """연속조회검색조건"""
    key: str
    """연속조회키"""
    size: int | None
    """커서 길이"""

    def __init__(self, size: int | None = None, search: str | None = None, key: str | None = None):
        super().__init__()
        self.size = size
        self.search = search or ""
        self.key = key or ""

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if (search := data.get("ctx_area_fk100")) is not None:
            self.search = search
            self.key = data["ctx_area_nk100"]
            self.size = 100
        elif (search := data.get("ctx_area_fk200")) is not None:
            self.search = search
            self.key = data["ctx_area_nk200"]
            self.size = 200
        else:
            raise ValueError(f"페이지 커서를 파싱할 수 없었습니다. {data}")

    @property
    def is_empty(self) -> bool:
        """커서가 비어있는지 확인합니다."""
        return (not self.key or self.key.isspace()) and (not self.search or self.search.isspace())

    @property
    def is_first(self) -> bool:
        """첫 번째 페이지인지 확인합니다."""
        return self.is_empty

    @property
    def is_100(self) -> bool:
        """커서 길이가 100인지 확인합니다."""
        return self.size == 100

    @property
    def is_200(self) -> bool:
        """커서 길이가 200인지 확인합니다."""
        return self.size == 200

    def to(self, size: int) -> "KisPage":
        """커서 길이를 변경합니다."""
        if len(self.key) > size or len(self.search) > size:
            raise ValueError(f"커서 길이가 이미 {size}보다 큽니다.")

        return type(self)(size, self.search, self.key)

    def build(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """요청 폼을 생성합니다."""
        if self.size is None:
            raise ValueError("커서 길이가 지정되지 않았습니다.")

        data = data or {}
        data[f"ctx_area_fk{self.size}"] = self.search
        data[f"ctx_area_nk{self.size}"] = self.key

        return data

    @classmethod
    def first(cls, size: int | None = None) -> "KisPage":
        """첫 번째를 만듭니다."""
        return cls(size)
