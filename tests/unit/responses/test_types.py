from datetime import date, datetime, time
from decimal import Decimal

import pytest

from vmkis.responses.dynamic import KisNoneValueError
from vmkis.responses.types import (
    KisAny,
    KisBool,
    KisDate,
    KisDatetime,
    KisDecimal,
    KisDict,
    KisDynamicDict,
    KisFloat,
    KisInt,
    KisString,
    KisTime,
    KisTimeToDatetime,
)
from vmkis.utils.timezone import TIMEZONE


def test_kis_dynamic_dict_from_and_getattr_and_repr():
    d = {"a": 1, "nested": {"b": 2}, "arr": [{"c": 3}, 4]}
    kd = KisDynamicDict.from_dict(d)

    assert kd.a == 1
    # nested returns KisDynamicDict
    nested = kd.nested
    assert isinstance(nested, KisDynamicDict)
    assert nested.b == 2
    # list mapping
    arr = kd.arr
    assert isinstance(arr[0], KisDynamicDict)
    assert arr[1] == 4
    # repr contains keys
    s = repr(kd)
    assert "a" in s and "nested" in s


def test_kis_any_transform_custom_and_default():
    anyt = KisAny(lambda v: "X" if v == "in" else {})
    assert anyt.transform("in") == "X"

    # default KisAny without arg returns KisDynamicDict when transforming
    any_default = KisAny()
    res = any_default.transform({"k": "v"})
    assert isinstance(res, KisDynamicDict)
    # default transform returns an empty KisDynamicDict instance (no __data__ set)
    # attempting to access attributes should raise AttributeError because __data__ is None
    with pytest.raises(AttributeError):
        _ = res.k


def test_basic_string_int_float_decimal_bool_transforms():
    s = KisString()
    assert s.transform(123) == "123"
    assert s.transform("abc") == "abc"

    i = KisInt()
    assert i.transform(5) == 5
    assert i.transform("42") == 42
    with pytest.raises(KisNoneValueError):
        i.transform("")

    f = KisFloat()
    assert f.transform(1.5) == 1.5
    assert f.transform("2.5") == 2.5
    with pytest.raises(KisNoneValueError):
        f.transform("")

    d = KisDecimal()
    assert d.transform("1.2300") == Decimal("1.23")
    with pytest.raises(KisNoneValueError):
        d.transform("")

    b = KisBool()
    assert b.transform(True) is True
    assert b.transform("Y") is True
    assert b.transform("true") is True
    assert b.transform(0) is False
    assert b.transform("n") is False


def test_date_time_datetime_and_dict_transforms():
    kd = KisDict()
    assert kd.transform({"x": 1}) == {"x": 1}
    with pytest.raises(KisNoneValueError):
        kd.transform("")

    kd_date = KisDate()
    dt = kd_date.transform("20250101")
    assert isinstance(dt, date)
    assert dt == datetime.strptime("20250101", "%Y%m%d").replace(tzinfo=TIMEZONE).date()

    kd_time = KisTime()
    t = kd_time.transform("235959")
    assert isinstance(t, time)
    assert t.hour == 23 and t.minute == 59 and t.second == 59

    kd_dt = KisDatetime()
    full = kd_dt.transform("20250101123045")
    assert isinstance(full, datetime)
    assert full.year == 2025 and full.hour == 12 and full.minute == 30 and full.second == 45


def test_time_to_datetime_transform():
    ktt = KisTimeToDatetime()
    res = ktt.transform("120000")
    assert isinstance(res, datetime)
    assert res.time().hour == 12 and res.time().minute == 0


# ---------------------------------------------------------------------------
# transform()의 두 공통 경로
#
# 대부분의 KisType.transform()은 다음 두 가지를 먼저 처리한다.
#   1) 이미 목표 타입인 값은 그대로 반환한다 (멱등)
#   2) 빈 문자열은 KisNoneValueError로 "값 없음"을 알린다
#
# 두 경로 모두 API 응답에 빈 칸이 섞여 들어오거나 이미 변환된 값이 재차 흘러올 때
# 동작을 좌우하지만 테스트가 없었다.
# ---------------------------------------------------------------------------

ALREADY_CONVERTED = [
    (KisDecimal, Decimal("1.5")),
    (KisBool, True),
    (KisDate, date(2026, 8, 27)),
    (KisTime, time(9, 30)),
    (KisDatetime, datetime(2026, 8, 27, 9, 30, tzinfo=TIMEZONE)),
    (KisDict, {"a": 1}),
    (KisTimeToDatetime, datetime(2026, 8, 27, 9, 30, tzinfo=TIMEZONE)),
]


@pytest.mark.parametrize(
    ("kis_type", "value"),
    ALREADY_CONVERTED,
    ids=[t.__name__ for t, _ in ALREADY_CONVERTED],
)
def test_transform_is_idempotent_for_converted_values(kis_type, value):
    """이미 목표 타입인 값은 변환 없이 그대로 반환한다."""
    assert kis_type().transform(value) is value


EMPTY_STRING_RAISES = [
    KisDecimal,
    KisBool,
    KisDate,
    KisTime,
    KisDatetime,
    KisDict,
    KisTimeToDatetime,
]


@pytest.mark.parametrize("kis_type", EMPTY_STRING_RAISES, ids=lambda t: t.__name__)
def test_empty_string_raises_none_value_error(kis_type):
    """빈 문자열은 '값 없음'으로 취급한다."""
    with pytest.raises(KisNoneValueError):
        kis_type().transform("")


def test_bool_transform_coerces_non_string_input():
    """문자열도 bool도 int도 아닌 값은 str()로 강제 변환 후 판정한다."""

    class Truthy:
        def __str__(self):
            return "Y"

    class Falsy:
        def __str__(self):
            return "N"

    assert KisBool().transform(Truthy()) is True
    assert KisBool().transform(Falsy()) is False


def test_dict_transform_accepts_mapping_pairs():
    """Dict가 아닌 매핑 가능한 입력은 dict()로 변환한다."""
    assert KisDict().transform([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}


class TestKisDynamicDictDunders:
    """`KisDynamicDict`의 특수 메서드."""

    def test_str_matches_repr(self):
        """__str__은 __repr__과 같은 문자열을 낸다."""
        instance = KisDynamicDict.from_dict({"a": 1})

        assert str(instance) == repr(instance)

    def test_dict_returns_backing_data(self):
        """__dict__()는 원본 데이터를 그대로 돌려준다."""
        data = {"a": 1, "b": 2}

        assert KisDynamicDict.from_dict(data).__dict__() == data

    def test_missing_key_falls_back_to_attribute_lookup(self):
        """없는 키는 일반 속성 조회로 넘어가고, 그마저 없으면 AttributeError."""
        instance = KisDynamicDict.from_dict({"a": 1})
        # 속성명을 변수로 두는 이유: 상수를 쓰면 ruff B009, 그냥 접근하면 B018이 걸린다.
        missing = "does_not_exist"

        with pytest.raises(AttributeError):
            getattr(instance, missing)
