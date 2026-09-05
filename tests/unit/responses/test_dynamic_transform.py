"""Cleaned transform tests for KisObject.transform_ edge cases."""

from dataclasses import dataclass
from decimal import Decimal

import pytest

from vmkis.responses.dynamic import KisList, KisObject
from vmkis.responses.response import KisResponse
from vmkis.responses.types import KisBool, KisDecimal, KisInt, KisString

pytestmark = pytest.mark.unit


@dataclass
class SimpleResponse(KisResponse):
    name: str = KisString()
    value: int = KisInt()

    def __pre_init__(self, data: dict) -> None:
        data.setdefault("rt_cd", "0")
        data.setdefault("msg_cd", "")
        data.setdefault("msg1", "")
        data.setdefault("__response__", None)
        super().__pre_init__(data)


@dataclass
class NestedItem(KisResponse):
    id: int = KisInt()
    name: str = KisString()

    def __pre_init__(self, data: dict) -> None:
        data.setdefault("rt_cd", "0")
        data.setdefault("msg_cd", "")
        data.setdefault("msg1", "")
        data.setdefault("__response__", None)
        super().__pre_init__(data)


@dataclass
class ComplexResponse(KisResponse):
    symbol: str = KisString()
    price: Decimal = KisDecimal()
    items: list[NestedItem] = KisList(NestedItem)
    active: bool = KisBool()

    def __pre_init__(self, data: dict) -> None:
        data.setdefault("rt_cd", "0")
        data.setdefault("msg_cd", "")
        data.setdefault("msg1", "")
        data.setdefault("__response__", None)
        super().__pre_init__(data)


@dataclass
class OptionalFieldResponse(KisResponse):
    required: str = KisString()
    optional: int | None = KisInt()

    def __pre_init__(self, data: dict) -> None:
        data.setdefault("rt_cd", "0")
        data.setdefault("msg_cd", "")
        data.setdefault("msg1", "")
        data.setdefault("__response__", None)
        super().__pre_init__(data)


class TestKisObjectTransformEdgeCases:
    def test_transform_with_valid_data(self):
        data = {"name": "test", "value": "123"}
        result = KisObject.transform_(data, SimpleResponse)
        assert isinstance(result, SimpleResponse)
        assert result.name == "test"
        assert result.value == 123

    def test_transform_with_none_values(self):
        data = {"name": None, "value": None}
        with pytest.raises(ValueError):
            KisObject.transform_(data, SimpleResponse)

    def test_transform_with_empty_dict(self):
        data = {}
        with pytest.raises(KeyError):
            KisObject.transform_(data, SimpleResponse)

    def test_transform_with_missing_fields(self):
        data = {"name": "test"}
        with pytest.raises(KeyError):
            KisObject.transform_(data, SimpleResponse)

    def test_transform_with_nested_objects(self):
        data = {
            "symbol": "000660",
            "price": "70000.50",
            "items": [{"id": "1", "name": "item1"}, {"id": "2", "name": "item2"}],
            "active": "true",
        }
        result = KisObject.transform_(data, ComplexResponse)
        assert result.symbol == "000660"
        assert result.price == Decimal("70000.50")
        assert len(result.items) == 2
        assert result.items[0].id == 1
        assert result.items[0].name == "item1"
        assert result.active is True

    def test_transform_with_null_list(self):
        data = {"symbol": "000660", "price": "70000", "items": None, "active": "true"}
        with pytest.raises(ValueError):
            KisObject.transform_(data, ComplexResponse)

    def test_transform_with_invalid_type_conversion(self):
        data = {"name": "test", "value": "not_a_number"}
        with pytest.raises((ValueError, TypeError)):
            KisObject.transform_(data, SimpleResponse)

    def test_transform_with_optional_fields_present(self):
        data = {"required": "test", "optional": "123"}
        result = KisObject.transform_(data, OptionalFieldResponse)
        assert result.required == "test"
        assert result.optional == 123

    def test_transform_with_optional_fields_absent(self):
        data = {"required": "test"}
        with pytest.raises(KeyError):
            KisObject.transform_(data, OptionalFieldResponse)

    def test_transform_with_boolean_variations(self):
        cases = ["true", "false", "1", "0", "yes", "no"]
        for c in cases:
            data = {"symbol": "000660", "price": "70000", "items": [], "active": c}
            result = KisObject.transform_(data, ComplexResponse)
            if c == "true":
                assert result.active is True
            elif c == "false":
                assert result.active is False
            else:
                assert isinstance(result.active, bool)


class TestKisObjectTransformErrorHandling:
    def test_transform_with_invalid_response_type(self):
        with pytest.raises((TypeError, AttributeError)):
            KisObject.transform_({"name": "test"}, str)

    def test_transform_with_none_data(self):
        with pytest.raises((TypeError, AttributeError)):
            KisObject.transform_(None, SimpleResponse)

    def test_transform_with_non_dict_data(self):
        with pytest.raises((TypeError, AttributeError)):
            KisObject.transform_("not a dict", SimpleResponse)
