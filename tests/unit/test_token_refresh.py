from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

from pykis.api.auth import KisAuth
from pykis.api.client import KisRawClient, SyncKisRawClient
from pykis.api.raw.types import Endpoint


class DummyRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")


class DummyResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    rt_cd: str
    msg_cd: str
    msg1: str


def _make_auth() -> KisAuth:
    return KisAuth(
        id="test",
        app_key="a" * 36,
        secret_key="b" * 180,
        account=None,
        demo=True,
    )


def _make_endpoint() -> Endpoint[DummyRequest, DummyResponse]:
    return Endpoint(
        id="test.endpoint",
        name="Test Endpoint",
        method="GET",
        path="/uapi/test",
        request_model=DummyRequest,
        response_model=DummyResponse,
        description=None,
        real_tr_id=None,
        demo_tr_id=None,
        auth_required=True,
        hashkey_required=False,
    )


@pytest.mark.unit
def test_sync_refreshes_invalid_token() -> None:
    token_calls = 0
    api_calls = 0
    auth_headers: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal token_calls, api_calls
        if request.url.path == "/oauth2/tokenP":
            token_calls += 1
            return httpx.Response(
                200,
                json={"access_token": f"token{token_calls}", "token_type": "Bearer", "expires_in": 3600},
            )
        if request.url.path == "/uapi/test":
            api_calls += 1
            auth_headers.append(request.headers.get("authorization"))
            if auth_headers[-1] == "Bearer token1":
                return httpx.Response(
                    500,
                    json={"rt_cd": "1", "msg_cd": "EGW00121", "msg1": "유효하지 않은 token 입니다."},
                )
            return httpx.Response(200, json={"rt_cd": "0", "msg_cd": "0", "msg1": "OK"})
        return httpx.Response(404, json={"rt_cd": "1", "msg_cd": "NOT_FOUND", "msg1": "not found"})

    transport = httpx.MockTransport(handler)
    client = SyncKisRawClient(
        _make_auth(),
        domain="demo",
        client=httpx.Client(transport=transport),
        revoke_on_close=False,
    )
    endpoint = _make_endpoint()
    response, _ = client.call(endpoint, {})
    client.close()

    assert response.rt_cd == "0"
    assert token_calls == 2
    assert api_calls == 2


@pytest.mark.unit
def test_sync_refresh_singleton_concurrent() -> None:
    token_calls = 0
    api_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal token_calls, api_calls
        if request.url.path == "/oauth2/tokenP":
            token_calls += 1
            return httpx.Response(
                200,
                json={"access_token": f"token{token_calls}", "token_type": "Bearer", "expires_in": 3600},
            )
        if request.url.path == "/uapi/test":
            api_calls += 1
            if request.headers.get("authorization") == "Bearer token1":
                return httpx.Response(
                    500,
                    json={"rt_cd": "1", "msg_cd": "EGW00121", "msg1": "유효하지 않은 token 입니다."},
                )
            return httpx.Response(200, json={"rt_cd": "0", "msg_cd": "0", "msg1": "OK"})
        return httpx.Response(404, json={"rt_cd": "1", "msg_cd": "NOT_FOUND", "msg1": "not found"})

    transport = httpx.MockTransport(handler)
    client = SyncKisRawClient(
        _make_auth(),
        domain="demo",
        client=httpx.Client(transport=transport),
        revoke_on_close=False,
    )
    endpoint = _make_endpoint()
    client.ensure_token()

    barrier = Barrier(5)

    def worker() -> str:
        barrier.wait()
        return client.call(endpoint, {})[0].rt_cd

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda _: worker(), range(5)))

    client.close()

    assert all(result == "0" for result in results)
    assert token_calls == 2
    assert 6 <= api_calls <= 10


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_refreshes_invalid_token() -> None:
    token_calls = 0
    api_calls = 0
    auth_headers: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal token_calls, api_calls
        if request.url.path == "/oauth2/tokenP":
            token_calls += 1
            return httpx.Response(
                200,
                json={"access_token": f"token{token_calls}", "token_type": "Bearer", "expires_in": 3600},
            )
        if request.url.path == "/uapi/test":
            api_calls += 1
            auth_headers.append(request.headers.get("authorization"))
            if auth_headers[-1] == "Bearer token1":
                return httpx.Response(
                    500,
                    json={"rt_cd": "1", "msg_cd": "EGW00121", "msg1": "유효하지 않은 token 입니다."},
                )
            return httpx.Response(200, json={"rt_cd": "0", "msg_cd": "0", "msg1": "OK"})
        return httpx.Response(404, json={"rt_cd": "1", "msg_cd": "NOT_FOUND", "msg1": "not found"})

    transport = httpx.MockTransport(handler)
    client = KisRawClient(
        _make_auth(),
        domain="demo",
        client=httpx.AsyncClient(transport=transport),
        revoke_on_close=False,
    )
    endpoint = _make_endpoint()
    try:
        response, _ = await client.call(endpoint, {})
    finally:
        await client.aclose()

    assert response.rt_cd == "0"
    assert token_calls == 2
    assert api_calls == 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_refresh_singleton_concurrent() -> None:
    token_calls = 0
    api_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal token_calls, api_calls
        if request.url.path == "/oauth2/tokenP":
            token_calls += 1
            return httpx.Response(
                200,
                json={"access_token": f"token{token_calls}", "token_type": "Bearer", "expires_in": 3600},
            )
        if request.url.path == "/uapi/test":
            api_calls += 1
            if request.headers.get("authorization") == "Bearer token1":
                return httpx.Response(
                    500,
                    json={"rt_cd": "1", "msg_cd": "EGW00121", "msg1": "유효하지 않은 token 입니다."},
                )
            return httpx.Response(200, json={"rt_cd": "0", "msg_cd": "0", "msg1": "OK"})
        return httpx.Response(404, json={"rt_cd": "1", "msg_cd": "NOT_FOUND", "msg1": "not found"})

    transport = httpx.MockTransport(handler)
    client = KisRawClient(
        _make_auth(),
        domain="demo",
        client=httpx.AsyncClient(transport=transport),
        revoke_on_close=False,
    )
    endpoint = _make_endpoint()
    await client.ensure_token()

    start = asyncio.Event()

    async def worker() -> str:
        await start.wait()
        return (await client.call(endpoint, {}))[0].rt_cd

    tasks = [asyncio.create_task(worker()) for _ in range(5)]
    start.set()
    results = await asyncio.gather(*tasks)

    await client.aclose()

    assert all(result == "0" for result in results)
    assert token_calls == 2
    assert 6 <= api_calls <= 10
