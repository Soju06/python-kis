from __future__ import annotations

from pydantic import Field

from pykis.api._sync.client import _apply_blank_allowed
from pykis.api.raw.base import RawModel


class _BlankAllowedRequest(RawModel):
    count: int | None = Field(default=None, alias="COUNT", json_schema_extra={"blank_allowed": True})
    price: int | None = Field(default=None, alias="PRICE")


def _build_payload(model: RawModel) -> dict[str, object]:
    payload = {key: value for key, value in model.model_dump(by_alias=True, exclude_none=True).items()}
    return _apply_blank_allowed(model, payload)


def test_blank_allowed_inserts_empty_string() -> None:
    model = _BlankAllowedRequest()
    payload = _build_payload(model)
    assert payload == {"COUNT": ""}


def test_blank_allowed_preserves_value() -> None:
    model = _BlankAllowedRequest(count=5)
    payload = _build_payload(model)
    assert payload == {"COUNT": 5}
