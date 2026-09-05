"""`VmKis.fetch_pages()` 검증 (이슈 #44).

**이 파일이 필요한 이유.** 연속조회 루프는 엔드포인트마다 각자 복사돼 있었고
(#44 착수 시점 8곳), **그 루프를 직접 검증하는 테스트가 하나도 없었습니다.**
루프를 한 곳으로 모았으니 여기서 한 번만 검증합니다.

`continuous` / `is_last` / `next_page` 를 잘못 다루면 **무한 루프이거나 첫
페이지만 반환**합니다. 둘 다 조용히 틀립니다.
"""

from types import SimpleNamespace

import pytest

from vmkis.client.endpoint import KisEndpoint
from vmkis.client.page import KisPage
from vmkis.kis import MAX_PAGES, VmKis

ENDPOINT = KisEndpoint(
    path="/uapi/test/pages",
    tr_live="TTTEST01R",
    page_size=100,
)


class _Page:
    """`KisPage` 자리에 놓을 최소 커서."""

    def __init__(self, is_first: bool):
        self.is_first = is_first

    def to(self, size: int) -> "_Page":
        return self


class FakeKis:
    """`fetch_pages` 가 실제로 쓰는 것만 갖춘 목.

    `fetch` 만 가짜로 두고 `call` / `fetch_pages` 는 실제 구현을 바인딩합니다.
    스펙 해석과 페이징 루프가 함께 검증됩니다.
    """

    def __init__(self, pages: int, *, always_more: bool = False):
        self.paper = False
        self.pages = pages
        self.always_more = always_more
        self.calls: list[dict] = []

    def call(self, *args, **kwargs):
        return VmKis.call(self, *args, **kwargs)

    def fetch_pages(self, *args, **kwargs):
        return VmKis.fetch_pages(self, *args, **kwargs)

    def fetch(self, *args, **kwargs):
        self.calls.append(kwargs)
        n = len(self.calls)
        return SimpleNamespace(
            items=[f"P{n}"],
            is_last=False if self.always_more else n >= self.pages,
            next_page=_Page(is_first=False),
        )


def _run(kis: FakeKis, **kwargs):
    return kis.fetch_pages(
        ENDPOINT,
        response_type=lambda: SimpleNamespace(items=[]),
        merge=lambda first, more: first.items.extend(more.items),
        **kwargs,
    )


def test_single_page():
    """첫 페이지가 곧 마지막이면 한 번만 호출한다."""
    kis = FakeKis(pages=1)

    result = _run(kis)

    assert len(kis.calls) == 1
    assert result.items == ["P1"]


def test_multiple_pages_accumulate():
    """여러 페이지를 첫 페이지에 누적한다."""
    kis = FakeKis(pages=3)

    result = _run(kis)

    assert len(kis.calls) == 3
    assert result.items == ["P1", "P2", "P3"]


def test_continuous_false_stops_after_first_page():
    """`continuous=False` 면 다음 페이지가 있어도 첫 페이지만 가져온다."""
    kis = FakeKis(pages=3)

    result = _run(kis, continuous=False)

    assert len(kis.calls) == 1
    assert result.items == ["P1"]


def test_max_pages_guard_raises():
    """`is_last` 가 끝내 오지 않아도 무한 루프가 되지 않는다.

    조용히 도는 것보다 명시적으로 실패하는 편이 낫습니다.
    """
    kis = FakeKis(pages=0, always_more=True)

    with pytest.raises(RuntimeError, match="연속조회가 5페이지를 넘겼습니다"):
        _run(kis, max_pages=5)

    assert len(kis.calls) == 5


def test_default_max_pages_is_bounded():
    """상한 기본값이 존재한다 — 넘기지 않아도 무한이 아니다."""
    kis = FakeKis(pages=0, always_more=True)

    with pytest.raises(RuntimeError):
        _run(kis)

    assert len(kis.calls) == MAX_PAGES


def test_continuous_header_only_after_first_page():
    """첫 페이지는 연속조회가 아니고, 두 번째부터 연속조회다.

    반대로 하면 첫 요청이 "이어서 조회"로 나가 서버가 빈 결과를 줍니다.
    """
    kis = FakeKis(pages=2)

    _run(kis)

    assert kis.calls[0]["continuous"] is False
    assert kis.calls[1]["continuous"] is True


def test_resolves_endpoint_spec():
    """TR ID 와 도메인은 스펙에서 나온다."""
    kis = FakeKis(pages=1)

    _run(kis)

    assert kis.calls[0]["api"] == "TTTEST01R"
    assert kis.calls[0]["domain"] == "live"


def test_page_size_comes_from_spec():
    """커서 길이를 스펙이 정한다 — 호출부가 `page.to(100)` 을 적지 않는다."""
    sizes: list[int] = []

    class SizeSpyPage(KisPage):
        def to(self, size: int):
            sizes.append(size)
            return super().to(size)

    kis = FakeKis(pages=1)
    _run(kis, page=SizeSpyPage())

    assert sizes == [100]


def test_instance_response_type_is_rejected():
    """팩토리가 아니라 인스턴스를 주면 즉시 막는다.

    `KisObject.transform_` 은 인스턴스를 받으면 **그 인스턴스에 그대로
    파싱**합니다. 하나를 돌려 쓰면 모든 페이지가 같은 객체가 되고
    `merge(first, result)` 가 자기 자신을 이어붙여 결과가 불어납니다.
    """
    from vmkis.responses.types import KisDynamicDict

    kis = FakeKis(pages=2)

    with pytest.raises(TypeError, match="팩토리를 주세요"):
        kis.fetch_pages(
            ENDPOINT,
            response_type=KisDynamicDict(),
            merge=lambda first, more: None,
        )

    assert kis.calls == []
