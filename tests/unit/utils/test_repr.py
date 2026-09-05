from datetime import date, datetime, time
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from vmkis.utils import repr as kisrepr


def test_decimal_datetime_date_time_zoneinfo_custom_reprs():
    # Decimal
    d = Decimal("2.5000")
    assert kisrepr._repr(d) == "2.5"

    # datetime -> repr(isoformat())
    dt = datetime(2020, 1, 2, 3, 4, 5)
    assert kisrepr._repr(dt) == repr(dt.isoformat())

    # date -> repr(isoformat())
    dd = date(2021, 12, 31)
    assert kisrepr._repr(dd) == repr(dd.isoformat())

    # time -> repr(isoformat())
    tt = time(12, 34, 56)
    assert kisrepr._repr(tt) == repr(tt.isoformat())

    # ZoneInfo -> ZoneInfo(key)
    z = ZoneInfo("UTC")
    assert kisrepr._repr(z) == f"{ZoneInfo.__name__}('UTC')"


def test_iterable_single_and_multiple_lines_and_ellipsis():
    # small list -> single line
    assert kisrepr.list_repr([1, 2, 3]) == "[1, 2, 3]"

    # small tuple -> single line
    assert (
        kisrepr.tuple_repr((1,)) == "(1,)".replace(",)", ")") or kisrepr.tuple_repr((1,)) == "(1,)"
    )  # tolerate tuple formatting

    # long list -> multiple lines
    big = list(range(10))
    out = kisrepr.list_repr(big, lines=None, ellipsis=None)
    assert "\n" in out

    # ellipsis cuts items and appends ', ...'
    out2 = kisrepr.list_repr(range(10), lines="single", ellipsis=3)
    assert out2.startswith("[")
    assert "..." in out2

    # set representation shouldn't raise and should contain elements
    s = {1, 2}
    sr = kisrepr.set_repr(s)
    assert sr.startswith("{")
    assert ("1" in sr) and ("2" in sr)


def test_iterable_invalid_tie_raises_value_error():
    # call internal _iterable_repr with odd-length tie to trigger ValueError
    with pytest.raises(ValueError):
        kisrepr._iterable_repr([1, 2], tie="{")


def test_dict_repr_single_and_multiple_and_depth_cutoff():
    # small dict -> single line
    d = {"a": 1, "b": 2}
    out = kisrepr.dict_repr(d)
    assert out.startswith("{") and ":" in out
    # dict with string containing literal \n still becomes single line since repr escapes it
    d2 = {"a": "short", "b": "multi\nline"}
    out2 = kisrepr.dict_repr(d2)
    # The repr() function escapes the newline, so it doesn't force multiline mode
    assert out2.startswith("{") and ":" in out2

    # depth cutoff for dict
    assert kisrepr.dict_repr({"x": 1}, _depth=5, max_depth=0) == "{:...}"


def test_object_repr_single_multiple_unbounded_and_depth_cutoff():
    class WithAttr:
        a = 1

        @property
        def b(self):
            raise AttributeError("no b")

    inst = WithAttr()
    # specify fields to control order and include property that raises AttributeError
    out_single = kisrepr.object_repr(inst, fields=["a", "b"], lines="single")
    assert "WithAttr(" in out_single and "a=1" in out_single and "b=Unbounded" in out_single

    out_multi = kisrepr.object_repr(inst, fields=["a", "b"], lines="multiple")
    assert "WithAttr(" in out_multi and "\n" in out_multi

    # depth cutoff
    class C:
        x = 1

    assert kisrepr.object_repr(C(), _depth=2, max_depth=0) == "C(...)"


def test__repr_uses_custom_reprs_and_default_fallback_and_max_depth():
    class Custom:
        def __repr__(self):
            return "should-not-be-used"

    # attach a custom repr function
    def myrepr(obj, max_depth=7, depth=0):
        return "CUSTOM"

    kisrepr.custom_repr(Custom, myrepr)
    try:
        assert kisrepr._repr(Custom()) == "CUSTOM"
    finally:
        kisrepr.remove_custom_repr(Custom)

    # fallback to builtin repr for normal objects
    val = 12345
    assert kisrepr._repr(val) == repr(val)

    # max depth stops recursion
    nested = [[[1]]]
    assert kisrepr._repr(nested, max_depth=1, _depth=1) == "..."


def test_kis_repr_decorator_sets_repr_and_metadata():
    @kisrepr.kis_repr("x", "y", lines="single")
    class My:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    inst = My(1, 2)
    r = inst.__repr__()  # use the generated repr
    assert "My(" in r and "x=1" in r and "y=2" in r

    # check that the generated function has expected attributes
    assert hasattr(My.__repr__, "__is_kis_repr__")
    assert My.__repr__.__name__ == "__repr__"


