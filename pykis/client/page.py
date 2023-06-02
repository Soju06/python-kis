from typing import Literal


KisPageStatus = Literal["begin", "end"]


def to_page_status(status: str) -> KisPageStatus:
    if status == "F" or status == "M":
        return "begin"
    elif status == "D" or status == "E":
        return "end"
    else:
        raise ValueError(f"Invalid page status: {status}")


class KisPage:
    """한국투자증권 페이징 정보"""

    search: str
    """CTX_AREA_FK{size}	연속조회검색조건"""
    key: str
    """CTX_AREA_NK{size}	연속조회키"""
    size: int
    """조회키 크기"""

    def __init__(self, data: dict | tuple[str, str] | None = None, size: int = 100):
        self.size = size
        if data:
            if isinstance(data, tuple):
                self.search = data[0]
                self.key = data[1]
            if isinstance(data, dict):
                self.search = data[f'ctx_area_fk{"" if not size else size}']
                self.key = data[f'ctx_area_nk{"" if not size else size}']
            else:
                raise ValueError(f"Invalid data type: {type(data)}")
        else:
            self.search = ""
            self.key = ""

    @property
    def empty(self) -> bool:
        """페이징 정보가 비어있는지 확인합니다."""
        return self.search == "" and self.key == ""

    @property
    def long(self) -> bool:
        """긴 페이징 정보인지 확인합니다."""
        return self.size == 200

    def to_long(self) -> "KisLongPage":
        """긴 페이징 정보로 변환합니다."""
        return KisLongPage((self.search, self.key))

    @property
    def zero(self) -> bool:
        """0 페이징 정보인지 확인합니다."""
        return self.size == 0

    def to_zero(self) -> "KisZeroPage":
        """0 페이징 정보로 변환합니다."""
        return KisZeroPage((self.search, self.key))

    def build_body(self, body: dict) -> dict:
        """페이징 정보를 추가합니다."""
        body[f'CTX_AREA_FK{"" if not self.size else self.size}'] = self.search
        body[f'CTX_AREA_NK{"" if not self.size else self.size}'] = self.key

        return body

    @staticmethod
    def first(size: int = 100) -> "KisPage":
        """첫 페이지"""
        return KisPage(None, size)


class KisLongPage(KisPage):
    """한국투자증권 페이징 정보"""

    def __init__(self, data: dict | tuple[str, str] | None = None):
        super().__init__(data, 200)

    @staticmethod
    def first() -> "KisLongPage":
        """첫 페이지"""
        return KisLongPage(None)


class KisZeroPage(KisPage):
    """한국투자증권 페이징 정보"""

    def __init__(self, data: dict | tuple[str, str] | None = None):
        super().__init__(data, 0)

    @staticmethod
    def first() -> "KisZeroPage":
        """첫 페이지"""
        return KisZeroPage(None)
