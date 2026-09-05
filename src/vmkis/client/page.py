from typing import Any, Literal

from vmkis.client.form import KisForm
from vmkis.responses.dynamic import KisDynamic
from vmkis.utils.repr import kis_repr

__all__ = [
    "KisPageStatus",
    "to_page_status",
    "KisPage",
    "NO_SUFFIX",
]

KisPageStatus = Literal["begin", "end"]

NO_SUFFIX = 0
"""접미사 없는 `CTX_AREA_FK` / `CTX_AREA_NK` 를 나타내는 `KisPage.size` 값입니다.

KIS API의 커서 파라미터에는 네 가지 변형이 있고, 그중 하나는 길이 접미사가
없습니다. `size` 는 필드명에 붙는 숫자를 그대로 담으므로 "숫자 없음"을 0 으로
표현합니다. 커서 길이가 0 이라는 뜻이 아닙니다.
"""

#: 파싱 시도 순서. 각 항목은 (필드 접미사, 그때의 `size`) 입니다.
_CURSOR_VARIANTS: tuple[tuple[str, int], ...] = (
    ("100", 100),
    ("200", 200),
    ("50", 50),
    ("", NO_SUFFIX),
)


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

        # 접미사 변형 네 가지를 모두 받습니다. 공식 샘플 274개 REST API 전수
        # 조사 기준 분포는 FK100 15개 / FK200 25개 / FK 2개 / FK50 1개입니다.
        # 예전에는 100·200만 받아, 접미사 없는 `CTX_AREA_FK` 를 쓰는 API(예:
        # 국내휴장일조회 CTCA0903R)가 KisPaginationAPIResponse 를 상속하는
        # 순간 파싱 단계에서 죽었습니다.
        for suffix, size in _CURSOR_VARIANTS:
            if (search := data.get(f"ctx_area_fk{suffix}")) is None:
                continue

            self.search = search
            self.key = data[f"ctx_area_nk{suffix}"]
            self.size = size
            return

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

    @property
    def field_suffix(self) -> str:
        """`ctx_area_fk` / `ctx_area_nk` 뒤에 붙는 접미사입니다."""
        if self.size is None:
            raise ValueError("커서 길이가 지정되지 않았습니다.")

        # NO_SUFFIX(0)는 "길이 0"이 아니라 "접미사 없음"입니다.
        return "" if self.size == NO_SUFFIX else str(self.size)

    def to(self, size: int) -> "KisPage":
        """커서 길이를 변경합니다."""
        # NO_SUFFIX 변형에는 문서화된 길이 제한이 없으므로 검사하지 않습니다.
        # 검사하면 접미사 없는 커서를 파싱한 뒤 `to(NO_SUFFIX)`가 항상 실패합니다.
        if size != NO_SUFFIX and (len(self.key) > size or len(self.search) > size):
            raise ValueError(f"커서 길이가 이미 {size}보다 큽니다.")

        return type(self)(size, self.search, self.key)

    def build(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """요청 폼을 생성합니다."""
        suffix = self.field_suffix

        data = data or {}
        data[f"ctx_area_fk{suffix}"] = self.search
        data[f"ctx_area_nk{suffix}"] = self.key

        return data

    @classmethod
    def first(cls, size: int | None = None) -> "KisPage":
        """첫 번째를 만듭니다."""
        return cls(size)
