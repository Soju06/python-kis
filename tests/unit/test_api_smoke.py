from __future__ import annotations

from pathlib import Path
from typing import cast

from pydantic import BaseModel

from codegen.api.models import EndpointSpec
from codegen.api.report_models import SmokeReport
from codegen.api.steps.smoke import _detect_sentinel_success, run_smoke
from codegen.core.types import JsonObject
from pykis.api.client import SyncKisRawClient
from pykis.api.errors import KisResponseError
from pykis.api.raw.types import Endpoint


class _DummyAuth:
    account_number: tuple[str, str] = ("12345678", "01")
    app_key: str = "app"
    secret_key: str = "secret"
    id: str = "tester"


class _DummyResponse:
    status_code: int
    _payload: JsonObject

    def __init__(self, status_code: int, payload: JsonObject) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> JsonObject:
        return self._payload


class _RequestModel(BaseModel):
    pass


class _ResponseModel(BaseModel):
    rt_cd: str | None = None


class _DummyClient:
    auth: _DummyAuth
    call_count: int
    _outcomes: list[str | Exception]

    def __init__(self, outcomes: list[str | Exception]) -> None:
        self.auth = _DummyAuth()
        self.call_count = 0
        self._outcomes = outcomes

    def call(self, endpoint: Endpoint, request: object) -> tuple[_ResponseModel, _DummyResponse]:
        if self.call_count >= len(self._outcomes):
            raise RuntimeError("no outcome configured")
        outcome = self._outcomes[self.call_count]
        self.call_count += 1
        if isinstance(outcome, Exception):
            raise outcome
        if outcome != "ok":
            raise RuntimeError(f"unsupported outcome: {outcome}")
        response = endpoint.response_model.model_validate({"rt_cd": "0"})
        return response, _DummyResponse(200, {"rt_cd": "0"})


def _build_spec(endpoint_id: str = "smoke-test-endpoint") -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": endpoint_id,
            "name": "smoke test endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/smoke",
            "domains": {"real": "Y", "demo": None},
            "request": {"headers": [], "query": [], "body": []},
            "response": {"headers": [], "body": [], "outputs": []},
            "errors": [],
            "source_path": "tmp/docs/normalized/test/smoke.json",
        }
    )


def _build_list_output_spec(endpoint_id: str) -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": endpoint_id,
            "name": "sentinel test endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/sentinel",
            "domains": {"real": "Y", "demo": None},
            "request": {"headers": [], "query": [], "body": []},
            "response": {
                "headers": [],
                "body": [],
                "outputs": [
                    {
                        "code": "output",
                        "name": "output",
                        "fields": [],
                    }
                ],
            },
            "errors": [],
            "source_path": "tmp/docs/normalized/test/sentinel.json",
        }
    )


def _build_news_like_payload() -> JsonObject:
    rows: list[JsonObject] = []
    for index in range(30):
        rows.append(
            {
                "cntt_usiq_srno": str(1000 + index),
                "news_ofer_entp_code": "A",
                "data_dt": "20260214",
                "data_tm": "093000",
                "hts_pbnt_titl_cntt": f"title-{index}",
                "news_lrdv_code": "0",
                "dorg": "SOURCE",
                "iscd1": "",
                "iscd2": "",
                "iscd3": "",
                "iscd4": "",
                "iscd5": "",
                "iscd6": "",
                "iscd7": "",
                "iscd8": "",
                "iscd9": "",
                "iscd10": "",
            }
        )
    return cast(
        JsonObject,
        {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": rows,
        },
    )


def _build_endpoint(spec: EndpointSpec) -> Endpoint:
    return Endpoint(
        id=spec.id,
        name=spec.name,
        method=spec.method,
        path=spec.path,
        request_model=_RequestModel,
        response_model=_ResponseModel,
        description=spec.description,
        real_tr_id=spec.real_tr_id,
        demo_tr_id=spec.demo_tr_id,
        auth_required=True,
        hashkey_required=False,
    )


