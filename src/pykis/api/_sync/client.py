from __future__ import annotations

import asyncio
import atexit
import time
from datetime import date, datetime
from datetime import time as time_value
from decimal import Decimal
from pathlib import Path
from typing import Literal, Mapping, TypeVar
from urllib.parse import urljoin

import httpx
from httpx_retries import Retry, RetryTransport
from pydantic import BaseModel

from pykis.api.auth import KisAuth
from pykis.api.constants import DEMO_DOMAIN, REAL_DOMAIN
from pykis.api.errors import (
    KisAuthError,
    KisErrorContext,
    KisHttpError,
    KisRateLimitError,
    KisResponseError,
    KisTransportError,
    KisUnsupportedEndpointError,
)
from pykis.api.raw.types import Endpoint, KisResponse
from pykis.api.token import KisAccessToken
from pykis.api.token_cache import KisTokenCache, default_token_cache_dir
from pykis.logging import get_logger

RequestT = TypeVar("RequestT", bound=BaseModel)
ResponseT = TypeVar("ResponseT", bound=BaseModel)

DEFAULT_TIMEOUT = 8
TOKEN_RATE_LIMIT_WAIT = 300

logger = get_logger(__name__)


def _build_retry(rate_limit: float) -> Retry:
    backoff_factor = rate_limit if rate_limit > 0 else 0.0
    max_backoff_wait = rate_limit if rate_limit > 0 else 120.0
    return Retry(
        total=2,
        allowed_methods=("GET",),
        status_forcelist=(429, 500, 502, 503, 504),
        backoff_factor=backoff_factor,
        max_backoff_wait=max_backoff_wait,
        backoff_jitter=0.0,
        respect_retry_after_header=True,
    )


def _error_context(
    *,
    endpoint_id: str | None = None,
    method: str | None = None,
    path: str | None = None,
    status_code: int | None = None,
    message: str | None = None,
) -> KisErrorContext:
    return KisErrorContext(
        endpoint_id=endpoint_id,
        method=method,
        path=path,
        status_code=status_code,
        message=message,
    )


def _encode_request_value(value: object) -> object:
    if isinstance(value, datetime):
        return value.strftime("%Y%m%d%H%M%S")
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.strftime("%Y%m%d")
    if isinstance(value, time_value):
        return value.strftime("%H%M%S")
    if isinstance(value, bool):
        return "Y" if value else "N"
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _encode_request_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_encode_request_value(val) for val in value]
    return value


def _coerce_query_params(payload: Mapping[str, object]) -> dict[str, str | int | float | None]:
    params: dict[str, str | int | float | None] = {}
    for key, value in payload.items():
        if value is None:
            params[str(key)] = None
        elif isinstance(value, (str, int, float)):
            params[str(key)] = value
        else:
            params[str(key)] = str(value)
    return params