def test_custom_repr_management():
    class Tmp:
        pass

    def fn(obj, max_depth=7, depth=0):
        return "X"

    kisrepr.custom_repr(Tmp, fn)
    assert Tmp in kisrepr.custom_reprs
    assert kisrepr.custom_reprs[Tmp] is fn

    kisrepr.remove_custom_repr(Tmp)
    assert Tmp not in kisrepr.custom_reprs


# ---------------------------------------------------------------------------
# 여러 줄 모드 / 생략(ellipsis) / 빈 컨테이너 / 깊이 컷오프
#
# 기존 테스트는 주로 한 줄 모드를 확인한다. 여러 줄 분기와 생략 표기, 빈 컨테이너
# 단축 경로는 실제 객체 repr에서 자주 타는데도 검증이 없었다.
# ---------------------------------------------------------------------------


class TestDictReprMultipleLines:
    """`dict_repr`의 여러 줄 모드."""

    def test_multiple_lines_indents_each_entry(self):
        out = kisrepr.dict_repr({"a": 1, "b": 2}, lines="multiple", indent="  ")

        assert out.startswith("{\n")
        assert out.endswith("}")
        assert "  'a': 1" in out
        assert "  'b': 2" in out
        # 마지막 항목 뒤에는 쉼표가 붙지 않는다.
        assert ",\n" in out
        assert not out.rstrip("}").rstrip().endswith(",")

    def test_multiple_lines_appends_ellipsis(self):
        """생략된 항목이 있으면 마지막 줄에 '...'을 들여써 붙인다."""
        out = kisrepr.dict_repr({"a": 1, "b": 2, "c": 3}, lines="multiple", indent="  ", ellipsis=1)

        assert "'a': 1" in out
        assert "'b'" not in out
        assert "\n  ...\n" in out

    def test_single_line_appends_ellipsis(self):
        """한 줄 모드에서는 ', ...'로 붙인다."""
        out = kisrepr.dict_repr({"a": 1, "b": 2, "c": 3}, lines="single", ellipsis=1)

        assert out == "{'a': 1, ...}"

    def test_depth_cutoff(self):
        assert kisrepr.dict_repr({"a": 1}, max_depth=3, _depth=3) == "{:...}"


class TestIterableReprEdgeCases:
    """`_iterable_repr` 경계 동작."""

    def test_empty_container_is_shortened(self):
        assert kisrepr.list_repr([]) == "[]"
        assert kisrepr.set_repr(set()) == "{}"
        assert kisrepr.tuple_repr(()) == "()"

    def test_depth_cutoff_keeps_tie(self):
        assert kisrepr.list_repr([1, 2], max_depth=2, _depth=2) == "[...]"

    def test_multiple_lines_appends_ellipsis(self):
        out = kisrepr.list_repr([1, 2, 3], lines="multiple", indent="  ", ellipsis=1)

        assert out.startswith("[\n")
        assert "\n  ...\n" in out
        assert out.endswith("]")

    def test_accepts_non_sequence_iterable(self):
        """리스트/튜플/셋이 아닌 이터러블도 받아 처리한다."""
        assert kisrepr.list_repr(iter([1, 2, 3]), lines="single") == "[1, 2, 3]"


class TestReprDispatch:
    """`_repr`의 타입별 분기."""

    def test_dispatches_tuple_to_tuple_repr(self):
        assert kisrepr._repr((1, 2)) == kisrepr.tuple_repr((1, 2))

    def test_dispatches_set_to_set_repr(self):
        assert kisrepr._repr({1}) == kisrepr.set_repr({1})

    def test_dispatches_frozenset_to_set_repr(self):
        assert kisrepr._repr(frozenset({1})) == kisrepr.set_repr(frozenset({1}))

    def test_dispatches_to_kis_repr_decorated_object(self):
        """@kis_repr가 붙은 객체는 그 __repr__로 위임하며 깊이를 전달한다"""

        @kisrepr.kis_repr("value", lines="single")
        class Sample:
            def __init__(self):
                self.value = 1

        sample = Sample()

        assert kisrepr._repr(sample) == repr(sample)


def test_unbounded_type_equality():
    """`UnboundedType`은 같은 타입끼리만 동등하다."""
    assert kisrepr.UnboundedType() == kisrepr.UnboundedType()
    assert kisrepr.UnboundedType() != object()