def _run_with_clients(
    tmp_path: Path,
    real_outcomes: list[str | Exception],
    endpoint_id: str = "smoke-test-endpoint",
) -> tuple[_DummyClient, _DummyClient, SmokeReport]:
    spec = _build_spec(endpoint_id)
    endpoint = _build_endpoint(spec)
    demo_client = _DummyClient([])
    real_client = _DummyClient(real_outcomes)
    overrides_path = tmp_path / "overrides.yaml"
    out_path = tmp_path / "smoke.json"
    detail_out_path = tmp_path / "smoke_requests.json"
    overrides_path.write_text("{}", encoding="utf-8")
    report = run_smoke(
        [spec],
        {spec.id: endpoint},
        cast(SyncKisRawClient, demo_client),
        cast(SyncKisRawClient, real_client),
        overrides_path,
        out_path,
        detail_out_path,
    )
    return demo_client, real_client, report


def test_smoke_stops_after_first_success(tmp_path: Path) -> None:
    _, real_client, report = _run_with_clients(
        tmp_path,
        ["ok", RuntimeError("request transport error")],
    )

    assert real_client.call_count == 1
    assert report.errors == 0
    assert len(report.results) == 1
    assert report.results[0].status == "ok"
    assert report.results[0].attempt == 1


def test_smoke_uses_successful_retry_as_final_status(tmp_path: Path) -> None:
    _, real_client, report = _run_with_clients(
        tmp_path,
        [RuntimeError("request transport error"), "ok"],
    )

    assert real_client.call_count == 2
    assert report.errors == 0
    assert len(report.results) == 1
    assert report.results[0].status == "ok"
    assert report.results[0].attempt == 2


def test_smoke_reports_error_after_retry_exhausted(tmp_path: Path) -> None:
    _, real_client, report = _run_with_clients(
        tmp_path,
        [RuntimeError("request transport error"), RuntimeError("request transport error")],
    )

    assert real_client.call_count == 2
    assert report.errors == 1
    assert len(report.results) == 1
    assert report.results[0].status == "error"
    assert report.results[0].attempt == 2
    assert report.results[0].reason == "request transport error"


def test_sentinel_detection_reports_news_like_payload_for_generic_endpoint() -> None:
    spec = _build_list_output_spec("sentinel-generic")
    payload = _build_news_like_payload()

    probe = _detect_sentinel_success(spec, payload)

    assert probe is not None
    assert probe["output"] == "output"


def test_sentinel_detection_ignores_news_expansion_fields_for_specific_endpoint() -> None:
    spec = _build_list_output_spec("b73a4cdf-402b-4e11-a161-609ea9451835")
    payload = _build_news_like_payload()

    probe = _detect_sentinel_success(spec, payload)

    assert probe is None


def test_smoke_retries_nonfatal_server_error_until_success(tmp_path: Path) -> None:
    nonfatal = KisResponseError(
        "API error for 3ed0247e-d717-43ed-85e9-51f952844687: OPSQ2001 ERROR WRONG VALUE SIZE [START_DATE]:[14]",
        payload={"msg_cd": "OPSQ2001", "msg1": "ERROR WRONG VALUE SIZE [START_DATE]:[14]"},
    )
    _, real_client, report = _run_with_clients(
        tmp_path,
        [nonfatal, nonfatal, "ok"],
        endpoint_id="3ed0247e-d717-43ed-85e9-51f952844687",
    )

    assert real_client.call_count == 3
    assert report.errors == 0
    assert len(report.results) == 1
    assert report.results[0].status == "ok"
    assert report.results[0].attempt == 3


def test_smoke_nonfatal_server_error_max_attempts_four(tmp_path: Path) -> None:
    nonfatal = KisResponseError(
        "API error for 3ed0247e-d717-43ed-85e9-51f952844687: OPSQ2001 ERROR WRONG VALUE SIZE [START_DATE]:[14]",
        payload={"msg_cd": "OPSQ2001", "msg1": "ERROR WRONG VALUE SIZE [START_DATE]:[14]"},
    )
    _, real_client, report = _run_with_clients(
        tmp_path,
        [nonfatal, nonfatal, nonfatal, nonfatal],
        endpoint_id="3ed0247e-d717-43ed-85e9-51f952844687",
    )

    assert real_client.call_count == 4
    assert report.errors == 0
    assert len(report.results) == 1
    assert report.results[0].status == "skipped"
    assert report.results[0].reason == "nonfatal_server_error"
    assert report.results[0].attempt == 4