class SyncKisRawClient:
    auth: KisAuth
    domain: Literal["demo", "real"]
    rate_limit: float
    _client: httpx.Client
    _token_cache: dict[str, KisAccessToken]
    _token_cache_store: KisTokenCache | None
    _revoke_on_close: bool
    _closed: bool

    __slots__ = (
        "auth",
        "domain",
        "rate_limit",
        "_client",
        "_token_cache",
        "_token_cache_store",
        "_revoke_on_close",
        "_closed",
    )

    def __init__(
        self,
        auth: KisAuth,
        domain: Literal["demo", "real"] | None = None,
        rate_limit: float = 0.4,
        *,
        keep_token: bool | str | Path | None = None,
        revoke_on_close: bool | None = None,
        client: httpx.Client | None = None,
        atexit_close: bool = True,
    ) -> None:
        self.auth = auth
        self.domain = domain or "demo"
        self.rate_limit = rate_limit
        transport = None
        if client is None:
            retry = _build_retry(self.rate_limit)
            transport = RetryTransport(retry=retry)
        self._client = client or httpx.Client(timeout=DEFAULT_TIMEOUT, transport=transport)
        self._token_cache = {}
        self._token_cache_store = None
        if keep_token:
            cache_dir = default_token_cache_dir() if keep_token is True else Path(keep_token).expanduser()
            self._token_cache_store = KisTokenCache(cache_dir, auth)
        if revoke_on_close is None:
            self._revoke_on_close = self._token_cache_store is None
        else:
            self._revoke_on_close = revoke_on_close
        self._closed = False
        if atexit_close:
            atexit.register(self._atexit_close)

    def _atexit_close(self) -> None:
        if self._closed:
            return
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            self.close()
        else:
            logger.warning("SyncKisRawClient still open; call close() explicitly.")

    def _sleep(self) -> None:
        if self.rate_limit > 0:
            time.sleep(self.rate_limit)

    def _base_url(self, base_url: str | None = None) -> str:
        if base_url:
            return base_url
        return REAL_DOMAIN if self.domain == "real" else DEMO_DOMAIN

    def ensure_token(self, base_url: str | None = None) -> None:
        self._get_token(self._base_url(base_url))

    def _issue_token(self, base_url: str) -> KisAccessToken:
        while True:
            self._sleep()
            try:
                resp = self._client.post(
                    urljoin(base_url, "/oauth2/tokenP"),
                    headers={"content-type": "application/json; charset=UTF-8"},
                    json={
                        "grant_type": "client_credentials",
                        "appkey": self.auth.appkey,
                        "appsecret": self.auth.appsecret,
                    },
                )
            except httpx.HTTPError as exc:
                raise KisTransportError(
                    "token issuance transport error",
                    original=exc,
                    context=_error_context(method="POST", path="/oauth2/tokenP"),
                ) from exc

            if resp.status_code != 403:
                if resp.status_code == 200 and "text/html" in (resp.headers.get("content-type") or ""):
                    snippet = resp.text[:200]
                    logger.warning(
                        "token response not JSON (status=%s body=%r); retrying after %ss",
                        resp.status_code,
                        snippet,
                        TOKEN_RATE_LIMIT_WAIT,
                    )
                    time.sleep(TOKEN_RATE_LIMIT_WAIT)
                    continue
                try:
                    resp.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    raise KisHttpError(
                        f"token issuance failed with status {resp.status_code}",
                        context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
                        payload=resp.text[:200],
                    ) from exc
                try:
                    payload = resp.json()
                except Exception as exc:
                    snippet = resp.text[:200]
                    raise KisAuthError(
                        "token response not JSON",
                        context=_error_context(
                            method="POST",
                            path="/oauth2/tokenP",
                            status_code=resp.status_code,
                            message=snippet,
                        ),
                    ) from exc
                token = KisAccessToken.from_payload(payload)
                if not token.token:
                    raise KisAuthError(
                        "token issuance returned empty access_token",
                        context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
                    )
                return token

            try:
                payload = resp.json()
            except Exception:
                payload = {}

            if payload.get("error_code") == "EGW00133":
                logger.warning("token rate-limited; waiting %ss before retry", TOKEN_RATE_LIMIT_WAIT)
                time.sleep(TOKEN_RATE_LIMIT_WAIT)
                continue
            error_code = payload.get("error_code")
            error_desc = payload.get("error_description")
            raise KisAuthError(
                f"token issuance failed: {error_code} {error_desc}".strip(),
                context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
            )

    def _get_token(self, base_url: str) -> KisAccessToken:
        token = self._token_cache.get(base_url)
        if token and not token.expired:
            return token
        if token and token.expired:
            self._token_cache.pop(base_url, None)
        if self._token_cache_store:
            cached = self._token_cache_store.load(base_url)
            if cached and not cached.expired:
                self._token_cache[base_url] = cached
                return cached
            if cached and cached.expired:
                self._token_cache_store.clear(base_url)
        token = self._issue_token(base_url)
        self._token_cache[base_url] = token
        if self._token_cache_store:
            self._token_cache_store.save(base_url, token)
        return token

    def _hashkey(self, base_url: str, body: Mapping[str, object]) -> str:
        self._sleep()
        try:
            resp = self._client.post(
                urljoin(base_url, "/uapi/hashkey"),
                headers={
                    "content-type": "application/json",
                    "appkey": self.auth.appkey,
                    "appsecret": self.auth.appsecret,
                },
                json=body,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise KisHttpError(
                f"hashkey failed with status {exc.response.status_code}",
                context=_error_context(method="POST", path="/uapi/hashkey", status_code=exc.response.status_code),
                payload=exc.response.text[:200],
            ) from exc
        except httpx.HTTPError as exc:
            raise KisTransportError(
                "hashkey transport error",
                original=exc,
                context=_error_context(method="POST", path="/uapi/hashkey"),
            ) from exc
        payload = resp.json()
        return payload.get("HASH") or payload.get("hash") or ""

    def _revoke_token(self, base_url: str, token: KisAccessToken) -> None:
        self._sleep()
        try:
            resp = self._client.post(
                urljoin(base_url, "/oauth2/revokeP"),
                headers={"content-type": "application/json; charset=UTF-8"},
                json=token.revoke_payload(self.auth.appkey, self.auth.appsecret),
            )
            resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - best effort on shutdown
            logger.warning("token revoke failed: %s", exc)

    def request(
        self,
        *,
        method: str,
        base_url: str,
        path: str,
        headers: Mapping[str, str] | None,
        params: Mapping[str, str | int | float | None] | None,
        body: Mapping[str, object] | None,
        auth_required: bool,
        hashkey_required: bool,
    ) -> KisResponse:
        headers = dict(headers or {})
        if auth_required:
            token = self._get_token(base_url)
            headers["authorization"] = token.authorization()

        if hashkey_required and body:
            headers["hashkey"] = self._hashkey(base_url, dict(body))

        self._sleep()
        try:
            response = self._client.request(
                method=method,
                url=urljoin(base_url, path),
                headers=headers,
                params=params,
                json=body if method == "POST" else None,
                timeout=DEFAULT_TIMEOUT,
            )
        except httpx.HTTPError as exc:
            raise KisTransportError(
                "request transport error",
                original=exc,
                context=_error_context(method=method, path=path),
            ) from exc
        return response

    def call(
        self,
        endpoint: Endpoint[RequestT, ResponseT],
        request: RequestT | Mapping[str, object],
        headers: Mapping[str, str] | None = None,
    ) -> tuple[ResponseT, KisResponse]:
        if isinstance(request, BaseModel):
            model = request
        else:
            model = endpoint.request_model.model_validate(dict(request))
        payload: Mapping[str, object] = model.model_dump(by_alias=True, exclude_none=True)
        request_payload = {key: _encode_request_value(value) for key, value in payload.items()}
        if endpoint.method == "GET":
            query = _coerce_query_params(request_payload)
            body = {}
        else:
            query = {}
            body = request_payload

        built_headers: dict[str, str] = dict(headers or {})
        built_headers.setdefault("content-type", "application/json; charset=utf-8")
        built_headers.setdefault("appkey", self.auth.appkey)
        built_headers.setdefault("appsecret", self.auth.appsecret)
        built_headers.setdefault("custtype", self.auth.custtype)
        tr_id = endpoint.real_tr_id if self.domain == "real" else endpoint.demo_tr_id
        has_tr_id = endpoint.real_tr_id is not None or endpoint.demo_tr_id is not None
        if has_tr_id:
            if tr_id is None:
                raise KisUnsupportedEndpointError(
                    f"endpoint not supported in {self.domain} domain: {endpoint.id}",
                    context=_error_context(endpoint_id=endpoint.id, method=endpoint.method, path=endpoint.path),
                )
            built_headers.setdefault("tr_id", tr_id)

        response = self.request(
            method=endpoint.method,
            base_url=self._base_url(),
            path=endpoint.path,
            headers=built_headers,
            params=query if query else None,
            body=body if body else None,
            auth_required=endpoint.auth_required,
            hashkey_required=endpoint.hashkey_required,
        )
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after and retry_after.isdigit() else None
            raise KisRateLimitError(
                f"rate limited for {endpoint.id}",
                retry_after=wait,
                context=_error_context(
                    endpoint_id=endpoint.id,
                    method=endpoint.method,
                    path=endpoint.path,
                    status_code=response.status_code,
                ),
            )
        if response.is_success:
            try:
                data = response.json()
            except Exception as exc:
                snippet = response.text[:200]
                raise KisResponseError(
                    f"invalid JSON for {endpoint.id}",
                    context=_error_context(
                        endpoint_id=endpoint.id,
                        method=endpoint.method,
                        path=endpoint.path,
                        status_code=response.status_code,
                        message=snippet,
                    ),
                ) from exc
            if isinstance(data, dict):
                data_map = {str(key): value for key, value in data.items()}
                if str(data_map.get("rt_cd")) not in ("0", "OK"):
                    raise KisResponseError(
                        f"API error for {endpoint.id}: {data_map.get('msg_cd')} {data_map.get('msg1')}".strip(),
                        context=_error_context(
                            endpoint_id=endpoint.id,
                            method=endpoint.method,
                            path=endpoint.path,
                            status_code=response.status_code,
                            message=str(data_map.get("msg1") or ""),
                        ),
                        payload=data_map,
                    )
                return endpoint.response_model.model_validate(data_map), response
            return endpoint.response_model.model_validate(data), response
        raise KisHttpError(
            f"HTTP {response.status_code} for {endpoint.id}",
            context=_error_context(
                endpoint_id=endpoint.id,
                method=endpoint.method,
                path=endpoint.path,
                status_code=response.status_code,
            ),
            payload=response.text[:200],
        )

    def close(self) -> None:
        if self._closed:
            return
        if self._revoke_on_close:
            for base_url, token in list(self._token_cache.items()):
                if token.token:
                    self._revoke_token(base_url, token)
                    if self._token_cache_store:
                        self._token_cache_store.clear(base_url)
        self._client.close()
        self._closed = True

    def __enter__(self) -> "SyncKisRawClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
