import pytest

import vmkis.responses.websocket as wsmod
from vmkis.responses.dynamic import KisNoneValueError, empty
from vmkis.responses.websocket import KisWebsocketResponse


def test_parse_no_fields_calls_pre_and_post_init_and_sets_data():
    called = {}

    class R(KisWebsocketResponse):
        __fields__ = []

        def __pre_init__(self, data):
            called["pre"] = True

        def __post_init__(self):
            called["post"] = True

    items = list(wsmod.KisWebsocketResponse.parse("A^B", response_type=R))
    assert len(items) == 1
    inst = items[0]
    assert inst.__data__ == ["A", "B"]
    assert called.get("pre") and called.get("post")


def test_parse_invalid_data_length_raises():
    class R(KisWebsocketResponse):
        __fields__ = [object(), object()]

    with pytest.raises(ValueError, match="Invalid data length"):
        list(wsmod.KisWebsocketResponse.parse("A^B^C", response_type=R))


def test_parse_invalid_count_raises():
    class R(KisWebsocketResponse):
        __fields__ = [object(), object()]

    # two items -> 1 record, but ask for count=2
    with pytest.raises(ValueError, match="Invalid data count"):
        list(wsmod.KisWebsocketResponse.parse("A^B", count=2, response_type=R))


def test_parse_with_field_transform_sets_attributes():
    class Field:
        def __init__(self, name):
            self.field = name
            self.default = empty
            self.absolute = False

        def transform(self, value):
            return value.upper()

    class Resp(KisWebsocketResponse):
        __fields__ = [Field("x"), Field("y")]
        __annotations__ = {"x": str, "y": str}

    res_list = list(KisWebsocketResponse.parse("a^b", response_type=Resp))
    assert len(res_list) == 1
    r = res_list[0]
    assert r.x == "A"
    assert r.y == "B"


def test_parse_kisnonevalueerror_uses_default_or_raises():
    # field that raises KisNoneValueError
    class FieldDefault:
        def __init__(self, name, default=empty):
            self.field = name
            self.default = default
            self.absolute = False

        def transform(self, value):
            raise KisNoneValueError()

    class Resp1(KisWebsocketResponse):
        __fields__ = [FieldDefault("v", default=5)]
        __annotations__ = {"v": int}

    out1 = list(KisWebsocketResponse.parse("x", response_type=Resp1))
    assert out1[0].v == 5

    # no default and not nullable -> should raise ValueError about None
    class Resp2(KisWebsocketResponse):
        __fields__ = [FieldDefault("v")]
        __annotations__ = {"v": int}

    with pytest.raises(ValueError, match="필드가 None일 수 없습니다"):
        list(KisWebsocketResponse.parse("x", response_type=Resp2))


def test_parse_transform_exception_is_wrapped():
    class FieldErr:
        def __init__(self, name):
            self.field = name
            self.default = empty
            self.absolute = False

        def transform(self, value):
            raise RuntimeError("boom")

    class Resp(KisWebsocketResponse):
        __fields__ = [FieldErr("z")]
        __annotations__ = {"z": str}

    with pytest.raises(ValueError) as excinfo:
        list(KisWebsocketResponse.parse("x", response_type=Resp))

    assert "데이터 파싱 중 오류" in str(excinfo.value)
