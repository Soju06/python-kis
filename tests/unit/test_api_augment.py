from __future__ import annotations

from pathlib import Path
from typing import cast

from pydantic import BaseModel

from codegen.api.models import EndpointSpec
from codegen.api.overrides import AugmentOverrides
from codegen.api.runtime import ValueResolver
from codegen.api.steps.augment import augment_endpoint
from codegen.core.types import JsonObject
from pykis.api.client import SyncKisRawClient
from pykis.api.errors import KisTransportError
from pykis.api.raw.types import Endpoint


class _DummyAuth:
    account_number: tuple[str, str] = ("12345678", "01")
    app_key: str = "app"
    secret_key: str = "secret"
    id: str = "tester"


class _DummyHttpResponse:
    status_code: int
    is_success: bool
    text: str
    _payload: JsonObject

    def __init__(self, payload: JsonObject) -> None:
        self.status_code = 200
        self.is_success = True
        self.text = ""
        self._payload = payload

    def json(self) -> JsonObject:
        return self._payload


class _DummyClient:
    auth: _DummyAuth
    _payload: JsonObject

    def __init__(self, payload: JsonObject) -> None:
        self.auth = _DummyAuth()
        self._payload = payload

    def request(
        self,
        *,
        method: str,
        base_url: str,
        path: str,
        headers: dict[str, str],
        params: dict[str, str | int | float | None] | None,
        body: JsonObject | None,
        auth_required: bool,
        hashkey_required: bool,
    ) -> _DummyHttpResponse:
        return _DummyHttpResponse(self._payload)


class _SequencedClient:
    auth: _DummyAuth
    _outcomes: list[JsonObject | Exception]
    call_count: int

    def __init__(self, outcomes: list[JsonObject | Exception]) -> None:
        self.auth = _DummyAuth()
        self._outcomes = outcomes
        self.call_count = 0

    def request(
        self,
        *,
        method: str,
        base_url: str,
        path: str,
        headers: dict[str, str],
        params: dict[str, str | int | float | None] | None,
        body: JsonObject | None,
        auth_required: bool,
        hashkey_required: bool,
    ) -> _DummyHttpResponse:
        if self.call_count >= len(self._outcomes):
            raise RuntimeError("no outcome configured")
        outcome = self._outcomes[self.call_count]
        self.call_count += 1
        if isinstance(outcome, Exception):
            raise outcome
        return _DummyHttpResponse(outcome)


class _RequestModel(BaseModel):
    pass


class _ResponseModelExpectingDict(BaseModel):
    rt_cd: str
    msg_cd: str
    msg1: str
    output: dict[str, str]


def _build_spec() -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": "augment-test-endpoint",
            "name": "augment test endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/augment",
            "domains": {"real": "https://example.com", "demo": None},
            "request": {"headers": [], "query": [], "body": []},
            "response": {
                "headers": [],
                "body": [],
                "outputs": [{"code": "output", "name": "output", "kind": "array", "fields": []}],
            },
            "errors": [],
            "source_path": "tmp/docs/normalized/test/augment.json",
        }
    )


def _build_spec_with_required_query() -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": "augment-test-endpoint-query",
            "name": "augment test endpoint query",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/augment-query",
            "domains": {"real": "https://example.com", "demo": None},
            "request": {
                "headers": [],
                "query": [
                    {
                        "code": "FID_INPUT_ISCD",
                        "name": "종목코드",
                        "required": True,
                        "type": "A0001",
                        "type_name": "String",
                        "length": "12",
                    }
                ],
                "body": [],
            },
            "response": {
                "headers": [],
                "body": [],
                "outputs": [{"code": "output", "name": "output", "kind": "single", "fields": []}],
            },
            "errors": [],
            "source_path": "tmp/docs/normalized/test/augment_query.json",
        }
    )


def test_augment_endpoint_downgrades_response_validation_failure(tmp_path: Path) -> None:
    spec = _build_spec()
    endpoint = Endpoint(
        id=spec.id,
        name=spec.name,
        method=spec.method,
        path=spec.path,
        request_model=_RequestModel,
        response_model=_ResponseModelExpectingDict,
        description=spec.description,
        real_tr_id=spec.real_tr_id,
        demo_tr_id=spec.demo_tr_id,
        auth_required=False,
        hashkey_required=False,
    )
    payload: JsonObject = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": [{"code": "A"}],
    }
    client = _DummyClient(payload)
    resolver = ValueResolver(cast(SyncKisRawClient, client), AugmentOverrides())

    result = augment_endpoint(
        spec,
        endpoint,
        cast(SyncKisRawClient, client),
        resolver,
        AugmentOverrides(),
        tmp_path,
        "real",
        "https://example.com",
    )

    assert result.status == "ok"
    assert result.note == "validation_error"
    assert (tmp_path / spec.id / "error_success.json").exists()


def test_augment_endpoint_ignores_probe_transport_error(tmp_path: Path) -> None:
    spec = _build_spec_with_required_query()
    endpoint = Endpoint(
        id=spec.id,
        name=spec.name,
        method=spec.method,
        path=spec.path,
        request_model=_RequestModel,
        response_model=_ResponseModelExpectingDict,
        description=spec.description,
        real_tr_id=spec.real_tr_id,
        demo_tr_id=spec.demo_tr_id,
        auth_required=False,
        hashkey_required=False,
    )
    success_payload: JsonObject = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": {"code": "A"},
    }
    transport_error = KisTransportError(
        "request transport error",
        original=RuntimeError("network timeout"),
        context=None,
    )
    client = _SequencedClient([success_payload, transport_error])
    resolver = ValueResolver(cast(SyncKisRawClient, client), AugmentOverrides())

    result = augment_endpoint(
        spec,
        endpoint,
        cast(SyncKisRawClient, client),
        resolver,
        AugmentOverrides(),
        tmp_path,
        "real",
        "https://example.com",
    )

    assert result.status == "ok"
    assert result.note is None
    assert client.call_count == 2
    assert (tmp_path / spec.id / "success.json").exists()
