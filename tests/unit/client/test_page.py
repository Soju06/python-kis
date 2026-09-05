import pytest

from vmkis.client.page import NO_SUFFIX, KisPage, to_page_status


def test_to_page_status_begin_and_end_and_invalid():
    assert to_page_status("F") == "begin"
    assert to_page_status("M") == "begin"
    assert to_page_status("D") == "end"
    assert to_page_status("E") == "end"

    with pytest.raises(ValueError):
        to_page_status("X")


def test_kispage_init_defaults_and_first():
    p = KisPage()
    assert p.size is None
    assert p.search == ""
    assert p.key == ""

    p2 = KisPage.first(50)
    assert isinstance(p2, KisPage)
    assert p2.size == 50


def test_pre_init_parses_100_and_200_and_raises():
    p = KisPage()
    data100 = {"ctx_area_fk100": "S100", "ctx_area_nk100": "K100"}
    p.__pre_init__(data100)
    assert p.search == "S100"
    assert p.key == "K100"
    assert p.size == 100

    p2 = KisPage()
    data200 = {"ctx_area_fk200": "S200", "ctx_area_nk200": "K200"}
    p2.__pre_init__(data200)
    assert p2.search == "S200"
    assert p2.key == "K200"
    assert p2.size == 200

    p3 = KisPage()
    with pytest.raises(ValueError):
        p3.__pre_init__({"other": 1})


def test_is_empty_is_first_and_size_checks():
    p = KisPage()
    assert p.is_empty
    assert p.is_first

    p.search = " "
    p.key = " "
    assert p.is_empty

    p.size = 100
    assert p.is_100
    assert not p.is_200

    p.size = 200
    assert p.is_200
    assert not p.is_100


def test_to_changes_size_or_raises_when_too_small():
    p = KisPage(size=50, search="ab", key="cd")
    new = p.to(100)
    assert isinstance(new, KisPage)
    assert new.size == 100
    assert new.search == "ab"

    p2 = KisPage(size=10, search="longsearch", key="k")
    with pytest.raises(ValueError):
        p2.to(5)


def test_build_requires_size_and_builds_keys():
    p = KisPage(size=100, search="s", key="k")
    d = p.build()
    assert d["ctx_area_fk100"] == "s"
    assert d["ctx_area_nk100"] == "k"

    p2 = KisPage()
    with pytest.raises(ValueError):
        p2.build()


# ---------------------------------------------------------------------------
# 커서 접미사 4변형 (이슈 #16)
#
# KIS API의 커서 파라미터는 CTX_AREA_FK100 / FK200 / FK50 / FK(접미사 없음)
# 네 가지다. 예전에는 100·200만 파싱해, 접미사 없는 변형을 쓰는 API가
# KisPaginationAPIResponse를 상속하는 순간 파싱 단계에서 죽었다.
# ---------------------------------------------------------------------------

VARIANTS = [
    pytest.param("100", 100, id="fk100"),
    pytest.param("200", 200, id="fk200"),
    pytest.param("50", 50, id="fk50"),
    pytest.param("", NO_SUFFIX, id="fk-접미사없음"),
]


@pytest.mark.parametrize("suffix, expected_size", VARIANTS)
def test_pre_init_parses_every_cursor_variant(suffix, expected_size):
    page = KisPage()
    page.__pre_init__({f"ctx_area_fk{suffix}": "S", f"ctx_area_nk{suffix}": "K"})

    assert page.search == "S"
    assert page.key == "K"
    assert page.size == expected_size


@pytest.mark.parametrize("suffix, size", VARIANTS)
def test_build_emits_matching_field_names(suffix, size):
    data = KisPage(size=size, search="S", key="K").build()

    assert data == {f"ctx_area_fk{suffix}": "S", f"ctx_area_nk{suffix}": "K"}


@pytest.mark.parametrize("suffix, size", VARIANTS)
def test_parse_then_build_round_trips(suffix, size):
    """응답에서 읽은 커서를 그대로 다음 요청에 실을 수 있어야 한다."""
    source = {f"ctx_area_fk{suffix}": "S", f"ctx_area_nk{suffix}": "K"}

    page = KisPage()
    page.__pre_init__(source)

    assert page.build() == source


def test_no_suffix_size_is_not_a_length():
    """NO_SUFFIX(0)는 '길이 0'이 아니라 '접미사 없음'이다.

    길이로 취급하면 `to(NO_SUFFIX)`가 비어 있지 않은 커서에서 항상 실패한다.
    """
    page = KisPage(size=100, search="문자열이_길어도", key="상관없음")

    moved = page.to(NO_SUFFIX)

    assert moved.size == NO_SUFFIX
    assert moved.field_suffix == ""
    assert moved.build() == {"ctx_area_fk": "문자열이_길어도", "ctx_area_nk": "상관없음"}


def test_field_suffix_requires_size():
    page = KisPage()

    with pytest.raises(ValueError):
        _ = page.field_suffix
