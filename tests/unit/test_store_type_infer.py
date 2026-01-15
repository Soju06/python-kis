from __future__ import annotations

from codegen.store.models import MasterField
from codegen.store.steps.infer import infer_field_from_values


def _field(name: str, description: str = "") -> MasterField:
    return MasterField(name=name, type="char", length=8, description=description)


def test_infer_bool() -> None:
    field = _field("flag_yn", "여부")
    infer = infer_field_from_values(field, ["Y", "N", "Y"])
    assert infer.kind == "bool"


def test_infer_bool_with_noise() -> None:
    field = _field("flag_yn", "여부")
    infer = infer_field_from_values(field, ["Y", "N", "X", "Y"])
    assert infer.kind == "bool"


def test_infer_date() -> None:
    field = _field("base_date", "기준일자")
    infer = infer_field_from_values(field, ["20240101", "20231231", "00000000"])
    assert infer.kind == "date"
    assert infer.nullable is True


def test_infer_int() -> None:
    field = _field("qty", "수량")
    infer = infer_field_from_values(field, ["1", "2", "3"])
    assert infer.kind == "int"


def test_infer_decimal() -> None:
    field = _field("price", "가격")
    infer = infer_field_from_values(field, ["1.25", "3.40"])
    assert infer.kind == "decimal"


def test_infer_enum() -> None:
    field = _field("status", "구분값")
    infer = infer_field_from_values(field, ["A", "B", "A", "B"])
    assert infer.kind == "str"


def test_infer_enum_from_description() -> None:
    field = _field("opt_cls", "1:콜 2:풋 3:기타")
    infer = infer_field_from_values(field, ["1", "2", "3"])
    assert infer.kind == "enum"
    assert infer.enum == ["1", "2", "3"]


def test_infer_enum_from_quoted_description() -> None:
    field = _field("rght_type_cls_code", "권리 유형 구분 코드 ''C'':콜 ''E'':기타 ''P'':풋")
    infer = infer_field_from_values(field, ["C", "E", "P"])
    assert infer.kind == "enum"
    assert infer.enum == ["C", "E", "P"]


def test_infer_enum_from_list_description() -> None:
    field = _field("lock_cls_code", "SW,SR,EW는 미해당")
    infer = infer_field_from_values(field, ["SW", "SR", "EW"])
    assert infer.kind == "enum"
    assert infer.enum == ["SW", "SR", "EW"]


def test_infer_enum_from_colonless_description() -> None:
    field = _field("mrkt_div", "N 해외지수 X 환율 KX 원화환율")
    infer = infer_field_from_values(field, ["N", "X", "KX"])
    assert infer.kind == "enum"
    assert infer.enum == ["N", "X", "KX"]


def test_infer_enum_from_colonless_multiword_description() -> None:
    field = _field("prdt_type", "512 미국 나스닥 / 513 미국 뉴욕 / 529 미국 아멕스")
    infer = infer_field_from_values(field, ["512", "513", "529"])
    assert infer.kind == "enum"
    assert infer.enum == ["512", "513", "529"]


def test_enum_does_not_drop_non_yn_codes() -> None:
    field = _field("mrkt_div", "N 해외지수 X 환율")
    infer = infer_field_from_values(field, ["N", "X"])
    assert infer.kind == "enum"
    assert infer.enum == ["N", "X"]


def test_description_enum_does_not_merge_observed() -> None:
    field = _field("opt_cls", "1:콜 2:풋")
    infer = infer_field_from_values(field, ["1", "2", "9"])
    assert infer.kind == "enum"
    assert infer.enum == ["1", "2"]


def test_infer_time() -> None:
    field = _field("tr_time", "체결시간")
    infer = infer_field_from_values(field, ["093000", "153500", "000000"])
    assert infer.kind == "time"
    assert infer.nullable is True


def test_infer_datetime() -> None:
    field = _field("tr_datetime", "체결일시")
    infer = infer_field_from_values(field, ["20240101153000", "20240102120000"])
    assert infer.kind == "datetime"


def test_code_like_stays_str() -> None:
    field = _field("item_code", "코드")
    infer = infer_field_from_values(field, ["001", "002", "010"])
    assert infer.kind == "str"
